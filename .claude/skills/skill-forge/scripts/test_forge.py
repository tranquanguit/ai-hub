import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(tmp_path, monkeypatch):
    monkeypatch.setenv("LUNO_ROOT", str(tmp_path))
    spec = importlib.util.spec_from_file_location("forge", HERE / "forge.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_candidates_new_skill_after_two_successes(tmp_path, monkeypatch):
    (tmp_path / "metrics").mkdir()
    rows = [{"task": "a", "task_type": "content-calendar", "verification_passed": True},
            {"task": "b", "task_type": "content-calendar", "verification_passed": True},
            {"task": "c", "task_type": "ops-review", "verification_passed": True}]
    (tmp_path / "metrics/ledger.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (tmp_path / ".claude/skills/ops-review").mkdir(parents=True)
    (tmp_path / ".claude/skills/ops-review/stats.json").write_text(json.dumps({"step_counts": {"format table": 3}}))
    (tmp_path / "memory/inbox").mkdir(parents=True)
    (tmp_path / "memory/inbox/x.md").write_text("---\ntype: skill-delta\nclaim: add step\ntags: [ops-review]\n---\nd\n")
    m = load(tmp_path, monkeypatch)
    c = m.candidates()
    assert c["new_skills"][0]["task_type"] == "content-calendar" and c["new_skills"][0]["trajectories"] == ["a", "b"]
    assert c["skill_deltas"][0]["tags"] == ["ops-review"]
    assert c["script_candidates"] == [{"skill": "ops-review", "step": "format table", "times": 3}]


def test_draft_and_changelog(tmp_path, monkeypatch):
    m = load(tmp_path, monkeypatch)
    m.main(["draft", "content-calendar", "--new"])
    d = tmp_path / ".claude/skill-drafts/content-calendar"
    assert "name: content-calendar" in (d / "SKILL.md").read_text()
    m.main(["changelog", "content-calendar", "--version", "0.2.0", "--why", "w", "--evidence", "tasks/a/LEDGER.md",
            "--eval-after", "evals/runs/x/results.json"])
    assert json.loads((d / "stats.json").read_text())["version"] == "0.2.0"
    assert "Eval after: evals/runs/x/results.json" in (d / "CHANGELOG.md").read_text()
