#!/usr/bin/env python3
"""Compute ads, SEO and CS KPIs and flags from exports (all arithmetic scripted; R7).

  compute_kpis.py <export-dir> [--out-json kpis.json] [--out-md kpis.md]

Expects in <export-dir>: ads.csv (date,platform,campaign,spend_vnd,impressions,clicks,conversions,
revenue_vnd), seo.csv (keyword,position_prev_week,position_this_week,clicks,impressions,landing_page),
cs.csv (date,channel,tickets,median_first_response_min,resolved,csat_avg,skin_reaction_reports),
targets.json (roas_min, cpa_max_vnd, ctr_min, cs_first_response_max_min, csat_min, resolution_rate_min).
Missing files are skipped and reported.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


def rd(p: Path) -> list[dict]:
    with p.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ratio(a, b):
    return round(a / b, 4) if b else None


def ads_kpis(rows: list[dict], t: dict) -> dict:
    agg = defaultdict(lambda: defaultdict(float))
    plat = {}
    for r in rows:
        k = r["campaign"]
        plat[k] = r["platform"]
        for f in ("spend_vnd", "impressions", "clicks", "conversions", "revenue_vnd"):
            agg[k][f] += float(r[f])
    camps = []
    for k, a in agg.items():
        c = {"campaign": k, "platform": plat[k], "spend_vnd": int(a["spend_vnd"]), "impressions": int(a["impressions"]),
             "clicks": int(a["clicks"]), "conversions": int(a["conversions"]), "revenue_vnd": int(a["revenue_vnd"]),
             "ctr": ratio(a["clicks"], a["impressions"]), "cpc_vnd": int(a["spend_vnd"] / a["clicks"]) if a["clicks"] else None,
             "cpa_vnd": int(a["spend_vnd"] / a["conversions"]) if a["conversions"] else None,
             "roas": round(a["revenue_vnd"] / a["spend_vnd"], 2) if a["spend_vnd"] else None}
        flags = []
        if c["roas"] is not None and c["roas"] < t.get("roas_min", 0):
            flags.append(f"ROAS {c['roas']} < {t['roas_min']}")
        if c["cpa_vnd"] is None or c["cpa_vnd"] > t.get("cpa_max_vnd", 1e18):
            flags.append(f"CPA {c['cpa_vnd']} > {t.get('cpa_max_vnd')}")
        if c["ctr"] is not None and c["ctr"] < t.get("ctr_min", 0):
            flags.append(f"CTR {c['ctr']:.2%} < {t['ctr_min']:.1%}")
        c["flags"] = flags
        camps.append(c)
    camps.sort(key=lambda c: (-(len(c["flags"])), c["roas"] or 0))
    by_plat = defaultdict(lambda: defaultdict(float))
    for c in camps:
        for f in ("spend_vnd", "conversions", "revenue_vnd", "clicks", "impressions"):
            by_plat[c["platform"]][f] += c[f]
    plats = [{"platform": p, "spend_vnd": int(v["spend_vnd"]), "conversions": int(v["conversions"]),
              "revenue_vnd": int(v["revenue_vnd"]), "roas": round(v["revenue_vnd"] / v["spend_vnd"], 2) if v["spend_vnd"] else None,
              "cpa_vnd": int(v["spend_vnd"] / v["conversions"]) if v["conversions"] else None} for p, v in by_plat.items()]
    tot_s = sum(c["spend_vnd"] for c in camps)
    tot_r = sum(c["revenue_vnd"] for c in camps)
    tot_c = sum(c["conversions"] for c in camps)
    return {"campaigns": camps, "platforms": sorted(plats, key=lambda p: -p["spend_vnd"]),
            "total": {"spend_vnd": tot_s, "revenue_vnd": tot_r, "conversions": tot_c,
                      "roas": round(tot_r / tot_s, 2) if tot_s else None, "cpa_vnd": int(tot_s / tot_c) if tot_c else None},
            "flagged": [c["campaign"] for c in camps if c["flags"]]}


def seo_kpis(rows: list[dict]) -> dict:
    kws = []
    for r in rows:
        prev, cur = int(r["position_prev_week"]), int(r["position_this_week"])
        kws.append({"keyword": r["keyword"], "prev": prev, "now": cur, "change": prev - cur, "clicks": int(r["clicks"]),
                    "impressions": int(r["impressions"]), "landing_page": r["landing_page"]})
    drops = [k for k in kws if k["change"] <= -3]
    gains = [k for k in kws if k["change"] >= 3]
    return {"keywords": sorted(kws, key=lambda k: k["change"]), "top10": sum(1 for k in kws if k["now"] <= 10),
            "drops": [k["keyword"] for k in drops], "gains": [k["keyword"] for k in gains],
            "avg_position_now": round(statistics.mean(k["now"] for k in kws), 1) if kws else None}


def cs_kpis(rows: list[dict], t: dict) -> dict:
    by_ch = defaultdict(list)
    for r in rows:
        by_ch[r["channel"]].append(r)
    chans = []
    breaches = []
    for ch, rs in by_ch.items():
        tickets = sum(int(r["tickets"]) for r in rs)
        resolved = sum(int(r["resolved"]) for r in rs)
        frt = [float(r["median_first_response_min"]) for r in rs]
        csat = round(sum(float(r["csat_avg"]) * int(r["tickets"]) for r in rs) / tickets, 2) if tickets else None
        days = [r["date"] for r in rs if float(r["median_first_response_min"]) > t.get("cs_first_response_max_min", 1e9)]
        breaches += [{"channel": ch, "date": d} for d in days]
        flags = []
        if days:
            flags.append(f"first response > {t['cs_first_response_max_min']} min on {', '.join(days)}")
        if csat is not None and csat < t.get("csat_min", 0):
            flags.append(f"CSAT {csat} < {t['csat_min']}")
        if tickets and resolved / tickets < t.get("resolution_rate_min", 0):
            flags.append(f"resolution {resolved / tickets:.1%} < {t['resolution_rate_min']:.0%}")
        chans.append({"channel": ch, "tickets": tickets, "resolution_rate": ratio(resolved, tickets),
                      "median_first_response_min": round(statistics.median(frt), 1), "max_first_response_min": max(frt),
                      "csat": csat, "skin_reaction_reports": sum(int(r["skin_reaction_reports"]) for r in rs), "flags": flags})
    return {"channels": sorted(chans, key=lambda c: -len(c["flags"])), "sla_breaches": breaches,
            "skin_reaction_reports": sum(c["skin_reaction_reports"] for c in chans),
            "flagged": [c["channel"] for c in chans if c["flags"]]}


def vnd(n):
    return f"{n:,}" if isinstance(n, int) else "–"


def to_md(k: dict) -> str:
    out = []
    if "ads" in k:
        a = k["ads"]
        out += ["### Ads theo chiến dịch / by campaign", "",
                "| campaign | platform | spend (VND) | conv | revenue (VND) | CTR | CPC | CPA | ROAS | flags |", "|---|---|---|---|---|---|---|---|---|---|"]
        for c in a["campaigns"]:
            out.append(f"| {c['campaign']} | {c['platform']} | {vnd(c['spend_vnd'])} | {c['conversions']} | {vnd(c['revenue_vnd'])} | "
                       f"{c['ctr']:.2%} | {vnd(c['cpc_vnd'])} | {vnd(c['cpa_vnd'])} | {c['roas']} | {'; '.join(c['flags']) or 'ok'} |")
        t = a["total"]
        out += [f"| **Total** | | {vnd(t['spend_vnd'])} | {t['conversions']} | {vnd(t['revenue_vnd'])} | | | {vnd(t['cpa_vnd'])} | {t['roas']} | |", ""]
    if "seo" in k:
        out += ["### SEO", "", "| keyword | prev | now | change | clicks |", "|---|---|---|---|---|"]
        out += [f"| {s['keyword']} | {s['prev']} | {s['now']} | {s['change']:+d} | {s['clicks']} |" for s in k["seo"]["keywords"]]
        out.append("")
    if "cs" in k:
        out += ["### CSKH / Customer service", "", "| channel | tickets | resolution | median FRT (min) | max FRT | CSAT | skin reports | flags |",
                "|---|---|---|---|---|---|---|---|"]
        out += [f"| {c['channel']} | {c['tickets']} | {c['resolution_rate']:.1%} | {c['median_first_response_min']} | "
                f"{c['max_first_response_min']} | {c['csat']} | {c['skin_reaction_reports']} | {'; '.join(c['flags']) or 'ok'} |"
                for c in k["cs"]["channels"]]
    return "\n".join(out) + "\n"


def compute(d: Path) -> dict:
    t = json.loads((d / "targets.json").read_text()) if (d / "targets.json").exists() else {}
    k = {"period": t.get("period"), "targets": t, "missing": []}
    for name, fn in (("ads", lambda r: ads_kpis(r, t)), ("seo", seo_kpis), ("cs", lambda r: cs_kpis(r, t))):
        p = d / f"{name}.csv"
        if p.exists():
            k[name] = fn(rd(p))
        else:
            k["missing"].append(f"{name}.csv")
    return k


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("export_dir"); ap.add_argument("--out-json"); ap.add_argument("--out-md")
    a = ap.parse_args(argv)
    k = compute(Path(a.export_dir))
    md = to_md(k)
    if a.out_json:
        Path(a.out_json).write_text(json.dumps(k, indent=1, ensure_ascii=False))
    if a.out_md:
        Path(a.out_md).write_text(md)
    print(md)
    print(f"flagged campaigns: {k.get('ads', {}).get('flagged')}; SEO drops: {k.get('seo', {}).get('drops')}; "
          f"CS flagged: {k.get('cs', {}).get('flagged')}; missing: {k['missing']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
