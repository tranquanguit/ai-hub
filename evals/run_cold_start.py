#!/usr/bin/env python3
"""Run golden tasks in fresh headless Claude Code sessions and compare with the previous run (Phase 7).

  python3 evals/run_cold_start.py --all [--model sonnet] [--label baseline] [--parallel 3]
  python3 evals/run_cold_start.py --task ops-review --use-draft ops-review --label forge-ops-review
  python3 evals/run_cold_start.py --grade-only <workspace> --task ops-review     # grade an existing dir
  python3 evals/run_cold_start.py --compare-only                                 # compare last two runs

Each task: `git worktree add` of HEAD in a temp dir (no history, no conversation), optional draft
skill copied over the active one, then `claude -p <prompt> --output-format json` with LUNO_ROLE set.
Measured from the JSON: total_cost_usd, usage tokens, num_turns. Questions = AskUserQuestion
attempts + [question] ledger lines + a final reply that ends in a question. Each question becomes a
`type: question` inbox item (a gap the repo should have answered). Results go to
evals/runs/<date>/<HHMMSS>-<label>/results.json (+ summary.md, per-task outputs).
Exit 1 on any regression versus the previous run (R6).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "evals" / "golden"
RUNS = ROOT / "evals" / "runs"
ALLOWED_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python3 *)", "Bash(mkdir *)", "Bash(ls *)",
                 "Bash(cat *)", "Bash(head *)", "Bash(tail *)", "Bash(wc *)", "Bash(grep *)", "Bash(sed -n *)",
                 "Bash(date *)", "Bash(cp inputs/*)", "Agent", "Skill", "TodoWrite"]


def load_grader(task: str):
    spec = importlib.util.spec_from_file_location(f"grade_{task}", GOLDEN / task / "grade.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def git(*args, cwd=ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def make_workspace(draft: str | None) -> Path:
    base = Path(tempfile.mkdtemp(prefix="luno-eval-"))
    ws = base / "ws"
    git("worktree", "add", "--detach", str(ws), "HEAD")
    if draft:
        src = ROOT / ".claude" / "skill-drafts" / draft
        if not src.exists():
            raise SystemExit(f"no draft {draft}")
        dst = ws / ".claude" / "skills" / draft
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    # Cold start: no previous work products. Finished task folders would let the agent copy an old
    # deliverable instead of doing the task (found in the first baseline run). Learned memory stays.
    for t in (ws / "tasks").glob("*"):
        if t.is_dir():
            shutil.rmtree(t)
    (ws / ".claude" / "state").mkdir(parents=True, exist_ok=True)
    (ws / ".claude" / "state" / "current_task").unlink(missing_ok=True)
    return ws


def drop_workspace(ws: Path) -> None:
    try:
        git("worktree", "remove", "--force", str(ws))
    except Exception:
        shutil.rmtree(ws, ignore_errors=True)
        git("worktree", "prune")
    shutil.rmtree(ws.parent, ignore_errors=True)


def count_questions(out: dict, ws: Path, task_type: str) -> list[str]:
    qs = [d.get("tool_input", {}).get("questions", [{}])[0].get("question", "AskUserQuestion")
          for d in out.get("permission_denials", []) if d.get("tool_name") == "AskUserQuestion"]
    for t in (ws / "tasks").glob("*/LEDGER.md"):
        qs += [l.split("] ", 1)[-1] for l in t.read_text().splitlines() if "[question]" in l]
    final = (out.get("result") or "").strip()
    if final.endswith("?"):
        qs.append(final.splitlines()[-1][:200])
    return qs


def run_task(task: str, model: str, draft: str | None, outdir: Path, keep: bool = False) -> dict:
    spec = json.loads((GOLDEN / task / "task.json").read_text())
    ws = make_workspace(draft)
    env = {**os.environ, "LUNO_ROLE": spec.get("role", "founder")}
    env.pop("CLAUDE_CODE_SESSION_ID", None)
    cmd = ["claude", "-p", spec["prompt"], "--output-format", "json", "--model", model, "--max-turns",
           str(spec.get("max_turns", 60)), "--permission-mode", "acceptEdits", "--no-session-persistence",
           "--allowedTools", *ALLOWED_TOOLS]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=ws, env=env, capture_output=True, text=True, timeout=spec.get("timeout_s", 1500))
        raw = p.stdout
    except subprocess.TimeoutExpired as e:
        raw = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    dur = round(time.time() - t0, 1)
    try:
        out = json.loads(raw.strip().splitlines()[-1]) if raw.strip() else {}
    except Exception:
        out = {"result": raw[-2000:], "is_error": True}
    grade = load_grader(task).grade(ws)
    u = out.get("usage") or {}
    qs = count_questions(out, ws, spec["task_type"])
    rework = sum(t.read_text().count("[rework]") for t in (ws / "tasks").glob("*/LEDGER.md"))
    tdir = outdir / task
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / "claude_output.json").write_text(json.dumps({k: v for k, v in out.items() if k != "modelUsage"}, indent=1,
                                                        ensure_ascii=False))
    (tdir / "grade.json").write_text(json.dumps(grade, indent=1, ensure_ascii=False))
    for t in (ws / "tasks").glob("*"):
        if (t / "TASK.md").exists():
            shutil.copytree(t, tdir / "task", dirs_exist_ok=True, ignore=shutil.ignore_patterns("private"))
    res = {"task": task, "passed": grade["passed"], "score": grade["score"], "model": model, "draft": draft,
           "tokens_in": (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)) or None,
           "tokens_out": u.get("output_tokens"), "cost_usd": out.get("total_cost_usd"), "turns": out.get("num_turns"),
           "duration_s": dur, "rework": rework, "questions": qs, "questions_asked": len(qs), "is_error": out.get("is_error"),
           "failed_checks": [c["name"] for c in grade["checks"] if not c["ok"]]}
    if not keep:
        drop_workspace(ws)
    else:
        res["workspace"] = str(ws)
    return res


def previous_results(exclude: Path | None) -> Path | None:
    runs = sorted(p for p in RUNS.glob("*/*/results.json")
                  if (exclude is None or p.parent != exclude) and not (p.parent / "INVALID.md").exists())
    return runs[-1] if runs else None


def compare(cur: dict, prev_path: Path | None) -> list[str]:
    if not prev_path:
        return ["no previous run: this run is the baseline"]
    prev = {r["task"]: r for r in json.loads(prev_path.read_text())["results"]}
    lines = [f"compared with {prev_path.relative_to(ROOT)}"]
    for r in cur["results"]:
        p = prev.get(r["task"])
        if not p:
            lines.append(f"  {r['task']}: new task")
            continue
        reg = (p["passed"] and not r["passed"]) or (r["score"] < p["score"] - 1e-9)
        delta_tok = (r["tokens_in"] or 0) + (r["tokens_out"] or 0) - (p.get("tokens_in") or 0) - (p.get("tokens_out") or 0)
        lines.append(f"  {'REGRESSION ' if reg else ''}{r['task']}: passed {p['passed']}->{r['passed']}, score {p['score']}->{r['score']}, "
                     f"turns {p.get('turns')}->{r.get('turns')}, tokens Δ{delta_tok:+,}, cost {p.get('cost_usd')}->{r.get('cost_usd')}")
    return lines


def file_questions(results: list[dict], run_rel: str) -> int:
    n = 0
    inbox = ROOT / "memory" / "inbox"
    for r in results:
        for i, q in enumerate(r["questions"], 1):
            slug = re.sub(r"[^a-z0-9]+", "-", f"eval-question-{r['task']}-{i}").strip("-")
            p = inbox / f"{datetime.now().date()}-{slug}.md"
            q1 = q.replace("\n", " ").replace('"', "'")[:300]
            p.write_text(f"---\ntype: question\nkey: question.eval.{r['task']}.{i}\nclaim: \"Cold-start agent asked: {q1}\"\n"
                         f"source: {run_rel}/{r['task']}/claude_output.json\ntags: [eval, question, {r['task']}]\n---\n"
                         "A fresh session needed to ask this; the repo should answer it (canon, memory or skill).\n")
            n += 1
    return n


def write_summary(res: dict, cmp_lines: list[str], outdir: Path) -> str:
    lines = [f"# Cold-start eval {res['run']}", "", f"commit {res['commit']} | model {res['model']}", "",
             "| task | passed | score | tokens in | tokens out | cost $ | turns | rework | questions | failed checks |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["results"]:
        lines.append(f"| {r['task']}{' (draft)' if r['draft'] else ''} | {'PASS' if r['passed'] else 'FAIL'} | {r['score']} | "
                     f"{r['tokens_in'] or '–'} | {r['tokens_out'] or '–'} | {r['cost_usd'] if r['cost_usd'] is not None else '–'} | "
                     f"{r['turns'] or '–'} | {r.get('rework', '–')} | {r['questions_asked']} | {', '.join(r['failed_checks']) or '–'} |")
    lines += ["", "## Comparison", ""] + [f"- {l}" for l in cmp_lines]
    text = "\n".join(lines) + "\n"
    (outdir / "summary.md").write_text(text)
    return text


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--task", action="append", default=[])
    ap.add_argument("--use-draft", action="append", default=[],
                    help="skill name whose .claude/skill-drafts/<name> replaces the active skill (repeatable, or 'all')")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--label", default="run")
    ap.add_argument("--parallel", type=int, default=3)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--baseline", help="results.json to compare against (default: previous valid run)")
    ap.add_argument("--invalidate", help="run dir to mark INVALID (excluded from comparisons)")
    ap.add_argument("--reason", default="")
    ap.add_argument("--grade-only")
    ap.add_argument("--compare-only", action="store_true")
    ap.add_argument("--no-questions", action="store_true", help="do not file questions into memory/inbox")
    a = ap.parse_args(argv)
    if a.invalidate:
        d = ROOT / a.invalidate
        (d / "INVALID.md").write_text(f"# INVALID run\n\n{a.reason or 'marked invalid'}\n")
        print(f"marked {a.invalidate} INVALID")
        return 0
    if a.grade_only:
        for t in a.task:
            print(json.dumps(load_grader(t).grade(Path(a.grade_only)), indent=1, ensure_ascii=False))
        return 0
    if a.compare_only:
        runs = sorted(p for p in RUNS.glob("*/*/results.json") if not (p.parent / "INVALID.md").exists())
        if len(runs) < 2:
            print("need two runs")
            return 0
        lines = compare(json.loads(runs[-1].read_text()), runs[-2])
        print("\n".join(lines))
        return 1 if any("REGRESSION" in l for l in lines) else 0
    tasks = sorted(p.name for p in GOLDEN.iterdir() if (p / "task.json").exists()) if a.all else a.task
    if not tasks:
        ap.error("--all or --task")
    now = datetime.now(timezone.utc)
    outdir = RUNS / now.strftime("%Y-%m-%d") / f"{now.strftime('%H%M%S')}-{a.label}"
    outdir.mkdir(parents=True, exist_ok=True)
    prev = (ROOT / a.baseline) if a.baseline else previous_results(outdir)
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as ex:
        def draft_for(t):
            if t in a.use_draft or ("all" in a.use_draft and (ROOT / ".claude" / "skill-drafts" / t).exists()):
                return t
            return None
        futs = {ex.submit(run_task, t, a.model, draft_for(t), outdir, a.keep): t for t in tasks}
        results = []
        for f in cf.as_completed(futs):
            try:
                results.append(f.result())
            except Exception as e:
                results.append({"task": futs[f], "passed": False, "score": 0.0, "error": str(e), "questions": [],
                                "questions_asked": 0, "tokens_in": None, "tokens_out": None, "cost_usd": None,
                                "turns": None, "draft": None, "failed_checks": ["runner_error"]})
    results.sort(key=lambda r: r["task"])
    res = {"run": str(outdir.relative_to(ROOT)), "date": now.isoformat(timespec="seconds"), "commit": git("rev-parse", "--short", "HEAD"),
           "model": a.model, "label": a.label, "results": results}
    (outdir / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    errored = [r["task"] for r in results if r.get("is_error") or r.get("error")]
    if errored:  # a session that errored (usage limit, crash) says nothing about the skill
        (outdir / "INVALID.md").write_text(f"# INVALID run\n\nSessions errored for: {', '.join(errored)}. "
                                           "Excluded from comparisons; re-run.\n")
        print(f"INVALID run: sessions errored for {errored}")
        return 2
    cmp_lines = compare(res, prev)
    print(write_summary(res, cmp_lines, outdir))
    if not a.no_questions:
        n = file_questions(results, res["run"])
        if n:
            print(f"{n} question(s) filed to memory/inbox as type: question")
    return 1 if any("REGRESSION" in l for l in cmp_lines) else 0


if __name__ == "__main__":
    sys.exit(main())
