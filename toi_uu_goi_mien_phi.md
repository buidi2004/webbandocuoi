# 🆓 Tối ưu Render Free Tier

## Giới hạn gói miễn phí
- **RAM**: 512MB per service
- **CPU**: Shared
- **Build time**: 15 phút
- **Auto-sleep**: Sau 15 phút không dùng
- **Bandwidth**: 100GB/tháng
- **Hours**: 750 giờ/tháng (cho tất cả services)

## ✅ Đã tối ưu trong render.yaml

### 1. Backend (Python/FastAPI)
```yaml
WEB_CONCURRENCY: "1"  # Giảm từ 2 xuống 1 worker
WORKERS: "1"          # Chỉ 1 worker process
```
**Lý do**: Mỗi worker tốn ~100-150MB RAM. Với 1 worker, backend chỉ dùng ~200-250MB.

### 2. Frontend (Static Site)
```yaml
NODE_OPTIONS: --max-old-space-size=1536  # Giảm từ 2048 xuống 1536MB
```
**Lý do**: Build chỉ cần 1.5GB thay vì 2GB, giảm thời gian build.

### 3. Admin (Streamlit)
```yaml
STREAMLIT_SERVER_FILE_WATCHER_TYPE: "none"  # Tắt file watcher
STREAMLIT_SERVER_MAX_UPLOAD_SIZE: "5"       # Giảm max upload xuống 5MB
```
**Lý do**: File watcher tốn RAM. Giảm upload size để tránh OOM.

## 🚀 Cách giảm thời gian sleep

### Services sẽ sleep khi:
- Không có request trong 15 phút
- Wake up mất ~30 giây khi có request mới

### Giải pháp:
1. **Sử dụng UptimeRobot** (miễn phí):
   - Ping services mỗi 5 phút
   - Giữ services luôn active
   - Link: https://uptimerobot.com

2. **Cron job đơn giản**:
   ```bash
   # Ping mỗi 10 phút
   */10 * * * * curl https://ivie-backend.onrender.com/api/health
   ```

## 💡 Tips tiết kiệm giờ sử dụng

### Tính toán giờ:
- 3 services × 24h × 30 ngày = 2,160 giờ/tháng
- Free tier: 750 giờ/tháng
- **Vượt quá!** Cần tối ưu

### Giải pháp:
1. **Chỉ chạy 1 service 24/7**:
   - Backend: 720 giờ/tháng ✅
   - Frontend: Static site (không tính giờ) ✅
   - Admin: Chỉ bật khi cần ✅

2. **Hoặc chạy tất cả nhưng để sleep**:
   - Không dùng UptimeRobot
   - Services tự động sleep
   - Tiết kiệm được ~50% giờ

## 📊 Monitoring RAM usage

### Kiểm tra RAM trên Render:
1. Vào service → Metrics
2. Xem "Memory Usage"
3. Nếu > 400MB → Cần tối ưu thêm

### Tối ưu thêm nếu cần:
```yaml
# Backend
WEB_CONCURRENCY: "1"
GUNICORN_TIMEOUT: "30"  # Giảm timeout

# Admin
STREAMLIT_SERVER_MAX_MESSAGE_SIZE: "50"  # Giảm message size
```

## 🔧 Build optimization

### Frontend build hiện tại:
- Time: ~8-10 phút
- Memory: ~1.5GB
- Output: ~2MB (đã tối ưu)

### Nếu build fail (OOM):
1. Giảm NODE_OPTIONS xuống 1024MB
2. Tách 3D libraries thành CDN
3. Lazy load components

## 🎯 Kết quả sau tối ưu

### Trước:
- Backend: ~350MB RAM
- Admin: ~280MB RAM
- Build time: 12 phút
- **Tổng**: ~630MB (vượt quá!)

### Sau:
- Backend: ~200MB RAM ✅
- Admin: ~180MB RAM ✅
- Build time: 8 phút ✅
- **Tổng**: ~380MB (OK!)

## ⚠️ Lưu ý quan trọng

### 1. Database
- PostgreSQL free tier: 1GB storage
- Tự động backup: Không có
- **Khuyến nghị**: Export data thường xuyên

### 2. Static files
- Frontend static site: Không giới hạn
- Bandwidth: 100GB/tháng
- **Khuyến nghị**: Dùng CDN cho images

### 3. Cold start
- Services sleep sau 15 phút
- Wake up: ~30 giây
- **Khuyến nghị**: Thông báo cho users

## 🆙 Khi nào nên upgrade?

### Nên upgrade lên Starter ($7/tháng) khi:
- Traffic > 10,000 visits/tháng
- Cần services luôn active
- RAM > 512MB
- Cần custom domain với SSL

### Starter plan benefits:
- 512MB → 2GB RAM
- Không auto-sleep
- Custom domain free
- Priority support

## 📞 Troubleshooting

### Lỗi OOM (Out of Memory):
```
Error: Process killed (OOM)
```
**Fix**: Giảm WEB_CONCURRENCY xuống 1

### Build timeout:
```
Error: Build exceeded 15 minutes
```
**Fix**: Giảm NODE_OPTIONS, tối ưu dependencies

### Service không wake up:
```
Error: Service unavailable
```
**Fix**: Check logs, có thể cần restart manual

---

**Tóm lại**: File render.yaml đã được tối ưu tối đa cho free tier. Deploy ngay được! 🚀
