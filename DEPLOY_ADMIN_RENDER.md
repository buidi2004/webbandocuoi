# 🚀 Deploy Admin Panel (Streamlit) Lên Render

## 📋 Tổng Quan

Admin panel là ứng dụng Python Streamlit để quản lý website. Deploy lên Render miễn phí.

**Thời gian:** ~10 phút

---

## 🔧 BƯỚC 1: Tạo Web Service

1. **Vào Render Dashboard:** https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Chọn **"Build and deploy from a Git repository"**
4. Click **"Next"**
5. Chọn repo **webbandocuoi** → Click **"Connect"**

---

## ⚙️ BƯỚC 2: Cấu Hình Service

Điền thông tin:

| Field | Giá Trị |
|-------|---------|
| **Name** | `ivie-admin` |
| **Region** | `Singapore` |
| **Branch** | `main` |
| **Root Directory** | `admin-python` ⚠️ QUAN TRỌNG! |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run quan_tri.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true` |
| **Plan** | **Free** ⭐ |

---

## 🔐 BƯỚC 3: Thêm Environment Variables

Click **"Add Environment Variable"** và thêm:

### DATABASE_URL
```
Key: DATABASE_URL
Value: <paste Internal Database URL từ Render PostgreSQL>
```

### PORT
```
Key: PORT
Value: 8501
```

### PYTHON_VERSION
```
Key: PYTHON_VERSION
Value: 3.12.0
```

### ADMIN_USERNAME (Tùy chọn)
```
Key: ADMIN_USERNAME
Value: admin
```

### ADMIN_PASSWORD (Tùy chọn)
```
Key: ADMIN_PASSWORD
Value: <your_secure_password>
```

---

## 🚀 BƯỚC 4: Deploy

1. Click **"Create Web Service"**
2. Render sẽ build và deploy (5-10 phút)
3. Theo dõi logs trong tab **"Logs"**

---

## ✅ BƯỚC 5: Kiểm Tra

Sau khi deploy thành công:

1. **Copy URL Admin:**
   - Ví dụ: `https://ivie-admin.onrender.com`

2. **Mở browser và truy cập:**
   - Vào URL Admin
   - Đăng nhập bằng username/password

3. **Test chức năng:**
   - Xem danh sách sản phẩm
   - Thêm/sửa/xóa dữ liệu
   - Kiểm tra analytics

---

## 🔒 BƯỚC 6: Bảo Mật (Quan Trọng!)

### 6.1. Thêm Authentication

Streamlit không có auth mặc định. Cần thêm:

**Option 1: Dùng Streamlit-Authenticator**
```python
# Đã có trong admin-python/auth.py
import streamlit_authenticator as stauth
```

**Option 2: Dùng Basic Auth của Render**
- Vào service Settings
- Scroll xuống "HTTP Basic Auth"
- Enable và set username/password

### 6.2. Giới Hạn Truy Cập

**Không share URL Admin công khai!**
- Chỉ dùng cho admin
- Có thể whitelist IP nếu cần

---

## 🐛 Troubleshooting

### Lỗi: Build Failed

**Nguyên nhân:** Thiếu dependencies

**Giải pháp:**
1. Kiểm tra `admin-python/requirements.txt`
2. Đảm bảo có:
```
streamlit==1.28.0
pandas==2.1.3
plotly==5.18.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
python-dotenv==1.0.0
streamlit-authenticator==0.2.3
```

### Lỗi: Application Failed to Start

**Nguyên nhân:** Start command sai

**Giải pháp:**
Đảm bảo Start Command:
```bash
streamlit run quan_tri.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

### Lỗi: Database Connection Failed

**Nguyên nhân:** DATABASE_URL sai

**Giải pháp:**
1. Dùng **Internal Database URL** từ PostgreSQL service
2. Format: `postgresql://user:password@host:port/database`

### Lỗi: Port Already in Use

**Nguyên nhân:** Port config sai

**Giải pháp:**
- Đảm bảo dùng `$PORT` trong Start Command
- Không hardcode port 8501

---

## 💡 Tips Tối Ưu

### 1. Tăng Tốc Load

Thêm vào đầu `quan_tri.py`:
```python
import streamlit as st

st.set_page_config(
    page_title="IVIE Admin",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### 2. Cache Data

Dùng `@st.cache_data` cho queries:
```python
@st.cache_data(ttl=300)  # Cache 5 phút
def load_products():
    # Query database
    return products
```

### 3. Giảm Cold Start

Admin ít traffic → Sẽ sleep sau 15 phút.
Chấp nhận cold start hoặc dùng UptimeRobot ping.

---

## 📊 Monitoring

### Xem Logs

1. Vào Render Dashboard
2. Chọn Admin service
3. Tab **"Logs"** → Real-time logs
4. Tab **"Metrics"** → CPU, Memory

### Restart Service

Nếu bị lỗi:
1. Tab **"Settings"**
2. Click **"Manual Deploy"**
3. Chọn **"Clear build cache & deploy"**

---

## 🔗 Kết Nối Với Backend

Admin và Backend dùng chung Database:
- ✅ Admin thay đổi data → Backend thấy ngay
- ✅ Backend thay đổi data → Admin thấy ngay
- ✅ Không cần sync

---

## 📝 Checklist Deploy

### Chuẩn Bị
- [ ] Có PostgreSQL database trên Render
- [ ] Có DATABASE_URL
- [ ] File `admin-python/requirements.txt` đầy đủ
- [ ] File `admin-python/quan_tri.py` hoạt động local

### Deploy
- [ ] Tạo Web Service
- [ ] Set Root Directory = `admin-python`
- [ ] Set Runtime = Python 3
- [ ] Set Build Command
- [ ] Set Start Command đúng
- [ ] Thêm DATABASE_URL
- [ ] Thêm PORT = 8501
- [ ] Bật Auto-Deploy

### Kiểm Tra
- [ ] Build thành công
- [ ] Service status = Live
- [ ] Truy cập URL được
- [ ] Đăng nhập được
- [ ] Xem data được
- [ ] Thêm/sửa/xóa hoạt động

---

## 🎉 Kết Luận

Bạn đã deploy thành công Admin Panel!

**URLs:**
- Admin: `https://ivie-admin.onrender.com`
- Backend: `https://webbandocuoi.onrender.com`
- Frontend: `https://ivie-wedding-frontend.vercel.app`
- Database: PostgreSQL trên Render

**Tổng chi phí:** $0/tháng 🎉

---

## 🔐 Bảo Mật Quan Trọng

⚠️ **KHÔNG BAO GIỜ:**
- Share URL Admin công khai
- Commit password vào Git
- Dùng password yếu

✅ **NÊN:**
- Dùng password mạnh (12+ ký tự)
- Enable 2FA cho Render account
- Thường xuyên đổi password
- Backup database định kỳ

---

## 📚 Tài Liệu Tham Khảo

- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Render Web Services](https://render.com/docs/web-services)
- [Streamlit Configuration](https://docs.streamlit.io/library/advanced-features/configuration)
