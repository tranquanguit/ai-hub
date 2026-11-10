"""Tests for promote.py (R2-R5, R9), skill_stats.py (R7), metrics.py, prune.py."""
import json
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import metrics  # noqa: E402
import promote  # noqa: E402
import prune  # noqa: E402
import skill_stats  # noqa: E402


@pytest.fixture
def repo(tmp_path, monkeypatch):
    for d in ["memory/inbox", "memory/semantic", "memory/conflicts", "memory/archive", "tasks/t/evidence",
              ".claude/hooks", ".claude/skills", ".claude/skill-drafts", "tools", "metrics"]:
        (tmp_path / d).mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO / ".claude/hooks/pre_tool_use.py", tmp_path / ".claude/hooks/")
    shutil.copy(REPO / ".claude/hooks/common.py", tmp_path / ".claude/hooks/")
    shutil.copy(REPO / "tools/validate_skills.py", tmp_path / "tools/")
    (tmp_path / "tasks/t/evidence/check.txt").write_text("PASS")
    monkeypatch.setattr(promote, "ROOT", tmp_path)
    monkeypatch.setattr(promote, "MEM", tmp_path / "memory")
    return tmp_path


def inbox(repo, name, **fm):
    base = {"type": "fact", "key": "product.serum.price", "claim": "Serum retail price is 450,000 VND", "value": "450000",
            "source": "canon/company.md", "confidence": "high", "tags": ["product"],
            "verification": {"kind": "tool", "evidence": "tasks/t/evidence/check.txt"}}
    base.update(fm)
    p = repo / "memory/inbox" / name
    promote.write_md(p, base, "body\n")
    return p


def test_add_verified_fact_and_index(repo):
    print(promote.apply_item(inbox(repo, "a.md")))
    f = repo / "memory/semantic/product.serum.price.md"
    assert f.exists()
    fm, _ = promote.read_md(f)
    assert fm["helpful"] == 0 and fm["source"] == "canon/company.md"
    promote.cmd_index(quiet=True)
    assert "product.serum.price" in (repo / "memory/INDEX.md").read_text()
    assert json.loads((repo / "memory/curation-log.jsonl").read_text().splitlines()[0])["action"] == "add"


def test_self_assessment_rejected(repo):
    msg = promote.apply_item(inbox(repo, "b.md", verification={"kind": "self", "evidence": "tasks/t/evidence/check.txt"}))
    assert "rejected" in msg and "R2" in msg
    fm, _ = promote.read_md(repo / "memory/archive/rejected/b.md")
    assert "R2" in fm["reject_reason"]


def test_missing_evidence_and_source_rejected(repo):
    assert "R2" in promote.apply_item(inbox(repo, "c.md", verification={"kind": "test", "evidence": "nope.txt"}))
    assert "R9" in promote.apply_item(inbox(repo, "d.md", source=""))


def test_pii_rejected(repo):
    assert "R15" in promote.apply_item(inbox(repo, "e.md", claim="Customer phone " + "09" + "12345678"))


def test_duplicate_merges_and_bumps_helpful(repo):
    promote.apply_item(inbox(repo, "a.md"))
    msg = promote.apply_item(inbox(repo, "a2.md", value="450,000"))
    assert "merged" in msg
    fm, _ = promote.read_md(repo / "memory/semantic/product.serum.price.md")
    assert fm["helpful"] == 1


def test_conflict_goes_to_conflicts(repo):
    promote.apply_item(inbox(repo, "a.md"))
    msg = promote.apply_item(inbox(repo, "z.md", value="390000", source="inputs/x.csv"))
    assert "set aside" in msg
    fm, _ = promote.read_md(repo / "memory/conflicts/z.md")
    assert fm["existing_value"] == "450000" and fm["source"] == "inputs/x.csv"  # both sources kept
    f, _ = promote.read_md(repo / "memory/semantic/product.serum.price.md")
    assert f["value"] == "450000"  # never overwritten (R4)


def test_resolve_keep_new_archives_old(repo):
    promote.apply_item(inbox(repo, "a.md"))
    promote.apply_item(inbox(repo, "z.md", value="390000"))
    promote.main(["resolve", str(repo / "memory/conflicts/z.md"), "--keep", "new"])
    f, _ = promote.read_md(repo / "memory/semantic/product.serum.price.md")
    assert str(f["value"]) == "390000" and (repo / "memory/archive/product.serum.price.md").exists()


def test_skill_delta_deferred(repo):
    assert "deferred" in promote.apply_item(inbox(repo, "s.md", type="skill-delta"))
    assert (repo / "memory/inbox/s.md").exists()


def make_draft(repo, name, lines=20, golden=False):
    d = repo / ".claude/skill-drafts" / name
    d.mkdir(parents=True)
    body = "\n".join(f"## {s}\nx" for s in ["When to use", "Inputs", "Steps", "Memory facts", "Verification", "Close"])
    pad = "\n".join("line" for _ in range(lines))
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Demo skill. Use in tests.\n---\n{body}\n{pad}\n")
    (d / "stats.json").write_text(json.dumps({**skill_stats.DEFAULT, "version": "0.2.0"}))
    (d / "CHANGELOG.md").write_text("## 0.2.0")
    if golden:
        (repo / "evals/golden" / name).mkdir(parents=True)
    return d


def test_skill_promotion_gates(repo):
    make_draft(repo, "demo", golden=True)
    assert promote.main(["skill", "demo"]) == 1  # needs eval (R6)
    (repo / "evals/runs/x").mkdir(parents=True)
    (repo / "evals/runs/x/results.json").write_text(json.dumps({"results": [{"task": "demo", "passed": False}]}))
    assert promote.main(["skill", "demo", "--eval", "evals/runs/x/results.json"]) == 1
    (repo / "evals/runs/x/results.json").write_text(json.dumps({"results": [{"task": "demo", "passed": True}]}))
    assert promote.main(["skill", "demo", "--eval", "evals/runs/x/results.json"]) == 0
    assert (repo / ".claude/skills/demo/SKILL.md").exists() and not (repo / ".claude/skill-drafts/demo").exists()


def test_skill_promotion_blocks_big_shrink(repo):
    make_draft(repo, "demo2", lines=100)
    assert promote.main(["skill", "demo2"]) == 0
    make_draft(repo, "demo2", lines=5)
    assert promote.main(["skill", "demo2"]) == 1  # R5 deltas, not rewrites
    assert promote.main(["skill", "demo2", "--allow-shrink"]) == 0


def test_skill_stats_and_candidates(tmp_path, monkeypatch):
    monkeypatch.setattr(skill_stats, "SKILLS", tmp_path)
    (tmp_path / "x").mkdir()
    for i in range(3):
        skill_stats.record("x", "pass", scripted="kpis", reasoned="format table")
    d = skill_stats.record("x", "fail", failure="bad sum")
    assert d["runs"] == 4 and d["failures"] == 1 and d["last_failure"]["why"] == "bad sum"
    assert d["scripted_steps"] == 3 and d["reasoned_steps"] == 3
    assert skill_stats.candidates() == [("x", "format table", 3)]


def test_metrics_report_and_worst(tmp_path, monkeypatch):
    led = tmp_path / "ledger.jsonl"
    monkeypatch.setattr(metrics, "LEDGER", led)
    rs = [{"date": "2026-11-02", "task": "a", "task_type": "ops-review", "tokens_in": 1000, "tokens_out": 100, "turns": 5,
           "questions_asked": 2, "verification_passed": True, "rework_count": 1, "scripted_steps": 1, "reasoned_steps": 3},
          {"date": "2026-11-10", "task": "b", "task_type": "ops-review", "tokens_in": 800, "tokens_out": 80, "turns": 3,
           "questions_asked": 0, "verification_passed": True, "rework_count": 0, "scripted_steps": 3, "reasoned_steps": 1}]
    led.write_text("".join(json.dumps(r) + "\n" for r in rs))
    rep = metrics.report()
    assert "ops-review | 2" in rep and "2026-W45" in rep and "2026-W46" in rep
    s = metrics.summarize(rs)
    assert s["first_pass_rate"] == 0.5 and s["scripted_ratio"] == 0.5 and s["median_tokens"] == 990
    # 1 question/task vs target 0.5 -> gap 0.5 beats first-pass gap (0.9-0.5)/0.9 = 0.44
    assert metrics.worst()["metric"] == "questions_per_task"


def test_prune_proposes_old_and_harmful(repo, monkeypatch):
    promote.apply_item(inbox(repo, "a.md"))
    promote.apply_item(inbox(repo, "b.md", key="channel.tiktok.cpc", value="1200", claim="TikTok CPC"))
    p = repo / "memory/semantic/channel.tiktok.cpc.md"
    fm, body = promote.read_md(p)
    fm["harmful"] = 2
    promote.write_md(p, fm, body)
    later = date.today() + timedelta(days=120)
    prop = prune.propose(later)
    names = dict(prop["facts"])
    assert "harmful" in names["channel.tiktok.cpc"] and "days" in names["product.serum.price"]


def test_plan_simulates_batch_conflicts(repo, capsys):
    inbox(repo, "a.md")
    inbox(repo, "b.md", value="390000")
    promote.cmd_plan(None)
    out = capsys.readouterr().out
    assert "add" in out and "conflict" in out and "earlier batch item a.md" in out
