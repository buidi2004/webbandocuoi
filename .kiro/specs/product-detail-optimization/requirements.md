# Requirements Document

## Introduction

Tối ưu hóa trang chi tiết sản phẩm cho IVIE Wedding Studio với các tính năng: ProductGallery component có zoom ảnh và hỗ trợ video, API gợi ý sản phẩm liên quan, và nút "Đặt lịch thử váy" nổi bật với hiệu ứng pulse.

## Glossary

- **ProductGallery**: Component React hiển thị gallery ảnh/video sản phẩm với chức năng zoom
- **Related_Products_API**: API endpoint trả về danh sách sản phẩm liên quan
- **Zoom_Modal**: Modal hiển thị ảnh phóng to với khả năng pan/zoom
- **Video_Player**: Component phát video ngắn giới thiệu sản phẩm
- **Pulse_Effect**: Hiệu ứng nhịp đập CSS animation thu hút sự chú ý

## Requirements

### Requirement 1: ProductGallery Component với Zoom

**User Story:** As a customer, I want to zoom in on product images, so that I can see the details of wedding dresses clearly.

#### Acceptance Criteria

1. WHEN a user clicks on the main product image, THE ProductGallery SHALL display a zoom modal with the full-size image
2. WHEN the zoom modal is open, THE ProductGallery SHALL allow users to pan around the image by dragging
3. WHEN a user scrolls or pinches on the zoom modal, THE ProductGallery SHALL zoom in/out the image smoothly
4. WHEN a user presses ESC or clicks outside, THE ProductGallery SHALL close the zoom modal
5. THE ProductGallery SHALL display thumbnail navigation below the main image
6. WHEN a user clicks a thumbnail, THE ProductGallery SHALL update the main image to show the selected image

### Requirement 2: Video Support trong Gallery

**User Story:** As a customer, I want to view short videos of wedding dresses, so that I can see how the dress looks in motion.

#### Acceptance Criteria

1. WHEN a product has video_url in its data, THE ProductGallery SHALL display a video thumbnail with play icon
2. WHEN a user clicks on a video thumbnail, THE ProductGallery SHALL play the video in the main display area
3. WHILE a video is playing, THE ProductGallery SHALL show video controls (play/pause, progress, mute)
4. WHEN a user clicks another thumbnail, THE ProductGallery SHALL pause the current video and switch to the new media
5. THE Video_Player SHALL support common video formats (mp4, webm)

### Requirement 3: Related Products API

**User Story:** As a customer, I want to see related products, so that I can discover similar wedding dresses.

#### Acceptance Criteria

1. WHEN a GET request is made to /api/products/{id}/related, THE Related_Products_API SHALL return products from the same collection
2. IF no products in the same collection exist, THEN THE Related_Products_API SHALL return products with the same style
3. THE Related_Products_API SHALL exclude the current product from the results
4. THE Related_Products_API SHALL limit results to maximum 8 products
5. THE Related_Products_API SHALL return products sorted by popularity (is_hot first, then by id desc)

### Requirement 4: Nút Đặt Lịch Thử Váy với Pulse Effect

**User Story:** As a business owner, I want the "Book Fitting" button to be prominent, so that customers are encouraged to schedule appointments.

#### Acceptance Criteria

1. THE Booking_Button SHALL be styled with gold/bronze color (#D4AF37) as primary color
2. THE Booking_Button SHALL have a pulse animation that runs continuously
3. THE Pulse_Effect SHALL be subtle (not distracting) with opacity changes between 0.7 and 1.0
4. WHEN a user hovers over the button, THE Booking_Button SHALL scale up slightly (1.05x)
5. WHEN a user clicks the button, THE System SHALL navigate to the booking/contact page
6. THE Booking_Button SHALL be responsive and maintain visibility on mobile devices

### Requirement 5: Related Products Display

**User Story:** As a customer, I want to see related products on the product detail page, so that I can easily browse similar items.

#### Acceptance Criteria

1. WHEN the product detail page loads, THE System SHALL fetch and display related products
2. THE Related_Products_Section SHALL display products in a horizontal scrollable carousel on mobile
3. THE Related_Products_Section SHALL display products in a 4-column grid on desktop
4. WHEN a user clicks on a related product, THE System SHALL navigate to that product's detail page
5. IF no related products are found, THEN THE Related_Products_Section SHALL be hidden
