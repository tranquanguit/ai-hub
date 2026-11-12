# HANDOFF: continue this task in a LOCAL session (Q:\Downloads is only readable there)

Opened in a cloud session on 2026-11-12. The founder will resume it on their PC with `claude --teleport`.

## Done (cloud)
- Task folder, TASK.md done-criteria, original survey: `evidence/source/khao-sat-goc.docx`.
- Survey content: 4 parts. (1) products, hero products, strengths, retail and promo prices; (2) wholesale minimum, CTV/wholesale discount %, wholesale support benefits; (3) first-month goal (retail / wholesale / 50-50), regions (13 Mekong Delta provinces vs Đồng Tháp and neighbours), retail and wholesale audience; (4) first-month Facebook budget tier, available media assets, hotline confirmation, staffing hours.
- The PII guard was upgraded with founder approval: spaced numbers are detected, and the business allowlist `canon/business-contacts.json` lets the company hotline appear.

## Local prerequisites (do these first, or the hooks fail open)
1. `python3 --version` must work in the shell Claude Code uses (Windows: Git Bash). Install Python 3 and make `python3` resolve; otherwise every hook errors and stops protecting.
2. `pip install -r requirements.txt`
3. `git config core.hooksPath .githooks`
4. If SessionStart says the role is not confirmed: `python3 tools/set_role.py founder`.

## Source files (Q:\Downloads); read with the Read tool, extract facts, do not commit the raw PDFs
- PCB (product notification): 05.2026 FOUNDATION SUNCREAM; 08.2026 TONE-UP SUNCREAM (FIX TĂNG MK); 07.2026 GENTLE CLEANSING FOAM; 09.2026 BRIGHTENING SERUM (HALAVI) (1)
- Lot test reports: GENTLE CLEANSING FOAM 010826; TONE-UP SUNCREAM 010626 and 010726; GENTLE MICELLAR 010726 and 020726; FOUNDATION SUNCREAM 010526
- `TỔNG HỢP PROFILE LUNOBEAU` (folder or file: check)
- SKIP: "Báo cáo kiểm tra lỗi Guaranteed vs Experienced False-Alert Rates (Conformal Selection)" (sent by mistake)

## Remaining steps
1. Log each read with `start_task.py log ... --scripted`, and record each file's sha256 (`certutil -hashfile <f> SHA256` or `sha256sum`).
2. `inputs/products/<product-slug>.md`: one sheet per product with PCB number, notifying company/manufacturer, volume, key ingredients/INCI, usage, warnings, lot test results (lot, date, criteria, result), and the source file and page for every fact. No customer data.
3. `canon/company.md`: replace the [SAMPLE] product table with the real line (Foundation Suncream, Tone-up Suncream, Gentle Cleansing Foam, Gentle Micellar, Brightening Serum Halavi). Prices only if the profile has them; otherwise add a row to `data/founder/decision-log.md`. The founder asked for this, so the canon edit is authorized.
4. Memory: `memory/semantic/product.lb-sun-01.claim.tone-up.md` (SAMPLE: "not tone-up") is now wrong. File a candidate with the real Tone-up product (`reflect.py candidate --kind human --evidence inputs/products/tone-up-suncream.md`), let curation set it aside as a conflict, then `promote.py resolve <conflict> --keep new`, citing the PCB. Archive the SAMPLE-only product facts with a reason.
5. Fill the survey with the docx skill, keeping the original formatting → `deliverables/khao-sat-ads-ngoc-han.docx`:
   - Part 1 from the product sheets (claims: tone-up is an allowed cosmetic effect if the PCB states it; no treatment claims).
   - Parts 2–4: proposals, each with a one-line reason, **highlighted yellow**: discount tiers need a margin check (cost unknown → say so); budget tier reasoned from the Q1 plan (Facebook ≈ 18M VND/month in the SAMPLE plan; first month as a test); regions and audience from the company location; assets: tick only what exists.
   - Hotline: write 0847 185 878 (allowlisted) and add "cần anh/chị xác nhận".
   - Also `deliverables/khao-sat-ads-ngoc-han.md` (same content) and a "Cần anh/chị duyệt" list of every highlighted proposal.
6. Verify (save outputs to evidence/): every question answered; every Part 1 fact cites a sheet; number of proposals = number of highlights; `python3 tools/secret_scan.py <deliverable.md>`; banned-claims check.
7. `task-close --skills ...`, `reflect`, `curate-learning`, commit, push. Then note that the SAMPLE-based deliverables and evals use the old product line (re-run planned).
