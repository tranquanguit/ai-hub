# Đánh giá vận hành tuần 2026-11-03..09

> **Dữ liệu SAMPLE**: toàn bộ số liệu lấy từ `inputs/SAMPLE-ops-export/` (dữ liệu tổng hợp, không phải số thật). Mục tiêu trong `targets.json` cũng là SAMPLE, chờ Founder xác nhận. Mọi số liệu trích từ `evidence/kpis.json` / `kpis.md`. Báo cáo chỉ đề xuất, chưa thực thi (R13).

## Tóm tắt
- Toàn tuần chi 43,950,000 VND, doanh thu 172,887,000 VND, ROAS 3.93, CPA trung bình 97,884 VND. Ba kênh hiệu quả: SP_Search_Ads, GG_Search_Brand, FB_Retargeting_Combo.
- 4/7 chiến dịch bị gắn cờ, trong đó TT_Broad_LipTint (ROAS 0.23) và GG_Search_Generic_Serum (ROAS 0.58) lỗ nặng. FB_Prospecting_Serum và TT_Spark_KOC_Sunscreen là hai chiến dịch lớn nhất, ROAS 1.68 và 1.8, gần mục tiêu 2.0.
- Mục tiêu CPA 90,000 VND mâu thuẫn với ROAS 2.0 (CPA tối đa hợp lý ≈ 192,524 VND), nên cờ CPA gắn sai lên cả chiến dịch đạt ROAS. Cần Founder đặt lại.
- SEO: "son tint lâu trôi" (22→31) và "kem chống nắng nâng tone" (27→41) tụt hạng.
- CSKH: cả 4 kênh có tỷ lệ giải quyết dưới 90%; TikTok Shop phản hồi chậm cuối tuần (07 và 08/11); có 1 ca kích ứng da trên Shopee (05/11).

## Quảng cáo

### Ads theo chiến dịch / by campaign

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

### Target consistency

AOV 385,048 VND / ROAS min 2.0 = max CPA 192,524 VND vs target 90,000 VND -> INCONSISTENT: cpa_max 90,000 < AOV/roas_min 192,524: CPA flags fire on campaigns that meet ROAS; ask the Founder to reset the CPA target

### Chẩn đoán
- **TT_Broad_LipTint**: CTR 0.60% thấp nhất và CPA 805,000 VND. Nguyên nhân khả dĩ: creative hoặc tệp đối tượng broad không phù hợp (giả thuyết, chưa kiểm chứng). Chiến dịch này cũng song hành với việc từ khóa "son tint lâu trôi" tụt hạng.
- **GG_Search_Generic_Serum**: CTR 2.10% tốt nhưng CPA 782,142 VND và ROAS 0.58, nghĩa là người click không mua. Nguyên nhân khả dĩ: landing page hoặc ưu đãi, hoặc từ khóa generic quá rộng (giả thuyết).
- **FB_Prospecting_Serum**: CTR 1.06% ổn, ROAS 1.68, CPA 251,414 VND cao hơn ngưỡng hợp lý 192,524 VND. Hướng: tối ưu landing page/ưu đãi, thử creative mới (giả thuyết).
- **TT_Spark_KOC_Sunscreen**: CTR 1.40% tốt, CPA 171,573 VND dưới 192,524 VND nhưng ROAS 1.8 vẫn dưới 2.0. Gần đạt mục tiêu, đáng giữ và tối ưu thay vì cắt.
- Ba chiến dịch ok (SP_Search_Ads, GG_Search_Brand, FB_Retargeting_Combo) có ROAS 8.4–14.71. Lưu ý GG_Search_Brand và FB_Retargeting_Combo phụ thuộc nhu cầu sẵn có từ kênh khác, nên tăng ngân sách có thể giảm hiệu quả biên (giả thuyết).

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

- **son tint lâu trôi** (−9): tụt khỏi trang 2 và chỉ còn 13 click. Nguyên nhân chưa xác định; cần kiểm tra nội dung trang /son (giả thuyết).
- **kem chống nắng nâng tone** (−14, 2 click): lượng click rất nhỏ nên ưu tiên thấp. Khi viết lại nội dung cần tuân thủ claim tại `canon/company.md#claims`.
- Hai serum đang đi lên (serum niacinamide +5, serum cấp ẩm cho da khô +6), cơ hội đẩy vào top 10.

## CSKH

### CSKH / Customer service

| channel | tickets | resolution | median FRT (min) | max FRT | CSAT | skin reports | flags |
|---|---|---|---|---|---|---|---|
| tiktok_shop_chat | 206 | 88.3% | 9.1 | 31.8 | 4.41 | 0 | first response > 15 min on 2026-11-07, 2026-11-08; CSAT 4.41 < 4.5; resolution 88.3% < 90% |
| shopee_chat | 158 | 88.0% | 7.8 | 11.2 | 4.41 | 1 | CSAT 4.41 < 4.5; resolution 88.0% < 90% |
| facebook_inbox | 176 | 89.8% | 8.9 | 11.7 | 4.58 | 0 | resolution 89.8% < 90% |
| hotline | 128 | 86.7% | 10.7 | 12.4 | 4.51 | 0 | resolution 86.7% < 90% |

- **tiktok_shop_chat**: FRT vượt 15 phút đúng vào thứ Bảy 07/11 và Chủ nhật 08/11 (max 31.8 phút). Giả thuyết: thiếu người trực cuối tuần, cần đối chiếu lịch trực.
- **shopee_chat**: có 1 ca kích ứng da ngày 2026-11-05. Đây là vấn đề an toàn sản phẩm, cần Founder biết (không ghi thông tin khách trong báo cáo).
- Cả 4 kênh có tỷ lệ giải quyết dưới 90% (hotline thấp nhất, 86.7%). Chưa có dữ liệu nguyên nhân (ticket chưa giải quyết thuộc loại nào), cần phân loại.

## Đề xuất

Tổng ngân sách đề xuất giữ nguyên 43,950,000 VND; mọi thay đổi cần Founder duyệt trước khi thực hiện.

1. **Mục tiêu CPA (targets.json: cpa_max_vnd)**: Founder đặt lại mục tiêu CPA từ 90,000 VND lên khoảng 190,000 VND (AOV/ROAS min = 192,524 VND) trong 3 ngày; owner: Founder; kiểm tra lại: số cờ CPA trong báo cáo tuần sau.
2. **TT_Broad_LipTint**: giảm 50% ngân sách, tức −3,220,000 VND/tuần, và thay creative trong 7 ngày; nếu ROAS vẫn dưới 1.0 thì dừng; owner: Marketing; kiểm tra lại: ROAS và CTR (mục tiêu CTR ≥ 0.8%).
3. **GG_Search_Generic_Serum**: giảm 50% ngân sách (−2,737,000 VND/tuần), loại từ khóa generic không ra đơn và rà landing page trong 7 ngày; owner: Marketing; kiểm tra lại: CPA và ROAS.
4. **SP_Search_Ads**: tăng ngân sách +3,000,000 VND/tuần (từ số tiết kiệm ở mục 2 và 3), theo dõi 7 ngày; owner: Marketing; kiểm tra lại: ROAS (giữ ≥ 8, giả định hiệu quả biên giảm).
5. **FB_Retargeting_Combo**: tăng ngân sách +2,900,000 VND/tuần, theo dõi tần suất quảng cáo, 7 ngày; owner: Marketing; kiểm tra lại: ROAS (giữ ≥ 5) và CPA. Phần dư 57,000 VND giữ làm dự phòng.
6. **FB_Prospecting_Serum**: giữ ngân sách, thử 2 creative mới và 1 phương án ưu đãi trên landing page trong 14 ngày; owner: Marketing; kiểm tra lại: ROAS từ 1.68 lên ≥ 2.0.
7. **TT_Spark_KOC_Sunscreen**: giữ ngân sách, mở rộng thêm 2 KOC trong 14 ngày; owner: Marketing; kiểm tra lại: ROAS từ 1.8 lên ≥ 2.0.
8. **son tint lâu trôi**: rà soát và làm mới nội dung trang /son trong 14 ngày; owner: Marketing; kiểm tra lại: thứ hạng từ 31 về ≤ 22.
9. **kem chống nắng nâng tone**: ưu tiên thấp, làm mới nội dung theo claim hợp lệ trong 21 ngày; owner: Marketing; kiểm tra lại: thứ hạng từ 41 về ≤ 27.
10. **shopee_chat (skin_reaction)**: báo Founder ca kích ứng da (kênh shopee_chat, ngày 2026-11-05); CS thu thập lô sản phẩm và triệu chứng trong `data/cs/private/` và phản hồi trong 2 ngày; owner: CS; kiểm tra lại: skin_reaction_reports tuần sau (mục tiêu 0 ca chưa xử lý).
11. **tiktok_shop_chat**: bổ sung 1 người trực thứ Bảy và Chủ nhật trong 7 ngày; owner: CS; kiểm tra lại: FRT tối đa dưới 15 phút.
12. **tiktok_shop_chat, shopee_chat, facebook_inbox, hotline (resolution)**: phân loại ticket chưa giải quyết và đưa tỷ lệ giải quyết lên ≥ 90% trong 14 ngày; owner: CS; kiểm tra lại: resolution mỗi kênh; ưu tiên hotline (86.7%) và CSAT của tiktok_shop_chat, shopee_chat (4.41 → 4.5).

## English summary
SAMPLE data. Spend was 43,950,000 VND, ROAS 3.93. Shopee Search, Google Brand and Facebook Retargeting perform well; TT_Broad_LipTint and GG_Search_Generic_Serum lose money. The CPA target (90,000 VND) is inconsistent with ROAS 2.0 (implied max about 192,524 VND), so the Founder should reset it. Proposal: shift about 5.96M VND/week from the two worst campaigns to Shopee Search and FB Retargeting within the same total, subject to Founder approval. SEO: two keywords dropped. CS: resolution below 90% on all channels, weekend slowness on TikTok Shop, and one skin-reaction case on Shopee (2026-11-05) needing Founder follow-up.
