# Tài Liệu Các Hàm Chính - Frontend IVIE Wedding Studio

## 1. Cấu Trúc Tổng Quan

```
frontend/src/
├── UngDung.jsx          # App chính, routing
├── api/                 # API clients
│   ├── khach_hang.js    # API sản phẩm, đơn hàng, liên hệ
│   └── nguoi_dung.js    # API đăng nhập, đăng ký
├── trang/               # Pages (24 trang)
└── thanh_phan/          # Components (65 components)
```

---

## 2. API Client (`api/khach_hang.js`)

### 2.1 Cấu hình Axios

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: { 'Content-Type': 'application/json' }
});
```

### 2.2 API Sản Phẩm (`sanPhamAPI`)

| Hàm | Mô tả | Endpoint |
|-----|-------|----------|
| `layTatCa(params)` | Lấy danh sách sản phẩm với filter | `GET /api/san_pham/` |
| `layTheoId(id)` | Lấy chi tiết 1 sản phẩm | `GET /api/san_pham/{id}` |
| `layDanhGia(id)` | Lấy đánh giá của sản phẩm | `GET /api/san_pham/{id}/danh_gia` |
| `guiDanhGia(id, formData)` | Gửi đánh giá mới | `POST /api/san_pham/{id}/danh_gia` |

### 2.3 API Đơn Hàng (`donHangAPI`)

| Hàm | Mô tả | Endpoint |
|-----|-------|----------|
| `tao(duLieu)` | Tạo đơn hàng mới | `POST /api/don_hang/` |
| `layTatCa()` | Lấy danh sách đơn hàng | `GET /api/don_hang/` |
| `layTheoId(id)` | Lấy chi tiết đơn hàng | `GET /api/don_hang/{id}` |
| `capNhat(id, duLieu)` | Cập nhật trạng thái | `PUT /api/don_hang/{id}` |

### 2.4 API Liên Hệ (`lienHeAPI`)

| Hàm | Mô tả | Endpoint |
|-----|-------|----------|
| `gui(duLieu)` | Gửi form liên hệ | `POST /api/lien_he` |
| `datLich(duLieu)` | Đặt lịch hẹn | `POST /api/lien_he/dat_lich` |

### 2.5 API Khác

| API | Hàm | Mô tả |
|-----|-----|-------|
| `bannerAPI` | `layTatCa()` | Lấy danh sách banner |
| `thuVienAPI` | `layTatCa()` | Lấy thư viện ảnh |
| `comboAPI` | `layTatCa()`, `layTheoId(id)` | Lấy gói combo |
| `doiTacAPI` | `dangKy()`, `layHoSo()` | Đăng ký đối tác |

### 2.6 Hàm Tiện Ích

```javascript
// Lấy URL hình ảnh đầy đủ
export const layUrlHinhAnh = (duongDan) => {
    if (!duongDan) return 'https://placehold.co/400x600/e5e5e5/333?text=No+Image';
    if (duongDan.startsWith('http')) return duongDan;
    if (duongDan.startsWith('/images')) return duongDan;
    return `${API_BASE_URL}${duongDan}`;
};
```

---

## 3. API Người Dùng (`api/nguoi_dung.js`)

| Hàm | Mô tả | Endpoint |
|-----|-------|----------|
| `dangKy(duLieu)` | Đăng ký tài khoản | `POST /api/nguoi_dung/dang_ky` |
| `dangNhap(duLieu)` | Đăng nhập | `POST /api/nguoi_dung/dang_nhap` |
| `dangNhapSocial(duLieu)` | Đăng nhập Google/Facebook | `POST /api/nguoi_dung/dang_nhap_social` |
| `layDonHang(token)` | Lấy đơn hàng của user | `GET /api/nguoi_dung/don_hang` |
| `capNhatProfile(duLieu, token)` | Cập nhật thông tin | `PUT /api/nguoi_dung/cap_nhat` |
| `kiemTraGiamGia(token)` | Kiểm tra mã giảm giá | `POST /api/nguoi_dung/kiem_tra_giam_gia` |

---

## 4. Trang Chính (`trang/TrangChu.jsx`)

### 4.1 State Management

```javascript
const [banners, setBanners] = useState([]);      // Danh sách banner
const [idxBanner, setIdxBanner] = useState(0);   // Index banner hiện tại
const [gioiThieu, setGioiThieu] = useState(null); // Nội dung giới thiệu
const [diemNhan, setDiemNhan] = useState([]);    // Điểm nhấn dịch vụ
const [thuVien, setThuVien] = useState([]);      // Thư viện ảnh
```

### 4.2 Hàm Chính

```javascript
// Lấy dữ liệu từ API khi component mount
useEffect(() => {
    const layDuLieu = async () => {
        const [resBanner, resGT, resDN, resTV] = await Promise.all([
            bannerAPI.layTatCa(),
            noiDungAPI.layGioiThieu(),
            noiDungAPI.layDiemNhan(),
            thuVienAPI.layTatCa()
        ]);
        setBanners(resBanner.data || []);
        setGioiThieu(resGT.data);
        setDiemNhan(resDN.data || []);
        setThuVien(resTV.data || []);
    };
    layDuLieu();
}, []);
```

### 4.3 Hiệu Ứng GSAP

```javascript
// Hiệu ứng Ken Burns zoom in/out cho banner
useEffect(() => {
    kenBurnsTimeline.current = gsap.timeline({ repeat: -1, yoyo: true })
        .to(imageEl, {
            scale: 1.15,
            duration: 12,
            ease: "power1.inOut"
        });
}, [idxBanner, banners.length]);

// Hiệu ứng fade-in khi scroll
useLayoutEffect(() => {
    gsap.utils.toArray('.fade-in-section').forEach(section => {
        gsap.fromTo(section,
            { opacity: 0, y: 50 },
            {
                opacity: 1, y: 0,
                scrollTrigger: { trigger: section, start: "top 85%" }
            }
        );
    });
}, []);
```

---

## 5. Trang Sản Phẩm (`trang/SanPham.jsx`)

### 5.1 State Management

```javascript
const [danhSachSanPham, setDanhSachSanPham] = useState([]); // Danh sách SP
const [dangTai, setDangTai] = useState(true);               // Loading state
const [boLoc, setBoLoc] = useState("all");                  // Filter danh mục
const [tieuMuc, setTieuMuc] = useState("all");              // Sub-category
const [phongCach, setPhongCach] = useState("all");          // Style filter
const [khoangGia, setKhoangGia] = useState("all");          // Price range
const [sapXep, setSapXep] = useState("hot");                // Sort order
const [sanPhamDaXem, setSanPhamDaXem] = useState([]);       // Viewed products
const [quickViewSP, setQuickViewSP] = useState(null);       // Quick view modal
```

### 5.2 Hàm Lấy Sản Phẩm

```javascript
const laySanPham = async (retry = 0) => {
    setDangTai(true);
    try {
        const thamSo = { sort_by: sapXep };
        if (boLoc !== "all") thamSo.danh_muc = boLoc;
        if (tieuMuc !== "all") thamSo.sub_category = tieuMuc;
        if (phongCach !== "all") thamSo.style = phongCach;
        if (khoangGia !== "all") thamSo.price_range = khoangGia;
        
        const phanHoi = await sanPhamAPI.layTatCa(thamSo);
        setDanhSachSanPham(Array.isArray(phanHoi.data) ? phanHoi.data : []);
    } catch (err) {
        // Retry nếu server đang khởi động (Render free tier)
        if (retry < 1) {
            setTimeout(() => laySanPham(retry + 1), 3000);
            return;
        }
        setLoi("Không thể tải dữ liệu sản phẩm");
    } finally {
        setDangTai(false);
    }
};
```

### 5.3 Hàm Xem Chi Tiết

```javascript
const xemChiTiet = (sp) => {
    // Lưu vào localStorage để hiển thị "Sản phẩm đã xem"
    const daXem = JSON.parse(localStorage.getItem("ivie_viewed") || "[]");
    const filtered = daXem.filter((item) => item.id !== sp.id);
    filtered.unshift({
        id: sp.id,
        name: sp.name,
        image_url: sp.image_url,
        rental_price_day: sp.rental_price_day,
    });
    localStorage.setItem("ivie_viewed", JSON.stringify(filtered.slice(0, 10)));
    navigate(`/san-pham/${sp.id}`);
};
```

### 5.4 Hàm Thêm Giỏ Hàng

```javascript
const themGioHang = (sp) => {
    const currentCart = JSON.parse(localStorage.getItem("ivie_cart") || "[]");
    const item = {
        id: sp.id,
        name: sp.name,
        code: sp.code,
        image_url: sp.image_url,
        purchase_price: sp.purchase_price,
        rental_price_day: sp.rental_price_day,
        price_to_use: sp.purchase_price,
        quantity: 1,
        loai: "mua",
        so_luong: sp.so_luong,
    };
    
    const existing = currentCart.findIndex(i => i.id === item.id && i.loai === "mua");
    if (existing > -1) {
        currentCart[existing].quantity += 1;
    } else {
        currentCart.push(item);
    }
    localStorage.setItem("ivie_cart", JSON.stringify(currentCart));
    addToast({ message: "Đã thêm vào giỏ hàng!", type: "success" });
};
```

---

## 6. Trang Giỏ Hàng (`trang/GioHang.jsx`)

### 6.1 State Management

```javascript
const [cartItems, setCartItems] = useState([]);           // Danh sách SP trong giỏ
const [deliveryType, setDeliveryType] = useState('delivery'); // Giao hàng/Nhận tại studio
const [paymentMethod, setPaymentMethod] = useState('cod');    // COD/Chuyển khoản
const [couponCode, setCouponCode] = useState('');             // Mã giảm giá
const [agreedPolicy, setAgreedPolicy] = useState(false);      // Đồng ý chính sách
const [customerInfo, setCustomerInfo] = useState({...});      // Thông tin khách
const [isSubmitted, setIsSubmitted] = useState(false);        // Đã đặt hàng
```

### 6.2 Hàm Cập Nhật Số Lượng

```javascript
const updateQuantity = (id, delta, loai) => {
    const newCart = cartItems.map(item => {
        if (item.id === id && (item.loai || 'mua') === (loai || 'mua')) {
            const newQty = Math.max(1, (item.quantity || 1) + delta);
            const maxQty = item.so_luong || 10;
            return { ...item, quantity: Math.min(newQty, maxQty) };
        }
        return item;
    });
    setCartItems(newCart);
    localStorage.setItem('ivie_cart', JSON.stringify(newCart));
};
```

### 6.3 Hàm Xóa Sản Phẩm

```javascript
const removeItem = (id, loai) => {
    const newCart = cartItems.filter(item => 
        !(item.id === id && (item.loai || 'mua') === (loai || 'mua'))
    );
    setCartItems(newCart);
    localStorage.setItem('ivie_cart', JSON.stringify(newCart));
};
```

### 6.4 Hàm Tính Tổng Tiền

```javascript
const getTotal = () => {
    return cartItems.reduce((total, item) => {
        const price = item.price_to_use || item.rental_price_day || item.purchase_price;
        return total + (price * (item.quantity || 1));
    }, 0);
};
```

### 6.5 Hàm Đặt Hàng

```javascript
const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate
    if (!agreedPolicy) {
        alert('Vui lòng đồng ý với chính sách');
        return;
    }
    
    // Tạo order data
    const orderData = {
        customer_name: customerInfo.name,
        customer_email: customerInfo.email,
        customer_phone: customerInfo.phone,
        shipping_address: customerInfo.address,
        total_amount: getTotal(),
        items: cartItems.map(item => ({
            product_id: item.id,
            quantity: item.quantity || 1,
            price: item.price_to_use,
            loai: item.loai || 'mua'
        })),
        payment_method: paymentMethod,
        delivery_type: deliveryType
    };
    
    // Gọi API
    await donHangAPI.tao(orderData);
    setIsSubmitted(true);
    localStorage.removeItem('ivie_cart');
};
```

---

## 7. Định Dạng Giá

```javascript
const dinhDangGia = (gia) => new Intl.NumberFormat("vi-VN").format(gia) + "đ";
// Ví dụ: 1500000 → "1.500.000đ"
```

---

## 8. LocalStorage Keys

| Key | Mô tả | Cấu trúc |
|-----|-------|----------|
| `ivie_cart` | Giỏ hàng | `[{id, name, quantity, price_to_use, loai}]` |
| `ivie_viewed` | SP đã xem | `[{id, name, image_url, rental_price_day}]` |
| `ivie_user` | Thông tin user | `{id, username, email, full_name, phone}` |
| `ivie_token` | JWT Token | `string` |

---

## 9. Routing (`UngDung.jsx`)

| Path | Component | Mô tả |
|------|-----------|-------|
| `/` | `TrangChu` | Trang chủ |
| `/san-pham` | `SanPham` | Danh sách sản phẩm |
| `/san-pham/:id` | `ChiTietSanPham` | Chi tiết sản phẩm |
| `/gio-hang` | `GioHang` | Giỏ hàng |
| `/dang-nhap` | `DangNhap` | Đăng nhập |
| `/dang-ky` | `DangKy` | Đăng ký |
| `/tai-khoan` | `TaiKhoan` | Tài khoản |
| `/thu-vien` | `ThuVien` | Thư viện ảnh |
| `/lien-he` | `LienHe` | Liên hệ |
| `/chon-combo` | `ChonCombo` | Chọn gói combo |
| `/blog` | `BaiViet` | Blog/Tin tức |
| `/chinh-sach` | `ChinhSach` | Chính sách |

---

## 10. Lazy Loading

```javascript
// Code splitting - chỉ load khi cần
const TrangChu = lazy(() => import('./trang/TrangChu'));
const SanPham = lazy(() => import('./trang/SanPham'));
const GioHang = lazy(() => import('./trang/GioHang'));

// Sử dụng với Suspense
<Suspense fallback={<PageLoader />}>
    <Routes>
        <Route path="/" element={<TrangChu />} />
        ...
    </Routes>
</Suspense>
```

---

## 11. Thư Viện Sử Dụng

| Thư viện | Mục đích |
|----------|----------|
| `react-router-dom` | Routing |
| `axios` | HTTP client |
| `gsap` | Animation |
| `sal.js` | Scroll animation |
| `atropos` | 3D parallax effect |

---

## 12. Biến Môi Trường

```env
VITE_API_BASE_URL=https://ivie-be-final.onrender.com
VITE_IMGBB_API_KEY=c525fc0204b449b541b0f0a5a4f5d9c4
```
