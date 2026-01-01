# Implementation Plan: Product Detail Optimization

## Overview

Triển khai tối ưu hóa trang chi tiết sản phẩm với ProductGallery (zoom + video), Related Products API, và BookingButton với pulse effect.

## Tasks

- [x] 1. Tạo ProductGallery Component với Zoom
  - [x] 1.1 Tạo component ProductGallery.jsx với state management
    - Tạo file `frontend/src/thanh_phan/ProductGallery.jsx`
    - Implement state: currentIndex, isZoomOpen, zoomLevel, panPosition
    - Render main image và thumbnails
    - _Requirements: 1.1, 1.5, 1.6_

  - [x] 1.2 Tạo ZoomModal component với pan/zoom functionality
    - Integrated trong ProductGallery.jsx
    - Implement drag-to-pan với mouse events
    - Implement scroll-to-zoom với wheel events
    - Constrain zoom level [1.0, 3.0] và pan position
    - _Requirements: 1.2, 1.3, 1.4_

  - [x] 1.3 Tạo CSS styles cho ProductGallery
    - Tạo file `frontend/src/thanh_phan/ProductGallery.css`
    - Style main image container, thumbnails, zoom modal
    - Responsive design cho mobile/desktop
    - _Requirements: 1.5_

- [x] 2. Thêm Video Support vào Gallery
  - [x] 2.1 Extend ProductGallery để hỗ trợ video
    - Detect video từ videoUrl prop
    - Render video thumbnail với play icon overlay
    - Switch giữa image và video display
    - _Requirements: 2.1, 2.2_

  - [x] 2.2 Implement video player controls
    - Sử dụng HTML5 video element với controls
    - Pause video khi switch sang media khác
    - Handle video load errors
    - _Requirements: 2.3, 2.4_

- [x] 3. Tạo Related Products API (Backend)
  - [x] 3.1 Thêm endpoint /pg/san-pham/{id}/lien-quan
    - Tạo route trong `backend/ung_dung/dinh_tuyen/api_pg.py`
    - Query products cùng danh_muc và gioi_tinh
    - Exclude current product từ results
    - Limit 8 products, sort by la_hot desc, id desc
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 3.2 Write property test cho Related Products API
    - **Property 4: Related Products Exclude Current**
    - **Property 5: Related Products Limit**
    - **Property 6: Related Products Sorting**
    - **Validates: Requirements 3.3, 3.4, 3.5**

- [x] 4. Tạo BookingButton với Pulse Effect
  - [x] 4.1 Tạo component BookingButton.jsx
    - Tạo file `frontend/src/thanh_phan/BookingButton.jsx`
    - Style với màu vàng đồng (#D4AF37)
    - Implement pulse animation CSS
    - Navigate to /lien-he on click
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 4.2 Tạo CSS với custom animation
    - Tạo file `frontend/src/thanh_phan/BookingButton.css`
    - Tạo pulse-gold keyframes animation
    - Hover scale effect (1.03x)
    - Responsive styling
    - _Requirements: 4.2, 4.3, 4.4, 4.6_

- [x] 5. Tạo RelatedProducts Component
  - [x] 5.1 Tạo component RelatedProducts.jsx
    - Tạo file `frontend/src/thanh_phan/RelatedProducts.jsx`
    - Fetch data từ API /pg/san-pham/{id}/lien-quan
    - Render product cards với image, name, price
    - Handle empty state (hide section)
    - _Requirements: 5.1, 5.5_

  - [x] 5.2 Style responsive layout
    - Tạo file `frontend/src/thanh_phan/RelatedProducts.css`
    - Mobile: horizontal scrollable carousel
    - Desktop: 4-column grid
    - Product card hover effects
    - _Requirements: 5.2, 5.3_

  - [x] 5.3 Implement navigation on product click
    - Navigate to /san-pham/{id} on card click
    - _Requirements: 5.4_

- [x] 6. Tích hợp vào ProductDetail Page
  - [x] 6.1 Update ProductDetail.jsx
    - Import ProductGallery, BookingButton, RelatedProducts
    - Add BookingButton vào product info section
    - Add RelatedProducts section cuối trang
    - _Requirements: 1.1, 4.5, 5.1_

  - [x] 6.2 Update API client
    - Thêm function laySanPhamLienQuan vào khach_hang.js
    - _Requirements: 5.1_

- [ ] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
