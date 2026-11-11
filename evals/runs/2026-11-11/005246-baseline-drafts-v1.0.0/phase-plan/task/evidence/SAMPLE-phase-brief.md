# [SAMPLE] Brief giai đoạn Q1/2027 — "Scale-up sau ra mắt"

> SAMPLE: synthetic input written during the repo build (founder chose labeled samples at intake).
> Replace with the real brief; numbers below are illustrative, not LunoBeau's actual data.

## Bối cảnh
- LunoBeau đã bán được 5 tháng, 4 SKU (xem `canon/company.md`). Doanh thu hiện chủ yếu từ Shopee và đơn inbox Facebook.
- Mục tiêu giai đoạn 01/2027–03/2027: tăng doanh thu và mở rộng kênh, giữ chi phí trên mỗi đơn trong ngưỡng.

## Mục tiêu
- Doanh thu: 1,200,000,000 VND trong 3 tháng.
- Đơn hàng: 4,000 đơn.
- Xây tệp khách hàng quay lại: tỷ lệ mua lại ≥ 18%.

## Yêu cầu
Lập kế hoạch giai đoạn: kênh bán hàng, khu vực trọng điểm, khách hàng mục tiêu, phân bổ ngân sách theo kênh và theo tháng, chiến lược từng kênh, KPI, lịch triển khai, rủi ro.

## Tham số (dùng cho script phân bổ)
```yaml
phase: Q1-2027
months: ["2027-01", "2027-02", "2027-03"]
month_weights: [0.30, 0.33, 0.37]     # ramp-up
total_budget_vnd: 300000000
reserve_pct: 0.10                     # quỹ dự phòng / test
channels:
  # benchmark từ quý trước (SAMPLE): cpa = chi phí/đơn, roas = doanh thu/chi phí
  facebook_ads:   {cpa: 78000,  roas: 3.1, weight: 1.0, min_share: 0.20, max_share: 0.40}
  tiktok_ads:     {cpa: 65000,  roas: 3.6, weight: 1.1, min_share: 0.15, max_share: 0.35}
  google_ads:     {cpa: 95000,  roas: 2.6, weight: 0.9, min_share: 0.10, max_share: 0.25}
  shopee_ads:     {cpa: 52000,  roas: 4.2, weight: 1.0, min_share: 0.10, max_share: 0.30}
  koc_affiliate:  {cpa: 70000,  roas: 3.3, weight: 0.8, min_share: 0.05, max_share: 0.15}
regions:
  ho_chi_minh: {share_of_orders_last_q: 0.46}
  ha_noi:      {share_of_orders_last_q: 0.31}
  da_nang:     {share_of_orders_last_q: 0.07}
  can_tho:     {share_of_orders_last_q: 0.04}
  other:       {share_of_orders_last_q: 0.12}
audiences_last_q:
  nu_18_24_sinh_vien:     {share: 0.38, aov_vnd: 265000}
  nu_25_34_van_phong:     {share: 0.44, aov_vnd: 340000}
  nu_35_44:               {share: 0.12, aov_vnd: 390000}
  nam_18_34:              {share: 0.06, aov_vnd: 240000}
```
