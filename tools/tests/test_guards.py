"""Tests for budget.py, validate_skills.py, secret_scan.py, session_stats.py, set_role.py, library_index.py.

Fixtures that look like secrets or PII are assembled at runtime so this file itself never contains
one (the PreToolUse hook and pre-commit scan would rightly block it)."""
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import budget  # noqa: E402
import library_index  # noqa: E402
import secret_scan  # noqa: E402
import session_stats  # noqa: E402
import validate_skills  # noqa: E402

FAKE_PHONE = "09" + "12345678"
FAKE_AWS = "AKIA" + "ABCDEFGHIJKLMNOP"

GOOD_SKILL = """---
name: demo-skill
description: Does a demo thing. Use when testing the validator.
---
# demo
## When to use
x
## Inputs
x
## Steps
1. Run `scripts/run.py`.
## Memory facts used
none
## Verification
x
## Close
x
"""


def make_skill(root, name="demo-skill", text=GOOD_SKILL, stats=True, script=True):
    d = root / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(text)
    (d / "CHANGELOG.md").write_text("# changelog")
    if stats:
        (d / "stats.json").write_text(json.dumps({"runs": 0, "passes": 0, "failures": 0, "last_failure": None, "version": "0.1.0"}))
    if script:
        (d / "scripts").mkdir()
        (d / "scripts" / "run.py").write_text("print(1)")
    return d


def test_validate_good_skill(tmp_path):
    assert validate_skills.validate(make_skill(tmp_path)) == []


@pytest.mark.parametrize("bad,expect", [
    (GOOD_SKILL.replace("name: demo-skill", "name: Demo_Skill"), "invalid name"),
    (GOOD_SKILL.replace("Does a demo thing.", "x" * 250), "> 200"),
    (GOOD_SKILL.replace("## Verification\nx\n", ""), "Verification"),
    (GOOD_SKILL.replace("scripts/run.py", "scripts/missing.py"), "referenced file missing"),
    ("no frontmatter", "frontmatter"),
])
def test_validate_rejects(tmp_path, bad, expect):
    errs = validate_skills.validate(make_skill(tmp_path, text=bad))
    assert any(expect in e for e in errs), errs


def test_validate_name_must_match_dir(tmp_path):
    errs = validate_skills.validate(make_skill(tmp_path, name="other-name"))
    assert any("must equal directory" in e for e in errs)


def test_validate_requires_stats(tmp_path):
    assert any("stats.json" in e for e in validate_skills.validate(make_skill(tmp_path, stats=False)))


def test_budget_counts_imports_and_flags_dates(tmp_path):
    (tmp_path / "AGENTS.md").write_text("rules " * 100)
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\nhello\n")
    rows = budget.items(tmp_path)
    assert rows[0][1] >= 150  # AGENTS.md expanded into CLAUDE.md
    assert budget.checks(tmp_path) == []
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\nStatus as of 2026-11-10\n")
    assert any("date" in e for e in budget.checks(tmp_path))
    (tmp_path / "CLAUDE.md").write_text("x\n" * 130)
    assert any("lines" in e for e in budget.checks(tmp_path))


def test_budget_flags_long_description(tmp_path):
    (tmp_path / ".claude" / "skills").mkdir(parents=True)
    make_skill(tmp_path / ".claude" / "skills", text=GOOD_SKILL.replace("Does a demo thing.", "y" * 230))
    assert any("description" in e for e in budget.checks(tmp_path))


def test_secret_scan_detects(tmp_path, monkeypatch):
    monkeypatch.setattr(secret_scan, "ROOT", tmp_path)
    (tmp_path / "memory").mkdir()
    (tmp_path / "memory" / "a.md").write_text(f"call {FAKE_PHONE} now")
    (tmp_path / "memory" / "b.md").write_text(f"key {FAKE_AWS}")
    (tmp_path / "memory" / "c.md").write_text("price 450000 VND, support@lunobeau.vn")
    assert any("PII" in h for h in secret_scan.scan_file("memory/a.md"))
    assert any("secret" in h for h in secret_scan.scan_file("memory/b.md"))
    assert secret_scan.scan_file("memory/c.md") == []


def test_session_stats_dedupes_usage(tmp_path):
    lines = [
        {"type": "user", "message": {"role": "user", "content": "do it"}, "timestamp": "2026-11-10T10:00:00Z"},
        {"type": "assistant", "message": {"id": "m1", "usage": {"input_tokens": 10, "cache_read_input_tokens": 100, "output_tokens": 5},
                                           "content": [{"type": "thinking"}]}},
        {"type": "assistant", "message": {"id": "m1", "usage": {"input_tokens": 10, "cache_read_input_tokens": 100, "output_tokens": 5},
                                           "content": [{"type": "tool_use"}]}},
        {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result"}]}},
        {"type": "assistant", "message": {"id": "m2", "usage": {"input_tokens": 3, "output_tokens": 7}, "content": [{"type": "text"}]},
         "timestamp": "2026-11-10T10:01:00Z"},
    ]
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(json.dumps(l) for l in lines))
    s = session_stats.parse_transcript(p)
    assert s["tokens_in"] == 113 and s["tokens_out"] == 12 and s["api_calls"] == 2
    assert s["tool_calls"] == 1 and s["turns"] == 1 and s["duration_s"] == 60


def test_session_stats_backfills_ledger(tmp_path, monkeypatch):
    led = tmp_path / "ledger.jsonl"
    led.write_text(json.dumps({"task": "t1", "tokens_in": None}) + "\n" + json.dumps({"task": "t2", "tokens_in": 9}) + "\n")
    monkeypatch.setattr(session_stats, "LEDGER", led)
    assert session_stats.backfill_ledger("t1", {"tokens_in": 50, "tokens_out": 5, "tool_calls": 2})
    rows = [json.loads(l) for l in led.read_text().splitlines()]
    assert rows[0]["tokens_in"] == 50 and rows[1]["tokens_in"] == 9


def test_set_role_writes_state(tmp_path, monkeypatch):
    import set_role
    (tmp_path / "canon" / "roles").mkdir(parents=True)
    (tmp_path / "canon" / "roles" / "ROLES.json").write_text(json.dumps({"roles": {"cs": {"data_areas": ["cs"]}}}))
    monkeypatch.setattr(set_role, "ROOT", tmp_path)
    assert set_role.main(["cs", "--session", "abc"]) == 0
    assert (tmp_path / ".claude" / "state" / "roles" / "abc").read_text() == "cs"
    with pytest.raises(SystemExit):
        set_role.main(["hacker", "--session", "abc"])


def test_card_validator(tmp_path):
    (tmp_path / "DESIGN.md").write_text("## learning-loop\nx\n")
    card = tmp_path / "1234.5678.md"
    body = "\n".join(f"## {s}\ntext" for s in library_index.SECTIONS)
    card.write_text(f"---\nid: '1234.5678'\ntitle: T\nyear: 2025\ntags: [a]\nadopted_in: [DESIGN.md#learning-loop]\n---\n{body}\n")
    assert library_index.check_card(card, tmp_path) == []
    card.write_text(card.read_text().replace("## Limits\ntext\n", "").replace("learning-loop]", "nope]"))
    errs = library_index.check_card(card, tmp_path)
    assert any("Limits" in e for e in errs) and any("anchor" in e for e in errs)
