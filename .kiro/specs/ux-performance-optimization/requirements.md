# Requirements Document: UX & Performance Optimization

## Introduction

Tối ưu hóa trải nghiệm người dùng (UX) và hiệu năng (Performance) cho website IVIE Wedding Studio, bao gồm: tối ưu tải ảnh, cải thiện CTA, tracking hành vi, và trang cảm ơn.

## Glossary

- **Lazy_Load**: Kỹ thuật chỉ tải ảnh khi người dùng cuộn đến vùng hiển thị
- **WebP**: Định dạng ảnh hiện đại với dung lượng nhỏ hơn JPEG/PNG 25-35%
- **CTA**: Call-to-Action - Nút kêu gọi hành động (Zalo, Nhận báo giá)
- **Sticky_CTA**: Nút CTA cố định khi cuộn trang
- **GA4**: Google Analytics 4 - Công cụ tracking hành vi người dùng
- **Thank_You_Page**: Trang cảm ơn sau khi khách gửi form
- **Conversion_Rate**: Tỷ lệ chuyển đổi từ khách xem sang khách để lại thông tin

## Requirements

### Requirement 1: Tối ưu tải ảnh với Lazy Loading

**User Story:** As a khách hàng, I want trang web tải nhanh khi cuộn, so that tôi có trải nghiệm mượt mà khi xem album ảnh.

#### Acceptance Criteria

1. WHEN trang web được tải, THE System SHALL chỉ tải ảnh trong viewport hiện tại
2. WHEN người dùng cuộn trang, THE System SHALL tải ảnh trước khi chúng xuất hiện trong viewport (threshold 200px)
3. WHILE ảnh đang tải, THE System SHALL hiển thị placeholder blur hoặc skeleton
4. WHEN ảnh tải xong, THE System SHALL fade-in ảnh mượt mà

### Requirement 2: Sticky CTA Buttons

**User Story:** As a khách hàng, I want luôn thấy nút liên hệ, so that tôi có thể liên hệ ngay khi cần tư vấn.

#### Acceptance Criteria

1. THE Sticky_CTA SHALL hiển thị cố định ở góc phải màn hình trên desktop
2. THE Sticky_CTA SHALL bao gồm nút Zalo và nút Gọi điện
3. WHEN người dùng hover vào Sticky_CTA, THE System SHALL mở rộng hiển thị text
4. THE Sticky_CTA SHALL không che nút quan trọng khác trên mobile
5. WHEN trên mobile, THE Sticky_CTA SHALL thu nhỏ và đặt ở vị trí không che form

### Requirement 3: Trang Cảm ơn (Thank You Page)

**User Story:** As a chủ studio, I want có trang cảm ơn sau khi khách gửi form, so that tôi có thể đo lường tỷ lệ chuyển đổi.

#### Acceptance Criteria

1. WHEN khách gửi form liên hệ thành công, THE System SHALL chuyển hướng đến trang cảm ơn
2. THE Thank_You_Page SHALL hiển thị thông điệp cảm ơn và thời gian phản hồi dự kiến
3. THE Thank_You_Page SHALL có nút quay lại trang chủ và nút xem thêm sản phẩm
4. THE Thank_You_Page SHALL có URL riêng `/cam-on` để tracking trong GA4

### Requirement 4: Google Analytics 4 Integration

**User Story:** As a chủ studio, I want tracking hành vi khách hàng, so that tôi biết sản phẩm nào được quan tâm nhất.

#### Acceptance Criteria

1. THE System SHALL tích hợp GA4 tracking code vào tất cả các trang
2. WHEN khách xem chi tiết sản phẩm, THE System SHALL gửi event `view_item` với product_id và product_name
3. WHEN khách thêm vào giỏ, THE System SHALL gửi event `add_to_cart`
4. WHEN khách gửi form liên hệ, THE System SHALL gửi event `generate_lead`
5. WHEN khách đến trang cảm ơn, THE System SHALL gửi event `conversion`

### Requirement 5: Cải thiện Mobile UX

**User Story:** As a khách hàng mobile, I want giao diện dễ sử dụng trên điện thoại, so that tôi có thể xem và liên hệ dễ dàng.

#### Acceptance Criteria

1. THE Zalo_Button SHALL không che nút "Gửi form" trên mobile
2. THE Zalo_Button SHALL có kích thước phù hợp (không quá 56px)
3. WHEN trên mobile, THE System SHALL đặt Zalo button ở góc phải dưới với margin đủ
4. THE System SHALL đảm bảo tất cả form fields có thể tap được dễ dàng (min 44px touch target)

### Requirement 6: SEO Hình ảnh

**User Story:** As a chủ studio, I want ảnh được tối ưu SEO, so that khách có thể tìm thấy qua Google Hình ảnh.

#### Acceptance Criteria

1. THE System SHALL sử dụng alt text mô tả cho tất cả ảnh sản phẩm
2. THE System SHALL format alt text theo pattern: `{tên-sản-phẩm}-ivie-wedding`
3. WHEN hiển thị ảnh sản phẩm, THE System SHALL include structured data (JSON-LD) cho Product

