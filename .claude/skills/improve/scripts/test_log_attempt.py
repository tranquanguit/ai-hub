import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def test_log_attempt(tmp_path, monkeypatch):
    monkeypatch.setenv("LUNO_ROOT", str(tmp_path))
    (tmp_path / "metrics").mkdir()
    spec = importlib.util.spec_from_file_location("log_attempt", HERE / "log_attempt.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.main(["--title", "t", "--metric", "scripted_ratio", "--hypothesis", "h", "--change", "c",
            "--before", "evals/runs/a/results.json", "--after", "evals/runs/b/results.json", "--decision", "reverted"])
    text = (tmp_path / "metrics/IMPROVEMENTS.md").read_text()
    assert "Decision: **reverted**" in text and "evals/runs/b/results.json" in text
