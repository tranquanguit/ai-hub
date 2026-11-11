# Đánh giá vận hành tuần 03–09/11/2026

> **Dữ liệu SAMPLE (tổng hợp, không phải số liệu thật).** Mọi kết luận dưới đây chỉ có giá trị minh hoạ quy trình cho đến khi thay bằng export thật. Targets trong `targets.json` cũng là SAMPLE, Founder cần xác nhận. Nguồn số: `evidence/kpis.json`.

## Tóm tắt
- Tổng chi ads 43,950,000 VND, doanh thu 172,887,000 VND, ROAS gộp 3.93, CPA gộp 97,884 VND. Số gộp tốt nhờ 3 chiến dịch hiệu quả cao (SP_Search_Ads, GG_Search_Brand, FB_Retargeting_Combo). Bốn chiến dịch còn lại, chiếm 32.7M (74% chi tiêu), đều dưới ROAS 2.0.
- TT_Broad_LipTint (ROAS 0.23) và GG_Search_Generic_Serum (ROAS 0.58) đang đốt ngân sách. FB_Prospecting_Serum (1.68) và TT_Spark_KOC_Sunscreen (1.80) gần ngưỡng, cần sửa chứ chưa cần dừng.
- **An toàn sản phẩm:** có 1 báo cáo phản ứng da (shopee_chat, 05/11). Cần Founder theo dõi.
- CSKH: cả 4 kênh có tỷ lệ giải quyết dưới 90%. TikTok Shop vượt 15 phút ở 07 và 08/11 (cuối tuần), tối đa 31.8 phút.
- SEO: "son tint lâu trôi" tụt 9 hạng, "kem chống nắng nâng tone" tụt 14 hạng. Từ khoá "nâng tone" không nên cố cứu (xem phần SEO).

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

**Chẩn đoán**
- **TT_Broad_LipTint:** CTR 0.60% thấp và CPA 805,000 VND, gần như mỗi ngày chỉ 1 đơn. Nguyên nhân khả dĩ nhất là creative hoặc đối tượng broad không khớp (giả định, chưa xác nhận được từ dữ liệu). Lưu ý từ khoá SEO "son tint lâu trôi" cũng tụt hạng, gợi ý dòng son đang yếu trên nhiều kênh.
- **GG_Search_Generic_Serum:** CTR 2.10% khá nhưng CPA 782,142 VND. Người dùng bấm nhưng không mua, nên nghi ngờ landing page hoặc offer, hoặc từ khoá generic kéo traffic chưa có ý định mua (giả định).
- **FB_Prospecting_Serum:** CTR 1.06% đạt, ROAS 1.68 và CPA 251,414 VND. CTR ổn mà chuyển đổi kém, nghi ngờ landing page hoặc offer (giả định).
- **TT_Spark_KOC_Sunscreen:** CTR 1.40% tốt, ROAS 1.80 sát ngưỡng. Đây là chiến dịch gần đạt nhất trong nhóm bị gắn cờ.
- **Target CPA mâu thuẫn với target ROAS:** AOV ngầm định = 172,887,000 / 449 = khoảng 385,000 VND. Theo fact `ads.targets.cpa-roas-consistency`, cpa_max phải ≥ AOV / roas_min = khoảng 192,500 VND, trong khi `targets.json` đặt 90,000 VND. Vì vậy cờ CPA kích hoạt cả với chiến dịch đạt ROAS. Với cpa_max khoảng 190,000, TT_Spark_KOC_Sunscreen (171,573) sẽ qua cờ CPA nhưng vẫn rớt cờ ROAS.

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

- **kem chống nắng nâng tone:** tụt 14 hạng, chỉ 2 click. Theo fact `product.lb-sun-01.claim.tone-up`, LB-SUN-01 không được mô tả là nâng tone trong canon, nên không tối ưu hay nhắm từ khoá này. Tụt hạng ở đây không phải vấn đề cần cứu.
- **son tint lâu trôi:** tụt 9 hạng (22 sang 31), 13 click. Nguyên nhân chưa rõ (hypothesis: nội dung trang `/son` yếu hoặc đối thủ tăng).
- Tín hiệu tốt: serum niacinamide (+5) và serum cấp ẩm cho da khô (+6), cùng "kem chống nắng da dầu" (+1, hạng 7). Đây là các từ khoá nên đẩy nội dung hỗ trợ.

## CSKH

| channel | tickets | resolution | median FRT (min) | max FRT | CSAT | skin reports | flags |
|---|---|---|---|---|---|---|---|
| tiktok_shop_chat | 206 | 88.3% | 9.1 | 31.8 | 4.41 | 0 | first response > 15 min on 2026-11-07, 2026-11-08; CSAT 4.41 < 4.5; resolution 88.3% < 90% |
| shopee_chat | 158 | 88.0% | 7.8 | 11.2 | 4.41 | 1 | CSAT 4.41 < 4.5; resolution 88.0% < 90% |
| facebook_inbox | 176 | 89.8% | 8.9 | 11.7 | 4.58 | 0 | resolution 89.8% < 90% |
| hotline | 128 | 86.7% | 10.7 | 12.4 | 4.51 | 0 | resolution 86.7% < 90% |

- **tiktok_shop_chat:** FRT 31.8 và 31.4 phút vào thứ Bảy 07/11 và Chủ nhật 08/11, trong khi các ngày thường dưới 12 phút. Nghi ngờ thiếu người trực cuối tuần (hypothesis; ca trực chưa có trong dữ liệu). CSAT cũng thấp nhất vào 2 ngày này (4.1 và 4.0).
- **shopee_chat:** 1 báo cáo phản ứng da ngày 05/11. Dữ liệu không nêu sản phẩm hay mức độ, cần CS thu thập (không ghi thông tin cá nhân khách ngoài `data/cs/private/`).
- **Tỷ lệ giải quyết dưới 90% ở cả 4 kênh**, thấp nhất là hotline 86.7%. Đây là vấn đề quy trình chung hơn là lỗi của một kênh.

## Đề xuất

Ngân sách tổng giữ nguyên 43,950,000 VND/tuần. Các mức dưới đây là đề xuất, chưa thực thi, cần Founder duyệt (R8).

1. **TT_Broad_LipTint** — tạm dừng, thu hồi 6,440,000 VND/tuần. Owner: Marketing, trong 3 ngày. Chạy lại chỉ với creative và đối tượng mới ở ngân sách thử 1,500,000 VND/tuần. Kiểm tra lại: ROAS ≥ 2.0 và CTR ≥ 0.8%.
2. **GG_Search_Generic_Serum** — giảm từ 5,475,000 xuống 2,000,000 VND/tuần (-3,475,000), loại từ khoá không có ý định mua. Owner: Marketing, trong 7 ngày. Kiểm tra lại: CPA dưới 250,000 VND và ROAS ≥ 2.0.
3. **FB_Prospecting_Serum** — giảm từ 10,308,000 xuống 7,000,000 VND/tuần (-3,308,000), thử 2 landing page và offer mới. Owner: Marketing, trong 14 ngày. Kiểm tra lại: ROAS ≥ 2.0 (hiện 1.68).
4. **TT_Spark_KOC_Sunscreen** — giữ 10,466,000 VND/tuần, thêm 2 video KOC mới và đặt hạn 14 ngày. Owner: Marketing. Kiểm tra lại: ROAS ≥ 2.0 (hiện 1.80); nếu không đạt thì giảm 30%.
5. **SP_Search_Ads** — tăng từ 4,213,000 lên 8,200,000 VND/tuần (+3,987,000), theo dõi mỗi 3 ngày. Owner: Sales. Kiểm tra lại: ROAS ≥ 8 (hiện 14.71). Giả định ROAS biên giảm khi tăng chi tiêu.
6. **FB_Retargeting_Combo** — tăng từ 5,011,000 lên 8,000,000 VND/tuần (+2,989,000). Owner: Marketing, trong 7 ngày. Kiểm tra lại: ROAS ≥ 5 và tần suất hiển thị, vì tệp retargeting nhỏ dễ bão hoà.
7. **Ngân sách chưa phân bổ** — dự phòng 4,747,000 VND = 13,223,000 thu hồi (mục 1–3) trừ 6,976,000 tăng (mục 5, 6) trừ 1,500,000 thử lại ở mục 1. Tổng chi vẫn 43,950,000. Owner: Founder quyết định trong 3 ngày.
8. **Mâu thuẫn target CPA / ROAS** — đề xuất đổi cpa_max từ 90,000 lên 190,000 VND (≥ AOV / roas_min = khoảng 192,500; AOV khoảng 385,000 từ SAMPLE). Owner: Founder, quyết định trong 7 ngày. Kiểm tra lại: số chiến dịch bị cờ CPA ở tuần sau.
9. **shopee_chat (phản ứng da, 1 báo cáo ngày 05/11)** — escalate Founder để theo dõi an toàn sản phẩm: xác định sản phẩm và lô liên quan, hướng dẫn khách ngưng dùng và gặp bác sĩ nếu cần, không đưa ra tư vấn y tế. Owner: Founder phối hợp CS, trong 2 ngày. Kiểm tra lại: skin_reaction_reports tuần sau và số báo cáo cùng sản phẩm.
10. **tiktok_shop_chat** — thêm 1 người trực cuối tuần (thứ Bảy, Chủ nhật) để đưa FRT dưới 15 phút. Owner: CS, trong 7 ngày. Kiểm tra lại: max FRT dưới 15 phút và CSAT ≥ 4.5.
11. **hotline** — rà soát ticket chưa giải quyết (86.7%) và đặt mục tiêu 90% trong 14 ngày. Owner: CS. Kiểm tra lại: resolution rate ≥ 90%.
12. **shopee_chat** — đạt CSAT ≥ 4.5 và resolution ≥ 90% (hiện 4.41 và 88.0%) bằng mẫu trả lời cho 5 câu hỏi thường gặp, trong 14 ngày. Owner: CS. Kiểm tra lại: CSAT và resolution tuần sau.
13. **facebook_inbox** — nâng resolution từ 89.8% lên 90%, theo dõi hằng ngày. Owner: CS, trong 7 ngày. Kiểm tra lại: resolution rate ≥ 90%.
14. **kem chống nắng nâng tone** — ngừng tối ưu từ khoá này (không khớp canon LB-SUN-01), chuyển công sức sang "kem chống nắng da dầu" (hạng 7, mục tiêu top 5). Owner: Marketing, trong 14 ngày. Kiểm tra lại: hạng và click của "kem chống nắng da dầu".
15. **son tint lâu trôi** — làm mới nội dung trang `/son` để lấy lại hạng 22 (hiện 31). Owner: Marketing, trong 14 ngày. Kiểm tra lại: vị trí tuần sau, mục tiêu ≤ 22.

## English summary
[SAMPLE data.] Total ad spend was 43.95M VND with ROAS 3.93, but 4 of 7 campaigns (74% of spend) are below ROAS 2.0; TT_Broad_LipTint (0.23) and GG_Search_Generic_Serum (0.58) are the worst. We propose pausing or cutting them and moving budget to SP_Search_Ads and FB_Retargeting_Combo, keeping the total unchanged and pending Founder approval. The CPA target (90k VND) conflicts with the ROAS target given an implied AOV of about 385k VND; we suggest about 190k. One skin-reaction report (shopee_chat, 05/11) is escalated to the Founder. CS resolution is under 90% on all channels and TikTok Shop first response breached 15 minutes on the weekend. SEO: do not chase "kem chống nắng nâng tone"; refresh the lip tint page.
