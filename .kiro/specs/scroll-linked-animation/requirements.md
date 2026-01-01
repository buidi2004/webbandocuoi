# Requirements Document

## Introduction

Tính năng Scroll-Linked Animation tạo hiệu ứng cuộn trang cao cấp giống Apple/Linear.app, với 4 section hiển thị văn bản bên trái và hình ảnh sticky bên phải. Hình ảnh sẽ thay đổi, trượt lên hoặc mờ dần khi người dùng cuộn trang, sử dụng Framer Motion và Tailwind CSS.

## Glossary

- **Scroll_Animation_Component**: Component React chính chứa toàn bộ hiệu ứng scroll-linked animation
- **Section**: Một phần nội dung gồm văn bản mô tả và hình ảnh tương ứng
- **Sticky_Image_Container**: Vùng chứa hình ảnh cố định (sticky) bên phải màn hình
- **Text_Content**: Phần văn bản mô tả bên trái của mỗi section
- **Scroll_Progress**: Giá trị tiến trình cuộn từ 0 đến 1 trong mỗi section
- **useScroll**: Hook của Framer Motion để theo dõi tiến trình cuộn
- **useTransform**: Hook của Framer Motion để chuyển đổi giá trị cuộn thành animation values

## Requirements

### Requirement 1: Cấu trúc Layout

**User Story:** As a user, I want to see a split-screen layout with text on the left and images on the right, so that I can read content while viewing related visuals.

#### Acceptance Criteria

1. THE Scroll_Animation_Component SHALL render 4 sections với layout 2 cột (text trái, image phải)
2. WHEN viewport width is less than 768px, THE Scroll_Animation_Component SHALL switch to single column layout với image trên, text dưới
3. THE Sticky_Image_Container SHALL remain fixed at viewport center-right WHILE user scrolls through text content
4. WHEN user scrolls past a section, THE Sticky_Image_Container SHALL transition to the next section's image

### Requirement 2: Scroll Progress Tracking

**User Story:** As a developer, I want to track scroll progress for each section, so that animations can be synchronized with user scrolling.

#### Acceptance Criteria

1. THE Scroll_Animation_Component SHALL use useScroll hook to track scroll progress for each section
2. WHEN a section enters viewport, THE Scroll_Progress SHALL start from 0
3. WHEN a section exits viewport, THE Scroll_Progress SHALL reach 1
4. THE Scroll_Animation_Component SHALL calculate individual progress for each of the 4 sections independently

### Requirement 3: Image Transition Effects

**User Story:** As a user, I want to see smooth image transitions when scrolling, so that the experience feels premium and engaging.

#### Acceptance Criteria

1. WHEN Scroll_Progress increases from 0 to 0.5, THE current image SHALL fade in from opacity 0 to 1
2. WHEN Scroll_Progress increases from 0.5 to 1, THE current image SHALL fade out from opacity 1 to 0
3. WHEN Scroll_Progress increases, THE current image SHALL translate upward (Y axis) creating slide-up effect
4. THE image transitions SHALL use easing function for smooth animation
5. WHEN transitioning between sections, THE Scroll_Animation_Component SHALL crossfade between images

### Requirement 4: Text Animation Effects

**User Story:** As a user, I want text content to animate as I scroll, so that the reading experience is dynamic and engaging.

#### Acceptance Criteria

1. WHEN a section's Scroll_Progress reaches 0.2, THE Text_Content SHALL begin fade-in animation
2. WHEN a section's Scroll_Progress reaches 0.8, THE Text_Content SHALL begin fade-out animation
3. THE Text_Content SHALL translate from Y offset 50px to 0px during fade-in
4. THE Text_Content SHALL translate from Y offset 0px to -50px during fade-out

### Requirement 5: Section Content Configuration

**User Story:** As a developer, I want to configure section content easily, so that I can customize the component for different use cases.

#### Acceptance Criteria

1. THE Scroll_Animation_Component SHALL accept an array of section data as props
2. WHEN section data is provided, THE component SHALL render title, description, and image for each section
3. THE Scroll_Animation_Component SHALL use images from ThuVien page (wedding/studio photos)
4. IF section data is not provided, THE component SHALL use default 4 sections with placeholder content

### Requirement 6: Performance Optimization

**User Story:** As a user, I want smooth animations without lag, so that the scrolling experience is pleasant.

#### Acceptance Criteria

1. THE Scroll_Animation_Component SHALL use CSS transform and opacity for animations (GPU accelerated)
2. THE Scroll_Animation_Component SHALL implement will-change CSS property for animated elements
3. WHEN images are loaded, THE component SHALL use lazy loading for off-screen images
4. THE animation calculations SHALL use requestAnimationFrame through Framer Motion

### Requirement 7: Visual Design

**User Story:** As a user, I want the component to have a premium, modern aesthetic, so that it matches the IVIE Studio brand.

#### Acceptance Criteria

1. THE Scroll_Animation_Component SHALL use Tailwind CSS for styling
2. THE component SHALL use IVIE brand colors (#b59410 gold, #2c2c2c dark, #f8f6f3 light)
3. THE images SHALL have rounded corners (rounded-2xl) and subtle shadow
4. THE text content SHALL use Be Vietnam Pro font family for Vietnamese support
5. THE component SHALL include subtle background gradients matching IVIE aesthetic
