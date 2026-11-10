#!/usr/bin/env python3
"""The only writer of semantic memory and active skills (RULES R2-R5, R9; DESIGN.md#learning-loop).

Memory (curator):
  promote.py plan                        inbox items with verdict preview (no changes)
  promote.py apply <inbox-file>          verified new fact -> memory/semantic/<slug>.md (or merge/conflict)
  promote.py reject <inbox-file> --reason TEXT
  promote.py conflict <inbox-file>       force set-aside to memory/conflicts/
  promote.py bump <fact-slug> --helpful|--harmful|--used
  promote.py resolve <conflict-file> --keep new|old   (human decision)
  promote.py archive <fact-slug> --reason TEXT        (prune, after approval)
  promote.py index                       regenerate memory/INDEX.md (score = recency + importance)
  promote.py lint                        check every semantic fact (source, fields)
  promote.py auto                        apply/reject every inbox item by the rules below (curate-learning)
Skills (skill-forge):
  promote.py skill <name> [--eval RESULTS_JSON] [--allow-shrink]   draft -> active after gates

Every decision is appended to memory/curation-log.jsonl.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MEM = ROOT / "memory"
VERIFIED_KINDS = {"test", "tool", "eval", "human"}
FACT_FIELDS = ["key", "claim", "value", "source", "confidence", "created", "last_verified", "used_count",
               "helpful", "harmful", "tags", "links", "verification", "roles"]


def paths():
    return {k: MEM / k for k in ("inbox", "semantic", "conflicts", "archive", "episodic")}


def today() -> str:
    return date.today().isoformat()


def read_md(p: Path) -> tuple[dict, str]:
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def write_md(p: Path, fm: dict, body: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip() + "\n---\n" + body.lstrip("\n"),
                 encoding="utf-8")


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9.]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-.")[:70] or "fact"


def log(action: str, item: str, reason: str, **kw) -> None:
    rec = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "action": action, "item": item,
           "reason": reason, **kw}
    with (MEM / "curation-log.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def facts() -> dict[str, tuple[Path, dict]]:
    out = {}
    for p in sorted(paths()["semantic"].glob("*.md")):
        fm, _ = read_md(p)
        out[p.stem] = (p, fm)
    return out


def pii_or_secret(text: str) -> str | None:
    sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("ptu", ROOT / ".claude" / "hooks" / "pre_tool_use.py")
    ptu = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ptu)
    return ptu.scan(text, ptu.SECRETS) or ptu.scan(text, ptu.PII)


def norm(v) -> str:
    return re.sub(r"[\s,._]", "", str(v)).lower()


def verdict(item: Path, pending: dict | None = None) -> tuple[str, str, str | None]:
    """Decide what to do with an inbox item: (action, reason, matching_fact_slug).
    `pending` = {key: (value, item_name)} of items earlier in the same batch (plan simulation)."""
    fm, body = read_md(item)
    typ = fm.get("type", "fact")
    if typ == "skill-delta":
        return "defer", "skill delta: handled by skill-forge", None
    if typ == "question":
        return "defer", "question for the human/repo: answer it in canon or memory, then delete", None
    leak = pii_or_secret(item.read_text())
    if leak:
        return "reject", f"contains {leak} (R12/R15)", None
    if not fm.get("source"):
        return "reject", "no source (R9)", None
    if not fm.get("key") or not fm.get("claim"):
        return "reject", "missing key or claim", None
    ver = fm.get("verification") or {}
    kind = (ver.get("kind") if isinstance(ver, dict) else str(ver)) or "none"
    if kind not in VERIFIED_KINDS:
        return "reject", f"verification kind '{kind}' is not external feedback (R2: test/tool/eval/human only)", None
    ev = ver.get("evidence") if isinstance(ver, dict) else None
    if not ev or not (ROOT / str(ev)).exists():
        return "reject", f"verification evidence path missing or not found: {ev} (R2)", None
    for slug, (_, f) in facts().items():
        if f.get("key") == fm["key"]:
            if fm.get("value") is not None and f.get("value") is not None and norm(f["value"]) != norm(fm["value"]):
                return "conflict", f"same key '{fm['key']}' but value '{fm['value']}' != existing '{f['value']}' (R4)", slug
            return "merge", f"duplicate of existing fact '{slug}': count as helpful re-verification", slug
    if pending and fm["key"] in pending:
        pv, pname = pending[fm["key"]]
        if norm(pv) != norm(fm.get("value")):
            return "conflict", f"same key as earlier batch item {pname} ('{pv}' vs '{fm.get('value')}') (R4)", None
        return "merge", f"duplicate of earlier batch item {pname}", None
    return "add", "verified, sourced, new key", None


def cmd_plan(_a) -> int:
    items = sorted(paths()["inbox"].glob("*.md"))
    pending: dict = {}
    for it in items:
        act, why, slug = verdict(it, pending)
        if act == "add":
            fm, _ = read_md(it)
            pending[fm["key"]] = (fm.get("value"), it.name)
        print(f"{act:<8} {it.name:<55} {why}")
    print(f"{len(items)} inbox item(s)")
    return 0


def _move(src: Path, dst_dir: Path, extra: dict) -> Path:
    fm, body = read_md(src)
    fm.update(extra)
    dst = dst_dir / src.name
    write_md(dst, fm, body)
    src.unlink()
    return dst


def apply_item(item: Path) -> str:
    act, why, slug = verdict(item)
    fm, body = read_md(item)
    if act == "add":
        new_slug = slugify(fm["key"])
        dst = paths()["semantic"] / f"{new_slug}.md"
        fact = {"key": fm["key"], "claim": fm["claim"], "value": fm.get("value"), "source": fm["source"],
                "confidence": fm.get("confidence", "medium"), "created": today(), "last_verified": today(),
                "used_count": 0, "helpful": 0, "harmful": 0, "tags": fm.get("tags", []), "links": fm.get("links", []),
                "verification": fm["verification"], "roles": fm.get("roles", ["all"])}
        write_md(dst, fact, body or f"{fm['claim']}\n")
        item.unlink()
        log("add", item.name, why, fact=new_slug)
        return f"added memory/semantic/{new_slug}.md"
    if act == "merge":
        p, f = facts()[slug]
        f["helpful"] = int(f.get("helpful", 0)) + 1
        f["last_verified"] = today()
        _, fbody = read_md(p)
        write_md(p, f, fbody)
        item.unlink()
        log("merge", item.name, why, fact=slug)
        return f"merged into {slug} (helpful+1)"
    if act == "conflict":
        p, f = facts()[slug]
        dst = _move(item, paths()["conflicts"], {"conflicts_with": f"memory/semantic/{slug}.md",
                                                  "existing_value": f.get("value"), "existing_source": f.get("source"),
                                                  "conflict_reason": why})
        log("conflict", item.name, why, fact=slug)
        return f"set aside -> {dst.relative_to(ROOT)}"
    if act == "reject":
        dst = _move(item, paths()["archive"] / "rejected", {"rejected": today(), "reject_reason": why})
        log("reject", item.name, why)
        return f"rejected -> {dst.relative_to(ROOT)}: {why}"
    return f"deferred: {why}"


def cmd_apply(a) -> int:
    print(apply_item(Path(a.item)))
    cmd_index(a, quiet=True)
    return 0


def cmd_auto(a) -> int:
    for it in sorted(paths()["inbox"].glob("*.md")):
        print(f"{it.name}: {apply_item(it)}")
    cmd_index(a)
    return 0


def cmd_reject(a) -> int:
    it = Path(a.item)
    dst = _move(it, paths()["archive"] / "rejected", {"rejected": today(), "reject_reason": a.reason})
    log("reject", it.name, a.reason)
    print(f"rejected -> {dst.relative_to(ROOT)}")
    return 0


def cmd_conflict(a) -> int:
    it = Path(a.item)
    dst = _move(it, paths()["conflicts"], {"conflict_reason": a.reason or "set aside by curator"})
    log("conflict", it.name, a.reason or "manual")
    print(f"set aside -> {dst.relative_to(ROOT)}")
    return 0


def cmd_bump(a) -> int:
    p, f = facts()[a.fact]
    for k, on in (("helpful", a.helpful), ("harmful", a.harmful), ("used_count", a.used)):
        if on:
            f[k] = int(f.get(k, 0)) + 1
    if a.helpful:
        f["last_verified"] = today()
    if a.used:
        f["last_used"] = today()
    _, body = read_md(p)
    write_md(p, f, body)
    log("bump", a.fact, a.reason or "", helpful=a.helpful, harmful=a.harmful, used=a.used)
    print(f"{a.fact}: used={f.get('used_count')} helpful={f.get('helpful')} harmful={f.get('harmful')}")
    cmd_index(a, quiet=True)
    return 0


def cmd_resolve(a) -> int:
    c = Path(a.item)
    fm, body = read_md(c)
    target = ROOT / fm["conflicts_with"]
    if a.keep == "new":
        old, obody = read_md(target)
        arch = paths()["archive"] / target.name
        old["archived"] = today()
        old["archive_reason"] = f"superseded by human-resolved conflict {c.name}"
        write_md(arch, old, obody)
        new = {k: fm.get(k) for k in FACT_FIELDS if k in fm}
        new.update({"created": today(), "last_verified": today(), "used_count": 0, "helpful": 0, "harmful": 0})
        write_md(target, new, body)
    c.unlink()
    log("resolve", c.name, f"human kept {a.keep}")
    cmd_index(a, quiet=True)
    print(f"resolved {c.name}: kept {a.keep}")
    return 0


def cmd_archive(a) -> int:
    p, f = facts()[a.fact]
    _, body = read_md(p)
    f.update({"archived": today(), "archive_reason": a.reason})
    write_md(paths()["archive"] / p.name, f, body)
    p.unlink()
    log("archive", a.fact, a.reason)
    cmd_index(a, quiet=True)
    print(f"archived {a.fact}: {a.reason}")
    return 0


def score(f: dict) -> float:
    """Generative-Agents style: recency + importance (+ relevance is applied at query time by tags)."""
    try:
        age = (date.today() - date.fromisoformat(str(f.get("last_verified")))).days
    except Exception:
        age = 365
    recency = 0.99 ** age
    importance = (int(f.get("helpful", 0)) - 2 * int(f.get("harmful", 0)) + 0.5 * int(f.get("used_count", 0)))
    conf = {"high": 1.0, "medium": 0.7, "low": 0.4, "assumption": 0.2}.get(str(f.get("confidence")), 0.5)
    return round(recency + 0.3 * importance + conf, 2)


def cmd_index(a=None, quiet=False) -> int:
    fs = facts()
    lines = ["# Memory index (generated by tools/promote.py index; do not edit)", "",
             "One line per verified fact: `slug` — claim [tags] (score, confidence). Open a fact file only when needed.", ""]
    for slug, (p, f) in sorted(fs.items(), key=lambda kv: -score(kv[1][1])):
        tags = ",".join(f.get("tags") or [])
        lines.append(f"- `{slug}` — {f.get('claim')} [{tags}] ({score(f)}, {f.get('confidence')})")
    if not fs:
        lines.append("_No verified facts yet._")
    (MEM / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if not quiet:
        print(f"memory/INDEX.md: {len(fs)} fact(s)")
    return 0


def cmd_lint(_a) -> int:
    errs = []
    for slug, (p, f) in facts().items():
        for k in ("key", "claim", "source", "confidence", "created", "last_verified", "verification"):
            if k not in f or f[k] in (None, ""):
                errs.append(f"{slug}: missing {k}")
        if f.get("confidence") not in ("high", "medium", "low", "assumption"):
            errs.append(f"{slug}: bad confidence")
    for e in errs:
        print("FAIL", e)
    print(f"lint: {len(facts())} facts, {len(errs)} problems")
    return 1 if errs else 0


# ---------------- skills ----------------
def cmd_skill(a) -> int:
    name = a.name
    draft = ROOT / ".claude" / "skill-drafts" / name
    active = ROOT / ".claude" / "skills" / name
    if not draft.exists():
        print(f"no draft at {draft.relative_to(ROOT)}")
        return 1
    v = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_skills.py"), str(draft)], capture_output=True, text=True)
    if v.returncode:
        print("draft fails validation:\n" + v.stdout)
        return 1
    tests = list((draft / "scripts").glob("test_*.py")) if (draft / "scripts").exists() else []
    if tests:
        t = subprocess.run([sys.executable, "-m", "pytest", "-q", *map(str, tests)], capture_output=True, text=True, cwd=ROOT)
        if t.returncode:
            print("draft script tests fail:\n" + t.stdout[-1500:])
            return 1
    golden = ROOT / "evals" / "golden" / name
    if golden.exists():
        if not a.eval:
            print(f"skill has a golden eval: pass --eval evals/runs/<date>/results.json from a run of the DRAFT (R6)")
            return 1
        res = json.loads((ROOT / a.eval).read_text())
        mine = [r for r in res.get("results", []) if r.get("task") == name]
        if not mine or not all(r.get("passed") for r in mine):
            print(f"eval {a.eval} has no passing result for {name}: not promoted (R6)")
            return 1
    if (active / "SKILL.md").exists() and not a.allow_shrink:
        old = len((active / "SKILL.md").read_text().splitlines())
        new = len((draft / "SKILL.md").read_text().splitlines())
        if new < 0.7 * old:
            print(f"draft removes {old - new} of {old} lines (>30%): pass --allow-shrink with a CHANGELOG reason (R5)")
            return 1
    stats = json.loads((active / "stats.json").read_text()) if (active / "stats.json").exists() else \
        json.loads((draft / "stats.json").read_text())
    dver = json.loads((draft / "stats.json").read_text()).get("version", "0.1.0")
    stats["version"] = dver
    if active.exists():
        prev = ROOT / ".claude" / "state" / "skill-backups" / f"{name}-{stats.get('version')}-{datetime.now().strftime('%H%M%S')}"
        shutil.copytree(active, prev)
        shutil.rmtree(active)
    shutil.copytree(draft, active, ignore=shutil.ignore_patterns("__pycache__"))
    (active / "stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    shutil.rmtree(draft)
    log("skill-promote", name, f"version {dver}", eval=a.eval)
    print(f"promoted .claude/skills/{name} (version {dver})")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("plan").set_defaults(f=cmd_plan)
    sp.add_parser("auto").set_defaults(f=cmd_auto)
    sp.add_parser("index").set_defaults(f=cmd_index)
    sp.add_parser("lint").set_defaults(f=cmd_lint)
    p = sp.add_parser("apply"); p.add_argument("item"); p.set_defaults(f=cmd_apply)
    p = sp.add_parser("reject"); p.add_argument("item"); p.add_argument("--reason", required=True); p.set_defaults(f=cmd_reject)
    p = sp.add_parser("conflict"); p.add_argument("item"); p.add_argument("--reason", default=""); p.set_defaults(f=cmd_conflict)
    p = sp.add_parser("bump"); p.add_argument("fact")
    for fl in ("--helpful", "--harmful", "--used"):
        p.add_argument(fl, action="store_true")
    p.add_argument("--reason", default=""); p.set_defaults(f=cmd_bump)
    p = sp.add_parser("resolve"); p.add_argument("item"); p.add_argument("--keep", choices=["new", "old"], required=True); p.set_defaults(f=cmd_resolve)
    p = sp.add_parser("archive"); p.add_argument("fact"); p.add_argument("--reason", required=True); p.set_defaults(f=cmd_archive)
    p = sp.add_parser("skill"); p.add_argument("name"); p.add_argument("--eval"); p.add_argument("--allow-shrink", action="store_true")
    p.set_defaults(f=cmd_skill)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
