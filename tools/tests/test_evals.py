"""Tests for evals/run_cold_start.py comparison/question filing and the golden graders."""
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("rcs", REPO / "evals" / "run_cold_start.py")
rcs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rcs)


def res(task, passed, score, tok=100):
    return {"task": task, "passed": passed, "score": score, "tokens_in": tok, "tokens_out": 10, "turns": 5, "cost_usd": 0.1}


def test_compare_flags_regressions(tmp_path, monkeypatch):
    monkeypatch.setattr(rcs, "ROOT", tmp_path)
    prev = tmp_path / "prev.json"
    prev.write_text(json.dumps({"results": [res("a", True, 1.0), res("b", True, 0.9)]}))
    lines = rcs.compare({"results": [res("a", True, 1.0), res("b", True, 0.8)]}, prev)
    assert any("REGRESSION b" in l for l in lines) and not any("REGRESSION a" in l for l in lines)
    lines = rcs.compare({"results": [res("a", False, 1.0)]}, prev)
    assert any("REGRESSION a" in l for l in lines)
    assert "baseline" in rcs.compare({"results": []}, None)[0]


def test_file_questions(tmp_path, monkeypatch):
    monkeypatch.setattr(rcs, "ROOT", tmp_path)
    (tmp_path / "memory" / "inbox").mkdir(parents=True)
    n = rcs.file_questions([{"task": "ops-review", "questions": ["What is the CPA target?"]}], "evals/runs/x")
    assert n == 1
    text = next((tmp_path / "memory" / "inbox").glob("*.md")).read_text()
    assert "type: question" in text and "CPA target" in text


def test_graders_on_empty_workspace(tmp_path):
    for t in ("ops-review", "cs-training", "phase-plan"):
        g = rcs.load_grader(t).grade(tmp_path)
        assert g["passed"] is False and g["checks"][0]["name"] == "task_folder_created"
