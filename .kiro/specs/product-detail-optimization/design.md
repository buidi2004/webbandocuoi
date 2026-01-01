# Design Document: Product Detail Optimization

## Overview

Tối ưu hóa trang chi tiết sản phẩm IVIE Wedding Studio với 3 tính năng chính:
1. **ProductGallery Component** - Gallery ảnh/video với zoom, pan, và video playback
2. **Related Products API** - Backend API gợi ý sản phẩm liên quan
3. **Booking Button với Pulse Effect** - Nút đặt lịch nổi bật với hiệu ứng animation

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ProductDetail Page                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────────────┐  │
│  │   ProductGallery    │  │      Product Info           │  │
│  │  ┌───────────────┐  │  │  - Title, Price             │  │
│  │  │  Main Display │  │  │  - Size/Color Options       │  │
│  │  │  (Image/Video)│  │  │  ┌─────────────────────┐    │  │
│  │  └───────────────┘  │  │  │  BookingButton      │    │  │
│  │  ┌───────────────┐  │  │  │  (Pulse Animation)  │    │  │
│  │  │  Thumbnails   │  │  │  └─────────────────────┘    │  │
│  │  └───────────────┘  │  └─────────────────────────────┘  │
│  └─────────────────────┘                                    │
├─────────────────────────────────────────────────────────────┤
│                  Related Products Section                    │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ SP1 │ │ SP2 │ │ SP3 │ │ SP4 │ │ SP5 │ │ SP6 │ │ SP7 │  │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. ProductGallery Component

```jsx
// Props Interface
interface ProductGalleryProps {
  images: string[];           // Danh sách URL ảnh
  videoUrl?: string;          // URL video (optional)
  productName: string;        // Tên sản phẩm cho alt text
}

// State Interface
interface GalleryState {
  currentIndex: number;       // Index media đang hiển thị
  isZoomOpen: boolean;        // Trạng thái zoom modal
  zoomLevel: number;          // Mức zoom (1.0 - 3.0)
  panPosition: { x: number, y: number };  // Vị trí pan
  isVideoPlaying: boolean;    // Trạng thái video
}
```

### 2. ZoomModal Component

```jsx
interface ZoomModalProps {
  src: string;                // URL ảnh
  alt: string;                // Alt text
  isOpen: boolean;            // Trạng thái mở
  onClose: () => void;        // Callback đóng modal
}
```

### 3. BookingButton Component

```jsx
interface BookingButtonProps {
  productId: string;          // ID sản phẩm
  productName: string;        // Tên sản phẩm
  className?: string;         // Custom class
}
```

### 4. RelatedProducts Component

```jsx
interface RelatedProductsProps {
  productId: string;          // ID sản phẩm hiện tại
  collection?: string;        // Bộ sưu tập
  style?: string;             // Phong cách
}

interface RelatedProduct {
  id: number;
  name: string;
  image_url: string;
  rental_price_day: number;
  is_hot: boolean;
}
```

### 5. Backend API Interface

```python
# GET /api/san_pham/{id}/lien_quan
# Response: List[SanPhamLienQuan]

class SanPhamLienQuan(BaseModel):
    id: int
    name: str
    code: str
    image_url: str
    rental_price_day: float
    purchase_price: float
    is_hot: bool
    is_new: bool
    style: Optional[str]
    collection: Optional[str]
```

## Data Models

### Product với Video Support

```python
# Thêm field video_url vào SanPham model
class SanPham:
    # ... existing fields ...
    video_url: Optional[str] = None  # URL video ngắn
    collection: Optional[str] = None  # Bộ sưu tập
    style: Optional[str] = None       # Phong cách (minimalist, princess, vintage, etc.)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Zoom/Pan State Consistency
*For any* zoom modal interaction (drag, scroll, pinch), the zoom level SHALL remain within bounds [1.0, 3.0] and pan position SHALL be constrained to keep the image visible.
**Validates: Requirements 1.2, 1.3**

### Property 2: Thumbnail Selection Updates Main Display
*For any* thumbnail click in the gallery, the main display SHALL update to show the corresponding media (image or video).
**Validates: Requirements 1.6, 2.2**

### Property 3: Video Pause on Media Switch
*For any* media switch while video is playing, the video SHALL be paused before switching to the new media.
**Validates: Requirements 2.4**

### Property 4: Related Products Exclude Current
*For any* product ID, the related products API response SHALL NOT contain that product ID.
**Validates: Requirements 3.3**

### Property 5: Related Products Limit
*For any* related products API request, the response SHALL contain at most 8 products.
**Validates: Requirements 3.4**

### Property 6: Related Products Sorting
*For any* related products API response with multiple products, products with is_hot=true SHALL appear before products with is_hot=false.
**Validates: Requirements 3.5**

### Property 7: Related Products Navigation
*For any* click on a related product card, the system SHALL navigate to `/san-pham/{product_id}` where product_id matches the clicked product.
**Validates: Requirements 5.4**

## Error Handling

### Frontend Errors
- **Image Load Error**: Hiển thị placeholder image với text "Không tải được ảnh"
- **Video Load Error**: Hiển thị thumbnail với icon lỗi, cho phép retry
- **API Error**: Hiển thị message "Không thể tải sản phẩm liên quan" và ẩn section

### Backend Errors
- **Product Not Found**: Return 404 với message "Không tìm thấy sản phẩm"
- **Database Error**: Return 500 với generic error message, log chi tiết

## Testing Strategy

### Unit Tests
- Test zoom level bounds (min 1.0, max 3.0)
- Test pan position constraints
- Test thumbnail click updates currentIndex
- Test video pause on media switch
- Test API response filtering (exclude current product)
- Test API response limit (max 8)
- Test API response sorting (is_hot first)

### Property-Based Tests
- **Property 1**: Generate random zoom/pan interactions, verify state stays within bounds
- **Property 4**: Generate random product IDs, verify exclusion from results
- **Property 5**: Generate random products, verify response length <= 8
- **Property 6**: Generate random products with mixed is_hot values, verify sorting

### Integration Tests
- Test ProductGallery renders correctly with images and video
- Test BookingButton navigates to contact page
- Test RelatedProducts fetches and displays data
- Test full page load with all components

## CSS Specifications

### Pulse Animation (Tailwind + Custom CSS)

```css
/* Custom animation for booking button */
@keyframes pulse-gold {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.7);
  }
  50% {
    opacity: 0.85;
    box-shadow: 0 0 0 10px rgba(212, 175, 55, 0);
  }
}

.btn-booking-pulse {
  background: linear-gradient(135deg, #D4AF37 0%, #C9A227 100%);
  color: white;
  animation: pulse-gold 2s infinite;
  transition: transform 0.2s ease;
}

.btn-booking-pulse:hover {
  transform: scale(1.05);
}
```

### Responsive Breakpoints
- Mobile: < 768px - Carousel horizontal scroll
- Tablet: 768px - 1024px - 2 columns grid
- Desktop: > 1024px - 4 columns grid
