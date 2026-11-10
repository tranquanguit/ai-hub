import importlib.util
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent


def setup(tmp_path, monkeypatch):
    monkeypatch.setenv("LUNO_ROOT", str(tmp_path))
    d = tmp_path / "tasks" / "2026-11-10-x"
    (d / "evidence").mkdir(parents=True)
    (d / "evidence" / "check.txt").write_text("PASS")
    (d / "TASK.md").write_text("---\ntask: 2026-11-10-x\ntask_type: ops-review\nrole: founder\nstatus: closed\n---\n")
    (d / "LEDGER.md").write_text("- [scripted] a -> b -> c\n- [question] clarify -> asked user: budget? -> 20m\n")
    (tmp_path / ".claude/state").mkdir(parents=True)
    (tmp_path / ".claude/state/current_task").write_text("tasks/2026-11-10-x")
    spec = importlib.util.spec_from_file_location("reflect", HERE / "reflect.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, d


def test_new_finish_cycle(tmp_path, monkeypatch):
    m, d = setup(tmp_path, monkeypatch)
    assert m.main(["new"]) == 0
    note = tmp_path / "memory/episodic/2026-11-10-x.md"
    assert "asked user: budget?" in note.read_text()
    assert m.main(["finish"]) == 1  # TODOs left
    note.write_text(note.read_text().replace("TODO", "done"))
    assert m.main(["finish"]) == 0
    assert "status: done" in (d / "TASK.md").read_text()
    assert not (tmp_path / ".claude/state/current_task").exists()


def test_candidate_format(tmp_path, monkeypatch):
    m, _ = setup(tmp_path, monkeypatch)
    m.main(["candidate", "--key", "ads.roas.floor", "--claim", "Pause campaigns under ROAS 1.5", "--value", "1.5",
            "--source", "tasks/2026-11-10-x/evidence/check.txt", "--kind", "tool",
            "--evidence", "tasks/2026-11-10-x/evidence/check.txt", "--tags", "ads,roas"])
    p = next((tmp_path / "memory/inbox").glob("*.md"))
    fm = yaml.safe_load(p.read_text().split("---")[1])
    assert fm["verification"] == {"kind": "tool", "evidence": "tasks/2026-11-10-x/evidence/check.txt"}
    assert fm["tags"] == ["ads", "roas"] and fm["task"] == "2026-11-10-x"
