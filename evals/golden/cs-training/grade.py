"""Golden grader: cs-training. Answer key is regenerated from the sheet by the frozen grader copy."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
import grade_common as g  # noqa: E402


def grade(ws: Path) -> dict:
    bp = g.load(HERE / "grader_lib" / "build_pack.py", "gbp")
    ct = g.load(HERE / "grader_lib" / "check_training.py", "gct")
    checks, deliv = g.pipeline_checks(g.find_task(ws, "cs-training"), "cs-training.md")
    if deliv:
        sheet = (ws / "inputs" / "SAMPLE-product-sheet.md").read_text(encoding="utf-8")
        _, _, key = bp.build(sheet)
        c, _ = g.run_checker(ct.checks, deliv.read_text(encoding="utf-8"), sheet, key)
        checks += c
    return g.summarize(checks)
