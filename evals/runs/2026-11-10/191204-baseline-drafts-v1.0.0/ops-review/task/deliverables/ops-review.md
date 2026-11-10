# Đánh giá vận hành tuần 03–09/11/2026 (ads, SEO, CSKH)

> Dữ liệu **SAMPLE** (synthetic export, `inputs/SAMPLE-ops-export/`). Mọi số liệu lấy từ `evidence/kpis.json` (tính bằng script `compute_kpis.py`); nguyên nhân chưa kiểm chứng được ghi là *giả thuyết*.

## Tóm tắt
- Tổng chi quảng cáo 43,950,000 VND, doanh thu 172,887,000 VND, ROAS tổng 3.93, 449 đơn (CPA bình quân 97,884 VND).
- 3 chiến dịch hiệu quả cao (SP_Search_Ads ROAS 14.71, GG_Search_Brand 13.77, FB_Retargeting_Combo 8.4), còn 4 chiến dịch dưới ngưỡng ROAS 2.0, trong đó TT_Broad_LipTint (ROAS 0.23) và GG_Search_Generic_Serum (ROAS 0.58) lỗ rõ.
- SEO: 2 từ khóa tụt mạnh ("kem chống nắng nâng tone" 27→41, "son tint lâu trôi" 22→31); "serum niacinamide" tăng 14→9.
- CSKH: TikTok Shop chat có phản hồi đầu tiên vượt 15 phút vào 07–08/11 (max 31.8 phút); tỷ lệ giải quyết của cả 4 kênh dưới 90%; **1 báo cáo kích ứng da trên Shopee (05/11)**.
- Mục tiêu CPA ≤ 90,000 VND mâu thuẫn với mục tiêu ROAS ≥ 2.0 ở AOV hiện tại (~385,000 VND): cần Founder chốt lại (xem Đề xuất 11).

## Quảng cáo

| campaign | platform | spend (VND) | conv | revenue (VND) | CTR | CPA | ROAS | chẩn đoán |
|---|---|---|---|---|---|---|---|---|
| TT_Broad_LipTint | tiktok | 6,440,000 | 8 | 1,479,000 | 0.60% | 805,000 | 0.23 | CTR thấp → creative/target rộng không hợp (giả thuyết) |
| GG_Search_Generic_Serum | google | 5,475,000 | 7 | 3,167,000 | 2.10% | 782,142 | 0.58 | CTR ổn nhưng CVR ~1% → landing page/ý định từ khóa (giả thuyết) |
| FB_Prospecting_Serum | facebook | 10,308,000 | 41 | 17,339,000 | 1.06% | 251,414 | 1.68 | sát ngưỡng; creative mỏi (giả thuyết) |
| TT_Spark_KOC_Sunscreen | tiktok | 10,466,000 | 61 | 18,799,000 | 1.40% | 171,573 | 1.8 | AOV thấp (~308,000) kéo ROAS |
| FB_Retargeting_Combo | facebook | 5,011,000 | 75 | 42,076,000 | 1.84% | 66,813 | 8.4 | tốt |
| GG_Search_Brand | google | 2,037,000 | 70 | 28,058,000 | 8.50% | 29,100 | 13.77 | tốt, bị giới hạn bởi nhu cầu thương hiệu |
| SP_Search_Ads | shopee | 4,213,000 | 187 | 61,969,000 | 3.38% | 22,529 | 14.71 | hiệu quả cao nhất trong tuần |

Bảng đầy đủ (CPC, cờ): `evidence/kpis.md`.

## SEO

| keyword | tuần trước | tuần này | thay đổi | clicks |
|---|---|---|---|---|
| kem chống nắng nâng tone | 27 | 41 | -14 | 2 |
| son tint lâu trôi | 22 | 31 | -9 | 13 |
| serum niacinamide | 14 | 9 | +5 | 19 |
| serum cấp ẩm cho da khô | 19 | 13 | +6 | 49 |

Lưu ý: Daily Light Sunscreen không được mô tả là "nâng tone" trong `canon/company.md`. Nhắm từ khóa này có thể gây kỳ vọng sai, nên cân nhắc bỏ thay vì cố kéo hạng.

## CSKH

| channel | tickets | giải quyết | FRT trung vị (phút) | FRT max | CSAT | báo kích ứng |
|---|---|---|---|---|---|---|
| tiktok_shop_chat | 206 | 88.3% | 9.1 | 31.8 | 4.41 | 0 |
| shopee_chat | 158 | 88.0% | 7.8 | 11.2 | 4.41 | 1 |
| facebook_inbox | 176 | 89.8% | 8.9 | 11.7 | 4.58 | 0 |
| hotline | 128 | 86.7% | 10.7 | 12.4 | 4.51 | 0 |

CSAT dưới ngưỡng 4.5 ở tiktok_shop_chat và shopee_chat (cùng 4.41). Ca kích ứng da (Shopee, 05/11) phải được báo Founder theo quy trình. Báo cáo này không chứa thông tin cá nhân khách hàng; chi tiết ca nằm ở `data/cs/private/`.

## Đề xuất
1. TT_Broad_LipTint: Marketing **tạm dừng** chiến dịch (tiết kiệm ~6,440,000 VND/tuần); thử lại sau 14 ngày với 2 creative mới và target nữ 18–24, ngân sách test 1,500,000 VND, dừng nếu CTR < 0.8% sau 3 ngày.
2. GG_Search_Generic_Serum: Marketing giảm 50% ngân sách (còn ~2,700,000 VND/tuần), thêm từ khóa phủ định, A/B test landing page serum; kiểm tra lại CVR sau 7 ngày (mục tiêu ≥ 2.5%).
3. FB_Prospecting_Serum: Marketing giữ ngân sách, thay 3 creative mới và thu hẹp nữ 25–34; kiểm tra lại ROAS sau 7 ngày (mục tiêu ≥ 2.0).
4. TT_Spark_KOC_Sunscreen: Marketing thêm ưu đãi combo Sunscreen + Cleanser để nâng AOV lên ≥ 380,000 VND; kiểm tra lại ROAS sau 7 ngày (mục tiêu ≥ 2.2).
5. Phân bổ lại ngân sách tiết kiệm từ (1)+(2) (~9,200,000 VND/tuần): Marketing đề xuất +3,500,000 cho SP_Search_Ads, +2,500,000 cho FB_Retargeting_Combo, +1,000,000 cho GG_Search_Brand, 2,200,000 giữ dự phòng; **Founder duyệt trước khi thay đổi** (tổng chi không tăng).
6. kem chống nắng nâng tone: Marketing ngừng tối ưu từ khóa này trong 30 ngày (sai lệch với mô tả sản phẩm), chuyển nội dung sang "kem chống nắng da dầu" (đang hạng 7).
7. son tint lâu trôi: Marketing cập nhật trang /son (thêm 6 bảng màu, review đã kiểm duyệt, internal link từ 2 bài blog); kiểm tra lại hạng sau 14 ngày (mục tiêu ≤ 20).
8. tiktok_shop_chat: CS bổ sung 1 ca trực cuối tuần 8:00–22:00; mục tiêu FRT max ≤ 15 phút, kiểm tra lại sau 7 ngày.
9. shopee_chat: CS báo Founder ca kích ứng da ngày 05/11 trong hôm nay (xin ảnh, mã đơn, lô sản xuất); Founder liên hệ nhà sản xuất nếu có ≥ 2 ca cùng lô trong 30 ngày.
10. facebook_inbox, hotline, shopee_chat, tiktok_shop_chat: CS rà soát toàn bộ ticket chưa giải quyết (tỷ lệ 86.7–89.8%), phân loại nguyên nhân; mục tiêu ≥ 90% sau 7 ngày.
11. Mục tiêu: Founder xác nhận lại CPA tối đa. Ở ROAS 2.0 và AOV ~385,000 VND, CPA hòa vốn mục tiêu ≈ 192,000 VND, nên ngưỡng 90,000 VND đang gắn cờ cả các chiến dịch đạt ROAS. Cần chốt trong 3 ngày.

## English summary
SAMPLE data, week 3–9 Nov 2026. Spend 43.95M VND, revenue 172.9M VND, blended ROAS 3.93. Shopee search, Google brand and Facebook retargeting carry the account. TT_Broad_LipTint (ROAS 0.23) and GG_Search_Generic_Serum (0.58) should be paused or halved, freeing ~9.2M VND/week for the winners, subject to Founder approval. Two SEO keywords dropped; one ("tone-up sunscreen") doesn't match the product claim and should be dropped. CS: TikTok Shop weekend response times breach the 15-minute SLA, all channels resolve under 90%, and one Shopee skin-reaction report must be escalated to the Founder today. The CPA target (90k VND) is inconsistent with the ROAS target (2.0) at the current AOV, so the Founder should reset it.
