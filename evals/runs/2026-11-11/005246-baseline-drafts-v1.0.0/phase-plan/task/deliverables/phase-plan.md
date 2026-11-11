# Kế hoạch giai đoạn Q1/2027 — "Scale-up sau ra mắt" (01–03/2027)

> **SAMPLE:** toàn bộ số liệu đầu vào (benchmark, tỷ trọng khu vực/khách hàng) lấy từ `inputs/SAMPLE-phase-brief.md`, là dữ liệu giả lập, không phải số thật của LunoBeau. Kế hoạch này là bản dựng theo quy trình; cần thay bằng brief thật trước khi chạy ngân sách.

**Mục tiêu theo brief:** doanh thu 1,200,000,000 VND; 4,000 đơn; mua lại ≥ 18%.
**Kết quả dự kiến theo benchmark brief (script):** 4,049 đơn, 935,859,600 VND → **đạt đơn, thiếu doanh thu ~264 triệu (22%)**. Xem "Khoảng cách mục tiêu" bên dưới.

## Kênh bán hàng
Kênh bán (canon/company.md, mục Sales channels, [SAMPLE]): Shopee Mall, TikTok Shop, Facebook/Instagram (đơn inbox), website, Lazada. Kênh quảng cáo được cấp ngân sách theo brief:

| Kênh quảng cáo | Vai trò | Kênh bán nhận đơn |
|---|---|---|
| Shopee Ads | Chuyển đổi nhu cầu có sẵn, ROAS cao nhất (4.2) | Shopee |
| TikTok Ads | Tạo nhu cầu + bán trực tiếp | TikTok Shop |
| Facebook Ads | Remarketing, đơn inbox, combo | Inbox FB/IG, website |
| KOC / Affiliate | Uy tín nội dung, trả theo đơn | TikTok Shop, Shopee |
| Google Ads | Tìm kiếm thương hiệu và danh mục (Search, YouTube) | Website, Shopee |

Lazada và bán lẻ offline: không cấp ngân sách quảng cáo trong giai đoạn này (brief không có benchmark) — giữ hiện diện, không đầu tư thêm.

## Khu vực trọng điểm
Xếp hạng theo `share_of_orders_last_q` của brief (SAMPLE):

| Hạng | Khu vực | Tỷ trọng đơn quý trước | Vai trò |
|---|---|---|---|
| 1 | TP.HCM | 46% | Giữ vị trí; ưu tiên ngân sách giao nhanh, remarketing |
| 2 | Hà Nội | 31% | Mở rộng; thử KOC địa phương |
| 3 | Đà Nẵng | 7% | Thử nghiệm nhỏ bằng quỹ dự phòng |
| 4 | Cần Thơ | 4% | Chỉ nhận đơn tự nhiên, chưa chạy riêng |
| – | Khác | 12% | Không nhắm riêng; theo kênh sàn |

Hai thành phố đầu chiếm 77% đơn → dồn ~85% ngân sách nhắm vị trí vào HCM + Hà Nội (giả định, cần kiểm lại bằng dữ liệu quảng cáo thật).

## Khách hàng mục tiêu
Xếp hạng theo `audiences_last_q` (SAMPLE):

| Nhóm | Tỷ trọng | AOV (VND) | Ưu tiên |
|---|---|---|---|
| Nữ 25–34 văn phòng | 44% | 340,000 | **Chính** — serum + kem chống nắng, combo |
| Nữ 18–24 sinh viên | 38% | 265,000 | **Chính** — sản phẩm giá thấp, voucher sàn, KOC |
| Nữ 35–44 | 12% | 390,000 | Phụ — AOV cao nhất, remarketing combo |
| Nam 18–34 | 6% | 240,000 | Thử nhỏ — sữa rửa mặt, kem chống nắng |

AOV bình quân theo tỷ trọng nhóm = **311,500 VND** (tính từ bảng trên, `evidence/implied_aov.txt`).

## Ngân sách
Tổng 300,000,000 VND, dự phòng 10%, trọng số tháng 30/33/37%. Bảng do script `allocate_budget.py` tạo (`evidence/allocation.md`), sao nguyên văn:

| Kênh / Channel | Tỷ trọng | 2027-01 | 2027-02 | 2027-03 | Tổng (VND) | Đơn dự kiến | Doanh thu dự kiến (VND) |
|---|---|---|---|---|---|---|---|
| shopee_ads | 23.4% | 21,060,000 | 23,166,000 | 25,975,000 | 70,201,000 | 1,350 | 294,844,200 |
| tiktok_ads | 22.1% | 19,856,000 | 21,842,000 | 24,490,000 | 66,188,000 | 1,018 | 238,276,800 |
| facebook_ads | 18.0% | 16,200,000 | 17,820,000 | 19,980,000 | 54,000,000 | 692 | 167,400,000 |
| koc_affiliate | 13.5% | 12,150,000 | 13,365,000 | 14,985,000 | 40,500,000 | 578 | 133,650,000 |
| google_ads | 13.0% | 11,733,000 | 12,906,000 | 14,472,000 | 39,111,000 | 411 | 101,688,600 |
| reserve (dự phòng/test) | 10.0% | 9,000,000 | 9,900,000 | 11,100,000 | 30,000,000 | – | – |
| **Tổng / Total** | 100% | 89,999,000 | 98,999,000 | 111,002,000 | **300,000,000** | 4,049 | 935,859,600 |

expected orders 4,049; expected revenue 935,859,600 VND (benchmarks from the brief; label as assumption)

### Khoảng cách mục tiêu (doanh thu)
- Dự kiến 935,859,600 vs mục tiêu 1,200,000,000 → **thiếu 264,140,400 VND (22.0%)**. Mình không nới benchmark để che khoảng trống.
- Nguyên nhân: AOV ngầm định của benchmark = CPA × ROAS = 218,400–247,000 VND (bình quân gia quyền 231,134), thấp hơn AOV các nhóm khách (bình quân 311,500) (fact `ads.benchmarks.implied-aov`). Để đạt 1.2 tỷ với 4,049 đơn cần AOV ≈ 296,369 VND.
- **Đòn bẩy (có số, chưa cộng dồn vì chồng lấn):**
  1. **Tăng AOV +10% bằng combo / ngưỡng freeship:** +93,585,960 VND. Ví dụ combo Serum + Kem chống nắng 770,000 gốc, ưu đãi nhẹ; ngưỡng freeship 399,000 VND (fact `policy.free-shipping.threshold-vnd`, SAMPLE) đẩy giỏ hàng từ ~340k lên ≥ 399k.
  2. **Chuyển quỹ dự phòng sang Shopee Ads tới trần 30%** (90,000,000): thêm 19,799,000 chi → +83,155,800 VND doanh thu (ROAS 4.2), nhưng dự phòng còn ~10 triệu. Chỉ làm sau tháng 1 khi ROAS Shopee thực tế ≥ 4.0.
  3. **Doanh thu mua lại / CRM không tính phí quảng cáo:** mục tiêu mua lại 18%. 18% của 4,049 đơn = ~729 đơn lặp; ở AOV 311,500 ≈ 227 triệu nếu các đơn này phát sinh trong quý (giả định, thời gian mua lại sản phẩm chưa có dữ liệu). Các đòn bẩy chồng lấn một phần nên không cộng thẳng; cần ít nhất hai đòn cùng đạt mới phủ được khoảng trống 264 triệu, không đòn nào đủ riêng lẻ.

## Chiến lược theo kênh

### shopee_ads
- **Mục tiêu:** 1,350 đơn; ROAS ≥ 4.0.
- **Khách hàng:** nữ 18–34 đã tìm kiếm chăm sóc da / chống nắng.
- **Ưu đãi:** combo Serum + Sunscreen, voucher shop đạt ngưỡng 399,000 VND freeship.
- **Góc sáng tạo:** hình sản phẩm sạch, bảng thành phần (niacinamide 5%, HA) kèm nguồn; không hứa hiệu quả y tế.
- **KPI:** CPA ≤ 52,000; ROAS ≥ 4.0; CTR tìm kiếm theo dõi hằng tuần.

### tiktok_ads
- **Mục tiêu:** 1,018 đơn theo benchmark; **cổng ROAS** vì số đo thực tế gần nhất thấp hơn nhiều.
- **Khách hàng:** nữ 18–24 và 25–34.
- **Ưu đãi:** son Velvet Lip Tint (189,000) làm sản phẩm mồi, upsell sunscreen.
- **Góc sáng tạo:** video ngắn, routine buổi sáng, đánh giá thật từ KOC; giọng thân thiện, trung thực.
- **KPI:** CPA ≤ 65,000; ROAS ≥ 3.6 theo brief nhưng **gate**: nếu ROAS tuần < 2.0 hai tuần liên tiếp, giảm 50% ngân sách chuyển sang Shopee (cần founder duyệt).
- Mâu thuẫn dữ liệu: brief nói 3.6, tuần 03–09/11/2026 đo 1.2 ([SAMPLE], `memory/conflicts/2026-11-10-benchmark-tiktok-ads-roas.md`, chưa giải quyết).

### facebook_ads
- **Mục tiêu:** 692 đơn; ROAS ≥ 3.1.
- **Khách hàng:** nữ 25–34 văn phòng, nữ 35–44 (remarketing AOV cao).
- **Ưu đãi:** combo 2–3 sản phẩm, quà tặng mẫu thử; inbox tư vấn chốt đơn.
- **Góc sáng tạo:** hướng dẫn routine chăm da, kem chống nắng dùng hằng ngày; không dùng "nâng tone" cho LB-SUN-01 (fact `product.lb-sun-01.claim.tone-up`).
- **KPI:** CPA ≤ 78,000; ROAS ≥ 3.1; tỷ lệ chốt inbox theo dõi.

### koc_affiliate
- **Mục tiêu:** 578 đơn; 5–15% ngân sách.
- **Khách hàng:** nữ 18–24 sinh viên và nữ 25–34 ở HCM, Hà Nội.
- **Ưu đãi:** mã giảm riêng mỗi KOC, hoa hồng theo đơn.
- **Góc sáng tạo:** review thật, bám brief claims (không "trị", không so sánh trước/sau).
- **KPI:** CPA ≤ 70,000; ROAS ≥ 3.3; ≥ 20 KOC hoạt động.

### google_ads
- **Mục tiêu:** 411 đơn; vai trò bổ trợ.
- **Khách hàng:** nữ 25–34 tìm sản phẩm theo tên thương hiệu và danh mục.
- **Ưu đãi:** trang đích combo trên website.
- **Góc sáng tạo:** Search từ khóa thương hiệu + danh mục; YouTube remarketing.
- **KPI:** CPA ≤ 95,000; ROAS ≥ 2.6; nếu < 2.0 sau tháng 1 giảm về mức tối thiểu 10%.

## KPI
Mục tiêu theo tháng (đơn dự kiến chia theo trọng số tháng 30/33/37%, giả định; doanh thu từ bảng ngân sách):

| KPI | 2027-01 | 2027-02 | 2027-03 | Cả quý |
|---|---|---|---|---|
| Ngân sách quảng cáo (VND) | 89,999,000 | 98,999,000 | 111,002,000 | 300,000,000 |
| Đơn hàng | ~1,215 | ~1,336 | ~1,498 | 4,049 |
| Doanh thu (VND), theo benchmark | ~280.8 triệu | ~308.8 triệu | ~346.3 triệu | 935.9 triệu |
| Doanh thu mục tiêu brief (VND) | 360 triệu | 396 triệu | 444 triệu | 1,200 triệu |
| ROAS tổng (không tính dự phòng) | ≥ 3.4 | ≥ 3.4 | ≥ 3.4 | ≥ 3.4 |
| CPA bình quân (không tính dự phòng) | ≤ 66,700 | ≤ 66,700 | ≤ 66,700 | ≤ 66,700 |
| Tỷ lệ mua lại | – | ≥ 8% | ≥ 18% (lũy kế) | ≥ 18% |
| AOV | ≥ 250,000 | ≥ 280,000 | ≥ 296,000 | ≥ 296,000 |

Ghi chú: ROAS tổng = 935.9 triệu / 270 triệu chi kênh (đã loại dự phòng 30 triệu) = 3.47; CPA = 270 triệu / 4,049 đơn = ~66,700. Đây là ngưỡng theo dõi theo benchmark SAMPLE, không phải cam kết. Nếu tính cả dự phòng thì ROAS = 3.12.

## Lịch triển khai
| Thời gian | Việc |
|---|---|
| Tuần 0 (cuối 12/2026) | Duyệt brief thật; chốt ngày Tết 2027 và tồn kho; chuẩn bị creative, combo, mã KOC |
| Tháng 1/2027 | Chạy 5 kênh theo ngân sách tháng 1; review hằng tuần bằng `ops-review`; kiểm tra gate TikTok |
| Cuối tháng 1 | Quyết định chuyển dự phòng sang Shopee nếu ROAS ≥ 4.0 (cần founder duyệt) |
| Tháng 2/2027 | Tăng ngân sách theo kênh vượt benchmark; chạy combo AOV; bắt đầu CRM mua lại |
| Tháng 3/2027 | Tăng tốc kênh có ROAS tốt; chiến dịch 8/3 (cần xác nhận tồn kho); đo tỷ lệ mua lại |
| Cuối quý | Báo cáo kết quả, sửa benchmark trong memory, brief quý sau |

## Rủi ro
| Rủi ro | Tác động | Giảm thiểu |
|---|---|---|
| ROAS TikTok thực tế 1.2 so với 3.6 ([SAMPLE]) | Nếu ROAS 1.2, 66,188,000 chi chỉ ra ~79 triệu, mất ~159 triệu doanh thu | Gate ROAS hằng tuần, giảm 50% và chuyển Shopee |
| Khoảng cách doanh thu 22% | Không đạt 1.2 tỷ | 3 đòn bẩy AOV / dự phòng / mua lại; báo founder sớm |
| Tồn kho Tết và 8/3 chưa rõ | Hết hàng giữa đợt chạy | Hỏi nhà sản xuất lead time trước tuần 0 |
| Tết 2027 làm giảm vận chuyển và nhu cầu | Giảm đơn tháng 2 | Điều chỉnh trọng số tháng sau khi có lịch Tết |
| Rủi ro quảng cáo mỹ phẩm (claims) | Bị gỡ quảng cáo, vi phạm | Duyệt creative theo canon claims; pháp lý xem lại |
| Tỷ lệ mua lại 18% chưa có baseline | KPI không đo được | Xây theo dõi mã khách `KH-####` trong CS |

## Giả định & nguồn
- **SAMPLE:** CPA, ROAS, weight, min/max share, regions, audiences — `inputs/SAMPLE-phase-brief.md` (số giả lập).
- ROAS TikTok 3.6: SAMPLE brief (fact `benchmark.tiktok-ads.roas`, confidence low); 1.2: `tasks/2026-11-10-ops-review-w45/evidence/kpis.json` (SAMPLE, conflict chưa giải quyết).
- AOV ngầm định = CPA × ROAS: fact `ads.benchmarks.implied-aov`; tính ở `evidence/implied_aov.txt`.
- Ngưỡng freeship 399,000: fact `policy.free-shipping.threshold-vnd` (SAMPLE).
- Giá sản phẩm: `canon/company.md` ([SAMPLE]).
- *Giả định:* phân bổ đơn theo tháng, ~85% nhắm HCM + Hà Nội, 18% mua lại phát sinh trong quý, doanh thu mua lại không được tính trong bảng quảng cáo. Chưa có số liệu thực kiểm chứng.
- Claims theo `canon/company.md#claims` (confidence: assumption, cần pháp lý).

## English summary
- Plan for Q1/2027 (Jan–Mar) with a 300,000,000 VND budget, 10% reserve, monthly weights 30/33/37%; built on **SAMPLE** inputs.
- Five paid channels (Shopee, TikTok, Facebook, KOC, Google); focus regions HCMC + Hanoi (77% of orders); core audiences women 25–34 and 18–24.
- Benchmarks yield 4,049 orders (goal 4,000 met) but 935.9M VND revenue vs the 1.2B goal: a 22% gap caused by low implied AOV (~231k vs ~311k segment AOV).
- Levers: +10% AOV via combos (+93.6M), shift reserve to Shopee (+83.2M), repeat purchase (~227M if 18% is reached); none closes the gap alone.
- Main risk: TikTok measured ROAS 1.2 vs benchmark 3.6; a weekly ROAS gate is built in.
- Needs founder decisions: reserve reallocation, TikTok cuts, Tết stock and dates.
