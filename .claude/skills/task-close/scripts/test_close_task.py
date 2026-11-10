import importlib.util
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "AGENTS.md").exists())


def setup(tmp_path, monkeypatch, evidence=True, ref=True):
    monkeypatch.setenv("LUNO_ROOT", str(tmp_path))
    (tmp_path / "tools").mkdir()
    for f in ("metrics.py", "skill_stats.py"):
        shutil.copy(REPO / "tools" / f, tmp_path / "tools" / f)
    d = tmp_path / "tasks" / "2026-11-10-x"
    (d / "evidence").mkdir(parents=True)
    (d / "TASK.md").write_text("---\ntask: 2026-11-10-x\ntask_type: ops-review\nrole: founder\nstatus: open\nrework_count: 1\n"
                               'skills: ["ops-review"]\n---\n# x\n')
    (d / "LEDGER.md").write_text("# L\n- a [scripted] k -> s -> o\n- b [reasoned] r -> r -> r\n- c [question] q -> q -> q\n"
                                 + ("- v [scripted] verify -> check -> evidence/check.txt PASS\n" if ref else ""))
    if evidence:
        (d / "evidence" / "check.txt").write_text("PASS")
    (tmp_path / ".claude/state").mkdir(parents=True)
    (tmp_path / ".claude/state/current_task").write_text("tasks/2026-11-10-x")
    (tmp_path / ".claude/skills/ops-review").mkdir(parents=True)
    spec = importlib.util.spec_from_file_location("close_task", HERE / "close_task.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, d


def test_close_refuses_without_evidence(tmp_path, monkeypatch):
    m, d = setup(tmp_path, monkeypatch, evidence=False)
    assert m.main(["--passed", "true"]) == 1
    assert "status: open" in (d / "TASK.md").read_text()


def test_close_refuses_without_ledger_reference(tmp_path, monkeypatch):
    m, _ = setup(tmp_path, monkeypatch, ref=False)
    assert m.main(["--passed", "true"]) == 1


def test_close_writes_ledger_and_stats(tmp_path, monkeypatch):
    m, d = setup(tmp_path, monkeypatch)
    assert m.main(["--passed", "true", "--tokens-in", "1000", "--cost", "0.12"]) == 0
    row = json.loads((tmp_path / "metrics/ledger.jsonl").read_text().splitlines()[0])
    assert row["task_type"] == "ops-review" and row["scripted_steps"] == 2 and row["reasoned_steps"] == 1
    assert row["questions_asked"] == 1 and row["rework_count"] == 1 and row["tokens_in"] == 1000
    assert "ops-review" in row["skills_used"]
    st = json.loads((tmp_path / ".claude/skills/ops-review/stats.json").read_text())
    assert st["runs"] == 1 and st["passes"] == 1
    assert "status: closed" in (d / "TASK.md").read_text()
