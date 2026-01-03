# 🔗 Fix Frontend-Backend Connection

## 🎯 Vấn Đề Hiện Tại

Frontend (Vercel) và Backend (Render) chưa kết nối được với nhau.

**Nguyên nhân:**
1. ❌ Backend CORS chưa cho phép domain Vercel
2. ⚠️ Frontend environment variable cần kiểm tra

---

## ✅ GIẢI PHÁP - 2 BƯỚC

### 📍 BƯỚC 1: Cập Nhật CORS Trong Backend (Render)

Backend hiện tại chỉ cho phép localhost. Cần thêm domain Vercel của bạn.

#### 1.1. Lấy Domain Frontend

Vào Vercel Dashboard → Chọn project Frontend → Copy domain (ví dụ: `https://ivie-wedding.vercel.app`)

#### 1.2. Thêm Environment Variable Trong Render

1. Vào **Render Dashboard**: https://dashboard.render.com
2. Chọn service **Backend** (ivie-be-final)
3. Tab **"Environment"**
4. Tìm biến `CORS_ORIGINS` (nếu chưa có thì thêm mới)
5. Click **"Add Environment Variable"**:

```
Key: CORS_ORIGINS
Value: https://ivie-wedding.vercel.app,http://localhost:5173,http://localhost:3000
```

**⚠️ LƯU Ý:**
- Thay `https://ivie-wedding.vercel.app` bằng domain Vercel thực tế của bạn
- Các domain cách nhau bằng dấu phẩy (,)
- KHÔNG có khoảng trắng
- KHÔNG có dấu / ở cuối

#### 1.3. Save & Redeploy

1. Click **"Save Changes"**
2. Render sẽ tự động redeploy Backend (chờ 2-3 phút)
3. Kiểm tra logs để đảm bảo deploy thành công

---

### 📍 BƯỚC 2: Kiểm Tra Environment Variable Trong Vercel

Frontend cần biết địa chỉ Backend để gọi API.

#### 2.1. Lấy URL Backend

Vào Render Dashboard → Chọn Backend service → Copy URL (ví dụ: `https://ivie-be-final.onrender.com`)

#### 2.2. Kiểm Tra Environment Variable

1. Vào **Vercel Dashboard**: https://vercel.com/dashboard
2. Chọn project **Frontend**
3. Tab **"Settings"** → **"Environment Variables"**
4. Tìm biến `VITE_API_URL`

**Nếu ĐÃ CÓ `VITE_API_URL`:**
- Kiểm tra giá trị có đúng URL Backend không
- Ví dụ: `https://ivie-be-final.onrender.com`
- **KHÔNG có dấu / ở cuối**

**Nếu CHƯA CÓ:**
- Click **"Add New"**
- Key: `VITE_API_URL`
- Value: `https://ivie-be-final.onrender.com` (thay bằng URL Backend thực tế)
- Environment: **Production**, **Preview**, **Development** (chọn cả 3)
- Click **"Save"**

#### 2.3. Redeploy Frontend

1. Tab **"Deployments"**
2. Click **"..."** ở deployment mới nhất
3. Click **"Redeploy"**
4. Chờ 1-2 phút

---

## 🧪 BƯỚC 3: Kiểm Tra Kết Nối

### 3.1. Test Backend CORS

Mở browser console (F12) trên trang Frontend, chạy:

```javascript
fetch('https://ivie-be-final.onrender.com/api/health')
  .then(r => r.json())
  .then(d => console.log('✅ Backend OK:', d))
  .catch(e => console.error('❌ Backend Error:', e))
```

**Kết quả mong đợi:**
```
✅ Backend OK: {status: "healthy"}
```

**Nếu lỗi CORS:**
```
❌ Access to fetch at '...' from origin '...' has been blocked by CORS policy
```
→ Quay lại Bước 1, kiểm tra lại `CORS_ORIGINS`

### 3.2. Test API Call

Trên trang Frontend, thử một chức năng gọi API (ví dụ: xem sản phẩm, đăng nhập, v.v.)

**Nếu thành công:**
- ✅ Dữ liệu hiển thị bình thường
- ✅ Không có lỗi trong console

**Nếu thất bại:**
- ❌ Kiểm tra Network tab (F12) → Xem request có gọi đúng URL không
- ❌ Kiểm tra Console → Xem lỗi cụ thể

---

## 🐛 Troubleshooting

### Lỗi: CORS Policy Blocked

**Triệu chứng:**
```
Access to fetch at 'https://ivie-be-final.onrender.com/api/...' 
from origin 'https://ivie-wedding.vercel.app' 
has been blocked by CORS policy
```

**Giải pháp:**
1. Kiểm tra `CORS_ORIGINS` trong Render có domain Vercel chưa
2. Đảm bảo domain CHÍNH XÁC (không có typo)
3. Đảm bảo Backend đã redeploy sau khi thêm biến
4. Xóa cache browser (Ctrl+Shift+Delete) và thử lại

### Lỗi: Network Error / Failed to Fetch

**Triệu chứng:**
```
TypeError: Failed to fetch
```

**Giải pháp:**
1. Kiểm tra Backend có đang chạy không:
   - Vào `https://ivie-be-final.onrender.com/api/health`
   - Nếu không load → Backend bị lỗi
2. Kiểm tra `VITE_API_URL` trong Vercel có đúng không
3. Kiểm tra Backend logs trong Render Dashboard

### Lỗi: 404 Not Found

**Triệu chứng:**
```
GET https://ivie-be-final.onrender.com/api/san_pham/ 404
```

**Giải pháp:**
1. Kiểm tra endpoint có tồn tại không:
   - Vào `https://ivie-be-final.onrender.com/docs`
   - Tìm endpoint trong Swagger UI
2. Kiểm tra đường dẫn API trong Frontend code có đúng không

### Lỗi: Cold Start (Chậm lần đầu)

**Triệu chứng:**
- Request đầu tiên mất 15-30 giây
- Các request sau nhanh hơn

**Giải pháp:**
- Đây là hành vi bình thường của Render Free tier
- Backend tự động sleep sau 15 phút không có traffic
- Dùng UptimeRobot để ping mỗi 5 phút (xem phần Bonus)

---

## 🎯 Checklist Hoàn Thành

### Backend (Render)
- [ ] Thêm `CORS_ORIGINS` environment variable
- [ ] Giá trị chứa domain Vercel chính xác
- [ ] Backend đã redeploy thành công
- [ ] Test `/api/health` endpoint hoạt động

### Frontend (Vercel)
- [ ] Có `VITE_API_URL` environment variable
- [ ] Giá trị là URL Backend chính xác
- [ ] Frontend đã redeploy thành công
- [ ] Test fetch từ browser console thành công

### Connection
- [ ] Không có lỗi CORS trong console
- [ ] API calls hoạt động bình thường
- [ ] Dữ liệu hiển thị đúng trên Frontend

---

## 🚀 Bonus: Giữ Backend Luôn Hoạt Động

Render Free tier tự động sleep sau 15 phút không có traffic. Để tránh cold start:

### Dùng UptimeRobot (Miễn Phí)

1. Đăng ký: https://uptimerobot.com
2. Tạo monitor mới:
   - Monitor Type: **HTTP(s)**
   - Friendly Name: `IVIE Backend`
   - URL: `https://ivie-be-final.onrender.com/api/health`
   - Monitoring Interval: **5 minutes**
3. Save

UptimeRobot sẽ ping Backend mỗi 5 phút → Backend không bao giờ sleep → Không có cold start!

---

## 📊 Kiểm Tra Cuối Cùng

Sau khi hoàn thành 2 bước trên, test các chức năng:

1. **Trang chủ:** Sản phẩm hiển thị đúng
2. **Chi tiết sản phẩm:** Ảnh và thông tin load được
3. **Đăng nhập:** Có thể đăng nhập/đăng ký
4. **Giỏ hàng:** Thêm sản phẩm vào giỏ
5. **Đặt hàng:** Tạo đơn hàng thành công

Nếu TẤT CẢ hoạt động → ✅ **HOÀN THÀNH!**

---

## 📝 Tóm Tắt

**2 việc cần làm:**

1. **Render (Backend):**
   ```
   CORS_ORIGINS = https://your-frontend.vercel.app,http://localhost:5173
   ```

2. **Vercel (Frontend):**
   ```
   VITE_API_URL = https://your-backend.onrender.com
   ```

**Sau đó:** Redeploy cả 2 services và test!

---

## 🆘 Cần Trợ Giúp?

Nếu vẫn gặp vấn đề:

1. **Check Backend logs:** Render Dashboard → Backend service → Logs tab
2. **Check Frontend console:** F12 → Console tab
3. **Check Network requests:** F12 → Network tab
4. **Test endpoints:** Vào `/docs` của Backend để test trực tiếp

Gửi screenshot lỗi để được hỗ trợ cụ thể hơn!
