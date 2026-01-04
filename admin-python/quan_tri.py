"""
IVIE Wedding Studio - Admin Panel
Trang quản trị đơn giản cho website cưới
"""

import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Config
API_BASE = os.getenv("API_BASE_URL", "https://ivie-be-final.onrender.com")
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "admin123")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "c525fc0204b449b541b0f0a5a4f5d9c4")

# Page config
st.set_page_config(
    page_title="IVIE Admin",
    page_icon="💒",
    layout="wide"
)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ============ LOGIN ============
def login_page():
    st.title("🔐 Đăng nhập Admin")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        
        if st.button("Đăng nhập", use_container_width=True):
            if username == ADMIN_USER and password == ADMIN_PASS:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu!")

# ============ API HELPERS ============
def api_get(endpoint):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=30)
        return r.json() if r.ok else []
    except:
        return []

def api_post(endpoint, data):
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=30)
        return r.ok, r.json() if r.ok else r.text
    except Exception as e:
        return False, str(e)

def api_put(endpoint, data):
    try:
        r = requests.put(f"{API_BASE}{endpoint}", json=data, timeout=30)
        return r.ok, r.json() if r.ok else r.text
    except Exception as e:
        return False, str(e)

def api_delete(endpoint):
    try:
        r = requests.delete(f"{API_BASE}{endpoint}", timeout=30)
        return r.ok
    except:
        return False

# ============ UPLOAD ẢNH ============
def upload_image(file_bytes, file_name):
    """Upload ảnh lên ImgBB và trả về URL"""
    if file_bytes is None:
        return None
    
    try:
        # Encode base64
        base64_image = base64.b64encode(file_bytes).decode('utf-8')
        
        # Upload lên ImgBB
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": IMGBB_API_KEY,
                "image": base64_image,
                "name": file_name
            },
            timeout=60
        )
        
        if response.ok:
            data = response.json()
            if data.get("success"):
                return data["data"]["url"]
            else:
                st.error(f"ImgBB error: {data.get('error', {}).get('message', 'Unknown')}")
        else:
            st.error(f"HTTP error: {response.status_code}")
        return None
    except Exception as e:
        st.error(f"Lỗi upload: {e}")
        return None

def image_uploader(label="Chọn ảnh", key=None):
    """Component upload ảnh với preview"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            label, 
            type=["jpg", "jpeg", "png", "gif", "webp"],
            key=key
        )
    
    with col2:
        image_url = st.text_input("Hoặc nhập URL", key=f"{key}_url" if key else "url_input")
    
    # Preview và lưu bytes ngay khi có file
    if uploaded_file:
        # Đọc bytes ngay và lưu vào session state
        file_bytes = uploaded_file.getvalue()
        file_name = uploaded_file.name
        st.image(file_bytes, width=200, caption="Preview")
        return {"file_bytes": file_bytes, "file_name": file_name, "url": None}
    elif image_url:
        try:
            st.image(image_url, width=200, caption="Preview từ URL")
        except:
            pass
        return {"file_bytes": None, "file_name": None, "url": image_url}
    
    return {"file_bytes": None, "file_name": None, "url": None}

def get_image_url(image_data):
    """Lấy URL từ file upload hoặc URL nhập tay"""
    if image_data.get("file_bytes"):
        with st.spinner("Đang upload ảnh..."):
            url = upload_image(image_data["file_bytes"], image_data["file_name"])
            if url:
                st.success("✅ Upload thành công!")
                return url
            else:
                st.error("❌ Upload thất bại!")
                return None
    elif image_data.get("url"):
        return image_data["url"]
    return None


# ============ DASHBOARD ============
def dashboard():
    st.title("📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Lấy dữ liệu
    products = api_get("/api/san_pham/")
    orders = api_get("/api/don_hang/")
    users = api_get("/api/nguoi_dung/")
    contacts = api_get("/api/lien_he/")
    
    with col1:
        st.metric("🛍️ Sản phẩm", len(products) if isinstance(products, list) else 0)
    with col2:
        st.metric("📦 Đơn hàng", len(orders) if isinstance(orders, list) else 0)
    with col3:
        st.metric("👥 Người dùng", len(users) if isinstance(users, list) else 0)
    with col4:
        st.metric("📞 Liên hệ", len(contacts) if isinstance(contacts, list) else 0)
    
    st.divider()
    
    # Đơn hàng gần đây
    st.subheader("📦 Đơn hàng gần đây")
    if orders and isinstance(orders, list) and len(orders) > 0:
        import pandas as pd
        df = pd.DataFrame(orders[:10])
        if not df.empty:
            cols = ["id", "customer_name", "customer_phone", "total_amount", "status", "created_at"]
            cols = [c for c in cols if c in df.columns]
            st.dataframe(df[cols], use_container_width=True)
    else:
        st.info("Chưa có đơn hàng nào")

# ============ QUẢN LÝ SẢN PHẨM ============
def quan_ly_san_pham():
    st.title("👗 Quản lý Sản phẩm")
    
    tab1, tab2 = st.tabs(["📋 Danh sách", "➕ Thêm mới"])
    
    with tab1:
        products = api_get("/api/san_pham/")
        if products and isinstance(products, list):
            for p in products:
                with st.expander(f"#{p.get('id')} - {p.get('name', 'N/A')}"):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if p.get('image_url'):
                            st.image(p['image_url'], width=150)
                    with col2:
                        st.write(f"**Mã:** {p.get('code', 'N/A')}")
                        st.write(f"**Danh mục:** {p.get('category', 'N/A')}")
                        st.write(f"**Giá thuê/ngày:** {p.get('rental_price_day', 0):,}đ")
                        st.write(f"**Giá bán:** {p.get('sale_price', 0):,}đ")
                        
                        if st.button(f"🗑️ Xóa", key=f"del_{p.get('id')}"):
                            if api_delete(f"/api/san_pham/{p.get('id')}"):
                                st.success("Đã xóa!")
                                st.rerun()
                            else:
                                st.error("Lỗi khi xóa!")
        else:
            st.info("Chưa có sản phẩm nào")
    
    with tab2:
        st.subheader("➕ Thêm sản phẩm mới")
        
        name = st.text_input("Tên sản phẩm *")
        code = st.text_input("Mã sản phẩm *")
        category = st.selectbox("Danh mục", ["Váy cưới", "Vest", "Áo dài", "Phụ kiện"])
        gender = st.selectbox("Giới tính", ["Nữ", "Nam", "Unisex"])
        
        col1, col2 = st.columns(2)
        with col1:
            rental_price = st.number_input("Giá thuê/ngày", min_value=0, step=100000)
        with col2:
            sale_price = st.number_input("Giá bán", min_value=0, step=100000)
        
        st.write("**Hình ảnh sản phẩm:**")
        image_data = image_uploader("Chọn ảnh sản phẩm", key="product_img")
        
        description = st.text_area("Mô tả")
        
        if st.button("➕ Thêm sản phẩm", use_container_width=True):
            if name and code:
                image_url = get_image_url(image_data)
                
                data = {
                    "name": name,
                    "code": code,
                    "category": category,
                    "gender": gender,
                    "rental_price_day": rental_price,
                    "sale_price": sale_price,
                    "image_url": image_url or "",
                    "description": description,
                    "is_available": True
                }
                ok, res = api_post("/api/san_pham/", data)
                if ok:
                    st.success("✅ Thêm sản phẩm thành công!")
                    st.rerun()
                else:
                    st.error(f"❌ Lỗi: {res}")
            else:
                st.warning("⚠️ Vui lòng nhập tên và mã sản phẩm!")


# ============ QUẢN LÝ ĐƠN HÀNG ============
def quan_ly_don_hang():
    st.title("📦 Quản lý Đơn hàng")
    
    orders = api_get("/api/don_hang/")
    
    if orders and isinstance(orders, list) and len(orders) > 0:
        # Filter
        status_filter = st.selectbox("Lọc theo trạng thái", 
            ["Tất cả", "pending", "confirmed", "completed", "cancelled"])
        
        filtered = orders
        if status_filter != "Tất cả":
            filtered = [o for o in orders if o.get("status") == status_filter]
        
        for order in filtered:
            with st.expander(f"🧾 Đơn #{order.get('id')} - {order.get('customer_name', 'N/A')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Khách hàng:** {order.get('customer_name')}")
                    st.write(f"**SĐT:** {order.get('customer_phone')}")
                    st.write(f"**Email:** {order.get('customer_email', 'N/A')}")
                    st.write(f"**Địa chỉ:** {order.get('customer_address', 'N/A')}")
                
                with col2:
                    st.write(f"**Tổng tiền:** {order.get('total_amount', 0):,}đ")
                    st.write(f"**Ngày tạo:** {order.get('created_at', 'N/A')}")
                    
                    current_status = order.get('status', 'pending')
                    new_status = st.selectbox(
                        "Trạng thái",
                        ["pending", "confirmed", "completed", "cancelled"],
                        index=["pending", "confirmed", "completed", "cancelled"].index(current_status),
                        key=f"status_{order.get('id')}"
                    )
                    
                    if new_status != current_status:
                        if st.button(f"💾 Cập nhật", key=f"update_{order.get('id')}"):
                            ok, res = api_put(f"/api/don_hang/{order.get('id')}", {"status": new_status})
                            if ok:
                                st.success("Đã cập nhật!")
                                st.rerun()
                            else:
                                st.error(f"Lỗi: {res}")
    else:
        st.info("Chưa có đơn hàng nào")

# ============ QUẢN LÝ NGƯỜI DÙNG ============
def quan_ly_nguoi_dung():
    st.title("👥 Quản lý Người dùng")
    
    users = api_get("/api/nguoi_dung/")
    
    if users and isinstance(users, list) and len(users) > 0:
        import pandas as pd
        df = pd.DataFrame(users)
        
        # Ẩn password
        if 'password' in df.columns:
            df = df.drop(columns=['password'])
        if 'hashed_password' in df.columns:
            df = df.drop(columns=['hashed_password'])
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Chưa có người dùng nào")

# ============ QUẢN LÝ LIÊN HỆ ============
def quan_ly_lien_he():
    st.title("📞 Quản lý Liên hệ")
    
    contacts = api_get("/api/lien_he/")
    
    if contacts and isinstance(contacts, list) and len(contacts) > 0:
        for c in contacts:
            with st.expander(f"📧 {c.get('name', 'N/A')} - {c.get('email', 'N/A')}"):
                st.write(f"**Tên:** {c.get('name')}")
                st.write(f"**Email:** {c.get('email')}")
                st.write(f"**SĐT:** {c.get('phone', 'N/A')}")
                st.write(f"**Nội dung:** {c.get('message', 'N/A')}")
                st.write(f"**Ngày gửi:** {c.get('created_at', 'N/A')}")
                
                if st.button(f"🗑️ Xóa", key=f"del_contact_{c.get('id')}"):
                    if api_delete(f"/api/lien_he/{c.get('id')}"):
                        st.success("Đã xóa!")
                        st.rerun()
    else:
        st.info("Chưa có liên hệ nào")

# ============ QUẢN LÝ THƯ VIỆN ============
def quan_ly_thu_vien():
    st.title("📸 Quản lý Thư viện ảnh")
    
    gallery = api_get("/api/thu_vien/")
    
    tab1, tab2 = st.tabs(["📋 Danh sách", "➕ Thêm mới"])
    
    with tab1:
        if gallery and isinstance(gallery, list) and len(gallery) > 0:
            cols = st.columns(4)
            for i, img in enumerate(gallery):
                with cols[i % 4]:
                    if img.get('image_url'):
                        st.image(img['image_url'], use_container_width=True)
                    st.caption(img.get('title', 'N/A'))
                    if st.button("🗑️", key=f"del_img_{img.get('id')}"):
                        if api_delete(f"/api/thu_vien/{img.get('id')}"):
                            st.rerun()
        else:
            st.info("Chưa có ảnh nào")
    
    with tab2:
        st.subheader("➕ Thêm ảnh mới")
        
        title = st.text_input("Tiêu đề")
        category = st.selectbox("Danh mục", ["Váy cưới", "Vest", "Áo dài", "Studio", "Outdoor"])
        
        st.write("**Hình ảnh:**")
        image_data = image_uploader("Chọn ảnh", key="gallery_img")
        
        if st.button("➕ Thêm ảnh", use_container_width=True):
            image_url = get_image_url(image_data)
            if image_url:
                data = {"title": title, "image_url": image_url, "category": category}
                ok, res = api_post("/api/thu_vien/", data)
                if ok:
                    st.success("✅ Thêm ảnh thành công!")
                    st.rerun()
                else:
                    st.error(f"❌ Lỗi: {res}")
            else:
                st.warning("⚠️ Vui lòng chọn ảnh hoặc nhập URL!")


# ============ QUẢN LÝ BANNER ============
def quan_ly_banner():
    st.title("🖼️ Quản lý Banner")
    
    banners = api_get("/api/anh_bia/")
    
    tab1, tab2 = st.tabs(["📋 Danh sách", "➕ Thêm mới"])
    
    with tab1:
        if banners and isinstance(banners, list) and len(banners) > 0:
            for b in banners:
                with st.expander(f"Banner #{b.get('id')} - {b.get('title', 'N/A')}"):
                    if b.get('image_url'):
                        st.image(b['image_url'], use_container_width=True)
                    st.write(f"**Tiêu đề:** {b.get('title')}")
                    st.write(f"**Link:** {b.get('link', 'N/A')}")
                    st.write(f"**Active:** {'✅' if b.get('is_active') else '❌'}")
                    
                    if st.button(f"🗑️ Xóa", key=f"del_banner_{b.get('id')}"):
                        if api_delete(f"/api/anh_bia/{b.get('id')}"):
                            st.success("Đã xóa!")
                            st.rerun()
        else:
            st.info("Chưa có banner nào")
    
    with tab2:
        st.subheader("➕ Thêm banner mới")
        
        title = st.text_input("Tiêu đề")
        link = st.text_input("Link (khi click)")
        is_active = st.checkbox("Hiển thị", value=True)
        
        st.write("**Hình ảnh banner:**")
        image_data = image_uploader("Chọn ảnh banner", key="banner_img")
        
        if st.button("➕ Thêm banner", use_container_width=True):
            image_url = get_image_url(image_data)
            if image_url:
                data = {"title": title, "image_url": image_url, "link": link, "is_active": is_active}
                ok, res = api_post("/api/anh_bia/", data)
                if ok:
                    st.success("✅ Thêm banner thành công!")
                    st.rerun()
                else:
                    st.error(f"❌ Lỗi: {res}")
            else:
                st.warning("⚠️ Vui lòng chọn ảnh hoặc nhập URL!")

# ============ CÀI ĐẶT ============
def cai_dat():
    st.title("⚙️ Cài đặt")
    
    st.subheader("🔗 Kết nối API")
    st.code(API_BASE)
    
    # Test connection
    if st.button("🔄 Test kết nối"):
        try:
            r = requests.get(f"{API_BASE}/api/health", timeout=10)
            if r.ok:
                st.success(f"✅ Kết nối thành công! {r.json()}")
            else:
                st.error(f"❌ Lỗi: {r.status_code}")
        except Exception as e:
            st.error(f"❌ Không thể kết nối: {e}")
    
    st.divider()
    
    st.subheader("🔐 Đổi mật khẩu")
    st.info("Để đổi mật khẩu, sửa file .env trên server")
    
    st.divider()
    
    if st.button("🚪 Đăng xuất"):
        st.session_state.logged_in = False
        st.rerun()

# ============ MAIN ============
def main():
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar menu
    st.sidebar.title("💒 IVIE Admin")
    st.sidebar.divider()
    
    menu = st.sidebar.radio(
        "Menu",
        ["📊 Dashboard", "👗 Sản phẩm", "📦 Đơn hàng", "👥 Người dùng", 
         "📞 Liên hệ", "📸 Thư viện", "🖼️ Banner", "⚙️ Cài đặt"]
    )
    
    st.sidebar.divider()
    st.sidebar.caption(f"API: {API_BASE}")
    
    # Route
    if menu == "📊 Dashboard":
        dashboard()
    elif menu == "👗 Sản phẩm":
        quan_ly_san_pham()
    elif menu == "📦 Đơn hàng":
        quan_ly_don_hang()
    elif menu == "👥 Người dùng":
        quan_ly_nguoi_dung()
    elif menu == "📞 Liên hệ":
        quan_ly_lien_he()
    elif menu == "📸 Thư viện":
        quan_ly_thu_vien()
    elif menu == "🖼️ Banner":
        quan_ly_banner()
    elif menu == "⚙️ Cài đặt":
        cai_dat()

if __name__ == "__main__":
    main()
