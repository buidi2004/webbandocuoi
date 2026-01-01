// IVIE Wedding Studio - Main App
import { useEffect, lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import sal from 'sal.js';
import 'sal.js/dist/sal.css';

// Core components - load immediately
import DauTrang from './thanh_phan/DauTrang';
import ChanTrang from './thanh_phan/ChanTrang';
import CuonLenDau from './thanh_phan/CuonLenDau';
import StickyBottomBar from './thanh_phan/StickyBottomBar';
import StickyCTA from './thanh_phan/StickyCTA';
import StickyContactBar from './thanh_phan/StickyContactBar';

// Lazy load heavy components
const ChatBox = lazy(() => import('./thanh_phan/ChatBox'));
const HieuUngLaRoi = lazy(() => import('./thanh_phan/HieuUngLaRoi'));
const HieuUngChuyenTrang = lazy(() => import('./thanh_phan/HieuUngChuyenTrang'));

// Lazy load pages - Code splitting
const TrangChu = lazy(() => import('./trang/TrangChu'));
const SanPham = lazy(() => import('./trang/SanPham'));
const ProductDetail = lazy(() => import('./trang/ProductDetail'));
const ThuVien = lazy(() => import('./trang/ThuVien'));
const DichVuTrangDiem = lazy(() => import('./trang/DichVuTrangDiem'));
const ChonCombo = lazy(() => import('./trang/ChonCombo'));
const LienHe = lazy(() => import('./trang/LienHe'));
const TaiKhoan = lazy(() => import('./trang/TaiKhoan'));
const DangNhap = lazy(() => import('./trang/DangNhap'));
const DangKy = lazy(() => import('./trang/DangKy'));
const GioHang = lazy(() => import('./trang/GioHang'));
const DoiTacPortal = lazy(() => import('./trang/DoiTacPortal'));
const Blog = lazy(() => import('./trang/Blog'));
const ChiTietBlog = lazy(() => import('./trang/ChiTietBlog'));
const ChinhSach = lazy(() => import('./trang/ChinhSach'));
const CamOn = lazy(() => import('./trang/CamOn'));

// Demo pages - rarely used
const AntiGravityLanding = lazy(() => import('./trang/AntiGravityLanding'));
const GalleryDemo = lazy(() => import('./trang/GalleryDemo'));
const CuonPhongTo = lazy(() => import('./trang/CuonPhongTo'));
const DemoHieuUng = lazy(() => import('./trang/DemoHieuUng'));

// Loading fallback component
const PageLoader = () => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '60vh',
    background: '#fff'
  }}>
    <div style={{
      width: '40px',
      height: '40px',
      border: '3px solid #f3f3f3',
      borderTop: '3px solid #c9a86c',
      borderRadius: '50%',
      animation: 'spin 1s linear infinite'
    }} />
  </div>
);

// Component to handle sal.js initialization on route change
function SalInitializer() {
  const location = useLocation();

  useEffect(() => {
    // Skip sal animations on home page
    if (location.pathname !== '/') {
      sal({
        threshold: 0.1,
        once: true,
      });
    }
  }, [location]);

  return null;
}

function UngDung() {
  return (
    <Router>
      <div className="App">
        <CuonLenDau />
        <SalInitializer />
        
        {/* Lazy load decorative effects */}
        <Suspense fallback={null}>
          <HieuUngLaRoi />
          <HieuUngChuyenTrang />
        </Suspense>
        
        <DauTrang />
        <main>
          <Suspense fallback={<PageLoader />}>
            <Routes>
              <Route path="/" element={<TrangChu />} />
              <Route path="/san-pham" element={<SanPham />} />
              <Route path="/san-pham/:id" element={<ProductDetail />} />
              <Route path="/thu-vien" element={<ThuVien />} />
              <Route path="/dich-vu-trang-diem" element={<DichVuTrangDiem />} />
              <Route path="/chon-combo" element={<ChonCombo />} />
              <Route path="/lien-he" element={<LienHe />} />
              <Route path="/tai-khoan" element={<TaiKhoan />} />
              <Route path="/dang-nhap" element={<DangNhap />} />
              <Route path="/dang-ky" element={<DangKy />} />
              <Route path="/gio-hang" element={<GioHang />} />
              <Route path="/doi-tac-portal" element={<DoiTacPortal />} />
              <Route path="/blog" element={<Blog />} />
              <Route path="/blog/:slug" element={<ChiTietBlog />} />
              <Route path="/chinh-sach" element={<ChinhSach />} />
              <Route path="/anti-gravity" element={<AntiGravityLanding />} />
              <Route path="/san-pham-demo" element={<ProductDetail />} />
              <Route path="/gallery-demo" element={<GalleryDemo />} />
              <Route path="/cuon-phong-to" element={<CuonPhongTo />} />
              <Route path="/demo-hieu-ung" element={<DemoHieuUng />} />
              <Route path="/cam-on" element={<CamOn />} />
            </Routes>
          </Suspense>
        </main>
        <ChanTrang />
        
        {/* Lazy load chat */}
        <Suspense fallback={null}>
          <ChatBox />
        </Suspense>
        
        <StickyBottomBar />
        <StickyCTA 
          zaloLink="https://zalo.me/0739193848"
          phoneNumber="0739193848"
        />
        <StickyContactBar 
          phoneNumber="0739193848"
          zaloLink="https://zalo.me/0739193848"
          mapsLink="https://maps.app.goo.gl/YourGoogleMapsLink"
        />
      </div>
    </Router>
  );
}

export default UngDung;
