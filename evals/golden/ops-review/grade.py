"""Golden grader: ops-review. Reference KPIs are recomputed from the inputs by the frozen grader copy."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
import grade_common as g  # noqa: E402


def grade(ws: Path) -> dict:
    ck = g.load(HERE / "grader_lib" / "compute_kpis.py", "gck")
    cr = g.load(HERE / "grader_lib" / "check_review.py", "gcr")
    checks, deliv = g.pipeline_checks(g.find_task(ws, "ops-review"), "ops-review.md")
    if deliv:
        ref = ck.compute(ws / "inputs" / "SAMPLE-ops-export")
        c, _ = g.run_checker(cr.checks, deliv.read_text(encoding="utf-8"), ref)
        checks += c
    return g.summarize(checks)
