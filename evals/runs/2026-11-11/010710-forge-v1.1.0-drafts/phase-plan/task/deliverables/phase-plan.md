# Kế hoạch giai đoạn Q1/2027 — "Scale-up sau ra mắt"

> **SAMPLE:** kế hoạch này dựng trên brief `inputs/SAMPLE-phase-brief.md` và `canon/company.md` (sản phẩm, giá, kênh đều đánh dấu SAMPLE). Mọi con số benchmark, tỷ trọng khu vực/khách hàng là dữ liệu mẫu, chưa phải số thật của LunoBeau. Thay brief thật rồi chạy lại script phân bổ trước khi chi tiền.

Mục tiêu (brief): doanh thu 1,200,000,000 VND; 4,000 đơn; tỷ lệ mua lại ≥ 18%; tổng ngân sách ads 300,000,000 VND (gồm 10% dự phòng); giai đoạn 01–03/2027.

**Kết luận nhanh:** với benchmark của brief, ngân sách 300 triệu cho khoảng 4,049 đơn (đạt mục tiêu đơn) nhưng chỉ khoảng 935,9 triệu VND doanh thu, **thiếu ~264,1 triệu (22%)** so với mục tiêu. Nguyên nhân là AOV ngầm định (CPA × ROAS) chỉ 231,133 VND. Kế hoạch giữ nguyên benchmark, không "kéo" số cho đẹp, và đưa ra 3 đòn bẩy có số ở mục Ngân sách.

## Kênh bán hàng

Kênh bán (nơi khách chốt đơn) theo `canon/company.md` [SAMPLE]; kênh quảng cáo/tạo nhu cầu theo brief.

| Kênh bán | Vai trò Q1/2027 | Kênh kéo traffic được tài trợ |
|---|---|---|
| Shopee (Mall) | Kênh chốt đơn chính, doanh thu hiện tại chủ yếu từ đây (brief) | Shopee Ads |
| TikTok Shop | Kênh tăng trưởng chính: video + KOC dẫn thẳng vào giỏ hàng | TikTok Ads, KOC/affiliate |
| Facebook/Instagram inbox | Chốt đơn tư vấn, bán combo, thu thập khách để mua lại | Facebook Ads |
| Website lunobeau.vn [SAMPLE] | Thu nhận tìm kiếm có chủ đích, tệp CRM của riêng mình | Google Ads (Search, YouTube) |
| Lazada | Duy trì danh mục, **không** chi quảng cáo trong quý này (brief không có benchmark) | — |

Ưu tiên: Shopee và TikTok nhận ~45% ngân sách vì CPA thấp và ROAS cao nhất trong benchmark (Shopee ROAS 4.2, TikTok 3.6 — nguồn brief SAMPLE).

## Khu vực trọng điểm

Xếp hạng theo `regions.share_of_orders_last_q` của brief (SAMPLE):

| Hạng | Khu vực | Tỷ trọng đơn quý trước | Vai trò |
|---|---|---|---|
| 1 | TP.HCM | 46% | Trọng điểm 1: tập trung ads, KOC địa phương, giao nhanh |
| 2 | Hà Nội | 31% | Trọng điểm 2: ads + KOC, chú ý mùa lạnh/khô |
| 3 | Đà Nẵng | 7% | Thử nghiệm có kiểm soát bằng quỹ dự phòng (geo test) |
| 4 | Cần Thơ | 4% | Giữ tự nhiên qua Shopee, không chi riêng |
| 5 | Các tỉnh khác | 12% | Phủ qua Shopee/TikTok Shop, không nhắm theo địa lý |

HCM + Hà Nội = 77% đơn. Đề xuất phân bổ ngân sách theo vùng cho ads có định hướng địa lý: khoảng 55% HCM, 35% Hà Nội, 10% Đà Nẵng (test) — **giả định**, cần điều chỉnh sau 2 tuần dữ liệu đầu tiên.

## Khách hàng mục tiêu

Xếp hạng theo `audiences_last_q` (brief SAMPLE); doanh thu tương đối = tỷ trọng × AOV (tính tại `evidence/levers.txt`, AOV gia quyền 311,500 VND).

| Hạng | Nhóm | Tỷ trọng đơn | AOV | Tỷ trọng doanh thu | Vai trò |
|---|---|---|---|---|---|
| 1 | Nữ 25–34, văn phòng | 44% | 340,000 | 48,0% | Lõi: combo routine (serum + kem chống nắng + sữa rửa mặt), mua lại |
| 2 | Nữ 18–24, sinh viên | 38% | 265,000 | 32,3% | Khối lượng: sản phẩm đơn lẻ giá mềm (son, sữa rửa mặt), TikTok/KOC |
| 3 | Nữ 35–44 | 12% | 390,000 | 15,0% | AOV cao nhất: Facebook inbox, tư vấn, Google Search |
| 4 | Nam 18–34 | 6% | 240,000 | 4,6% | Chỉ giữ tự nhiên, không chi riêng (thử nhỏ bằng quỹ dự phòng nếu còn) |

Nhóm 35–44 có AOV cao nhất nhưng nhỏ; ưu tiên nhân rộng nhóm 25–34 (đòn bẩy AOV lớn nhất) rồi mở rộng 35–44.

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

expected orders 4,049; expected revenue 935,859,600 VND (benchmarks from the brief; label as assumption)
implied AOV (CPA x ROAS) 231,133 VND; revenue gap vs goal -264140400; orders gap 49

Nguồn: `evidence/allocation.md` do `allocate_budget.py` tạo (tổng đúng 300,000,000 VND; tỷ trọng tháng 30/33/37% theo brief; mọi kênh nằm trong min/max share).

### Khoảng cách mục tiêu và 3 đòn bẩy

Doanh thu dự kiến 935,9 triệu so với mục tiêu 1.200 triệu: thiếu **264,1 triệu VND**. Số đơn (4,049) đạt mục tiêu, nên vấn đề là **giá trị mỗi đơn**: cần AOV ≈ 296,369 VND (+65,236) thay vì 231,133. Tính tại `evidence/levers.txt`:

| Đòn bẩy | Cách làm | Hiệu ứng doanh thu | Điều kiện / giả định |
|---|---|---|---|
| A. Combo / nâng AOV | 30% đơn thành combo (ví dụ serum + sữa rửa mặt), thêm trung bình +120,000 VND/đơn | +145,8 triệu | Giả định 30% đơn là combo và +120,000/đơn; kiểm tra bằng A/B trong tháng 1 |
| B. Mua lại | Mục tiêu 18% khách mua lại → ~729 đơn × 231,133; **tính 50%** vì cửa sổ chỉ 3 tháng | +84,2 triệu (tối đa 168,5) | Dựa trên CRM/inbox, không tốn ads; cần có tệp khách từ 5 tháng bán trước |
| C. Chuyển dự phòng sang kênh ROAS cao | Chuyển 15,000,000 VND dự phòng sang Shopee Ads (ROAS 4.2, CPA 52,000) | +63,0 triệu (+288 đơn) | Shopee tổng 85,201,000 ≤ trần 90,000,000 (30%); dự phòng còn 15 triệu (5%) |

A + B (50%) + C ≈ **+293,0 triệu**, tức bù ~111% khoảng thiếu. Biên an toàn mỏng và toàn bộ dựa trên giả định, nên kế hoạch **không** tuyên bố đạt 1.200 triệu; mục tiêu cam kết: **≥ 1.000 triệu** (sàn, chỉ cần A hoặc B đạt một phần), mục tiêu kéo giãn 1.200 triệu. Quyết định chuyển dự phòng (đòn C) cần founder duyệt vì thay đổi phân bổ ngân sách (quy tắc R8).

## Chiến lược theo kênh

### Shopee Ads
- **Mục tiêu:** ~1,350 đơn, doanh thu dự kiến 294,8 triệu; CPA ≤ 52,000, ROAS ≥ 4.2 (benchmark brief, SAMPLE).
- **Khách hàng:** nữ 25–34 và 18–24 đang tìm sản phẩm theo từ khóa; HCM và Hà Nội.
- **Ưu đãi:** combo routine trên gian hàng Mall; voucher nhỏ theo ngưỡng freeship 399,000 VND (SAMPLE, nguồn `inputs/SAMPLE-product-sheet.md`) để kéo AOV; flash sale ngày đôi (1.1, 2.2, 3.3 — lịch Shopee cần xác nhận).
- **Góc sáng tạo:** ảnh/video mô tả thành phần và cách dùng theo nhãn; không nêu công dụng chưa có nguồn.
- **KPI:** CPA, ROAS, tỷ lệ chuyển đổi trang sản phẩm, % đơn combo.

### TikTok Ads
- **Mục tiêu:** ~1,018 đơn, doanh thu 238,3 triệu; ROAS ≥ 3.6 là benchmark brief (SAMPLE, độ tin cậy thấp: fact `benchmark.tiktok-ads.roas`), **cổng kiểm soát**: nếu ROAS tuần thực đo < 3.0 hai tuần liền, chuyển ngân sách sang Shopee/Facebook sau khi founder duyệt.
- **Khách hàng:** nữ 18–24 (khối lượng) và 25–34.
- **Ưu đãi:** TikTok Shop combo giá ưu đãi, livestream cuối tuần.
- **Góc sáng tạo:** video ngắn "routine hằng ngày" 15–30 giây, giọng thân thiện, trung thực theo brand voice.
- **KPI:** CPA, ROAS, view-through 6 giây, tỷ lệ thêm vào giỏ.

### Facebook Ads
- **Mục tiêu:** ~692 đơn, doanh thu 167,4 triệu; CPA ≤ 78,000, ROAS ≥ 3.1.
- **Khách hàng:** nữ 25–44 ở HCM/Hà Nội; remarketing người đã nhắn tin/xem video.
- **Ưu đãi:** tư vấn inbox kèm combo; chương trình khách cũ (tặng mẫu thử) để tăng mua lại.
- **Góc sáng tạo:** nội dung người dùng chia sẻ cách dùng, bài so sánh thành phần có dẫn nguồn.
- **KPI:** CPA, ROAS, tỷ lệ chốt inbox, % khách cũ quay lại.

### KOC / Affiliate
- **Mục tiêu:** ~578 đơn, doanh thu 133,7 triệu; CPA ≤ 70,000, ROAS ≥ 3.3.
- **Khách hàng:** nữ 18–34 theo cộng đồng KOC địa phương HCM/Hà Nội; thử 1 KOC ở Đà Nẵng bằng dự phòng.
- **Ưu đãi:** hoa hồng theo đơn thành công kèm mã riêng; sản phẩm gửi mẫu cho KOC.
- **Góc sáng tạo:** KOC tự trình bày trải nghiệm; mọi nội dung duyệt trước theo `canon/company.md#claims`, KOC không được nêu công dụng điều trị.
- **KPI:** số KOC hoạt động (mục tiêu 30), đơn/KOC, CPA, tỷ lệ nội dung được duyệt đạt.

### Google Ads
- **Mục tiêu:** ~411 đơn, doanh thu 101,7 triệu; CPA ≤ 95,000, ROAS ≥ 2.6 (kênh có CPA cao nhất, ngân sách giữ gần mức tối thiểu).
- **Khách hàng:** nữ 25–44 tìm kiếm chủ đích; từ khóa thương hiệu và tên sản phẩm.
- **Ưu đãi:** trang đích website có combo và đăng ký thành viên (thu tệp CRM).
- **Góc sáng tạo:** quảng cáo Search theo tên sản phẩm/thành phần; YouTube chỉ remarketing.
- **KPI:** CPA, ROAS, tỷ lệ chuyển đổi trang đích, số lượt đăng ký thành viên.

## KPI

Mục tiêu mỗi tháng theo trọng số ramp-up 30/33/37% của brief (đơn và doanh thu tính trên mục tiêu 4,000 đơn và 1.200 triệu; ngân sách từ bảng trên):

| KPI | 2027-01 | 2027-02 | 2027-03 | Tổng Q1 |
|---|---|---|---|---|
| Ngân sách chi (VND, gồm dự phòng) | 89,999,000 | 98,999,000 | 111,002,000 | 300,000,000 |
| Đơn hàng (mục tiêu) | 1,200 | 1,320 | 1,480 | 4,000 |
| Doanh thu mục tiêu (VND) | 360,000,000 | 396,000,000 | 444,000,000 | 1,200,000,000 |
| Doanh thu cam kết sàn (VND) | 300,000,000 | 330,000,000 | 370,000,000 | 1,000,000,000 |
| AOV mục tiêu (VND) | 300,000 | 300,000 | 300,000 | 300,000 |
| Tỷ lệ mua lại tích lũy | 6% | 12% | 18% | ≥ 18% |
| % đơn là combo | 15% | 25% | 30% | 30% |

KPI theo kênh (cổng cảnh báo): CPA tối đa và ROAS tối thiểu như từng mục "Chiến lược theo kênh"; tuần nào kênh vượt CPA 20% hoặc thấp hơn ROAS 20% thì đưa vào `ops-review` và đề xuất điều chỉnh (việc đổi ngân sách cần duyệt của founder).

## Lịch triển khai

| Thời gian | Việc chính |
|---|---|
| Tuần 0 (cuối 12/2026) | Founder duyệt kế hoạch; thay brief thật; xác nhận tồn kho và thời gian sản xuất cho đỉnh Tết; chuẩn bị creative; dựng báo cáo tuần |
| 01/2027 (tuần 1–4) | Chạy 5 kênh ở mức ngân sách tháng 1; A/B combo; tuyển 30 KOC; mở tệp CRM; flash sale 1.1; review tuần |
| 02/2027 | Tết Nguyên Đán 2027 (mùng 1 dự kiến 06/02/2027 — giả định, cần xác nhận): tăng quà biếu/Valentine 14/02 trước Tết, dự phòng nhịp giao hàng nghỉ Tết; bắt đầu chương trình khách cũ |
| 03/2027 | Tháng ngân sách cao nhất (37%); sale 3.3; chuẩn bị 8/3 (nằm ngoài quý này, đặt hàng trước tháng 2); chốt đo tỷ lệ mua lại |
| Hằng tuần | `ops-review` trên dữ liệu export; điều chỉnh theo cổng KPI; báo founder |
| Cuối quý (31/03) | Báo cáo kết quả so mục tiêu; ghi benchmark thực đo vào memory (qua inbox) |

## Rủi ro

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Doanh thu thiếu ~22% so với mục tiêu nếu không có đòn bẩy AOV | Cao | Đòn A/B/C; cam kết sàn 1.000 triệu; theo dõi AOV hằng tuần |
| Benchmark brief là SAMPLE, ROAS TikTok độ tin cậy thấp | Cao | Cổng ROAS 3.0; thay bằng số thật từ `ops-review` khi có |
| Hết hàng trước/trong Tết hoặc sản xuất gia công không kịp | Cao | Xác nhận lead time và tồn kho với nhà sản xuất ngay tuần 0 (chưa có trong repo) |
| Nghỉ Tết làm giao hàng và CS gián đoạn | Trung bình | Lịch nghỉ công bố trước, tăng tồn trong kho sàn, đội CS trực luân phiên |
| Claim quảng cáo vi phạm quy định mỹ phẩm | Cao | Mọi creative theo `canon/company.md#claims`; KOC được duyệt nội dung; cần rà soát pháp lý (nguồn claim là giả định) |
| Dồn tiền vào kênh sàn làm phụ thuộc Shopee | Trung bình | Giữ tối thiểu theo min_share, đầu tư CRM/website, thử TikTok Shop |
| Dữ liệu khách hàng bị lộ khi làm KOC/CRM | Cao | Chỉ dùng mã KH-####, tệp thô trong `data/cs/private/` (quy tắc R15) |
| Mục tiêu mua lại 18% không đạt trong 3 tháng | Trung bình | Chương trình khách cũ, nhắc mua lại 45–60 ngày, đo từ tháng 1 |

## Giả định & nguồn

| Nội dung | Nguồn / trạng thái |
|---|---|
| Mục tiêu, ngân sách 300 triệu, 10% dự phòng, trọng số tháng 30/33/37% | `inputs/SAMPLE-phase-brief.md` — **SAMPLE** (dữ liệu tổng hợp) |
| CPA/ROAS từng kênh | Brief — **SAMPLE**, đánh dấu *giả định*; TikTok ROAS theo fact `benchmark.tiktok-ads.roas` (độ tin cậy thấp) |
| Khu vực và nhóm khách hàng (tỷ trọng, AOV) | Brief `regions`, `audiences_last_q` — **SAMPLE** |
| AOV ngầm định = CPA × ROAS | Fact `ads.benchmarks.implied-aov`; tính bởi script (`evidence/allocation.md`) |
| Đòn bẩy A (30% combo, +120,000), B (50% hiệu lực), C (chuyển 15 triệu) | *Giả định* của kế hoạch, tính tại `evidence/levers.txt` |
| Phân bổ vùng 55/35/10 | *Giả định*, cần điều chỉnh sau 2 tuần |
| Sản phẩm, giá, kênh bán | `canon/company.md` — **SAMPLE** |
| Ngưỡng freeship 399,000 VND | Fact `policy.free-shipping.threshold-vnd` — SAMPLE, độ tin cậy thấp |
| Ngày Tết 2027 (06/02/2027), lịch sale Shopee | *Giả định*, chưa xác nhận trong repo |
| Quy định claim mỹ phẩm | `canon/company.md#claims` — nguồn là giả định, chưa rà soát pháp lý |

Điểm chưa có trong repo: tồn kho và thời gian sản xuất cho Tết, số liệu thật của quý trước.

## English summary

- Plan for Q1/2027 (Jan–Mar) built on a **SAMPLE** brief: 5 funded ad channels, 300,000,000 VND total, 10% reserve, split 30/33/37% by month (script-generated, exact total).
- Focus regions: Ho Chi Minh City (46% of orders) and Hanoi (31%); Da Nang is a small geo test. Core audience: women 25–34 (44% of orders, 48% of revenue).
- With the brief's benchmarks, the budget yields ~4,049 orders but only ~935.9M VND revenue, a 264.1M gap (22%) to the 1.2B goal; implied AOV is 231,133 VND.
- Three levers close the gap on paper (combos +145.8M, repeat purchase at 50% haircut +84.2M, moving 15M of reserve to Shopee Ads +63.0M, total ≈ +293M), but all rest on assumptions, so the committed floor is 1.0B and 1.2B is a stretch.
- Weekly ops-review gates (CPA/ROAS ±20%) and founder approval are required for any budget change.
- Open items: real (non-SAMPLE) benchmarks, stock/lead time for Tết, Tết date, legal review of the claims list.
