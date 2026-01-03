import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { sanPhamAPI, layUrlHinhAnh } from "../api/khach_hang";
import { useToast } from "../thanh_phan/Toast";
import QuickViewModal from "../thanh_phan/QuickViewModal";
import LazyImage from "../thanh_phan/LazyImage";
import "../styles/products.css";

const SanPham = () => {
  const [danhSachSanPham, setDanhSachSanPham] = useState([]);
  const [dangTai, setDangTai] = useState(true);
  const [loi, setLoi] = useState(null);
  const [boLoc, setBoLoc] = useState("all");
  const [tieuMuc, setTieuMuc] = useState("all");
  const [phongCach, setPhongCach] = useState("all");
  const [khoangGia, setKhoangGia] = useState("all");
  const [sapXep, setSapXep] = useState("hot");
  const [sanPhamDaXem, setSanPhamDaXem] = useState([]);
  const [quickViewSP, setQuickViewSP] = useState(null);

  const navigate = useNavigate();
  const { addToast } = useToast();

  // Lấy sản phẩm đã xem từ localStorage
  useEffect(() => {
    const daXem = JSON.parse(localStorage.getItem("ivie_viewed") || "[]");
    setSanPhamDaXem(daXem.slice(0, 4));
  }, []);

  useEffect(() => {
    laySanPham();
  }, [boLoc, tieuMuc, phongCach, khoangGia, sapXep]);

  const laySanPham = async () => {
    setDangTai(true);
    setLoi(null);
    try {
      const thamSo = { sort_by: sapXep };
      if (boLoc !== "all") thamSo.danh_muc = boLoc;
      if (tieuMuc !== "all") thamSo.sub_category = tieuMuc;
      if (phongCach !== "all") thamSo.style = phongCach;
      if (khoangGia !== "all") thamSo.price_range = khoangGia;
      const phanHoi = await sanPhamAPI.layTatCa(thamSo);
      setDanhSachSanPham(Array.isArray(phanHoi.data) ? phanHoi.data : []);
    } catch {
      setLoi("Không thể tải dữ liệu sản phẩm.");
    } finally {
      setDangTai(false);
    }
  };

  const dinhDangGia = (gia) => new Intl.NumberFormat("vi-VN").format(gia) + "đ";

  const xemChiTiet = (sp) => {
    // Lưu vào sản phẩm đã xem
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

  const xoaLichSu = () => {
    localStorage.removeItem("ivie_viewed");
    setSanPhamDaXem([]);
  };

  const danhMuc = [
    { id: "all", nhan: "Tất cả" },
    { id: "wedding_modern", nhan: "Váy Cưới" },
    { id: "vest", nhan: "Vest Nam" },
    { id: "aodai", nhan: "Áo Dài" },
  ];

  const tieuMucTheoLoai = {
    aodai: [
      { id: "all", nhan: "Tất cả" },
      { id: "nam", nhan: "Áo Dài Nam" },
      { id: "nu", nhan: "Áo Dài Nữ" },
    ],
    wedding_modern: [
      { id: "all", nhan: "Tất cả" },
      { id: "xoe", nhan: "Váy Xòe" },
      { id: "duoi_ca", nhan: "Váy Đuôi Cá" },
      { id: "ngan", nhan: "Váy Ngắn" },
    ],
    vest: [
      { id: "all", nhan: "Tất cả" },
      { id: "hien_dai", nhan: "Vest Hiện Đại" },
      { id: "han_quoc", nhan: "Vest Hàn Quốc" },
    ],
  };

  const sapXepOptions = [
    { id: "hot", nhan: "Nổi bật" },
    { id: "best_sell", nhan: "Bán chạy" },
    { id: "new", nhan: "Mới" },
    { id: "price_asc", nhan: "Giá thấp" },
    { id: "price_desc", nhan: "Giá cao" },
  ];

  const phongCachOptions = [
    { id: "all", nhan: "Tất cả" },
    { id: "minimalist", nhan: "Minimalist" },
    { id: "princess", nhan: "Công chúa" },
    { id: "vintage", nhan: "Vintage" },
    { id: "sexy", nhan: "Quyến rũ" },
    { id: "classic", nhan: "Cổ điển" },
  ];

  const khoangGiaOptions = [
    { id: "all", nhan: "Tất cả giá" },
    { id: "duoi_500k", nhan: "Dưới 500K" },
    { id: "500k_1tr", nhan: "500K - 1 triệu" },
    { id: "1tr_2tr", nhan: "1 - 2 triệu" },
    { id: "tren_2tr", nhan: "Trên 2 triệu" },
  ];

  return (
    <div className="products-page-new">
      {/* Breadcrumb */}
      <div className="breadcrumb">
        <div className="container">
          <Link to="/">Trang chủ</Link>
          <span className="sep">›</span>
          <span>{danhSachSanPham.length} Sản phẩm</span>
        </div>
      </div>

      {/* Sản phẩm đã xem */}
      {sanPhamDaXem.length > 0 && (
        <div className="viewed-section">
          <div className="container">
            <div className="viewed-header">
              <h3>Sản phẩm đã xem</h3>
              <button onClick={xoaLichSu} className="clear-history">
                Xóa lịch sử
              </button>
            </div>
            <div className="viewed-list">
              {sanPhamDaXem.map((sp) => (
                <div
                  key={sp.id}
                  className="viewed-item"
                  onClick={() => navigate(`/san-pham/${sp.id}`)}
                >
                  <button
                    className="remove-viewed"
                    onClick={(e) => {
                      e.stopPropagation();
                      const daXem = JSON.parse(
                        localStorage.getItem("ivie_viewed") || "[]",
                      );
                      const filtered = daXem.filter(
                        (item) => item.id !== sp.id,
                      );
                      localStorage.setItem(
                        "ivie_viewed",
                        JSON.stringify(filtered),
                      );
                      setSanPhamDaXem(filtered.slice(0, 4));
                    }}
                  >
                    ×
                  </button>
                  <LazyImage
                    src={layUrlHinhAnh(sp.image_url)}
                    alt={`${sp.name.toLowerCase().replace(/\s+/g, "-")}-ivie-wedding`}
                    style={{ width: "100%", height: "100%" }}
                  />
                  <div className="viewed-info">
                    <p className="viewed-name">{sp.name}</p>
                    <p className="viewed-price">
                      {dinhDangGia(sp.rental_price_day)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Banner quảng cáo */}
      <div className="promo-banners">
        <div className="container">
          <div className="banner-grid">
            <div
              className="banner-item"
              style={{
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              }}
            >
              <div className="banner-content">
                <h4>Ưu đãi mùa cưới</h4>
                <p>
                  Giảm đến <strong>30%</strong>
                </p>
                <span className="banner-tag">Hot Deal</span>
              </div>
            </div>
            <div
              className="banner-item"
              style={{
                background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
              }}
            >
              <div className="banner-content">
                <h4>Thuê váy trọn gói</h4>
                <p>
                  Chỉ từ <strong>2 triệu</strong>
                </p>
                <span className="banner-tag">Best Seller</span>
              </div>
            </div>
            <div
              className="banner-item"
              style={{
                background: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
              }}
            >
              <div className="banner-content">
                <h4>Bộ sưu tập mới</h4>
                <p>
                  Xu hướng <strong>2025</strong>
                </p>
                <span className="banner-tag">New Arrival</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="filter-section">
        <div className="container">
          <div className="category-tabs">
            {danhMuc.map((dm) => (
              <button
                key={dm.id}
                className={`cat-tab ${boLoc === dm.id ? "active" : ""}`}
                onClick={() => {
                  setBoLoc(dm.id);
                  setTieuMuc("all");
                  setPhongCach("all");
                }}
              >
                <span>{dm.nhan}</span>
              </button>
            ))}
          </div>

          {/* Sub-filter cho từng danh mục */}
          {tieuMucTheoLoai[boLoc] && (
            <div className="sub-category-tabs">
              {tieuMucTheoLoai[boLoc].map((sub) => (
                <button
                  key={sub.id}
                  className={`sub-cat-tab ${tieuMuc === sub.id ? "active" : ""}`}
                  onClick={() => setTieuMuc(sub.id)}
                >
                  {sub.nhan}
                </button>
              ))}
            </div>
          )}

          {/* Bộ lọc phong cách */}
          <div className="style-filter-section">
            <span className="filter-label">Phong cách:</span>
            <div className="style-tabs">
              {phongCachOptions.map((pc) => (
                <button
                  key={pc.id}
                  className={`style-tab ${phongCach === pc.id ? "active" : ""}`}
                  onClick={() => setPhongCach(pc.id)}
                >
                  <span>{pc.nhan}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Bộ lọc khoảng giá */}
          <div className="price-filter-section">
            <span className="filter-label">Khoảng giá:</span>
            <div className="price-tabs">
              {khoangGiaOptions.map((kg) => (
                <button
                  key={kg.id}
                  className={`price-tab ${khoangGia === kg.id ? "active" : ""}`}
                  onClick={() => setKhoangGia(kg.id)}
                >
                  {kg.nhan}
                </button>
              ))}
            </div>
          </div>

          <div className="sort-tabs">
            <span className="sort-label">Sắp xếp theo:</span>
            {sapXepOptions.map((opt) => (
              <button
                key={opt.id}
                className={`sort-tab ${sapXep === opt.id ? "active" : ""}`}
                onClick={() => setSapXep(opt.id)}
              >
                {opt.nhan}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="products-section">
        <div className="container">
          {loi && <div className="error-msg">{loi}</div>}
          {dangTai ? (
            <div className="loading-msg">Đang tải sản phẩm...</div>
          ) : (
            <div className="products-grid-new">
              {danhSachSanPham.length > 0 ? (
                danhSachSanPham.map((sp) => (
                  <div
                    key={sp.id}
                    className={`product-card-new ${sp.het_hang ? "out-of-stock" : ""}`}
                  >
                    <div onClick={() => xemChiTiet(sp)}>
                      {sp.het_hang && (
                        <div className="sold-out-overlay">
                          <span>HẾT HÀNG</span>
                        </div>
                      )}
                      {!sp.het_hang && sp.is_hot && (
                        <div className="promo-tag hot-deal">🔥 Hot Deal</div>
                      )}
                      {!sp.het_hang && sp.is_new && (
                        <div className="new-tag new-arrival">✨ Mới</div>
                      )}
                      <div className="product-img">
                        <LazyImage
                          src={layUrlHinhAnh(sp.image_url)}
                          alt={`${sp.name.toLowerCase().replace(/\s+/g, "-")}-ivie-wedding-studio`}
                          style={{ width: "100%", height: "100%" }}
                        />
                        {/* Icon buttons on hover */}
                        {!sp.het_hang && (
                          <div className="product-hover-actions">
                            <button
                              className="hover-btn quick-view"
                              onClick={(e) => {
                                e.stopPropagation();
                                setQuickViewSP(sp);
                              }}
                              title="Xem nhanh"
                            >
                              👁️
                            </button>
                            <button
                              className="hover-btn add-wishlist"
                              onClick={(e) => {
                                e.stopPropagation();
                                addToast({
                                  message: "Đã thêm vào yêu thích!",
                                  type: "success",
                                });
                              }}
                              title="Yêu thích"
                            >
                              ❤️
                            </button>
                            <button
                              className="hover-btn quick-add"
                              onClick={(e) => {
                                e.stopPropagation();
                                const currentCart = JSON.parse(
                                  localStorage.getItem("ivie_cart") || "[]",
                                );
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
                                const existing = currentCart.findIndex(
                                  (i) => i.id === item.id && i.loai === "mua",
                                );
                                if (existing > -1) {
                                  currentCart[existing].quantity =
                                    (currentCart[existing].quantity || 1) + 1;
                                } else {
                                  currentCart.push(item);
                                }
                                localStorage.setItem(
                                  "ivie_cart",
                                  JSON.stringify(currentCart),
                                );
                                addToast({
                                  message: "Đã thêm vào giỏ hàng!",
                                  type: "success",
                                });
                              }}
                              title="Thêm giỏ hàng"
                            >
                              🛒
                            </button>
                          </div>
                        )}
                      </div>
                      <div className="product-details">
                        <h3 className="product-title">{sp.name}</h3>
                        <div className="product-prices">
                          <span className="price-main">
                            {dinhDangGia(sp.rental_price_day)}
                          </span>
                          <span className="price-unit">/ngày</span>
                        </div>
                        {sp.purchase_price > 0 && (
                          <div className="price-buy">
                            Mua:{" "}
                            <strong>{dinhDangGia(sp.purchase_price)}</strong>
                          </div>
                        )}
                        <div className="product-meta">
                          <span className="rating">⭐ 4.9</span>
                          <span className="reviews">(128 đánh giá)</span>
                          {sp.so_luong !== undefined &&
                            sp.so_luong <= 5 &&
                            sp.so_luong > 0 && (
                              <span className="stock-warning">
                                Còn {sp.so_luong} sản phẩm
                              </span>
                            )}
                        </div>
                      </div>
                    </div>
                    {/* Nút thêm giỏ hàng và mua ngay */}
                    {!sp.het_hang && (
                      <div className="product-actions">
                        <button
                          className="btn-add-cart"
                          onClick={(e) => {
                            e.stopPropagation();
                            const currentCart = JSON.parse(
                              localStorage.getItem("ivie_cart") || "[]",
                            );
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
                            const existing = currentCart.findIndex(
                              (i) => i.id === item.id && i.loai === "mua",
                            );
                            if (existing > -1) {
                              currentCart[existing].quantity =
                                (currentCart[existing].quantity || 1) + 1;
                            } else {
                              currentCart.push(item);
                            }
                            localStorage.setItem(
                              "ivie_cart",
                              JSON.stringify(currentCart),
                            );
                            addToast({
                              message: "Đã thêm vào giỏ hàng!",
                              type: "success",
                            });
                          }}
                        >
                          🛒 Thêm giỏ
                        </button>
                        <button
                          className="btn-buy-now"
                          onClick={(e) => {
                            e.stopPropagation();
                            const currentCart = JSON.parse(
                              localStorage.getItem("ivie_cart") || "[]",
                            );
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
                            const existing = currentCart.findIndex(
                              (i) => i.id === item.id && i.loai === "mua",
                            );
                            if (existing > -1) {
                              currentCart[existing].quantity =
                                (currentCart[existing].quantity || 1) + 1;
                            } else {
                              currentCart.push(item);
                            }
                            localStorage.setItem(
                              "ivie_cart",
                              JSON.stringify(currentCart),
                            );
                            navigate("/gio-hang");
                          }}
                        >
                          Mua ngay
                        </button>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="no-products">Không tìm thấy sản phẩm nào.</div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Quick View Modal */}
      {quickViewSP && (
        <QuickViewModal
          sanPham={quickViewSP}
          onClose={() => setQuickViewSP(null)}
        />
      )}
    </div>
  );
};

export default SanPham;
