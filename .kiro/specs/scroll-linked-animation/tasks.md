# Implementation Plan: Scroll-Linked Animation

## Overview

Triển khai component `HieuUngCuonDinh` với Framer Motion và Tailwind CSS, tạo hiệu ứng scroll-linked animation giống Apple/Linear.app.

## Tasks

- [x] 1. Tạo cấu trúc component cơ bản
  - [x] 1.1 Tạo file `frontend/src/thanh_phan/HieuUngCuonDinh.jsx`
    - Định nghĩa interface SectionData
    - Tạo default sections data với nội dung IVIE
    - Setup refs cho container và sections
    - _Requirements: 5.1, 5.4_

  - [x] 1.2 Implement layout 2 cột với Tailwind CSS
    - Grid layout: text trái (40%), image phải (60%)
    - Sticky positioning cho image container
    - Height 100vh cho mỗi section
    - _Requirements: 1.1, 1.3_

- [x] 2. Implement scroll tracking với Framer Motion
  - [x] 2.1 Setup useScroll hook cho container
    - Track scrollYProgress cho toàn bộ container
    - Offset configuration ["start start", "end end"]
    - _Requirements: 2.1, 2.4_

  - [x] 2.2 Tính toán progress cho từng section
    - Chia scrollYProgress thành 4 phần cho 4 sections
    - Mỗi section có progress riêng từ 0-1
    - _Requirements: 2.2, 2.3, 2.4_

  - [ ]* 2.3 Write property test cho scroll progress boundaries
    - **Property 1: Scroll Progress Boundaries**
    - **Validates: Requirements 2.2, 2.3**

- [x] 3. Implement image animations
  - [x] 3.1 Tạo StickyImageStack component
    - Stack 4 images với position absolute
    - Z-index management cho active image
    - _Requirements: 1.4_

  - [x] 3.2 Implement opacity transformation với useTransform
    - Fade in: progress 0-0.5 → opacity 0-1
    - Fade out: progress 0.5-1 → opacity 1-0
    - _Requirements: 3.1, 3.2_

  - [x] 3.3 Implement Y translation animation
    - Transform Y từ 0 đến -100px theo progress
    - Easing function cho smooth animation
    - _Requirements: 3.3, 3.4_

  - [ ]* 3.4 Write property test cho image opacity transformation
    - **Property 2: Image Opacity Transformation**
    - **Validates: Requirements 3.1, 3.2**

  - [ ]* 3.5 Write property test cho image Y translation
    - **Property 3: Image Y Translation**
    - **Validates: Requirements 3.3**

- [x] 4. Implement text animations
  - [x] 4.1 Tạo SectionText component
    - Render title, description, highlight
    - Apply motion.div với animated styles
    - _Requirements: 5.2_

  - [x] 4.2 Implement text opacity và Y transformation
    - Opacity: [0, 0.2] → 0, [0.2, 0.8] → 1, [0.8, 1] → 0
    - Y: 50px → 0px → -50px theo progress
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ]* 4.3 Write property test cho text Y transformation
    - **Property 4: Text Y Transformation**
    - **Validates: Requirements 4.3, 4.4**

- [x] 5. Implement crossfade và section transitions
  - [x] 5.1 Implement crossfade giữa các images
    - Overlap opacity khi chuyển section
    - Smooth transition với easing
    - _Requirements: 3.5_

  - [ ]* 5.2 Write property test cho section image transition
    - **Property 7: Section Image Transition**
    - **Validates: Requirements 1.4, 3.5**

- [x] 6. Checkpoint - Kiểm tra animations cơ bản
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Implement responsive design
  - [x] 7.1 Add responsive breakpoints
    - Mobile (<768px): single column, image trên text dưới
    - Tablet (768-1024px): 50/50 split
    - Desktop (>1024px): 40/60 split
    - _Requirements: 1.2_

  - [ ]* 7.2 Write property test cho responsive layout
    - **Property 6: Responsive Layout Switch**
    - **Validates: Requirements 1.2**

- [x] 8. Performance optimization
  - [x] 8.1 Add will-change CSS property
    - Apply will-change: transform, opacity cho animated elements
    - _Requirements: 6.2_

  - [x] 8.2 Implement lazy loading cho images
    - Add loading="lazy" attribute
    - Placeholder gradient khi loading
    - _Requirements: 6.3_

  - [x] 8.3 Ensure GPU-accelerated animations
    - Use transform và opacity only
    - Avoid layout-triggering properties
    - _Requirements: 6.1_

- [x] 9. Visual styling và branding
  - [x] 9.1 Apply IVIE brand colors
    - Gold: #b59410, Dark: #2c2c2c, Light: #f8f6f3
    - Background gradients
    - _Requirements: 7.2, 7.5_

  - [x] 9.2 Style images và text
    - Images: rounded-2xl, shadow-2xl
    - Text: Be Vietnam Pro font
    - _Requirements: 7.3, 7.4_

- [x] 10. Tích hợp với ThuVien images
  - [x] 10.1 Fetch images từ ThuVien API
    - Sử dụng thuVienAPI.layTatCa()
    - Fallback to placeholder nếu API fail
    - _Requirements: 5.3_

  - [ ]* 10.2 Write property test cho section data rendering
    - **Property 5: Section Data Rendering**
    - **Validates: Requirements 5.2**

- [x] 11. Final checkpoint
  - Ensure all tests pass, ask the user if questions arise.
  - Test trên các viewport sizes khác nhau
  - Verify smooth animations trên mobile

## Notes

- Tasks marked with `*` are optional property-based tests
- Component sử dụng Framer Motion hooks: useScroll, useTransform
- Tailwind CSS cho styling, không cần file CSS riêng
- Images từ ThuVien page hoặc placeholder nếu chưa có data
