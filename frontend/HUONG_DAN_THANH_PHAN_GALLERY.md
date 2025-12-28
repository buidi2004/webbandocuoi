# Hướng Dẫn Các Thành Phần Gallery - IVIE Studio

## Tổng Quan

Bộ sưu tập các thành phần gallery cao cấp được xây dựng với React, Tailwind CSS và Framer Motion.

---

## 1. Bộ Sưu Tập Gạch (BoSuuTapGach)

Bố cục kiểu Pinterest với các ảnh có kích thước khác nhau xếp tự nhiên.

### Cách Sử Dụng

```jsx
import BoSuuTapGach from '../thanh_phan/BoSuuTapGach';

const danhSachAnh = [
  { url: 'duong-dan-anh.jpg', moTa: 'Mô tả ảnh' },
  // ...
];

<BoSuuTapGach danhSachAnh={danhSachAnh} />
```

### Tính Năng
- Bố cục nhiều cột tự động điều chỉnh
- Hiệu ứng phóng to khi hover
- Hộp thoại xem ảnh lớn với hiệu ứng 3D
- Hiệu ứng xuất hiện lần lượt

---

## 2. Album Thông Minh (AlbumThongMinh)

Gallery với lightbox hỗ trợ vuốt trên mobile.

### Cách Sử Dụng

```jsx
import AlbumThongMinh from '../thanh_phan/AlbumThongMinh';

<AlbumThongMinh danhSachAnh={danhSachAnh} />
```

### Tính Năng
- Điều hướng bằng phím mũi tên
- Hỗ trợ vuốt trên mobile
- Nút điều hướng trái/phải
- Hiển thị số thứ tự ảnh

---

## 3. Gắn Thẻ Sản Phẩm (GanTheSanPham)

Cho phép gắn thẻ sản phẩm lên ảnh với các điểm hotspot.

### Cách Sử Dụng

```jsx
import GanTheSanPham, { duLieuTheMau } from '../thanh_phan/GanTheSanPham';

<GanTheSanPham 
  duongDanAnh="anh-chinh.jpg"
  danhSachThe={duLieuTheMau}
/>
```

### Cấu Trúc Dữ Liệu Thẻ

```jsx
const danhSachThe = [
  {
    id: 1,
    viTriTren: 35,      // Vị trí từ trên (%)
    viTriTrai: 25,      // Vị trí từ trái (%)
    idSanPham: 1,
    tenSanPham: 'Tên sản phẩm',
    maSanPham: 'WD-001',
    anhSanPham: 'anh-san-pham.jpg',
  },
];
```

### Tính Năng
- Điểm hotspot với hiệu ứng nhấp nháy
- Tooltip hiển thị thông tin sản phẩm
- Nút xem chi tiết điều hướng đến trang sản phẩm

---

## 4. Thanh Trượt Trước/Sau (ThanhTruotTruocSau)

So sánh ảnh trước và sau chỉnh sửa.

### Cách Sử Dụng

```jsx
import ThanhTruotTruocSau from '../thanh_phan/ThanhTruotTruocSau';

<ThanhTruotTruocSau 
  anhTruoc="anh-truoc.jpg"
  anhSau="anh-sau.jpg"
  moTa="So sánh ảnh"
/>
```

### Tính Năng
- Kéo thanh trượt để so sánh
- Hỗ trợ cả chuột và cảm ứng
- Nhãn TRƯỚC/SAU tự động ẩn/hiện
- Tay cầm thanh trượt với hiệu ứng hover

---

## 5. Bộ Sưu Tập Đan Xen (BoSuuTapDanXen)

Bố cục ảnh lớn/nhỏ xen kẽ trái phải.

### Cách Sử Dụng

```jsx
import BoSuuTapDanXen from '../thanh_phan/BoSuuTapDanXen';

<BoSuuTapDanXen danhSachAnh={danhSachAnh} />
```

### Tính Năng
- Dòng 1: Ảnh lớn trái, ảnh nhỏ phải
- Dòng 2: Đảo ngược
- Hiệu ứng fade-in khi cuộn
- Overlay thông tin khi hover

---

## 6. Bộ Sưu Tập Tỉ Lệ Vàng (BoSuuTapTiLeVang)

Ảnh với tỉ lệ vàng 3:2 (ngang) và 2:3 (dọc).

### Cách Sử Dụng

```jsx
import BoSuuTapTiLeVang, { duLieuAnhTiLeVangMau } from '../thanh_phan/BoSuuTapTiLeVang';

<BoSuuTapTiLeVang danhSachAnh={duLieuAnhTiLeVangMau} />
```

### Cấu Trúc Dữ Liệu

```jsx
const danhSachAnh = [
  {
    url: 'anh.jpg',
    moTa: 'Mô tả',
    huong: 'doc',    // 'doc' (2:3) hoặc 'ngang' (3:2)
  },
];
```

### Tính Năng
- Khung viền vàng sang trọng
- Góc trang trí vàng khi hover
- Lightbox với khung vàng

---

## 7. Cuộn Phóng To (CuonPhongTo)

Hiệu ứng scroll-driven zoom cho ảnh hero.

### Cách Sử Dụng

```jsx
import CuonPhongTo from '../trang/CuonPhongTo';

<CuonPhongTo />
```

### Tính Năng
- Container 300vh để cuộn
- Ảnh phóng to từ scale 1 → 2
- Typography xuất hiện/biến mất theo scroll
- Thanh tiến trình
- Chỉ báo cuộn với animation

---

## Yêu Cầu

```bash
npm install framer-motion lucide-react
```

---

## Tác Giả

IVIE Studio - © 2024
