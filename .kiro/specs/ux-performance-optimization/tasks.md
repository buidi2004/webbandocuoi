# Implementation Plan: UX & Performance Optimization

## Overview

Triển khai các cải tiến UX và Performance cho IVIE Wedding Studio: Lazy Loading, Sticky CTA, Thank You Page, GA4 Tracking.

## Tasks

- [x] 1. Tạo LazyImage Component
  - [x] 1.1 Tạo component LazyImage.jsx với Intersection Observer
    - Tạo file `frontend/src/thanh_phan/LazyImage.jsx`
    - Implement Intersection Observer với rootMargin 200px
    - Hiển thị placeholder blur/skeleton khi chưa load
    - Fade-in animation khi ảnh load xong
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [x] 1.2 Tạo CSS cho LazyImage
    - Tạo file `frontend/src/thanh_phan/LazyImage.css`
    - Style placeholder, fade-in animation
    - _Requirements: 1.3, 1.4_

  - [x] 1.3 Áp dụng LazyImage vào các trang chính
    - Update TrangChu.jsx, SanPham.jsx, ThuVien.jsx
    - Replace img tags với LazyImage component
    - _Requirements: 1.1_

- [x] 2. Tạo Sticky CTA Component
  - [x] 2.1 Tạo component StickyCTA.jsx
    - Tạo file `frontend/src/thanh_phan/StickyCTA.jsx`
    - Nút Zalo với link OA
    - Nút Gọi điện với tel: link
    - Hover expand effect trên desktop
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 2.2 Tạo CSS responsive cho StickyCTA
    - Tạo file `frontend/src/thanh_phan/StickyCTA.css`
    - Desktop: góc phải, expanded on hover
    - Mobile: compact, không che form buttons
    - _Requirements: 2.4, 2.5, 5.1, 5.2, 5.3_

  - [x] 2.3 Tích hợp StickyCTA vào App
    - Add StickyCTA vào UngDung.jsx
    - Đảm bảo z-index không conflict với StickyBottomBar
    - _Requirements: 2.1_

- [x] 3. Tạo Thank You Page
  - [x] 3.1 Tạo component CamOn.jsx (Thank You Page)
    - Tạo file `frontend/src/trang/CamOn.jsx`
    - Hiển thị thông điệp cảm ơn
    - Thời gian phản hồi dự kiến (24h)
    - Nút quay lại trang chủ, xem sản phẩm
    - _Requirements: 3.1, 3.2, 3.3_

  - [x] 3.2 Tạo CSS cho Thank You Page
    - Tạo file `frontend/src/styles/thank-you.css`
    - Design đẹp, professional
    - _Requirements: 3.2_

  - [x] 3.3 Thêm route /cam-on
    - Update UngDung.jsx với route mới
    - _Requirements: 3.4_

  - [x] 3.4 Update form liên hệ để redirect
    - Update LienHe.jsx để navigate đến /cam-on sau khi submit
    - Pass form type qua state
    - _Requirements: 3.1_

- [x] 4. Tích hợp Google Analytics 4
  - [x] 4.1 Tạo GA4 tracking service
    - Tạo file `frontend/src/utils/analytics.js`
    - Functions: trackPageView, trackViewItem, trackAddToCart, trackGenerateLead, trackConversion
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 4.2 Thêm GA4 script vào index.html
    - Thêm gtag.js script (placeholder ID, user sẽ thay)
    - _Requirements: 4.1_

  - [x] 4.3 Tích hợp tracking vào các trang
    - ProductDetail: trackViewItem khi load
    - GioHang: trackAddToCart khi thêm
    - LienHe: trackGenerateLead khi submit
    - CamOn: trackConversion khi load
    - _Requirements: 4.2, 4.3, 4.4, 4.5_

- [x] 5. Cải thiện SEO Hình ảnh
  - [x] 5.1 Update alt text cho ảnh sản phẩm
    - Update ProductDetail.jsx với alt text format: `{tên-sản-phẩm}-ivie-wedding`
    - Update SanPham.jsx product cards
    - _Requirements: 6.1, 6.2_

  - [x] 5.2 Thêm JSON-LD structured data
    - Thêm Product schema vào ProductDetail.jsx
    - Include name, image, price, availability
    - _Requirements: 6.3_

- [x] 6. Checkpoint - Review và Test
  - Kiểm tra lazy loading hoạt động
  - Kiểm tra Sticky CTA không che elements
  - Kiểm tra Thank You page redirect
  - Kiểm tra GA4 events trong console
  - Hỏi user nếu có thắc mắc

## Notes

- GA4 Measurement ID cần được user cung cấp (format: G-XXXXXXXXXX)
- Zalo OA link và số hotline cần được user cung cấp
- Lazy loading sử dụng native Intersection Observer (không cần thư viện)
- Tasks tập trung vào code changes, không bao gồm image optimization (cần tool riêng)

