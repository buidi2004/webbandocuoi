import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import ImageModal from '../thanh_phan/ImageModal';
import { useToast } from '../thanh_phan/Toast';
import { sanPhamAPI, layUrlHinhAnh } from '../api/khach_hang';
import '../styles/product-detail.css';

export default function ProductDetail() {
  const { id } = useParams();
  const [sanPham, setSanPham] = useState(null);
  const [dangTai, setDangTai] = useState(true);
  const [index, setIndex] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const [extras, setExtras] = useState([]);
  const [days, setDays] = useState(1);
  const [total, setTotal] = useState(0);

  const navigate = useNavigate();
  const { addToast } = useToast();

  useEffect(() => {
    const layDuLieu = async () => {
      if (!id) {
        // Nếu không có ID, dùng dữ liệu demo
        setSanPham({
          id: 'demo',
          name: 'Váy Cưới Thanh Lịch',
          code: 'VD-M001',
          image_url: 'https://placehold.co/800x1100/eaeaea/333?text=Váy+Mẫu+1',
          gallery_images: [
            'https://placehold.co/800x1100/eaeaea/333?text=Váy+Mẫu+1',
            'https://placehold.co/800x1100/f7f1ea/333?text=Váy+Mẫu+2',
            'https://placehold.co/800x1100/fff0f0/333?text=Váy+Mẫu+3',
            'https://placehold.co/800x1100/e6f7f0/333?text=Váy+Mẫu+4'
          ],
          rental_price_day: 2200000,
          purchase_price: 50000000
        });
        setDangTai(false);
        return;
      }

      try {
        const res = await sanPhamAPI.layTheoId(id);
        setSanPham(res.data);
      } catch (err) {
        console.error("Lỗi tải sản phẩm:", err);
        addToast({ message: "Không tìm thấy sản phẩm", type: "error" });
      } finally {
        setDangTai(false);
      }
    };
    layDuLieu();
  }, [id]);

  useEffect(() => {
    if (sanPham) {
      setTotal(sanPham.rental_price_day * days + extras.reduce((s, e) => s + e, 0));
    }
  }, [extras, days, sanPham]);

  function toggleAccessory(el) {
    const price = Number(el.dataset.price || 0);
    const checked = el.checked;
    setExtras(prev => checked ? [...prev, price] : prev.filter(p => p !== price));
  }

  function addToCart() {
    if (!sanPham) return;
    const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
    const item = {
      id: sanPham.id,
      name: sanPham.name,
      code: sanPham.code,
      image_url: gallery[index],
      rental_price_day: sanPham.rental_price_day,
      price_to_use: total,
      quantity: 1,
      rental_days: days,
      accessories: extras
    };
    const existing = currentCart.findIndex(i => i.id === item.id && i.rental_days === days);
    if (existing > -1) {
      currentCart[existing].quantity = (currentCart[existing].quantity || 1) + 1;
      currentCart[existing].price_to_use = total;
      currentCart[existing].accessories = extras;
    } else {
      currentCart.push(item);
    }
    localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
    addToast({ message: 'Đã thêm vào giỏ hàng!', type: 'success' });
  }

  function buyNow() {
    addToCart();
    navigate('/gio-hang');
  }

  if (dangTai) return <div style={{textAlign:'center',padding:'100px'}}>Đang tải...</div>;
  if (!sanPham) return <div style={{textAlign:'center',padding:'100px'}}>Không tìm thấy sản phẩm</div>;

  // Lấy gallery images: ưu tiên gallery_images, fallback về image_url
  const gallery = Array.isArray(sanPham.gallery_images) && sanPham.gallery_images.length > 0
    ? sanPham.gallery_images
    : [sanPham.image_url];

  function next() { setIndex(i => (i + 1) % gallery.length); }
  function prev() { setIndex(i => (i - 1 + gallery.length) % gallery.length); }

  return (
    <main className="product-page">
      <div className="product-grid">
        <section className="gallery" aria-label="Hình ảnh sản phẩm">
          <div className="gallery-main">
            <button className="control-btn" onClick={prev} aria-label="Hình trước">◀</button>
            <img 
              id="mainImg" 
              src={layUrlHinhAnh(gallery[index])} 
              alt={`${sanPham.name} - ${index+1}`} 
              style={{cursor:'zoom-in'}} 
              onClick={() => setModalOpen(true)}
              onError={(e) => e.target.src = 'https://placehold.co/800x1100?text=IVIE+Studio'}
            />
            <div className="gallery-controls" aria-hidden="true">
              <button className="control-btn" onClick={() => setModalOpen(true)} title="Xem lớn">🔍</button>
            </div>
            <button className="control-btn" onClick={next} aria-label="Hình kế tiếp" style={{right:66}}>▶</button>
          </div>

          <div className="gallery-thumbs" role="tablist" aria-label="Ảnh thu nhỏ">
            {gallery.map((src,i) => (
              <div 
                key={src+i} 
                className={`thumb ${i === index ? 'active' : ''}`} 
                data-src={src} 
                tabIndex={0} 
                onClick={() => setIndex(i)} 
                onKeyDown={(e)=>{ if(e.key==='Enter') setIndex(i) }}
                style={{position:'relative'}}
              >
                <img 
                  src={layUrlHinhAnh(src)} 
                  alt={`Thumb ${i+1}`}
                  onError={(e) => e.target.src = 'https://placehold.co/160x220?text=Mẫu+'+(i+1)}
                />
                <div style={{
                  position:'absolute',
                  bottom:'8px',
                  left:'50%',
                  transform:'translateX(-50%)',
                  background:'rgba(0,0,0,0.7)',
                  color:'white',
                  padding:'4px 12px',
                  borderRadius:'12px',
                  fontSize:'0.75rem',
                  fontWeight:'600',
                  pointerEvents:'none'
                }}>
                  Mẫu {i+1}
                </div>
              </div>
            ))}
          </div>
        </section>

        <aside className="info" aria-label="Thông tin sản phẩm">
          <div className="title-row">
            <div>
              <h1 className="product-title">{sanPham.name}</h1>
              <div className="product-code">Mã: {sanPham.code}</div>
            </div>
            <div style={{textAlign:'right'}}>
              <div className="price-main">{total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ'}</div>
              <div className="price-sub">Giá thuê: {sanPham.rental_price_day.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')}đ</div>
            </div>
          </div>

          <div className="options">
            <div className="option-group">
              <label className="option-label">Kích thước</label>
              <div className="sizes" role="radiogroup" aria-label="Kích thước">
                {['XS','S','M','L','XL'].map(s => (
                  <React.Fragment key={s}>
                    <input type="radio" id={`size_${s}`} name="size" value={s} defaultChecked={s==='XS'} />
                    <label className="size-btn" htmlFor={`size_${s}`}>{s}</label>
                  </React.Fragment>
                ))}
              </div>
            </div>

            <div className="option-group">
              <label className="option-label">Màu sắc</label>
              <div className="colors" role="radiogroup" aria-label="Màu sắc">
                <input type="radio" id="clr_ivory" name="color" value="ivory" defaultChecked />
                <label className="swatch" htmlFor="clr_ivory" style={{background:'#fffaf0',border:'1px solid #f1e8df'}} title="Ivory" />

                <input type="radio" id="clr_blush" name="color" value="blush" />
                <label className="swatch" htmlFor="clr_blush" style={{background:'#fff0f3'}} title="Blush" />

                <input type="radio" id="clr_pearl" name="color" value="pearl" />
                <label className="swatch" htmlFor="clr_pearl" style={{background:'#f3f9ff'}} title="Pearl" />

                <input type="radio" id="clr_champ" name="color" value="champ" />
                <label className="swatch" htmlFor="clr_champ" style={{background:'#f5eee6'}} title="Champagne" />
              </div>
            </div>

            <div style={{margin:'18px 0'}}>
              <label className="option-label">Số ngày thuê</label>
              <div style={{display:'flex',gap:8,margin:'8px 0 18px 0'}}>
                {[1,2,3,4,5,6,7].map(d=>(
                  <button
                    key={d}
                    type="button"
                    style={{
                      minWidth:36,padding:'7px 0',borderRadius:7,
                      border:days===d?'2px solid #222':'1.5px solid #bbb',
                      background:days===d?'#f5f5f5':'#fff',
                      fontWeight:days===d?700:500,cursor:'pointer',color:'#222',fontSize:'1rem'
                    }}
                    onClick={()=>setDays(d)}
                  >{d}</button>
                ))}
              </div>
            </div>
            <div className="accessories">
              <div style={{fontWeight:700,marginBottom:8,color:'var(--muted)'}}>Phụ kiện kèm theo</div>
              <table className="access" role="table" aria-label="Bảng phụ kiện">
                <tbody>
                  {[{name:'Vai nơ',price:150000},{name:'Lúp voan',price:220000},{name:'Găng tay ren',price:90000}].map(a => (
                    <tr key={a.name}>
                      <td>
                        <label>
                          <input type="checkbox" className="acc" data-price={a.price} onChange={(e)=> toggleAccessory(e.target)} /> {a.name}
                        </label>
                      </td>
                      <td className="price">{a.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="summary">Tổng hiện tại: <strong>{total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ'}</strong></div>
            </div>

            <div className="actions" role="group" aria-label="Hành động sản phẩm">
              <button className="btn btn-primary" onClick={() => addToCart()}>THÊM VÀO GIỎ</button>
              <button className="btn btn-primary" onClick={() => buyNow()}>THUÊ NGAY</button>
              <button className="btn btn-outline" onClick={() => buyNow()}>MUA NGAY</button>
            </div>
          </div>

          <div className="description" aria-labelledby="descTitle">
            <h4 id="descTitle">Mô tả sản phẩm</h4>
            <p style={{margin: '0 0 8px', color: 'var(--muted)'}}>{sanPham.description || 'Một chiếc váy cưới thanh lịch, phù hợp với cả tiệc cưới ngoài trời và trong nhà.'}</p>
            <ul>
              <li>Chất liệu: {sanPham.fabric_type || 'Ren cao cấp, lót satin mịn'}</li>
              <li>Màu sắc: {sanPham.color || 'Đa dạng'}</li>
              <li>Size: {sanPham.recommended_size || 'Đủ size'}</li>
              <li>Bảo quản: Giặt khô chuyên nghiệp, bảo quản nơi khô ráo.</li>
            </ul>
          </div>
        </aside>
      </div>

      <ImageModal src={layUrlHinhAnh(gallery[index])} alt={`${sanPham.name} - ${index+1}`} open={modalOpen} onClose={() => setModalOpen(false)} />
    </main>
  );
}
