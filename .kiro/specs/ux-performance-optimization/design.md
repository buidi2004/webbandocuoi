# Design Document: UX & Performance Optimization

## Overview

Tối ưu hóa toàn diện website IVIE Wedding Studio về mặt hiệu năng và trải nghiệm người dùng, tập trung vào:
1. Lazy Loading ảnh với placeholder
2. Sticky CTA (Zalo + Hotline)
3. Trang cảm ơn với tracking
4. Google Analytics 4 integration
5. Mobile UX improvements

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      IVIE Website                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  LazyImage      │  │  StickyCTA      │  │  GA4        │ │
│  │  Component      │  │  Component      │  │  Tracking   │ │
│  │  - Intersection │  │  - Zalo btn     │  │  - Events   │ │
│  │  - Placeholder  │  │  - Phone btn    │  │  - Pageview │ │
│  │  - Fade-in      │  │  - Responsive   │  │  - Ecommerce│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Thank You Page                            │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  /cam-on - Conversion tracking + CTA buttons            ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. LazyImage Component

```jsx
interface LazyImageProps {
  src: string;              // URL ảnh gốc
  alt: string;              // Alt text cho SEO
  className?: string;       // Custom class
  placeholderColor?: string; // Màu placeholder
  threshold?: number;       // Khoảng cách trigger load (default: 200px)
}
```

### 2. StickyCTA Component

```jsx
interface StickyCTAProps {
  zaloLink: string;         // Link Zalo OA
  phoneNumber: string;      // Số hotline
  showOnMobile?: boolean;   // Hiển thị trên mobile
}
```

### 3. GA4 Tracking Service

```javascript
// Tracking events
interface GA4Events {
  viewItem(productId: string, productName: string, price: number): void;
  addToCart(productId: string, productName: string, price: number): void;
  generateLead(formType: string): void;
  conversion(conversionType: string): void;
}
```

### 4. ThankYouPage Component

```jsx
interface ThankYouPageProps {
  formType?: string;        // Loại form đã gửi
  productName?: string;     // Tên sản phẩm (nếu có)
}
```

## Data Models

### GA4 Event Schema

```javascript
// view_item event
{
  event: 'view_item',
  ecommerce: {
    items: [{
      item_id: 'SP001',
      item_name: 'Váy cưới công chúa',
      price: 2500000,
      item_category: 'Váy cưới'
    }]
  }
}

// generate_lead event
{
  event: 'generate_lead',
  form_type: 'contact',
  product_interest: 'Váy cưới'
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system.*

### Property 1: Lazy Load Threshold
*For any* image on the page, the image SHALL only start loading when it is within 200px of the viewport.
**Validates: Requirements 1.1, 1.2**

### Property 2: Sticky CTA Visibility
*For any* scroll position on the page, the Sticky CTA SHALL remain visible and accessible.
**Validates: Requirements 2.1, 2.2**

### Property 3: Form Submission Redirect
*For any* successful form submission, the user SHALL be redirected to the Thank You page.
**Validates: Requirements 3.1, 3.4**

### Property 4: GA4 Event Firing
*For any* tracked user action (view, add to cart, submit form), the corresponding GA4 event SHALL be fired with correct parameters.
**Validates: Requirements 4.2, 4.3, 4.4, 4.5**

### Property 5: Mobile Touch Target
*For any* interactive element on mobile, the touch target SHALL be at least 44px.
**Validates: Requirements 5.4**

## Error Handling

### Frontend Errors
- **Image Load Error**: Hiển thị placeholder với icon broken image
- **GA4 Not Loaded**: Silently fail, không block user experience
- **Form Submit Error**: Hiển thị error message, không redirect

## Testing Strategy

### Unit Tests
- Test LazyImage loads when in viewport
- Test StickyCTA renders correctly on desktop/mobile
- Test GA4 events fire with correct data
- Test ThankYouPage displays correct content

### Integration Tests
- Test form submission → redirect → GA4 event flow
- Test lazy loading với scroll simulation

## Implementation Details

### GA4 Setup

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Lazy Loading với Intersection Observer

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        loadImage(entry.target);
        observer.unobserve(entry.target);
      }
    });
  },
  { rootMargin: '200px' }
);
```

### Sticky CTA CSS

```css
.sticky-cta {
  position: fixed;
  right: 20px;
  bottom: 100px; /* Above StickyBottomBar on mobile */
  z-index: 999;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (max-width: 768px) {
  .sticky-cta {
    right: 16px;
    bottom: 80px; /* Adjust for mobile bottom bar */
  }
}
```

## Responsive Breakpoints

- Mobile: < 768px - Compact CTA, adjusted positioning
- Tablet: 768px - 1024px - Standard CTA
- Desktop: > 1024px - Expanded CTA with labels

