import importlib.util
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


def load(tmp_path, monkeypatch):
    monkeypatch.setenv("LUNO_ROOT", str(tmp_path))
    spec = importlib.util.spec_from_file_location("start_task", HERE / "start_task.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_start_requires_role(tmp_path, monkeypatch):
    monkeypatch.delenv("LUNO_ROLE", raising=False)
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    m = load(tmp_path, monkeypatch)
    with pytest.raises(SystemExit):
        m.main(["--slug", "x", "--type", "ops-review", "--goal", "g"])


def test_start_and_log(tmp_path, monkeypatch):
    monkeypatch.setenv("LUNO_ROLE", "founder")
    (tmp_path / "memory" / "episodic").mkdir(parents=True)
    (tmp_path / "memory" / "INDEX.md").write_text("- `ads.roas.target` — ROAS target for ops-review is 2.0 [ads] (1.2, high)\n")
    m = load(tmp_path, monkeypatch)
    assert m.main(["--slug", "Weekly Review", "--type", "ops-review", "--goal", "Review ads", "--criterion", "kpis.json exists",
                   "--date", "2026-11-10"]) == 0
    d = tmp_path / "tasks" / "2026-11-10-weekly-review"
    t = (d / "TASK.md").read_text()
    assert "role: founder" in t and "- [ ] kpis.json exists" in t and "ads.roas.target" in t
    assert (tmp_path / ".claude/state/current_task").read_text() == "tasks/2026-11-10-weekly-review"
    m.main(["log", "compute", "ran compute_kpis.py", "12 campaigns", "--scripted"])
    m.main(["log", "fix", "recomputed", "ok", "--rework"])
    led = (d / "LEDGER.md").read_text()
    assert "[scripted] compute -> ran compute_kpis.py -> 12 campaigns" in led and "[rework]" in led
    assert "rework_count: 1" in (d / "TASK.md").read_text()
