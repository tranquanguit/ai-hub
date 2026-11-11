# Đánh giá vận hành tuần 03–09/11/2026

> **Dữ liệu SAMPLE (tổng hợp, không phải số thật).** Ngưỡng trong `targets.json` cũng là SAMPLE, chờ Founder xác nhận. Số liệu trích từ `evidence/kpis.json` (tính bằng `compute_kpis.py`).

## Tóm tắt
- Toàn tuần: chi 43,95 triệu VND, doanh thu 172,9 triệu, ROAS tổng 3,93, CPA tổng 97.884 VND (cao hơn mục tiêu 90.000).
- 4/7 chiến dịch bị gắn cờ, chiếm khoảng 32,7 triệu (74%) tổng chi: TT_Broad_LipTint, GG_Search_Generic_Serum, FB_Prospecting_Serum, TT_Spark_KOC_Sunscreen. Ba chiến dịch FB_Retargeting_Combo, GG_Search_Brand, SP_Search_Ads vượt chuẩn xa (ROAS 8,4–14,7).
- Mục tiêu CPA ≤ 90.000 và ROAS ≥ 2,0 **mâu thuẫn nhau**: AOV tuần ≈ 385.000 VND (172,887 triệu / 449 đơn) nên CPA tối đa tương ứng ROAS 2,0 là ≈ 192.500. Cần Founder chốt lại, nếu không cờ CPA báo sai (fact `ads.targets.cpa-roas-consistency`).
- SEO: 2 từ khóa tụt hạng ("kem chống nắng nâng tone" −14, "son tint lâu trôi" −9).
- CSKH: cả 4 kênh dưới ngưỡng tỉ lệ giải quyết 90%; tiktok_shop_chat phản hồi chậm (tối đa 31,8 phút) vào 07 và 08/11.
- **Có 1 báo cáo phản ứng da (shopee_chat) → chuyển Founder theo dõi an toàn sản phẩm.**

## Quảng cáo

| campaign | platform | spend (VND) | conv | revenue (VND) | CTR | CPC | CPA | ROAS | flags |
|---|---|---|---|---|---|---|---|---|---|
| TT_Broad_LipTint | tiktok | 6,440,000 | 8 | 1,479,000 | 0.60% | 6,295 | 805,000 | 0.23 | ROAS 0.23 < 2.0; CPA 805000 > 90000; CTR 0.60% < 0.8% |
| GG_Search_Generic_Serum | google | 5,475,000 | 7 | 3,167,000 | 2.10% | 7,832 | 782,142 | 0.58 | ROAS 0.58 < 2.0; CPA 782142 > 90000 |
| FB_Prospecting_Serum | facebook | 10,308,000 | 41 | 17,339,000 | 1.06% | 4,882 | 251,414 | 1.68 | ROAS 1.68 < 2.0; CPA 251414 > 90000 |
| TT_Spark_KOC_Sunscreen | tiktok | 10,466,000 | 61 | 18,799,000 | 1.40% | 2,721 | 171,573 | 1.8 | ROAS 1.8 < 2.0; CPA 171573 > 90000 |
| FB_Retargeting_Combo | facebook | 5,011,000 | 75 | 42,076,000 | 1.84% | 2,824 | 66,813 | 8.4 | ok |
| GG_Search_Brand | google | 2,037,000 | 70 | 28,058,000 | 8.50% | 2,505 | 29,100 | 13.77 | ok |
| SP_Search_Ads | shopee | 4,213,000 | 187 | 61,969,000 | 3.38% | 888 | 22,529 | 14.71 | ok |
| **Total** | | 43,950,000 | 449 | 172,887,000 | | | 97,884 | 3.93 | |

**Chẩn đoán** (nguyên nhân là giả thuyết, dữ liệu chưa đủ để khẳng định):
- **TT_Broad_LipTint**: CTR 0,60% dưới ngưỡng 0,8% → creative hoặc tệp đối tượng broad chưa phù hợp (giả thuyết). Chi 6,44 triệu chỉ ra 8 đơn.
- **GG_Search_Generic_Serum**: CTR 2,10% ổn nhưng chuyển đổi rất thấp (7 đơn trên 5,475 triệu) → landing page hoặc ưu đãi, hoặc từ khóa generic kéo traffic chưa có ý định mua (giả thuyết).
- **FB_Prospecting_Serum**: CTR 1,06% đạt, ROAS 1,68 gần ngưỡng → tối ưu creative/offer, chưa cần cắt. Chi lớn thứ hai (10,3 triệu).
- **TT_Spark_KOC_Sunscreen**: CTR 1,40% tốt, ROAS 1,8 sát ngưỡng; CPA 171.573 thấp hơn ngưỡng ngầm 192.500 nên cờ CPA chủ yếu do mục tiêu mâu thuẫn. Giữ và theo dõi.
- Retargeting, Brand search, Shopee ROAS rất cao, nhưng phần lớn là khách đã biết thương hiệu, nên tăng ngân sách chưa chắc tăng tuyến tính (giả thuyết).

## SEO

| keyword | prev | now | change | clicks |
|---|---|---|---|---|
| kem chống nắng nâng tone | 27 | 41 | -14 | 2 |
| son tint lâu trôi | 22 | 31 | -9 | 13 |
| sữa rửa mặt amino | 11 | 12 | -1 | 48 |
| lunobeau | 1 | 1 | +0 | 932 |
| kem chống nắng da dầu | 8 | 7 | +1 | 77 |
| serum niacinamide | 14 | 9 | +5 | 19 |
| serum cấp ẩm cho da khô | 19 | 13 | +6 | 49 |

- "kem chống nắng nâng tone" (27→41) và "son tint lâu trôi" (22→31) tụt hạng; cả hai vốn đã ở vị trí xa (>20), click nhỏ (2 và 13) nên tác động doanh thu tuần này thấp. Nguyên nhân chưa xác định được từ dữ liệu (đối thủ hoặc nội dung trang: giả thuyết).
- Serum niacinamide (14→9) và serum cấp ẩm (19→13) đang cải thiện; nên đẩy tiếp vào top 5.
- Nội dung cho từ khóa "nâng tone" phải tuân `canon/company.md#claims` (không claim điều trị; claim về hiệu quả cần nguồn dẫn).

## CSKH

| channel | tickets | resolution | median FRT (min) | max FRT | CSAT | skin reports | flags |
|---|---|---|---|---|---|---|---|
| tiktok_shop_chat | 206 | 88.3% | 9.1 | 31.8 | 4.41 | 0 | first response > 15 min on 2026-11-07, 2026-11-08; CSAT 4.41 < 4.5; resolution 88.3% < 90% |
| shopee_chat | 158 | 88.0% | 7.8 | 11.2 | 4.41 | 1 | CSAT 4.41 < 4.5; resolution 88.0% < 90% |
| facebook_inbox | 176 | 89.8% | 8.9 | 11.7 | 4.58 | 0 | resolution 89.8% < 90% |
| hotline | 128 | 86.7% | 10.7 | 12.4 | 4.51 | 0 | resolution 86.7% < 90% |

- **tiktok_shop_chat**: FRT trung vị 9,1 phút ổn nhưng vượt 15 phút vào 07 và 08/11 (thứ Bảy, Chủ nhật) → giả thuyết thiếu người trực cuối tuần, chưa kiểm chứng.
- Tỉ lệ giải quyết cả 4 kênh dưới 90% (86,7–89,8%): lệch nhỏ ở facebook_inbox, lớn nhất ở hotline.
- **shopee_chat có 1 báo cáo phản ứng da**: cần theo dõi an toàn sản phẩm (xem Đề xuất #6). Báo cáo này không chứa thông tin cá nhân khách hàng.

## Đề xuất
(Báo cáo chỉ đề xuất; thay đổi ngân sách và mọi hành động bên ngoài cần Founder duyệt. Tổng ngân sách tuần giữ nguyên 43,95 triệu VND.)

1. **TT_Broad_LipTint**: tạm dừng, thu hồi 6,44 triệu VND/tuần; làm lại creative và tệp đối tượng trong 14 ngày rồi mới chạy thử quy mô nhỏ (ngân sách do Founder duyệt riêng). Owner: Marketing. Kiểm tra lại: CTR ≥ 0,8% và ROAS ≥ 2,0.
2. **GG_Search_Generic_Serum**: giảm 50% (−2,74 triệu VND/tuần), loại từ khóa generic không ra đơn, rà landing page và offer trong 7 ngày. Owner: Marketing. Kiểm tra lại: CPA < 192.500 VND và ROAS ≥ 2,0.
3. **FB_Prospecting_Serum**: giữ 10,3 triệu và bổ sung 3,18 triệu VND cho thử nghiệm A/B creative/offer mới, đánh giá sau 7 ngày. Owner: Marketing. Kiểm tra lại: ROAS từ 1,68 lên ≥ 2,0.
4. **TT_Spark_KOC_Sunscreen**: giữ nguyên 10,47 triệu VND, không tăng cho tới khi ROAS ≥ 2,0 trong 2 tuần liên tiếp; duyệt nội dung KOC theo mục claims. Owner: Marketing. Kiểm tra lại: ROAS ≥ 2,0 (hiện 1,8).
5. **Phân bổ lại 6,0 triệu VND** (từ #1 và #2): +3,0 triệu cho **FB_Retargeting_Combo** (theo dõi tần suất quảng cáo để tránh bão hòa) và +3,0 triệu cho **SP_Search_Ads**; không tăng GG_Search_Brand (CTR 8,5%, dễ bão hòa). Cần Founder duyệt trước khi thực hiện. Owner: Founder (duyệt), Marketing (thực hiện). Kiểm tra lại: ROAS của hai chiến dịch vẫn ≥ 5 sau 7 ngày.
6. **shopee_chat (kích ứng da)**: escalate lên Founder; Founder xem xét 1 báo cáo kích ứng da / phản ứng da trong 2 ngày, hỏi nhà sản xuất về lô sản phẩm liên quan, và duyệt mẫu trả lời an toàn cho CS (khuyên ngưng dùng, hỏi ý kiến chuyên môn, không chẩn đoán). Owner: Founder. Kiểm tra lại: số báo cáo phản ứng da tuần sau và phương án xử lý đã ghi nhận.
7. **Mục tiêu CPA**: Founder quyết định trong 7 ngày giữa (a) nâng cpa_max lên ~190.000 VND để khớp ROAS 2,0, hoặc (b) giữ 90.000 và nâng roas_min lên ~4,3 (AOV ≈ 385.000). Owner: Founder. Kiểm tra lại: `targets.json` cập nhật và cờ CPA hết mâu thuẫn.
8. **kem chống nắng nâng tone** (SEO): viết lại nội dung trang /kem theo đúng claims, mục tiêu quay về hạng ≤ 27 trong 21 ngày. Owner: Marketing. Kiểm tra lại: vị trí trong `seo.csv` tuần sau.
9. **son tint lâu trôi** (SEO): cập nhật trang sản phẩm son tint và thêm nội dung hướng dẫn, mục tiêu hạng ≤ 22 trong 21 ngày. Owner: Marketing. Kiểm tra lại: vị trí và clicks (hiện 13) tuần sau.
10. **tiktok_shop_chat**: thêm 1 ca trực thứ Bảy và Chủ nhật, mục tiêu FRT tối đa ≤ 15 phút trong 14 ngày; Founder duyệt chi phí nhân sự. Owner: CS. Kiểm tra lại: max FRT từ 31,8 xuống ≤ 15 phút và CSAT ≥ 4,5 (hiện 4,41).
11. **shopee_chat**: rà các ticket chưa giải quyết (12% tồn) và bổ sung mẫu trả lời, mục tiêu tỉ lệ giải quyết ≥ 90% trong 14 ngày. Owner: CS. Kiểm tra lại: resolution (hiện 88,0%) và CSAT (hiện 4,41).
12. **facebook_inbox**: đóng nốt ticket tồn, mục tiêu tỉ lệ giải quyết ≥ 90% trong 7 ngày (hiện 89,8%). Owner: CS. Kiểm tra lại: resolution tuần sau.
13. **hotline**: phân tích nhóm ticket chưa giải quyết được, mục tiêu tỉ lệ giải quyết ≥ 90% trong 21 ngày (hiện 86,7%, thấp nhất). Owner: CS. Kiểm tra lại: resolution và CSAT (hiện 4,51).

## English summary
SAMPLE data, week 3–9 Nov 2026: total spend VND 43.95M, ROAS 3.93, CPA 97,884. Four campaigns (TT_Broad_LipTint, GG_Search_Generic_Serum, FB_Prospecting_Serum, TT_Spark_KOC_Sunscreen) take 74% of spend but miss targets. We propose pausing the worst, halving Google generic, testing new creative on Facebook prospecting, and shifting VND 6M to retargeting and Shopee, pending Founder approval. The CPA (90k) and ROAS (≥2.0) targets contradict each other given AOV ≈ 385k, so the Founder must reset one. Two SEO keywords dropped; all four CS channels are below the 90% resolution target, and TikTok Shop had weekend response delays. One skin-reaction report (shopee_chat) is escalated to the Founder for product-safety follow-up.
