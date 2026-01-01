# Design Document: PageSpeed Optimization

## Overview

Tối ưu PageSpeed cho hệ thống IVIE Wedding Studio bằng cách:
1. Thêm GZip compression và cache headers cho FastAPI backend
2. Tối ưu code splitting và lazy loading cho React frontend
3. Cấu hình Vite build để minify tối đa
4. Cải thiện TTFB với critical CSS và font preloading

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT (Browser)                         │
├─────────────────────────────────────────────────────────────┤
│  React App                                                   │
│  ├── Critical CSS (inline)                                  │
│  ├── Preloaded Fonts                                        │
│  ├── Code Split Chunks (lazy loaded)                        │
│  └── LazyImage Components                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                          │
├─────────────────────────────────────────────────────────────┤
│  Middleware Stack:                                           │
│  ├── GZipMiddleware (min_size=500)                          │
│  ├── CORSMiddleware                                         │
│  └── Cache-Control Headers                                  │
│                                                              │
│  Endpoints with Cache:                                       │
│  ├── /api/san_pham/ (5 min cache)                           │
│  ├── /api/banner/ (10 min cache)                            │
│  └── /api/thu_vien/, /api/blog/ (1 hour cache)              │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. FastAPI GZip Middleware

```python
# backend/ung_dung/chinh.py
from fastapi.middleware.gzip import GZipMiddleware

ung_dung.add_middleware(GZipMiddleware, minimum_size=500)
```

### 2. Cache Control Decorator

```python
# backend/ung_dung/cache_utils.py
from functools import wraps
from fastapi import Response

def cache_response(max_age: int = 300, public: bool = True):
    """Decorator để thêm Cache-Control header"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, response: Response = None, **kwargs):
            result = await func(*args, **kwargs)
            if response:
                cache_type = "public" if public else "private"
                response.headers["Cache-Control"] = f"{cache_type}, max-age={max_age}"
            return result
        return wrapper
    return decorator
```

### 3. LazyImage Component (Enhanced)

```jsx
// frontend/src/thanh_phan/LazyImage.jsx
const LazyImage = ({ 
    src, 
    alt = '', 
    width,
    height,
    aspectRatio = '4/3',
    placeholderColor = '#f0f0f0',
    threshold = 200,
    ...props 
}) => {
    // Intersection Observer for lazy loading
    // Skeleton placeholder while loading
    // Error state handling
    // Native loading="lazy" and decoding="async"
};
```

### 4. Vite Build Configuration

```javascript
// frontend/vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-animation': ['framer-motion', 'gsap'],
          'vendor-3d': ['three', '@react-three/fiber', '@react-three/drei'],
          'vendor-utils': ['axios', 'atropos'],
        },
      },
    },
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    cssMinify: true,
    chunkSizeWarningLimit: 500,
  },
});
```

## Data Models

### Cache Configuration

| Endpoint Pattern | Cache Duration | Cache Type |
|-----------------|----------------|------------|
| `/api/san_pham/` | 300s (5 min) | public |
| `/api/banner/` | 600s (10 min) | public |
| `/api/thu_vien/` | 3600s (1 hour) | public |
| `/api/blog/` | 3600s (1 hour) | public |
| POST/PUT/DELETE | 0s | no-store |

### Chunk Size Targets

| Chunk | Target Size | Contents |
|-------|-------------|----------|
| vendor-react | < 150KB | React, ReactDOM, Router |
| vendor-animation | < 200KB | Framer Motion, GSAP |
| vendor-3d | < 300KB | Three.js, R3F |
| vendor-utils | < 50KB | Axios, Atropos |
| Page chunks | < 100KB each | Individual pages |

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do.*

### Property 1: GZip Compression for Large Responses

*For any* API response larger than 500 bytes, when the client sends Accept-Encoding: gzip header, the response SHALL be gzip compressed (Content-Encoding: gzip).

**Validates: Requirements 1.2, 1.3**

### Property 2: No Cache on Mutation Requests

*For any* POST, PUT, PATCH, or DELETE request to the API, the response SHALL NOT include Cache-Control header with max-age > 0.

**Validates: Requirements 2.4**

### Property 3: Chunk Size Limit

*For any* JavaScript chunk generated by Vite build, the file size SHALL be less than 500KB.

**Validates: Requirements 5.5**

## Error Handling

1. **Image Load Failure**: LazyImage shows error state with fallback icon
2. **Chunk Load Failure**: React Suspense shows error boundary
3. **API Timeout**: Frontend shows loading state, retries with exponential backoff
4. **GZip Encoding Error**: FastAPI falls back to uncompressed response

## Testing Strategy

### Unit Tests
- Verify GZipMiddleware is registered
- Verify cache headers on specific endpoints
- Verify LazyImage renders with correct attributes
- Verify Vite config has correct settings

### Property-Based Tests
- Test gzip compression across various response sizes
- Test no-cache on all mutation endpoints
- Test chunk sizes after build

### Integration Tests
- End-to-end page load with Lighthouse
- Network waterfall analysis
- TTFB measurement from Vietnam
