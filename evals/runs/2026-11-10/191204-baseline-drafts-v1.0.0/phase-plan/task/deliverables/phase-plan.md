# Kế hoạch giai đoạn Q1/2027 — Scale-up sau ra mắt

> Dựa trên brief **SAMPLE** (`inputs/SAMPLE-phase-brief.md`). Mọi benchmark là số minh họa; thay bằng số thật trước khi duyệt ngân sách.
> Phân bổ ngân sách tính bằng script `allocate_budget.py` (evidence/allocation.json), không tính tay.

## Kênh bán hàng
- **Shopee (Mall + Search Ads)**: kênh chuyển đổi chính, CPA benchmark thấp nhất (52,000 VND), ROAS 4.2.
- **TikTok (Ads + TikTok Shop)**: kênh tăng trưởng cho nhóm 18–24, ROAS benchmark 3.6. Lưu ý: tuần đánh giá gần nhất (SAMPLE) đo được ROAS nền tảng TikTok chỉ 1.2 (`tasks/2026-11-10-ops-review-w45/evidence/kpis.json`).
- **Facebook/Instagram Ads**: prospecting serum + retargeting combo; retargeting đạt ROAS 8.4 ở tuần đánh giá gần nhất.
- **KOC/affiliate**: nội dung trải nghiệm, nuôi TikTok Shop và Shopee.
- **Google Ads**: giữ Search thương hiệu (ROAS cao), giới hạn generic serum cho đến khi landing page cải thiện.
- **Website**: kênh mua lại (CRM), không chạy ngân sách riêng trong giai đoạn này.

## Khu vực trọng điểm
| Khu vực | Tỷ trọng đơn quý trước | Vai trò Q1 |
|---|---|---|
| TP. Hồ Chí Minh | 46% | Trọng điểm 1, giao 1–2 ngày |
| Hà Nội | 31% | Trọng điểm 2, giao 1–2 ngày |
| Đà Nẵng | 7% | Thử nghiệm geo-targeting tháng 2–3 |
| Cần Thơ | 4% | Chỉ qua Shopee/TikTok Shop, không target riêng |
| Tỉnh khác | 12% | Qua sàn, không target riêng |
HCM + Hà Nội chiếm 77% đơn quý trước, nên được khoảng 80% ngân sách ads có geo-targeting.

## Khách hàng mục tiêu
| Phân khúc | Tỷ trọng | AOV (VND) | Ưu tiên | Kênh chính |
|---|---|---|---|---|
| Nữ 25–34 văn phòng | 44% | 340,000 | 1 (giá trị cao nhất theo tỷ trọng × AOV) | Shopee, Facebook, Google |
| Nữ 18–24 sinh viên | 38% | 265,000 | 2 | TikTok Shop, KOC |
| Nữ 35–44 | 12% | 390,000 | 3 (AOV cao nhất) | Facebook, Google Search serum |
| Nam 18–34 (mua quà) | 6% | 240,000 | Theo mùa: 14/2 và 8/3 | Facebook, TikTok (son làm quà) |

## Ngân sách
| Kênh / Channel | Tỷ trọng | 2027-01 | 2027-02 | 2027-03 | Tổng (VND) | Đơn dự kiến | Doanh thu dự kiến (VND) |
|---|---|---|---|---|---|---|---|
| shopee_ads | 23.4% | 21,060,000 | 23,166,000 | 25,975,000 | 70,201,000 | 1,350 | 294,844,200 |
| tiktok_ads | 22.1% | 19,856,000 | 21,842,000 | 24,490,000 | 66,188,000 | 1,018 | 238,276,800 |
| facebook_ads | 18.0% | 16,200,000 | 17,820,000 | 19,980,000 | 54,000,000 | 692 | 167,400,000 |
| koc_affiliate | 13.5% | 12,150,000 | 13,365,000 | 14,985,000 | 40,500,000 | 578 | 133,650,000 |
| google_ads | 13.0% | 11,733,000 | 12,906,000 | 14,472,000 | 39,111,000 | 411 | 101,688,600 |
| reserve (dự phòng/test) | 10.0% | 9,000,000 | 9,900,000 | 11,100,000 | 30,000,000 | – | – |
| **Tổng / Total** | 100% | 89,999,000 | 98,999,000 | 111,002,000 | **300,000,000** | 4,049 | 935,859,600 |

Chênh lệch so với mục tiêu: theo benchmark, kế hoạch đạt khoảng **4,049 đơn** (mục tiêu 4,000) nhưng chỉ khoảng **935,859,600 VND** doanh thu (mục tiêu 1,200,000,000 VND, thiếu khoảng 264,000,000 VND, tức 22%). Nguyên nhân: benchmark ngầm định AOV chỉ khoảng 231,000 VND (CPA × ROAS, `evidence/implied_aov.txt`), thấp hơn AOV mọi phân khúc (240,000–390,000 VND).
Đòn bẩy (Founder chọn):
1. **Nâng AOV bằng combo** (Serum + Sunscreen, Cleanser + Sunscreen): nếu AOV đạt 300,000 VND với cùng số đơn, doanh thu ≈ 4,049 × 300,000 = 1,214,700,000 VND, đạt mục tiêu.
2. **Mua lại (mục tiêu ≥ 18%)**: retargeting + CRM website; 18% của khoảng 3,300 khách mới ≈ 600 đơn mua lại × 340,000 ≈ 204,000,000 VND, chi phí chủ yếu là ưu đãi.
3. **Dùng quỹ dự phòng 30,000,000 VND cho Shopee** nếu tháng 1 xác nhận ROAS ≥ 4.0: thêm khoảng 126,000,000 VND doanh thu, đổi lại mất ngân sách test.

## Chiến lược theo kênh
### shopee_ads (70,201,000 VND)
- Mục tiêu: đơn giá rẻ, giữ ROAS ≥ 4.0. Search Ads theo từ khóa sản phẩm, voucher combo, Flash Sale dịp Tết.
- KPI: CPA ≤ 55,000 VND, ROAS ≥ 4.0.
### tiktok_ads (66,188,000 VND)
- Mục tiêu: tăng trưởng nhóm 18–24. Chỉ chạy Spark Ads từ video KOC đã có tương tác; dừng broad targeting (ROAS 0.23 ở tuần đánh giá gần nhất, SAMPLE).
- Điều kiện: ROAS ≥ 2.0 sau 2 tuần đầu, nếu không thì chuyển 50% ngân sách tháng 2 sang shopee_ads (Founder duyệt).
### facebook_ads (54,000,000 VND)
- 40% retargeting combo (ROAS tuần gần nhất 8.4), 60% prospecting nữ 25–34 và 35–44 với creative thành phần (Niacinamide 5%, SPF50+ PA++++).
- KPI: ROAS ≥ 3.0 toàn kênh.
### koc_affiliate (40,500,000 VND)
- 15–20 KOC micro, hoa hồng theo đơn; brief nội dung tuân thủ `canon/company.md#claims` (không dùng claim điều trị hay "nâng tone").
- KPI: CPA ≤ 70,000 VND.
### google_ads (39,111,000 VND)
- 30% Search thương hiệu, 70% Search sản phẩm có landing page mới (A/B test trước khi tăng ngân sách).
- KPI: ROAS ≥ 2.6, CVR ≥ 2.5%.

## KPI
| Tháng | Đơn | Doanh thu mục tiêu (VND) | ROAS tổng tối thiểu | Tỷ lệ mua lại |
|---|---|---|---|---|
| 2027-01 | 1,215 | 360,000,000 | 3.0 | theo dõi |
| 2027-02 | 1,336 | 396,000,000 | 3.2 | ≥ 12% |
| 2027-03 | 1,498 | 444,000,000 | 3.3 | ≥ 18% |
Mục tiêu tháng = mục tiêu quý × trọng số tháng (0.30/0.33/0.37); đơn = 4,049 × trọng số.

## Lịch triển khai
- Tuần 1–2/01: thiết lập combo, landing page Google, tuyển KOC, set geo HCM/HN.
- Tháng 01: chạy đủ kênh, ops-review hằng tuần, chốt ROAS TikTok sau 2 tuần.
- Tháng 02 (Tết và 14/2, ngày Tết cần xác nhận): tăng Shopee Flash Sale, chiến dịch son làm quà; lưu ý vận chuyển chậm quanh Tết.
- Tháng 03 (8/3): chiến dịch quà tặng 8/3, đẩy mua lại qua CRM, thử Đà Nẵng.
- Cuối mỗi tháng: điều chỉnh phân bổ theo ops-review (Founder duyệt).

## Rủi ro
- ROAS TikTok thực tế có thể thấp hơn benchmark rất nhiều (1.2 so với 3.6 ở tuần SAMPLE gần nhất). Có cổng chặn sau 2 tuần.
- Benchmark CPA/ROAS ngầm định AOV thấp (231,000 VND), nên doanh thu thiếu nếu không nâng AOV.
- Sản xuất thuê ngoài: cần xác nhận thời gian sản xuất/tồn kho cho đỉnh Tết và 8/3 (chưa có dữ liệu trong repo).
- Tuân thủ quảng cáo mỹ phẩm: mọi nội dung KOC phải qua kiểm tra claims.

## Giả định & nguồn
- Ngân sách, benchmark kênh, tỷ trọng khu vực và phân khúc: `inputs/SAMPLE-phase-brief.md` (SAMPLE, giả định).
- ROAS tuần gần nhất: `tasks/2026-11-10-ops-review-w45/evidence/kpis.json` (SAMPLE).
- Ngày Tết 2027 (khoảng đầu tháng 2) là giả định, cần xác nhận lịch.
- Phân bổ và dự báo đơn/doanh thu: `evidence/allocation.json` (script).

## English summary
SAMPLE-based Q1 2027 plan. Budget 300M VND split by script: Shopee 70.2M, TikTok 66.2M, Facebook 54.0M, KOC 40.5M, Google 39.1M, reserve 30M. Focus on HCM and Hanoi (77% of orders) and office women 25–34 as the primary segment. At the brief's benchmarks the plan reaches the order goal (~4,049) but only ~936M VND revenue, 22% short of 1.2B, because the benchmarks imply a ~231k VND AOV. The recommended lever is combos that lift AOV to ~300k, plus repeat purchase and a conditional shift of the reserve to Shopee. TikTok gets a 2-week ROAS gate because the latest measured week showed ROAS 1.2.
