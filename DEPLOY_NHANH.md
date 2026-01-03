# 🚀 TÓM TẮT NHANH - DEPLOY LÊN RENDER

## ⚡ 3 LINK QUAN TRỌNG

### 1. Đăng ký/Đăng nhập Render

```
https://dashboard.render.com
```

👉 Click "Continue with GitHub"

### 2. Tạo Blueprint

```
https://dashboard.render.com/blueprints/new
```

👉 Chọn repo: `buidi2004/webbandocuoi`

### 3. Xem Services đã deploy

```
https://dashboard.render.com
```

---

## 📋 CHECKLIST 1 PHÚT

```
☐ 1. Đăng nhập Render bằng GitHub
☐ 2. Tạo Blueprint từ repo buidi2004/webbandocuoi
☐ 3. Đợi 5-10 phút
☐ 4. Kiểm tra 3 URLs:
     - Backend:  https://ivie-be-final.onrender.com/docs
     - Frontend: https://ivie-fe-final.onrender.com
     - Admin:    https://ivie-ad-final.onrender.com
```

---

## 🎯 KẾT QUẢ

Sau khi deploy xong, bạn sẽ có:

| Service | URL | Test |
|---------|-----|------|
| **Backend API** | <https://ivie-be-final.onrender.com> | `/docs` |
| **Frontend** | <https://ivie-fe-final.onrender.com> | Trang chủ |
| **Admin** | <https://ivie-ad-final.onrender.com> | Login: admin/admin123 |
| **Database** | Internal | PostgreSQL Free |

---

## ⚠️ LƯU Ý GÓI MIỄN PHÍ

- ⏰ Service ngủ sau 15 phút không hoạt động
- 🐌 Lần đầu truy cập chờ 30-60 giây
- 💾 RAM: 512MB/service
- 📊 Bandwidth: 100GB/tháng

---

## 🔄 UPDATE CODE

```bash
git add .
git commit -m "update: ..."
git push origin main
# → Render tự động deploy lại
```

---

## 📚 HƯỚNG DẪN CHI TIẾT

Xem file: `HUONG_DAN_DEPLOY_CHI_TIET.md`

Hoặc: `DEPLOY_RENDER_3_BUOC.md`

---

**✅ DONE! Chỉ cần 3 bước là xong!**
