# Design Document: Scroll-Linked Animation

## Overview

Component `HieuUngCuonDinh` (Scroll-Linked Animation) tạo hiệu ứng cuộn trang cao cấp với 4 sections, mỗi section có text bên trái và hình ảnh sticky bên phải. Sử dụng Framer Motion hooks (useScroll, useTransform) để đồng bộ animation với scroll progress.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  HieuUngCuonDinh Component                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────────────┐  │
│  │   Text Container    │  │   Sticky Image Container    │  │
│  │   (Scrollable)      │  │   (Fixed Position)          │  │
│  │                     │  │                             │  │
│  │  ┌───────────────┐  │  │  ┌───────────────────────┐  │  │
│  │  │  Section 1    │  │  │  │                       │  │  │
│  │  │  - Title      │  │  │  │    Image Stack        │  │  │
│  │  │  - Desc       │  │  │  │    (4 images)         │  │  │
│  │  └───────────────┘  │  │  │                       │  │  │
│  │  ┌───────────────┐  │  │  │  - Opacity animated   │  │  │
│  │  │  Section 2    │  │  │  │  - Y translate        │  │  │
│  │  └───────────────┘  │  │  │  - Scale effect       │  │  │
│  │  ┌───────────────┐  │  │  │                       │  │  │
│  │  │  Section 3    │  │  │  └───────────────────────┘  │  │
│  │  └───────────────┘  │  │                             │  │
│  │  ┌───────────────┐  │  │                             │  │
│  │  │  Section 4    │  │  │                             │  │
│  │  └───────────────┘  │  │                             │  │
│  └─────────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Main Component: HieuUngCuonDinh

```jsx
interface SectionData {
  id: number;
  title: string;
  description: string;
  image: string;
  highlight?: string;
}

interface HieuUngCuonDinhProps {
  sections?: SectionData[];
  className?: string;
}

const HieuUngCuonDinh: React.FC<HieuUngCuonDinhProps>
```

### Sub-components

1. **SectionText**: Renders text content with scroll-based animations
2. **StickyImageStack**: Manages the sticky image container with crossfade effects

### Hooks Usage

```jsx
// Track overall container scroll
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ["start start", "end end"]
});

// Transform scroll progress to animation values
const imageOpacity = useTransform(scrollYProgress, [0, 0.25, 0.5, 0.75, 1], [1, 0, 1, 0, 1]);
const imageY = useTransform(scrollYProgress, [0, 1], [0, -100]);
const textOpacity = useTransform(sectionProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]);
const textY = useTransform(sectionProgress, [0, 0.2, 0.8, 1], [50, 0, 0, -50]);
```

## Data Models

### Section Configuration

```typescript
const defaultSections: SectionData[] = [
  {
    id: 1,
    title: "Chụp Ảnh Cưới Chuyên Nghiệp",
    description: "Lưu giữ khoảnh khắc hạnh phúc nhất của bạn với đội ngũ nhiếp ảnh gia giàu kinh nghiệm",
    image: "/api/placeholder/800/600", // Will use ThuVien images
    highlight: "500+ cặp đôi tin tưởng"
  },
  {
    id: 2,
    title: "Studio Hiện Đại",
    description: "Không gian chụp ảnh sang trọng với ánh sáng tự nhiên và thiết bị cao cấp",
    image: "/api/placeholder/800/600",
    highlight: "3 studio tại Hà Nội"
  },
  {
    id: 3,
    title: "Trang Điểm Cô Dâu",
    description: "Makeup artist chuyên nghiệp giúp bạn tỏa sáng trong ngày trọng đại",
    image: "/api/placeholder/800/600",
    highlight: "Top Artist được yêu thích"
  },
  {
    id: 4,
    title: "Album & In Ấn",
    description: "Album cưới cao cấp với chất liệu nhập khẩu, bền đẹp theo thời gian",
    image: "/api/placeholder/800/600",
    highlight: "Bảo hành trọn đời"
  }
];
```

### Animation Configuration

```typescript
interface AnimationConfig {
  // Image animations
  imageOpacityRange: [number, number, number, number, number]; // [0, 0.25, 0.5, 0.75, 1]
  imageYRange: [number, number]; // [0, -100]
  imageScaleRange: [number, number]; // [1, 1.05]
  
  // Text animations
  textOpacityRange: [number, number, number, number]; // [0, 1, 1, 0]
  textYRange: [number, number, number, number]; // [50, 0, 0, -50]
  
  // Timing
  sectionHeight: string; // "100vh" per section
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Scroll Progress Boundaries

*For any* section in the component, when the section enters the viewport the scroll progress SHALL be 0, and when the section exits the viewport the scroll progress SHALL be 1.

**Validates: Requirements 2.2, 2.3**

### Property 2: Image Opacity Transformation

*For any* scroll progress value between 0 and 1, the image opacity SHALL follow the transformation: opacity increases from 0 to 1 when progress is 0-0.5, and decreases from 1 to 0 when progress is 0.5-1.

**Validates: Requirements 3.1, 3.2**

### Property 3: Image Y Translation

*For any* scroll progress value, the image Y translation SHALL be inversely proportional to the progress (moving upward as progress increases).

**Validates: Requirements 3.3**

### Property 4: Text Y Transformation

*For any* section's scroll progress, the text Y offset SHALL interpolate from 50px to 0px during fade-in (progress 0.2-0.5) and from 0px to -50px during fade-out (progress 0.5-0.8).

**Validates: Requirements 4.3, 4.4**

### Property 5: Section Data Rendering

*For any* section data provided to the component, the rendered output SHALL contain the title, description, and image from that section data.

**Validates: Requirements 5.2**

### Property 6: Responsive Layout Switch

*For any* viewport width less than 768px, the component SHALL render in single-column layout instead of two-column layout.

**Validates: Requirements 1.2**

### Property 7: Section Image Transition

*For any* scroll position that crosses a section boundary, the sticky image container SHALL display the image corresponding to the current active section.

**Validates: Requirements 1.4, 3.5**

## Error Handling

1. **Missing Images**: Display placeholder gradient background if image fails to load
2. **Empty Sections**: Render default sections if no data provided
3. **Scroll Calculation Errors**: Clamp progress values between 0 and 1
4. **Mobile Detection**: Use CSS media queries as fallback if JS detection fails

## Testing Strategy

### Unit Tests
- Test component renders with default sections
- Test component renders with custom section data
- Test responsive layout classes are applied correctly
- Test image lazy loading attribute is present

### Property-Based Tests
- **Property 1**: Generate random scroll positions and verify progress boundaries
- **Property 2**: Generate random progress values and verify opacity transformation
- **Property 3**: Generate random progress values and verify Y translation direction
- **Property 5**: Generate random section data and verify all fields are rendered
- **Property 6**: Generate random viewport widths and verify layout class

### Integration Tests
- Test scroll behavior with simulated scroll events
- Test image crossfade during section transitions
- Test text animation timing with scroll progress

### Testing Framework
- Use Vitest for unit and property tests
- Use fast-check for property-based testing
- Use @testing-library/react for component testing
