# Design Document: Gallery Optimization

## Overview

Thiết kế hệ thống Gallery mới cho trang Thư Viện IVIE STUDIO, thay thế phần Gallery cũ bằng một giải pháp hiện đại với Masonry Grid layout, Lightbox viewer, lazy loading, và các hiệu ứng visual tinh tế. Hệ thống được xây dựng với React components, Tailwind CSS, và vanilla JavaScript cho animations.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ThuVien.jsx (Page)                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │              PetalBackground (Canvas)                │    │
│  │         Floating petal animation layer               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              GallerySection                          │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │           MasonryGrid                        │    │    │
│  │  │  ┌─────┐ ┌─────┐ ┌─────┐                    │    │    │
│  │  │  │Lazy │ │Lazy │ │Lazy │  ...               │    │    │
│  │  │  │Image│ │Image│ │Image│                    │    │    │
│  │  │  └─────┘ └─────┘ └─────┘                    │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Lightbox (Portal)                       │    │
│  │         Full-screen image viewer                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              FloatingCTA                             │    │
│  │         Fixed "Đặt Lịch" button                      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. MasonryGrid Component

```jsx
interface MasonryGridProps {
  images: Array<{
    url: string;
    title?: string;
    id: string | number;
  }>;
  gap?: number;           // Default: 20
  onImageClick: (index: number) => void;
}
```

**Implementation Strategy:**
- Use CSS `column-count` property for true masonry behavior
- Responsive breakpoints via Tailwind classes
- Each image wrapped in `break-inside-avoid` container

### 2. GalleryImage Component (Lazy Loading)

```jsx
interface GalleryImageProps {
  src: string;
  alt: string;
  index: number;
  onClick: () => void;
}
```

**Implementation Strategy:**
- Intersection Observer with threshold 0.1 and rootMargin "100px"
- Skeleton placeholder while loading
- Fade-in animation on load complete
- Hover effects with CSS transforms

### 3. Lightbox Component

```jsx
interface LightboxProps {
  images: Array<{ url: string; title?: string }>;
  currentIndex: number;
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (direction: 'prev' | 'next') => void;
}
```

**Implementation Strategy:**
- React Portal for rendering outside DOM hierarchy
- Keyboard event listeners (Escape, Arrow keys)
- Touch swipe support for mobile
- Smooth transitions between images

### 4. PetalBackground Component

```jsx
interface PetalBackgroundProps {
  petalCount?: number;    // Default: 20
  enabled?: boolean;      // Default: true
}
```

**Implementation Strategy:**
- Canvas-based rendering for performance
- Object pooling for petal instances
- requestAnimationFrame loop
- Visibility API to pause when tab inactive

### 5. FloatingCTA Component

```jsx
interface FloatingCTAProps {
  text?: string;          // Default: "Đặt Lịch"
  href?: string;          // Default: "/lien-he"
  icon?: ReactNode;
}
```

## Data Models

### Image Data Structure
```typescript
interface GalleryImage {
  id: string | number;
  url: string;
  title?: string;
  width?: number;
  height?: number;
}
```

### Petal Particle Structure
```typescript
interface Petal {
  x: number;
  y: number;
  size: number;
  rotation: number;
  rotationSpeed: number;
  fallSpeed: number;
  swayAmplitude: number;
  swaySpeed: number;
  opacity: number;
}
```

## Component Styling

### Color Palette
```css
:root {
  --gold-accent: #D4AF37;
  --gold-hover: #C9A227;
  --charcoal: #333333;
  --white: #FFFFFF;
  --overlay-dark: rgba(0, 0, 0, 0.95);
  --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.15);
}
```

### Typography
```css
/* Headings */
font-family: 'Playfair Display', Georgia, serif;

/* Body */
font-family: 'Montserrat', -apple-system, sans-serif;
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Responsive Column Count
*For any* viewport width, the Masonry_Grid column count SHALL be 3 for width ≥1024px, 2 for 768px-1023px, and 1 for <768px.
**Validates: Requirements 1.1**

### Property 2: Lazy Loading Viewport Detection
*For any* GalleryImage component, when the image element enters the viewport (intersection ratio ≥ 0.1), the image src SHALL be set and loading SHALL begin.
**Validates: Requirements 3.1, 3.2**

### Property 3: Image Fade-in on Load
*For any* GalleryImage that completes loading, the opacity SHALL transition from 0 to 1.
**Validates: Requirements 3.3**

### Property 4: Lightbox Opens on Click
*For any* gallery image click event, the Lightbox component SHALL render with isOpen=true and currentIndex matching the clicked image index.
**Validates: Requirements 4.1**

### Property 5: Lightbox Escape Key Closes
*For any* open Lightbox state, when Escape key is pressed, the Lightbox SHALL close (isOpen becomes false).
**Validates: Requirements 4.5**

### Property 6: Lightbox Overlay Click Closes
*For any* open Lightbox state, when user clicks on the overlay (outside image area), the Lightbox SHALL close.
**Validates: Requirements 4.6**

### Property 7: Lightbox Arrow Key Navigation
*For any* open Lightbox with multiple images, pressing Left arrow SHALL decrement currentIndex (with wrap), pressing Right arrow SHALL increment currentIndex (with wrap).
**Validates: Requirements 4.7**

### Property 8: Lightbox Index Display
*For any* open Lightbox state with N images at index I, the display SHALL show "(I+1) / N" format.
**Validates: Requirements 4.8**

### Property 9: Petal Count Bounds
*For any* PetalBackground animation state, the number of active petals SHALL be between 15 and 25 inclusive.
**Validates: Requirements 6.2**

### Property 10: Petal Size and Opacity Bounds
*For any* petal in the animation, size SHALL be between 10px and 25px, and opacity SHALL be between 0.3 and 0.7.
**Validates: Requirements 6.4**

### Property 11: Animation Pauses When Hidden
*For any* PetalBackground, when document.hidden is true, the animation loop SHALL not execute (no requestAnimationFrame calls).
**Validates: Requirements 6.6**

### Property 12: Touch-friendly Navigation Buttons
*For any* Lightbox navigation button on touch devices, the minimum dimension (width and height) SHALL be at least 44px.
**Validates: Requirements 8.3**

### Property 13: Touch Device Hover Disable
*For any* touch-enabled device, hover effects (scale, shadow) SHALL not be applied on GalleryImage components.
**Validates: Requirements 8.5**

## Error Handling

### Image Load Errors
- Display fallback placeholder image on load failure
- Log error to console for debugging
- Continue rendering other images in grid

### Lightbox Navigation Edge Cases
- Wrap around when navigating past first/last image
- Handle empty image array gracefully (don't open lightbox)

### Canvas Context Errors
- Fallback to CSS-only background if canvas not supported
- Check for getContext('2d') availability

### Intersection Observer Fallback
- If IntersectionObserver not supported, load all images immediately
- Use polyfill or feature detection

## Testing Strategy

### Unit Tests
- Test MasonryGrid renders correct number of columns at breakpoints
- Test GalleryImage lazy loading state transitions
- Test Lightbox open/close/navigate functions
- Test PetalBackground petal generation bounds
- Test FloatingCTA renders with correct props

### Property-Based Tests
Using fast-check library for JavaScript:

1. **Responsive columns**: Generate random viewport widths, verify column count
2. **Lightbox navigation**: Generate random image arrays and navigation sequences, verify index bounds
3. **Petal bounds**: Generate petal instances, verify size/opacity within bounds
4. **Index display format**: Generate random indices and totals, verify display format

### Integration Tests
- Test full gallery flow: load → scroll → lazy load → click → lightbox → navigate → close
- Test keyboard navigation in lightbox
- Test touch interactions on mobile viewport

### Visual Regression Tests
- Snapshot masonry layout at each breakpoint
- Snapshot lightbox open state
- Snapshot hover effects
