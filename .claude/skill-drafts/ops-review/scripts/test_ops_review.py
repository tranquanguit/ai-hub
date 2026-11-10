import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "AGENTS.md").exists())
EXPORT = REPO / "inputs" / "SAMPLE-ops-export"


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_compute_kpis_on_sample():
    ck = load("compute_kpis")
    k = ck.compute(EXPORT)
    assert k["missing"] == []
    camps = {c["campaign"]: c for c in k["ads"]["campaigns"]}
    assert len(camps) == 7
    t = k["ads"]["total"]
    assert t["spend_vnd"] == sum(c["spend_vnd"] for c in camps.values())
    assert abs(t["roas"] - t["revenue_vnd"] / t["spend_vnd"]) < 0.01
    assert "TT_Broad_LipTint" in k["ads"]["flagged"]  # weak campaign by construction
    assert "kem chống nắng nâng tone" in k["seo"]["drops"]
    assert k["cs"]["skin_reaction_reports"] == 1 and k["cs"]["sla_breaches"]


def test_checker(tmp_path):
    ck, cr = load("compute_kpis"), load("check_review")
    k = ck.compute(EXPORT)
    flagged = k["ads"]["flagged"] + k["seo"]["drops"] + k["cs"]["flagged"]
    recs = "\n".join(f"{i}. {n}: Marketing giảm 30% ngân sách, kiểm tra lại sau 7 ngày" for i, n in enumerate(flagged, 1))
    md = ("# Ops review (SAMPLE data)\n## Tóm tắt\nx\n## Quảng cáo\nx\n## SEO\nx\n## CSKH\nBáo Founder ca kích ứng.\n"
          f"## Đề xuất\n{recs}\n## English summary\nx\n")
    assert all(ok for _, ok, _ in cr.checks(md, k)), [c for c in cr.checks(md, k) if not c[1]]
    bad = md.replace(f"{flagged[0]}:", "something:") .replace("Báo Founder ca kích ứng.", "")
    failed = {n for n, ok, _ in cr.checks(bad, k) if not ok}
    assert {"every_flag_has_recommendation", "skin_reaction_escalated"} <= failed
    camp = k["ads"]["campaigns"][0]
    wrong = md.replace("## Quảng cáo\nx", f"## Quảng cáo\n{camp['campaign']} có ROAS {camp['roas'] + 1:.2f}")
    assert ("quoted_roas_matches_kpis", False) in [(n, ok) for n, ok, _ in cr.checks(wrong, k)]


def test_roas_check_ignores_day_counts_and_other_columns():
    ck, cr = load("compute_kpis"), load("check_review")
    k = ck.compute(EXPORT)
    camp = next(c for c in k["ads"]["campaigns"] if c["flags"])
    md = (f"| campaign | CPA | ROAS | note |\n|---|---|---|---|\n| {camp['campaign']} | 171,573 | {camp['roas']} | kéo ROAS |\n"
          f"1. {camp['campaign']}: Marketing kiểm tra lại ROAS sau 7 ngày (mục tiêu ≥ 2.0)\n")
    assert ("quoted_roas_matches_kpis", True) in [(n, ok) for n, ok, _ in cr.checks(md, k)]
