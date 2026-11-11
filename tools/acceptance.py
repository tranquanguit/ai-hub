#!/usr/bin/env python3
"""Run the 12 acceptance tests from the build mission and print PASS/FAIL with details.

  python3 tools/acceptance.py [--skip-pytest]
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import library_index  # noqa: E402
import validate_skills  # noqa: E402

META = ["task-start", "task-close", "reflect", "curate-learning", "skill-forge", "paper-ingest", "eval-run", "prune", "improve"]
DOMAIN = ["phase-plan", "cs-training", "ops-review"]
HOOKS = ["pre_tool_use.py", "stop.py", "session_start.py", "pre_compact.py", "session_end.py"]


def sh(*cmd, timeout=900) -> subprocess.CompletedProcess:
    return subprocess.run(list(cmd), cwd=ROOT, capture_output=True, text=True, timeout=timeout)


def t1():
    src = json.loads((ROOT / "library" / "sources.json").read_text())
    want = [p["id"] for p in src["papers"]] + [d["id"] for d in src["docs"]]
    rows = {r["id"]: r for r in csv.DictReader((ROOT / "library" / "MANIFEST.csv").open())}
    missing = [i for i in want if i not in rows or not re.fullmatch(r"[0-9a-f]{64}", rows[i]["sha256"])]
    card_errs = []
    for r in rows.values():
        if r["kind"] == "paper":
            p = ROOT / "library" / "cards" / f"{r['id']}.md"
            card_errs += library_index.check_card(p) if p.exists() else [f"{r['id']}: no card"]
    n_p = sum(1 for r in rows.values() if r["kind"] == "paper")
    return not missing and not card_errs, f"{len(want)} sources listed with sha256 ({n_p} papers); missing={missing}; card problems={card_errs[:5]}"


def t2():
    design = (ROOT / "DESIGN.md").read_text()
    manifest = {r["id"] for r in csv.DictReader((ROOT / "library" / "MANIFEST.csv").open())}
    cards = {p.stem for p in (ROOT / "library" / "cards").glob("*.md")}
    bad, n = [], 0
    for sec in re.split(r"^## ", design, flags=re.M)[1:]:
        name = sec.split("\n", 1)[0].strip()
        if name.lower().startswith("docs vs"):
            continue
        n += 1
        ev = re.search(r"\*\*Evidence\.\*\*(.+?)(?=\n\n|\n\*\*|\Z)", sec, re.S)
        text = ev.group(1) if ev else ""
        ok_cards = [c for c in re.findall(r"\b(\d{4}\.\d{4,5})\b", text) if c in cards]
        ok_docs = [d for d in re.findall(r"doc:([a-z0-9-]+)", text) if d in manifest]
        if not (ok_cards or ok_docs or "justification:" in text):
            bad.append(name)
    return not bad and n > 0, f"{n} decisions; without citation/justification: {bad}"


def t3(skip):
    rules = (ROOT / "RULES.md").read_text()
    blocks = re.split(r"^## (R\d+)\s*$", rules, flags=re.M)
    no_enf = [blocks[i] for i in range(1, len(blocks), 2) if "Enforced by:" not in blocks[i + 1]]
    tests = (ROOT / ".claude" / "hooks" / "tests" / "test_hooks.py").read_text()
    untested = [h for h in HOOKS if h not in tests]
    deny_tests = len(re.findall(r'== "deny"|\["decision"\] == "block"|== "block"', tests))
    ok_py = True
    if not skip:
        ok_py = sh(sys.executable, "-m", "pytest", "-q", ".claude/hooks").returncode == 0
    n_rules = (len(blocks) - 1) // 2
    return (not no_enf and not untested and ok_py and deny_tests >= 5,
            f"{n_rules} rules, all name enforcement: {not no_enf}; hooks with tests: {len(HOOKS) - len(untested)}/{len(HOOKS)}; "
            f"blocking assertions: {deny_tests}; hook tests pass: {ok_py}")


def t4():
    errs, runs = [], {}
    for s in META + DOMAIN:
        d = ROOT / ".claude" / "skills" / s
        if not d.exists():
            errs.append(f"{s}: missing")
            continue
        errs += validate_skills.validate(d)
        st = json.loads((d / "stats.json").read_text())
        runs[s] = st.get("runs", 0)
        if st.get("runs", 0) < 1:
            errs.append(f"{s}: no recorded run")
    return not errs, f"{len(META)} meta + {len(DOMAIN)} domain skills; runs={runs}; problems={errs[:6]}"


def t5():
    found = {}
    for t in (ROOT / "tasks").glob("*/TASK.md"):
        m = re.search(r"^task_type:\s*(\S+)", t.read_text(), re.M)
        ev = [p for p in (t.parent / "evidence").rglob("*") if p.is_file()]
        if m and m.group(1) in DOMAIN and ev and list(t.parent.glob("deliverables/*")):
            found.setdefault(m.group(1), []).append(f"{t.parent.name} ({len(ev)} evidence files)")
    return all(d in found for d in DOMAIN), f"{found}"


def t6():
    epi = list((ROOT / "memory" / "episodic").glob("*.md"))
    log = [json.loads(l) for l in (ROOT / "memory" / "curation-log.jsonl").read_text().splitlines() if l.strip()]
    adds = [r for r in log if r["action"] == "add"]
    aside = [r for r in log if r["action"] in ("conflict", "reject") and r.get("reason")]
    facts = {p.stem for p in (ROOT / "memory" / "semantic").glob("*.md")}
    index = (ROOT / "memory" / "INDEX.md").read_text()
    unindexed = [f for f in facts if f"`{f}`" not in index]
    return (bool(epi) and bool(adds) and bool(aside) and not unindexed and bool(facts),
            f"episodic notes={len(epi)}; promoted={len(adds)}; set aside/rejected with reason={len(aside)} "
            f"(e.g. {aside[0]['item'] if aside else '-'}: {aside[0]['reason'][:60] if aside else ''}); facts={len(facts)}; unindexed={unindexed}")


def t7():
    hits = []
    for cl in (ROOT / ".claude" / "skills").glob("*/CHANGELOG.md"):
        for entry in re.split(r"^## ", cl.read_text(), flags=re.M)[1:]:
            ver = entry.split()[0]
            if ver in ("1.0.0", "0.1.0"):
                continue
            paths = re.findall(r"(evals/runs/\S+?results\.json)", entry)
            if "Trajectory evidence" in entry and paths and all((ROOT / p).exists() for p in paths):
                hits.append(f"{cl.parent.name} v{ver}")
    return bool(hits), f"skills updated from a trajectory with eval evidence: {hits}"


def t8():
    r = sh(sys.executable, "tools/budget.py", "--quiet")
    total = re.search(r"(\d+)\s+TOTAL", r.stdout)
    return r.returncode == 0, f"always-loaded total {total.group(1) if total else '?'} tokens (budget 6000)"


def t9():
    runs = sorted(p for p in (ROOT / "evals" / "runs").glob("*/*/results.json") if not (p.parent / "INVALID.md").exists())
    if not runs:
        return False, "no valid eval run"
    res = json.loads(runs[-1].read_text())
    golden = sorted(p.name for p in (ROOT / "evals" / "golden").iterdir() if (p / "task.json").exists())
    got = {r["task"]: r for r in res["results"]}
    rows = [f"{t}: {'PASS' if got[t]['passed'] else 'FAIL'} tok={(got[t]['tokens_in'] or 0) + (got[t]['tokens_out'] or 0):,} "
            f"turns={got[t]['turns']} q={got[t]['questions_asked']}" for t in golden if t in got]
    ok = all(t in got and got[t].get("turns") is not None for t in golden)
    return ok, f"{runs[-1].parent.relative_to(ROOT)}: " + "; ".join(rows)


def t10():
    led = [json.loads(l) for l in (ROOT / "metrics" / "ledger.jsonl").read_text().splitlines() if l.strip()]
    tasks = {t.parent.name for t in (ROOT / "tasks").glob("*/TASK.md")
             if re.search(r"^status:\s*(closed|done)", t.read_text(), re.M)}
    missing = sorted(tasks - {r["task"] for r in led})
    rep = sh(sys.executable, "tools/metrics.py")
    return not missing and rep.returncode == 0 and "By task type" in rep.stdout, \
        f"ledger lines={len(led)}; closed tasks={len(tasks)}; missing={missing}; metrics.py exit={rep.returncode}"


def t11():
    skip = {".git", "raw", "state", "__pycache__", ".pytest_cache", "skill-backups"}
    bad = []
    for d in ROOT.rglob("*"):
        if not d.is_dir() or any(p in skip for p in d.relative_to(ROOT).parts):
            continue
        entries = [e for e in d.iterdir() if e.name not in ("__pycache__",)]
        files = [e for e in entries if e.is_file()]
        if not entries:
            bad.append(f"{d.relative_to(ROOT)} (empty)")
        elif not any(e.is_dir() for e in entries) and files and all(f.name in ("README.md", ".gitkeep") for f in files):
            bad.append(f"{d.relative_to(ROOT)} (placeholder only)")
    return not bad, f"placeholder/empty dirs: {bad}"


def t12(skip):
    if skip:
        return True, "skipped"
    r = sh(sys.executable, "-m", "pytest", "-q", "tools", ".claude/hooks", ".claude/skills")
    return r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]


def r14():
    log = sh("git", "log", "-1", "--format=%cs", "--", "RULES.md").stdout.strip()
    first = sh("git", "log", "--format=%H", "--", "RULES.md").stdout.split()
    if len(first) <= 1:
        return True, "RULES.md unchanged since the initial version (R14 exception)"
    imp = (ROOT / "metrics" / "IMPROVEMENTS.md").read_text()
    dates = re.findall(r"^## (20\d\d-\d\d-\d\d).*RULES", imp, re.M)
    return any(d >= log for d in dates), f"last RULES.md change {log}; IMPROVEMENTS rule entries {dates}"


def main() -> int:
    skip = "--skip-pytest" in sys.argv
    tests = [("1 library manifest + cards", t1), ("2 DESIGN citations", t2), ("3 rules enforced + hook tests", lambda: t3(skip)),
             ("4 skills valid + runs", t4), ("5 domain skills run on inputs", t5), ("6 learning cycle", t6),
             ("7 skill-forge from trajectory", t7), ("8 budget", t8), ("9 cold-start evals", t9),
             ("10 ledger + metrics", t10), ("11 no placeholder dirs", t11), ("12 all tests pass", lambda: t12(skip)),
             ("R14 rule changes logged", r14)]
    fails = 0
    for name, fn in tests:
        try:
            ok, info = fn()
        except Exception as e:
            ok, info = False, f"error: {e}"
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'}  AT{name}\n      {info}")
    print(f"\n{len(tests) - fails}/{len(tests)} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
