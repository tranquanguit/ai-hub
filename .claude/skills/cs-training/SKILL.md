---
name: cs-training
description: Builds a customer-service training pack (product facts, segments, service protocol, sample dialogues, FAQ, quiz with answer key) from the product sheet. Use to onboard or refresh CS staff.
---
# cs-training

## When to use
- Onboarding new CS staff, a new SKU or policy change, or retraining after an ops-review shows CS quality issues.
- Not for answering one live customer (use the facts directly) or for marketing copy.

## Inputs
- The product and service sheet (`inputs/*product-sheet*.md`): a product table with SKU, Tên, Dung tích, Giá (VND), Thành phần chính, Loại da, Cách dùng, Lưu ý, HSD sau mở nắp; a `## Chính sách` list; `## Phân khúc khách hàng`; FAQ list.
- `canon/company.md#claims` and `canon/roles/cs.md`.
- Optional: the latest ops-review CS findings (SLA breaches, CSAT drops) to focus the training on.

## Steps
1. Run `task-start --type cs-training`.
2. Generate the deterministic parts: `python3 .claude/skills/cs-training/scripts/build_pack.py <sheet> --out-dir tasks/<task>/evidence/pack`. This writes `product_facts.md`, `quiz.md` and `answer_key.json`. Log it `--scripted`.
3. Write the reasoned sections (segments, protocol, dialogues, FAQ) to `tasks/<task>/evidence/pack/reasoned_sections.md`, then assemble **by script**: `python3 .claude/skills/cs-training/scripts/assemble_pack.py --pack-dir tasks/<task>/evidence/pack --sections tasks/<task>/evidence/pack/reasoned_sections.md --sheet <sheet> --summary "<English summary>" --out tasks/<task>/deliverables/cs-training.md`. The deliverable has these headings:
   - `## Sản phẩm`: paste `product_facts.md` unchanged. Never add benefits that are not in the sheet.
   - `## Phân khúc khách hàng`: one block per segment in the sheet: needs, typical questions, recommended SKUs, tone.
   - `## Quy trình phục vụ`: greeting, needs check, recommendation, closing, plus the policies with their exact numbers (returns 7 days, SLA 15 minutes, free-ship threshold) and the **skin-reaction escalation** (stop use, rinse, ask for a photo and the order code, report to the Founder the same day).
   - `## Kịch bản mẫu`: at least 4 `### Kịch bản N: <situation>` dialogues, including one complaint and one skin-reaction case. Customers are pseudonyms only.
   - **Never write a banned phrase, not even as a "don't say" example or in a negation** (the claims check is literal; this caused reworks in 3 of 4 runs). Refer to `canon/company.md#claims` instead, and for acne questions use the phrasing in `memory/semantic/claims.acne.phrasing.md`.
   - `## Câu hỏi thường gặp`: answer every FAQ from the sheet. "Da mụn" questions get a compliant answer (suitable for oily or acne-prone skin as care) with no treatment claim.
   - `## Bài kiểm tra`: paste `quiz.md`, then `### Đáp án` with every answer from `answer_key.json`.
   - `## English summary`.
   - State at the top that the pack is built on SAMPLE input, if it is.
4. Check: `python3 .claude/skills/cs-training/scripts/check_training.py tasks/<task>/deliverables/cs-training.md --sheet <sheet> --key tasks/<task>/evidence/pack/answer_key.json > tasks/<task>/evidence/check_training.txt`. Fix any FAIL, log `--rework`, re-run.

## Memory facts used
- `memory/semantic/claims.acne.phrasing.md` (compliant wording for acne questions).
- Facts tagged `cs`, `policy` or `product` in `memory/INDEX.md`. If a fact disagrees with the sheet, follow the sheet and file a `reflect.py candidate`; curation will flag the conflict (R4).

## Verification
- `evidence/check_training.txt` ends with `=> PASS`, and LEDGER.md references it.

## Close
- `task-close --skills cs-training`, then `reflect`. Useful candidates: policy facts confirmed by the human (`--kind human`), FAQ answers that needed a claims rewrite (`--type skill-delta`).
