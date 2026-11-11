import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / "AGENTS.md").exists())
SHEET = (REPO / "inputs" / "SAMPLE-product-sheet.md").read_text()


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_parse_and_build():
    bp = load("build_pack")
    prods = bp.parse_products(SHEET)
    assert [p["sku"] for p in prods] == ["LB-SER-01", "LB-SUN-01", "LB-CLN-01", "LB-TNT-01"]
    assert prods[0]["price"] == "450000" and "Niacinamide" in prods[0]["ingredients"]
    facts, quiz, key = bp.build(SHEET)
    assert "450,000 VND" in facts and len(key) >= 14 and key["1"] == "450,000"


def good_pack(bp):
    facts, quiz, key = bp.build(SHEET)
    answers = "\n".join(f"- {n}: {a}" for n, a in key.items())
    dialogs = "\n".join(f"### Kịch bản {i}\nKhách: ...\nCSKH: Chào bạn ..." for i in range(1, 5))
    md = (f"# Training (SAMPLE)\n## Sản phẩm\n{facts}\n## Phân khúc khách hàng\nNữ 18–24 sinh viên; Nữ 25–34 văn phòng; "
          "Nữ 35–44; Nam 18–34\n## Quy trình phục vụ\nChào khách. Đổi trả trong 7 ngày. Phản hồi ≤ 15 phút. "
          "Khi khách báo kích ứng: hướng dẫn ngưng dùng, báo Founder trong ngày.\n"
          f"## Kịch bản mẫu\n{dialogs}\n## Câu hỏi thường gặp\nx\n## Bài kiểm tra\n{quiz}\n### Đáp án\n{answers}\n"
          "## English summary\nx\n")
    return md, key


def test_checker_pass_and_fail():
    bp, ct = load("build_pack"), load("check_training")
    md, key = good_pack(bp)
    assert all(ok for _, ok, _ in ct.checks(md, SHEET, key)), [c for c in ct.checks(md, SHEET, key) if not c[1]]
    bad = md.replace("450,000", "400,000").replace("Chào khách.", "Serum trị mụn hiệu quả.")
    failed = {n for n, ok, _ in ct.checks(bad, SHEET, key) if not ok}
    assert {"all_skus_with_price", "no_banned_claims"} <= failed


def test_assemble_pack_v110(tmp_path):
    bp, ap, ct = load("build_pack"), load("assemble_pack"), load("check_training")
    facts, quiz, key = bp.build(SHEET)
    (tmp_path / "product_facts.md").write_text(facts); (tmp_path / "quiz.md").write_text(quiz)
    (tmp_path / "answer_key.json").write_text(__import__("json").dumps(key, ensure_ascii=False))
    md, _ = good_pack(bp)
    sections = md.split("## Phân khúc khách hàng", 1)[1].split("## Bài kiểm tra", 1)[0]
    out = ap.assemble(tmp_path, "## Phân khúc khách hàng" + sections, SHEET, "x")
    assert all(ok for _, ok, _ in ct.checks(out, SHEET, key)), [c for c in ct.checks(out, SHEET, key) if not c[1]]
