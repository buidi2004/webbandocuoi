# Requirements Document

## Introduction

Tối ưu PageSpeed cho hệ thống IVIE Wedding Studio (React + FastAPI) để cải thiện trải nghiệm người dùng, đặc biệt là giảm TTFB (Time to First Byte) khi server đặt ở nước ngoài (Render - Singapore/Mỹ) và người dùng ở Việt Nam.

## Glossary

- **FastAPI_Backend**: Backend API server sử dụng FastAPI framework
- **React_Frontend**: Frontend application sử dụng React + Vite
- **GZipMiddleware**: Middleware nén response để giảm kích thước truyền tải
- **Cache_Control**: HTTP headers để browser/CDN cache response
- **Code_Splitting**: Kỹ thuật chia nhỏ bundle JavaScript thành các chunks
- **LazyImage_Component**: Component React tải ảnh lazy với placeholder
- **TTFB**: Time to First Byte - thời gian từ request đến byte đầu tiên
- **Vite_Build**: Build tool cho React với minification và optimization

## Requirements

### Requirement 1: FastAPI GZip Compression

**User Story:** As a user, I want API responses to be compressed, so that data transfers faster over slow networks.

#### Acceptance Criteria

1. WHEN the FastAPI_Backend starts, THE GZipMiddleware SHALL be enabled with minimum_size of 500 bytes
2. WHEN a response is larger than 500 bytes, THE FastAPI_Backend SHALL compress it using gzip
3. WHEN a client sends Accept-Encoding: gzip header, THE FastAPI_Backend SHALL return compressed response

### Requirement 2: API Response Caching

**User Story:** As a user, I want product listings to load instantly on repeat visits, so that I don't wait for the same data.

#### Acceptance Criteria

1. WHEN the FastAPI_Backend returns product list, THE Cache_Control header SHALL be set to "public, max-age=300" (5 minutes)
2. WHEN the FastAPI_Backend returns banner list, THE Cache_Control header SHALL be set to "public, max-age=600" (10 minutes)
3. WHEN the FastAPI_Backend returns static content (gallery, blog), THE Cache_Control header SHALL be set to "public, max-age=3600" (1 hour)
4. WHEN data is modified (POST/PUT/DELETE), THE FastAPI_Backend SHALL NOT cache the response

### Requirement 3: React Code Splitting for Routes

**User Story:** As a user, I want pages to load quickly, so that I can browse products without waiting for unused code.

#### Acceptance Criteria

1. WHEN the React_Frontend builds, THE Vite_Build SHALL split each route into separate chunks
2. WHEN a user navigates to a page, THE React_Frontend SHALL only load the chunk for that page
3. WHEN heavy components (3D, animations) are used, THE React_Frontend SHALL lazy load them separately
4. THE React_Frontend SHALL show a loading spinner while chunks are loading

### Requirement 4: Smart Image Component

**User Story:** As a user, I want images to load smoothly with placeholders, so that the page doesn't jump around.

#### Acceptance Criteria

1. WHEN an image is outside viewport, THE LazyImage_Component SHALL NOT load it
2. WHEN an image enters viewport (200px threshold), THE LazyImage_Component SHALL start loading
3. WHILE an image is loading, THE LazyImage_Component SHALL show a skeleton placeholder
4. WHEN an image fails to load, THE LazyImage_Component SHALL show an error state
5. THE LazyImage_Component SHALL use loading="lazy" and decoding="async" attributes
6. THE LazyImage_Component SHALL accept width, height, aspectRatio props for CLS prevention

### Requirement 5: Vite Production Build Optimization

**User Story:** As a developer, I want the production build to be as small as possible, so that users download less data.

#### Acceptance Criteria

1. WHEN building for production, THE Vite_Build SHALL minify JavaScript using terser
2. WHEN building for production, THE Vite_Build SHALL remove console.log and debugger statements
3. WHEN building for production, THE Vite_Build SHALL minify CSS
4. WHEN building for production, THE Vite_Build SHALL split vendor libraries into separate chunks
5. THE Vite_Build SHALL generate chunks smaller than 500KB each

### Requirement 6: TTFB Optimization

**User Story:** As a user in Vietnam, I want the first response to be fast, so that the page feels responsive.

#### Acceptance Criteria

1. WHEN the FastAPI_Backend receives a request, THE response SHALL start within 200ms for cached data
2. WHEN the React_Frontend loads, THE critical CSS SHALL be inlined in HTML
3. WHEN the React_Frontend loads, THE fonts SHALL be preloaded
4. THE React_Frontend SHALL show a loading placeholder immediately (FCP < 1.5s target)
