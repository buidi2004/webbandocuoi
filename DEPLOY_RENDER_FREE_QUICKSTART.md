# 🚀 DEPLOY NHANH LÊN RENDER (GÓI MIỄN PHÍ)

## ⚡ Quick Start (5 phút)

### Bước 1: Chuẩn bị
```bash
# Push code lên GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Bước 2: Deploy trên Render
1. Vào https://render.com và đăng nhập bằng GitHub
2. Click **"New +"** → **"Blueprint"**
3. Chọn repository của bạn
4. Render sẽ tự động đọc file `render.yaml` và deploy

### Bước 3: Đợi deploy hoàn tất
- ⏱️ Database: 1-2 phút
- ⏱️ Backend: 3-5 phút
- ⏱️ Frontend: 5-8 phút
- ⏱️ Admin: 3-4 phút
- **Tổng**: ~15-20 phút

### Bước 4: Truy cập
- Frontend: `https://ivie-frontend.onrender.com`
- Admin: `https://ivie-admin.onrender.com` (admin/admin123)
- API: `https://ivie-backend.onrender.com/docs`

---

## ✅ Đã tối ưu cho FREE TIER

### Giới hạn gói miễn phí
| Thông số | Giới hạn | Dự án này |
|----------|----------|-----------|
| RAM | 512MB | 200MB (Backend) + 180MB (Admin) = 380MB ✅ |
| Build time | 15 phút | 3-8 phút ✅ |
| Hours | 750h/tháng | ~400h/tháng (có sleep) ✅ |
| Database | 1GB | ~100MB (đủ 10k đơn) ✅ |

### Tối ưu đã áp dụng
- ✅ **1 worker** thay vì 2 → Tiết kiệm 50% RAM
- ✅ **Tắt file watcher** → Tiết kiệm 30-50MB RAM
- ✅ **Giảm timeout** → Response nhanh hơn
- ✅ **Auto-restart workers** → Dọn memory leak
- ✅ **Static frontend** → Không tính giờ sử dụng
- ✅ **CDN caching** → Load nhanh toàn cầu

---

## 🔄 Giữ service luôn active

### Option 1: UptimeRobot (Khuyến nghị)
1. Đăng ký: https://uptimerobot.com (miễn phí)
2. Tạo 2 monitors:
   - `https://ivie-backend.onrender.com/api/health` (5 phút)
   - `https://ivie-admin.onrender.com/_stcore/health` (5 phút)

### Option 2: GitHub Actions
```yaml
# .github/workflows/keep-alive.yml
name: Keep Alive
on:
  schedule:
    - cron: '*/10 * * * *'
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - run: curl https://ivie-backend.onrender.com/api/health
      - run: curl https://ivie-admin.onrender.com/_stcore/health
```

---

## 🐛 Troubleshooting nhanh

### Lỗi: Build timeout
```yaml
# Giảm NODE_OPTIONS trong render.yaml
NODE_OPTIONS: --max-old-space-size=1024  # Thay vì 1200
```

### Lỗi: Out of Memory
```yaml
# Đã set WEB_CONCURRENCY=1, nếu vẫn lỗi:
MAX_REQUESTS: "250"  # Thay vì 500
```

### Lỗi: CORS
```yaml
# Thêm domain vào CORS_ORIGINS trong render.yaml
CORS_ORIGINS: https://ivie-frontend.onrender.com,https://yourdomain.com
```

### Lỗi: Database connection
```bash
# Kiểm tra DATABASE_URL trong Backend Environment
# Phải có dạng: postgresql://user:pass@host/db
```

---

## 📊 Monitoring

### Kiểm tra RAM usage
1. Vào service → **Metrics**
2. Memory Usage nên < 400MB
3. Nếu > 450MB → Risk OOM

### Kiểm tra logs
```bash
# Render Dashboard → Service → Logs
# Hoặc dùng Render CLI:
render logs -s ivie-backend --tail
```

---

## ⚠️ Lưu ý quan trọng

### 1. Auto-sleep sau 15 phút
- Services sẽ sleep khi không dùng
- Cold start: 20-40 giây
- **Giải pháp**: Dùng UptimeRobot để ping

### 2. 750 giờ/tháng
- 3 services × 24h × 30 days = 2,160 giờ ❌
- **Giải pháp**: Để sleep hoặc chỉ giữ Backend active
- Frontend (static) không tính giờ ✅

### 3. Database backup
- Free tier không có auto-backup
- **Giải pháp**: Export thủ công mỗi tuần
```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### 4. Đổi mật khẩu admin
```
Login: https://ivie-admin.onrender.com
User: admin
Pass: admin123
→ Vào Settings → Đổi mật khẩu ngay!
```

---

## 📖 Tài liệu chi tiết

Xem file `HUONG_DAN_DEPLOY_RENDER_FREE.md` để biết:
- Hướng dẫn từng bước chi tiết
- Troubleshooting đầy đủ
- Best practices
- Advanced configurations

---

## 🎯 Checklist sau deploy

- [ ] Tất cả services status = **Live** (màu xanh)
- [ ] Frontend hiển thị đúng
- [ ] Admin login được
- [ ] Test đặt hàng thành công
- [ ] Đổi mật khẩu admin
- [ ] Setup UptimeRobot monitoring
- [ ] Export database backup đầu tiên
- [ ] Test trên mobile

---

## 💡 Tips tối ưu thêm

### 1. Giảm cold start time
```python
# Thêm vào backend/__init__.py
import sys
sys.dont_write_bytecode = True  # Không tạo .pyc files
```

### 2. Tối ưu database queries
```python
# Thêm indexes cho các trường thường query
class DonHang(Base):
    __table_args__ = (
        Index('idx_trang_thai', 'trang_thai'),
        Index('idx_ngay_tao', 'ngay_tao'),
    )
```

### 3. Compress images trước upload
```python
from PIL import Image

def compress_image(image_path, max_width=1920, quality=85):
    img = Image.open(image_path)
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    img.save(image_path, quality=quality, optimize=True)
```

---

## 🆙 Khi nào nên upgrade?

### Nên upgrade lên Starter ($7/tháng) khi:
- ✅ Traffic > 10,000 visits/tháng
- ✅ Cần services luôn active (không sleep)
- ✅ RAM > 512MB
- ✅ Cần custom domain + SSL
- ✅ Cần priority support

### Starter plan benefits:
- 512MB → **2GB RAM**
- **Không auto-sleep**
- **Custom domain** miễn phí
- **Priority support**
- **Faster builds**

---

## 📞 Hỗ trợ

- 📚 Docs: https://render.com/docs
- 💬 Community: https://community.render.com
- 📧 Support: dashboard.render.com → Help
- 🐙 GitHub Issues: Tạo issue trong repo

---

## ✅ Kết quả mong đợi

Sau khi deploy thành công:

```
✅ Backend API: https://ivie-backend.onrender.com
   - RAM usage: ~200MB
   - Response time: < 500ms
   - Uptime: 99.9% (với UptimeRobot)

✅ Frontend: https://ivie-frontend.onrender.com
   - Load time: < 2s
   - Always active (static site)
   - CDN cached globally

✅ Admin: https://ivie-admin.onrender.com
   - RAM usage: ~180MB
   - Streamlit dashboard
   - Full CRUD operations

✅ Database: PostgreSQL 1GB
   - Tables initialized
   - Connections: 97 max
   - Backup: Manual (weekly)
```

---

**🎉 Chúc bạn deploy thành công!**

*Made with ❤️ for IVIE Wedding Studio*

---

## 🔗 Quick Links

- [Hướng dẫn chi tiết](HUONG_DAN_DEPLOY_RENDER_FREE.md)
- [Tối ưu Free Tier](RENDER_FREE_TIER_OPTIMIZATION.md)
- [Deploy Guide](DEPLOY_GUIDE.md)
- [Render Dashboard](https://dashboard.render.com)
- [UptimeRobot](https://uptimerobot.com)