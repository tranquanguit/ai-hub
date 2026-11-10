"""Golden grader: phase-plan. Allocation is recomputed from the brief by the frozen grader copy."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
import grade_common as g  # noqa: E402


def grade(ws: Path) -> dict:
    ab = g.load(HERE / "grader_lib" / "allocate_budget.py", "gab")
    cp = g.load(HERE / "grader_lib" / "check_plan.py", "gcp")
    checks, deliv = g.pipeline_checks(g.find_task(ws, "phase-plan"), "phase-plan.md")
    if deliv:
        alloc = ab.allocate(ab.params(ws / "inputs" / "SAMPLE-phase-brief.md"))
        c, _ = g.run_checker(cp.checks, deliv.read_text(encoding="utf-8"), alloc)
        checks += c
    return g.summarize(checks)
