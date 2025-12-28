# IVIE Wedding Studio - Frontend

Giao diện React cho website IVIE Wedding Studio được xây dựng với Vite.

## Cài đặt

### 1. Cài đặt thư viện

```bash
cd frontend
npm install
```

### 2. Cấu hình môi trường

Tạo file `.env`:
```
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Chạy server phát triển

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: `http://localhost:5173`

### 4. Build cho production

```bash
npm run build
```

## Công nghệ sử dụng

- **React 18** - Thư viện UI
- **Vite** - Công cụ build
- **React Router** - Điều hướng
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Framer Motion** - Hiệu ứng animation

## Cấu trúc thư mục

```
frontend/
├── public/              # Tài nguyên tĩnh
├── src/
│   ├── api/            # API client
│   │   ├── khach_hang.js
│   │   ├── nguoi_dung.js
│   │   └── quan_tri.js
│   ├── thanh_phan/     # Các component tái sử dụng
│   │   ├── DauTrang.jsx
│   │   ├── ChanTrang.jsx
│   │   ├── BoSuuTapGach.jsx
│   │   └── ...
│   ├── trang/          # Các trang
│   │   ├── TrangChu.jsx
│   │   ├── SanPham.jsx
│   │   ├── ThuVien.jsx
│   │   └── ...
│   ├── styles/         # CSS files
│   ├── UngDung.jsx     # Component chính
│   ├── chinh.jsx       # Entry point
│   └── index.css       # CSS gốc
├── .env                # Biến môi trường
├── package.json
└── vite.config.js
```

## Các trang chính

- `/` - Trang chủ
- `/san-pham` - Danh sách sản phẩm
- `/san-pham/:id` - Chi tiết sản phẩm
- `/thu-vien` - Thư viện ảnh
- `/dich-vu-trang-diem` - Dịch vụ trang điểm
- `/lien-he` - Liên hệ
- `/blog` - Blog
- `/gio-hang` - Giỏ hàng
- `/tai-khoan` - Tài khoản

## Triển khai

Build production:
```bash
npm run build
```

Deploy thư mục `dist/` lên:
- Vercel
- Netlify
- GitHub Pages
