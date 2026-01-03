# 🚀 Hướng dẫn Fix Lỗi Deploy Frontend trên Render

## ❌ Các lỗi thường gặp

### 1. **Build Failed - Out of Memory (OOM)**
**Triệu chứng:** Build bị dừng giữa chừng, exit code 137
**Nguyên nhân:** Render free tier chỉ có 512MB RAM, không đủ để build các 3D libraries lớn

**Giải pháp:**
```bash
# Đã fix trong render.yaml:
NODE_OPTIONS="--max-old-space-size=2048" npm run build
```

### 2. **Environment Variables không load**
**Triệu chứng:** API calls fail, Firebase không hoạt động
**Nguyên nhân:** Biến môi trường VITE_ không được set trong Render

**Giải pháp:**
1. Vào Render Dashboard → ivie-frontend → Environment
2. Thêm các biến:
   ```
   VITE_API_BASE_URL=https://ivie-backend.onrender.com
   NODE_ENV=production
   ```

### 3. **Static Site vs Docker confusion**
**Triệu chứng:** Render không biết dùng Dockerfile hay build command
**Nguyên nhân:** Có cả Dockerfile và static site config

**Giải pháp:**
- Render static sites **KHÔNG** dùng Docker
- Dockerfile chỉ dùng cho local testing
- Deploy dùng `buildCommand` trong render.yaml

### 4. **Chunk size quá lớn**
**Triệu chứng:** Warning về chunk > 500KB
**Nguyên nhân:** Three.js và R3F libraries rất lớn

**Giải pháp:**
- Đã tách `vendor-3d` thành 2 chunks nhỏ hơn trong vite.config.js
- Tăng `chunkSizeWarningLimit` lên 1000

## ✅ Checklist Deploy

### Trước khi deploy:
- [ ] Đã commit tất cả changes
- [ ] Đã test build local: `npm run build`
- [ ] Đã check file `.node-version` (Node 20.18.0)
- [ ] Đã update `render.yaml` với build command mới

### Trong Render Dashboard:
- [ ] Environment variables đã set đúng
- [ ] Build command: `npm ci --legacy-peer-deps --prefer-offline && NODE_OPTIONS="--max-old-space-size=2048" npm run build`
- [ ] Publish directory: `dist`
- [ ] Auto-deploy: ON (nếu muốn)

### Sau khi deploy:
- [ ] Check build logs có lỗi không
- [ ] Test trang web: https://ivie-frontend.onrender.com
- [ ] Test API connection (mở DevTools → Network)
- [ ] Test các trang chính: Home, Products, Gallery

## 🔧 Debug Commands

### Test build locally:
```bash
cd frontend
npm ci --legacy-peer-deps
NODE_OPTIONS="--max-old-space-size=2048" npm run build
npm run preview  # Test production build
```

### Check bundle size:
```bash
npm run build
# Xem output trong terminal
```

### Test với production API:
```bash
# Tạo file .env.production
echo "VITE_API_BASE_URL=https://ivie-backend.onrender.com" > .env.production
npm run build
```

## 📊 Expected Build Output

Build thành công sẽ có output như sau:
```
✓ 2828 modules transformed.
dist/index.html                    5.13 kB
dist/assets/vendor-three-*.js    ~600 kB  (tách từ vendor-3d)
dist/assets/vendor-r3f-*.js      ~500 kB  (tách từ vendor-3d)
dist/assets/vendor-animation-*.js ~193 kB
...
✓ built in 10-15s
```

## 🆘 Nếu vẫn lỗi

### Option 1: Deploy bằng Docker (Web Service)
Nếu static site không work, có thể chuyển sang web service:

```yaml
# Trong render.yaml, thay đổi frontend service:
- type: web
  name: ivie-frontend
  runtime: docker
  dockerfilePath: ./Dockerfile
  # ... rest of config
```

### Option 2: Giảm dependencies
Nếu build vẫn OOM, có thể:
1. Lazy load 3D components
2. Dùng CDN cho Three.js
3. Remove unused 3D features

### Option 3: Upgrade Render plan
Free tier có giới hạn:
- RAM: 512MB
- Build time: 15 phút
- Bandwidth: 100GB/tháng

Nếu cần nhiều hơn, upgrade lên Starter ($7/tháng).

## 📞 Support

Nếu vẫn gặp vấn đề:
1. Check Render build logs
2. Check browser console (F12)
3. Tạo issue với logs đầy đủ
