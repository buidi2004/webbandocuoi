# Requirements Document

## Introduction

Refactor và tối ưu phần "Gallery" của trang Thư Viện IVIE STUDIO để cải thiện User Experience (UX) và Visual Appeal. Thay thế phần Gallery cũ bằng một hệ thống mới với Masonry Grid layout, hiệu ứng tương tác mượt mà, Lightbox viewer, và các tối ưu về performance.

## Glossary

- **Gallery_System**: Hệ thống hiển thị ảnh mới thay thế phần Gallery cũ trong trang ThuVien.jsx
- **Masonry_Grid**: Component layout hiển thị ảnh theo dạng lưới Pinterest-style với các cột có chiều cao khác nhau
- **Lightbox**: Modal full-screen để xem ảnh chi tiết với navigation
- **Lazy_Image**: Component ảnh với lazy loading sử dụng Intersection Observer API
- **Floating_CTA**: Nút "Đặt Lịch" cố định ở góc phải dưới màn hình
- **Petal_Animation**: Hiệu ứng cánh hoa rơi nền sử dụng Canvas/SVG

## Requirements

### Requirement 1: Masonry Grid Layout

**User Story:** As a visitor, I want to view gallery images in a Pinterest-style masonry grid, so that I can browse photos efficiently without dead space.

#### Acceptance Criteria

1. THE Masonry_Grid SHALL display images in 3 columns on Desktop (≥1024px), 2 columns on Tablet (768px-1023px), and 1 column on Mobile (<768px)
2. THE Masonry_Grid SHALL maintain consistent gap of 20px between all items
3. THE Masonry_Grid SHALL automatically calculate and position images based on their natural aspect ratios
4. WHEN images are loaded, THE Masonry_Grid SHALL recalculate layout to prevent overlapping
5. THE Masonry_Grid SHALL use CSS columns or CSS Grid with masonry behavior for optimal performance

### Requirement 2: Image Hover Effects

**User Story:** As a visitor, I want visual feedback when hovering over images, so that I know they are interactive.

#### Acceptance Criteria

1. WHEN user hovers over an image, THE Gallery_System SHALL apply scale(1.05) transform with 300ms ease transition
2. WHEN user hovers over an image, THE Gallery_System SHALL apply soft box-shadow (0 10px 30px rgba(0,0,0,0.15))
3. WHEN user stops hovering, THE Gallery_System SHALL smoothly return to original state with 300ms transition
4. THE hover effects SHALL NOT cause layout shift or affect neighboring images

### Requirement 3: Lazy Loading with Fade-in Animation

**User Story:** As a visitor, I want images to load smoothly as I scroll, so that the page feels fast and responsive.

#### Acceptance Criteria

1. THE Lazy_Image SHALL use Intersection Observer API to detect when image enters viewport
2. WHEN image enters viewport (threshold 0.1), THE Lazy_Image SHALL start loading the image
3. WHEN image finishes loading, THE Lazy_Image SHALL fade in with opacity transition from 0 to 1 over 500ms
4. WHILE image is loading, THE Lazy_Image SHALL display a placeholder with skeleton animation
5. THE Lazy_Image SHALL use rootMargin of 100px to preload images slightly before they enter viewport

### Requirement 4: Lightbox Viewer

**User Story:** As a visitor, I want to view images in full-screen mode with navigation, so that I can see photo details clearly.

#### Acceptance Criteria

1. WHEN user clicks on a gallery image, THE Lightbox SHALL open with full-screen overlay (background rgba(0,0,0,0.95))
2. THE Lightbox SHALL display the clicked image centered and scaled to fit viewport with padding
3. THE Lightbox SHALL include a Close button (X icon) positioned at top-right corner
4. THE Lightbox SHALL include Previous/Next arrow buttons for navigation between images
5. WHEN user presses Escape key, THE Lightbox SHALL close
6. WHEN user clicks outside the image area, THE Lightbox SHALL close
7. WHEN user presses Left/Right arrow keys, THE Lightbox SHALL navigate to previous/next image
8. THE Lightbox SHALL display current image index (e.g., "3 / 15")

### Requirement 5: Visual Style - Typography and Colors

**User Story:** As a visitor, I want the gallery to have an elegant, sophisticated visual style, so that it matches the premium brand identity.

#### Acceptance Criteria

1. THE Gallery_System SHALL use 'Playfair Display' serif font for headings
2. THE Gallery_System SHALL use 'Montserrat' sans-serif font for body text
3. THE Gallery_System SHALL use Gold (#D4AF37) for accent colors on icons and interactive elements
4. THE Gallery_System SHALL use Charcoal (#333333) for primary text color
5. THE Gallery_System SHALL maintain white (#FFFFFF) background

### Requirement 6: Petal Animation Background

**User Story:** As a visitor, I want to see subtle floating petal animations, so that the gallery feels elegant and alive.

#### Acceptance Criteria

1. THE Petal_Animation SHALL render floating petal particles using Canvas or SVG
2. THE Petal_Animation SHALL display 15-25 petals at any given time
3. THE petals SHALL float downward with gentle swaying motion
4. THE petals SHALL have varying sizes (10px-25px) and opacity (0.3-0.7)
5. THE Petal_Animation SHALL use requestAnimationFrame for smooth 60fps animation
6. THE Petal_Animation SHALL pause when tab is not visible to save resources

### Requirement 7: Floating CTA Button

**User Story:** As a visitor, I want easy access to booking, so that I can quickly schedule a photo session.

#### Acceptance Criteria

1. THE Floating_CTA SHALL be positioned fixed at bottom-right corner (right: 20px, bottom: 20px)
2. THE Floating_CTA SHALL display "Đặt Lịch" text with calendar icon
3. THE Floating_CTA SHALL use Gold (#D4AF37) background with white text
4. WHEN user hovers over Floating_CTA, THE button SHALL scale to 1.1 with shadow enhancement
5. WHEN user clicks Floating_CTA, THE system SHALL navigate to /lien-he page
6. THE Floating_CTA SHALL have z-index high enough to stay above all content

### Requirement 8: Responsive Design

**User Story:** As a visitor on any device, I want the gallery to work perfectly, so that I have a great experience regardless of screen size.

#### Acceptance Criteria

1. THE Gallery_System SHALL be fully functional on screens from 320px to 2560px width
2. THE Gallery_System SHALL adjust font sizes using clamp() for fluid typography
3. THE Lightbox navigation buttons SHALL be touch-friendly (min 44px tap target) on mobile
4. THE Floating_CTA SHALL reposition to center-bottom on mobile screens (<768px)
5. IF device is touch-enabled, THEN THE Gallery_System SHALL disable hover effects and use tap interactions

### Requirement 9: Performance Optimization

**User Story:** As a visitor, I want the gallery to load and perform quickly, so that I don't experience lag or delays.

#### Acceptance Criteria

1. THE Gallery_System SHALL achieve Largest Contentful Paint (LCP) under 2.5 seconds
2. THE Gallery_System SHALL use CSS transforms for animations (no layout-triggering properties)
3. THE Gallery_System SHALL implement will-change hints for animated elements
4. THE Petal_Animation SHALL use object pooling to minimize garbage collection
5. THE Gallery_System SHALL debounce resize events with 150ms delay
