import importlib.util
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "AGENTS.md").exists())


def test_curate_report(tmp_path, monkeypatch):
    monkeypatch.setenv("LUNO_ROOT", str(tmp_path))
    for d in ("tools", ".claude/hooks", "memory/inbox", "memory/semantic", "tasks/t/evidence"):
        (tmp_path / d).mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO / "tools/promote.py", tmp_path / "tools/")
    shutil.copy(REPO / ".claude/hooks/pre_tool_use.py", tmp_path / ".claude/hooks/")
    shutil.copy(REPO / ".claude/hooks/common.py", tmp_path / ".claude/hooks/")
    (tmp_path / "tasks/t/evidence/c.txt").write_text("ok")
    (tmp_path / "memory/inbox/good.md").write_text(
        "---\nkey: a.b\nclaim: A is B\nvalue: '1'\nsource: canon/company.md\nverification: {kind: tool, evidence: tasks/t/evidence/c.txt}\n---\nx\n")
    (tmp_path / "memory/inbox/bad.md").write_text(
        "---\nkey: a.c\nclaim: A is C\nsource: me\nverification: {kind: self, evidence: tasks/t/evidence/c.txt}\n---\nx\n")
    spec = importlib.util.spec_from_file_location("curate", HERE / "curate.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.main(["--out", "tasks/t/evidence/curation.md"])
    rep = (tmp_path / "tasks/t/evidence/curation.md").read_text()
    assert "| good.md | add |" in rep and "| bad.md | reject |" in rep and "add=1" in rep and "reject=1" in rep
    assert (tmp_path / "memory/semantic/a.b.md").exists() and (tmp_path / "memory/INDEX.md").exists()
