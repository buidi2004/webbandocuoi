# Implementation Plan: Gallery Optimization

## Overview

Thay thế phần Gallery cũ trong ThuVien.jsx bằng hệ thống mới với Masonry Grid, Lightbox, lazy loading và hiệu ứng visual. Dựa trên phân tích code hiện tại:
- `LazyImage.jsx` đã có sẵn với Intersection Observer và skeleton
- `BoSuuTapGach.jsx` có masonry nhưng thiếu responsive 3/2/1 columns và gap 20px
- Lightbox hiện tại thiếu navigation và keyboard support
- Cần tạo mới PetalBackground và FloatingCTA

## Tasks

- [x] 1. Tạo GalleryImage component với lazy loading và hover effects
  - [x] 1.1 Tạo file `frontend/src/thanh_phan/GalleryImage.jsx`
    - Sử dụng Intersection Observer (threshold 0.1, rootMargin 100px)
    - Skeleton placeholder với animation khi loading
    - Fade-in animation (opacity 0→1, 500ms) khi load xong
    - Hover effects: scale(1.05), box-shadow (0 10px 30px rgba(0,0,0,0.15)), transition 300ms
    - Không gây layout shift khi hover
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5_
  - [x] 1.2 Tạo file `frontend/src/thanh_phan/GalleryImage.css`
    - Skeleton animation styles
    - Hover transition styles
    - Fade-in animation
    - _Requirements: 2.1, 2.2, 2.3, 3.3, 3.4_

- [x] 2. Tạo MasonryGrid component với responsive columns
  - [x] 2.1 Tạo file `frontend/src/thanh_phan/MasonryGrid.jsx`
    - CSS columns: 3 cột (≥1024px), 2 cột (768-1023px), 1 cột (<768px)
    - Gap 20px giữa các items
    - break-inside-avoid cho mỗi item
    - Render GalleryImage components
    - onImageClick callback để mở lightbox
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [x] 2.2 Tạo file `frontend/src/thanh_phan/MasonryGrid.css`
    - Responsive column-count với media queries
    - Gap và spacing styles
    - _Requirements: 1.1, 1.2, 1.5_

- [x] 3. Tạo GalleryLightbox component với navigation đầy đủ
  - [x] 3.1 Tạo file `frontend/src/thanh_phan/GalleryLightbox.jsx`
    - React Portal để render ngoài DOM hierarchy
    - Full-screen overlay (background rgba(0,0,0,0.95))
    - Close button (X icon) góc trên phải
    - Prev/Next arrow buttons với wrap-around
    - Keyboard: Escape đóng, Left/Right arrows navigate
    - Click overlay đóng lightbox
    - Index display format "(I+1) / N"
    - Touch-friendly buttons (min 44px)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 8.3_
  - [x] 3.2 Tạo file `frontend/src/thanh_phan/GalleryLightbox.css`
    - Overlay và positioning styles
    - Navigation button styles (44px min size)
    - Transition animations
    - _Requirements: 4.2, 4.3, 4.4, 8.3_

- [x] 4. Tạo PetalBackground component với canvas animation
  - [x] 4.1 Tạo file `frontend/src/thanh_phan/PetalBackground.jsx`
    - Canvas-based rendering
    - 15-25 petals floating với swaying motion
    - Petal size: 10-25px, opacity: 0.3-0.7
    - requestAnimationFrame loop cho 60fps
    - Visibility API: pause khi tab hidden
    - Object pooling để minimize garbage collection
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 9.4_
  - [x] 4.2 Tạo file `frontend/src/thanh_phan/PetalBackground.css`
    - Canvas positioning (absolute, full size)
    - z-index để nằm dưới content
    - _Requirements: 6.1_

- [x] 5. Tạo GalleryFloatingCTA component
  - [x] 5.1 Tạo file `frontend/src/thanh_phan/GalleryFloatingCTA.jsx`
    - Fixed position: right 20px, bottom 20px
    - "Đặt Lịch" text với calendar icon
    - Background Gold (#D4AF37), text white
    - Hover: scale(1.1), shadow enhancement
    - Link to /lien-he
    - z-index cao để luôn hiển thị
    - Responsive: center-bottom trên mobile (<768px)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.4_
  - [x] 5.2 Tạo file `frontend/src/thanh_phan/GalleryFloatingCTA.css`
    - Fixed positioning styles
    - Hover transition effects
    - Mobile responsive positioning
    - _Requirements: 7.1, 7.3, 7.4, 8.4_

- [x] 6. Cập nhật ThuVien.jsx với GallerySection mới
  - [x] 6.1 Thay thế BoSuuTapGach bằng MasonryGrid + GalleryLightbox
    - Import các component mới
    - State management cho lightbox (isOpen, currentIndex)
    - Truyền images data và callbacks
    - _Requirements: 1.1, 4.1_
  - [x] 6.2 Thêm PetalBackground vào gallery section
    - Đặt làm background layer
    - _Requirements: 6.1_
  - [x] 6.3 Thêm GalleryFloatingCTA
    - Render ở cuối page
    - _Requirements: 7.1_
  - [x] 6.4 Cập nhật typography và colors
    - Heading: 'Playfair Display' serif
    - Body: 'Montserrat' sans-serif
    - Accent: Gold #D4AF37
    - Text: Charcoal #333333
    - Background: White #FFFFFF
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 7. Performance optimization
  - [x] 7.1 Thêm will-change hints cho animated elements
    - GalleryImage hover
    - Lightbox transitions
    - _Requirements: 9.3_
  - [x] 7.2 Debounce resize events (150ms)
    - MasonryGrid recalculation
    - PetalBackground canvas resize
    - _Requirements: 9.5_
  - [x] 7.3 Touch device detection
    - Disable hover effects trên touch devices
    - Use tap interactions thay thế
    - _Requirements: 8.5, 9.2_

- [x] 8. Checkpoint - Test thủ công
  - Kiểm tra responsive layout (320px → 2560px)
  - Test lightbox: open, close, navigate, keyboard
  - Test lazy loading và fade-in
  - Test petal animation pause khi tab hidden
  - Test floating CTA responsive
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Sử dụng Tailwind CSS kết hợp với CSS files riêng
- Không dùng jQuery hoặc thư viện nặng
- Đảm bảo responsive từ 320px đến 2560px
- CSS transforms cho animations (không dùng layout-triggering properties)
- Target LCP < 2.5s
