import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def test_rank(tmp_path, monkeypatch):
    monkeypatch.setenv("LUNO_ROOT", str(tmp_path))
    (tmp_path / "library/cards").mkdir(parents=True)
    (tmp_path / "library/cards/1.md").write_text("---\nid: '1'\ntags: [memory, curator]\n---\n## Claim\nmemory curator deltas\n"
                                                 "## We reject\nunrelated words zebra\n")
    (tmp_path / "DESIGN.md").write_text("## learning-loop\ncurator applies deltas to memory\n## evals\njudge zebra\n")
    spec = importlib.util.spec_from_file_location("affects", HERE / "affects.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    r = m.rank("1")
    assert r[0][0] == "learning-loop" and "curator" in r[0][2]
    assert all(a != "evals" for a, _, _ in r)  # "We reject" text is not used for matching
