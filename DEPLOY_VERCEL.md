# 🚀 Deploy Frontend Lên Vercel

## ✅ Ưu Điểm Vercel

- ✅ **Hoàn toàn MIỄN PHÍ** cho frontend
- ✅ **Tự động deploy** khi push code
- ✅ **CDN toàn cầu** - load cực nhanh
- ✅ **HTTPS tự động** - miễn phí SSL
- ✅ **Preview deployments** - test trước khi lên production
- ✅ **Tối ưu cho React/Vite** - build nhanh

---

## 📋 Các Bước Deploy

### Bước 1: Chuẩn Bị

File `vercel.json` đã được tạo sẵn với cấu hình:
- Build command: `cd frontend && npm install && npm run build`
- Output directory: `frontend/dist`
- SPA routing: redirect tất cả về `index.html`
- Cache static assets: 1 năm

### Bước 2: Push Code Lên GitHub

```bash
git add vercel.json DEPLOY_VERCEL.md
git commit -m "Add Vercel config for frontend deployment"
git push origin main
```

### Bước 3: Deploy Trên Vercel

#### A. Qua Dashboard (Khuyên Dùng)

1. **Vào Vercel:** https://vercel.com
2. **Đăng nhập** bằng GitHub
3. **Import Project:**
   - Click "Add New..." → "Project"
   - Chọn repo `webbandocuoi`
   - Click "Import"

4. **Cấu hình:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend` (QUAN TRỌNG!)
   - **Build Command:** `npm run build` (tự động)
   - **Output Directory:** `dist` (tự động)
   - **Install Command:** `npm install` (tự động)

5. **Environment Variables** (nếu cần):
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   VITE_FIREBASE_API_KEY=your-key
   VITE_FIREBASE_AUTH_DOMAIN=your-domain
   ```

6. **Deploy:**
   - Click "Deploy"
   - Chờ 2-3 phút
   - Done! 🎉

#### B. Qua CLI (Nâng Cao)

```bash
# Cài Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Deploy production
vercel --prod
```

---

## 🔧 Cấu Hình Backend URL

Sau khi deploy, bạn cần cập nhật Backend URL trong frontend:

### Cách 1: Environment Variables (Khuyên Dùng)

Trong Vercel Dashboard:
1. Vào Project Settings
2. Tab "Environment Variables"
3. Thêm:
   ```
   VITE_API_URL=https://ivie-be-final.onrender.com
   ```
4. Redeploy

### Cách 2: Hardcode (Không Khuyên)

Sửa file `frontend/src/api/nguoi_dung.js` hoặc config file:
```javascript
const API_URL = 'https://ivie-be-final.onrender.com';
```

---

## 🌐 Custom Domain (Tùy Chọn)

### Dùng Domain Miễn Phí Của Vercel

Vercel tự động cung cấp:
- `your-project.vercel.app`
- Có HTTPS
- Không cần config gì

### Dùng Domain Riêng

1. Vào Project Settings → Domains
2. Thêm domain của bạn (vd: `ivie-wedding.com`)
3. Cập nhật DNS records:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21

   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```
4. Chờ DNS propagate (~5-10 phút)

---

## 🔄 Auto Deploy

Vercel tự động deploy khi:
- ✅ Push lên branch `main` → Production
- ✅ Push lên branch khác → Preview
- ✅ Tạo Pull Request → Preview

Không cần làm gì thêm!

---

## 📊 So Sánh Vercel vs Render (Frontend)

| Tính Năng | Vercel | Render |
|-----------|--------|--------|
| **Giá** | FREE | FREE |
| **Build Time** | ~1-2 phút | ~3-4 phút |
| **CDN** | ✅ Toàn cầu | ✅ Toàn cầu |
| **Auto Deploy** | ✅ Tự động | ✅ Tự động |
| **Preview** | ✅ Mỗi PR | ❌ Không |
| **Analytics** | ✅ Miễn phí | ❌ Không |
| **Tối Ưu React** | ✅✅✅ Rất tốt | ✅ Tốt |

**Kết luận:** Vercel tốt hơn cho frontend!

---

## 🐛 Troubleshooting

### Lỗi: Build Failed

**Nguyên nhân:** Thiếu dependencies hoặc lỗi code

**Giải pháp:**
1. Check logs trong Vercel Dashboard
2. Test build local:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
3. Fix lỗi và push lại

### Lỗi: 404 Not Found Khi Refresh

**Nguyên nhân:** SPA routing không được config

**Giải pháp:** File `vercel.json` đã có config này:
```json
"rewrites": [
  { "source": "/(.*)", "destination": "/index.html" }
]
```

### Lỗi: API Calls Failed (CORS)

**Nguyên nhân:** Backend chưa cho phép domain Vercel

**Giải pháp:** Thêm vào Backend (FastAPI):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-project.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Lỗi: Environment Variables Không Hoạt Động

**Nguyên nhân:** Vite cần prefix `VITE_`

**Giải pháp:** Đổi tên biến:
- ❌ `API_URL`
- ✅ `VITE_API_URL`

Sử dụng:
```javascript
const apiUrl = import.meta.env.VITE_API_URL;
```

---

## 💡 Tips Tối Ưu

### 1. Giảm Bundle Size

```bash
# Analyze bundle
npm run build -- --mode analyze

# Remove unused dependencies
npm prune
```

### 2. Lazy Loading

```javascript
// Thay vì
import Component from './Component';

// Dùng
const Component = lazy(() => import('./Component'));
```

### 3. Image Optimization

Vercel tự động optimize images nếu dùng:
```javascript
import Image from 'next/image'; // Nếu dùng Next.js
```

Hoặc dùng CDN như Cloudinary cho Vite.

### 4. Enable Analytics

Trong Vercel Dashboard:
1. Tab "Analytics"
2. Enable "Web Analytics"
3. Xem traffic, performance, Core Web Vitals

---

## 🎯 Kiến Trúc Đề Xuất

```
Frontend (Vercel)
    ↓
Backend (Render)
    ↓
Database (Render PostgreSQL)
    ↓
Admin (Render)
```

**Lợi ích:**
- Frontend trên Vercel: CDN nhanh, tối ưu React
- Backend trên Render: Python runtime, kết nối DB dễ
- Tất cả đều FREE!

---

## 📝 Checklist Deploy

- [ ] Push code lên GitHub
- [ ] Tạo account Vercel (đăng nhập bằng GitHub)
- [ ] Import project từ GitHub
- [ ] Chọn Root Directory = `frontend`
- [ ] Thêm Environment Variables (nếu cần)
- [ ] Deploy
- [ ] Test website
- [ ] Cập nhật CORS trong Backend
- [ ] Test API calls
- [ ] (Tùy chọn) Setup custom domain

---

## 🎉 Kết Luận

Deploy Frontend lên Vercel là lựa chọn tốt nhất:
- ✅ Miễn phí 100%
- ✅ Nhanh nhất (CDN toàn cầu)
- ✅ Tự động deploy
- ✅ Preview cho mỗi PR
- ✅ Analytics miễn phí

**Backend + Database vẫn trên Render** (Python runtime, free tier)

Bạn có thể deploy ngay bây giờ! 🚀
