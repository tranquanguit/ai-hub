import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "AGENTS.md").exists())


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_allocation_sums_and_respects_bounds():
    ab = load("allocate_budget")
    p = ab.params(REPO / "inputs" / "SAMPLE-phase-brief.md")
    a = ab.allocate(p)
    total = sum(r["amount_vnd"] for r in a["rows"]) + a["reserve_vnd"]
    assert total == p["total_budget_vnd"] == 300_000_000
    for r in a["rows"]:
        c = p["channels"][r["channel"]]
        work_share = r["amount_vnd"] / (p["total_budget_vnd"] - a["reserve_vnd"])
        assert c["min_share"] - 0.001 <= work_share <= c["max_share"] + 0.001
        assert sum(r["per_month_vnd"]) == r["amount_vnd"]
    assert "**300,000,000**" in ab.to_md(a)


def test_shares_water_filling():
    ab = load("allocate_budget")
    s = ab.shares({"a": {"roas": 10, "min_share": 0, "max_share": 0.5}, "b": {"roas": 1, "min_share": 0.2, "max_share": 1},
                   "c": {"roas": 1, "min_share": 0, "max_share": 1}})
    assert abs(sum(s.values()) - 1) < 1e-9 and s["a"] == 0.5 and s["b"] >= 0.2


def test_checker_pass_and_fail(tmp_path):
    ab, cp = load("allocate_budget"), load("check_plan")
    a = ab.allocate(ab.params(REPO / "inputs" / "SAMPLE-phase-brief.md"))
    strat = "\n".join(f"### {r['channel']}\nplan" for r in a["rows"])
    good = (f"# Plan (SAMPLE input)\n## Kênh bán hàng\nx\n## Khu vực trọng điểm\nx\n## Khách hàng mục tiêu\nx\n"
            f"## Ngân sách\n{ab.to_md(a)}\n## Chiến lược theo kênh\n{strat}\n## KPI\nDoanh thu 1,200,000,000; đơn 4,000; CPA 75,000\n"
            "## Lịch triển khai\nx\n## Rủi ro\nx\n## Giả định & nguồn\nx\n## English summary\nx\n")
    assert all(ok for _, ok, _ in cp.checks(good, a))
    bad = good.replace("**300,000,000**", "**290,000,000**").replace("plan", "Serum đặc trị mụn")
    names = {n for n, ok, _ in cp.checks(bad, a) if not ok}
    assert {"budget_total_matches_brief", "no_banned_claims"} <= names
    pii = good + "\nGọi chị Lan " + "09" + "12345678"
    assert ("no_pii", False) in [(n, ok) for n, ok, _ in cp.checks(pii, a)]


def test_goal_gap_v110():
    ab = load("allocate_budget")
    p = ab.params(REPO / "inputs" / "SAMPLE-phase-brief.md")
    p["goals"] = {"revenue_vnd": 1_200_000_000, "orders": 4000}
    g = ab.allocate(p)["goal_gap"]
    assert 225_000 < g["implied_aov_vnd"] < 240_000 and g["revenue_gap_vnd"] < 0 and g["orders_gap"] > 0
