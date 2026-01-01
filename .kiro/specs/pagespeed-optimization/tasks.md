# Implementation Plan: PageSpeed Optimization

## Overview

Implement PageSpeed optimizations cho IVIE Wedding Studio với focus vào TTFB và bundle size.

## Tasks

- [x] 1. FastAPI Backend Optimization
  - [x] 1.1 Thêm GZipMiddleware vào FastAPI
    - Import và add GZipMiddleware với minimum_size=500
    - Đặt trước CORSMiddleware trong middleware stack
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 1.2 Tạo cache_utils.py với cache decorator
    - Tạo file backend/ung_dung/cache_utils.py
    - Implement cache_response decorator
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [x] 1.3 Áp dụng cache headers cho API endpoints
    - Thêm Cache-Control header cho /api/san_pham/ (5 min)
    - Thêm Cache-Control header cho /api/banner/ (10 min)
    - Thêm Cache-Control header cho /api/thu_vien/, /api/blog/ (1 hour)
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 2. React Frontend Optimization
  - [x] 2.1 Review và tối ưu LazyImage component
    - Verify loading="lazy" và decoding="async"
    - Verify width/height/aspectRatio props
    - Thêm srcSet support nếu cần
    - _Requirements: 4.5, 4.6_

  - [x] 2.2 Review code splitting trong UngDung.jsx
    - Verify tất cả routes đã lazy load
    - Verify heavy components (3D, animations) lazy load riêng
    - _Requirements: 3.1, 3.3_

- [x] 3. Vite Build Optimization
  - [x] 3.1 Review và tối ưu vite.config.js
    - Verify terser minification với drop_console
    - Verify manual chunks configuration
    - Thêm cssCodeSplit nếu cần
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 4. TTFB Optimization
  - [x] 4.1 Review index.html cho critical CSS và font preload
    - Verify critical CSS inline
    - Verify font preload links
    - Verify loading placeholder
    - _Requirements: 6.2, 6.3, 6.4_

- [ ] 5. Checkpoint - Test và verify
  - Build production và kiểm tra chunk sizes
  - Test API với gzip và cache headers
  - Chạy Lighthouse audit

## Notes

- Các component LazyImage, UngDung.jsx, vite.config.js đã có sẵn - chỉ cần review và tối ưu
- Focus chính là backend (GZip + Cache) vì frontend đã được tối ưu trước đó
- Property tests marked với * là optional
