"""
IVIE Admin - Dashboard Analytics Component
==========================================
Phần Dashboard nâng cao với các tính năng:
1. Dự báo doanh thu (Moving Average)
2. Phân tích khách hàng RFM
3. Cảnh báo đánh giá tiêu cực
4. Biểu đồ thống kê
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_dashboard(fetch_api_data, fetch_multiple_endpoints, HAS_ANALYTICS=False):
    """
    Render Dashboard với các tính năng analytics nâng cao
    """
    # Import analytics nếu có
    if HAS_ANALYTICS:
        try:
            from analytics import (
                tinh_doanh_thu_theo_thang, du_bao_moving_average, tinh_tang_truong,
                phan_tich_rfm, thong_ke_rfm,
                phan_tich_danh_gia_list, thong_ke_cam_xuc
            )
        except ImportError:
            HAS_ANALYTICS = False
    
    st.header("📊 Tổng quan Dashboard")
    
    # Fetch data
    stats = fetch_api_data("/api/thong_ke/tong_quan")
    don_hang_list = fetch_api_data("/api/don_hang/")
    
    # === METRICS ROW ===
    if stats:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("🛍️ SẢN PHẨM", stats.get('tong_san_pham', 0))
        with c2: st.metric("📦 ĐƠN HÀNG", stats.get('tong_don_hang', 0))
        with c3: st.metric("👤 NGƯỜI DÙNG", stats.get('tong_nguoi_dung', 0))
        with c4: st.metric("📞 LIÊN HỆ MỚI", stats.get('lien_he_chua_xu_ly', 0))
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("💰 DOANH THU", f"{stats.get('tong_doanh_thu', 0):,.0f}đ")
        with c2:
            st.metric("⏳ ĐƠN CHỜ XỬ LÝ", stats.get('don_hang_cho_xu_ly', 0))
    else:
        data = fetch_multiple_endpoints(["/api/san_pham/", "/api/lien_he/"])
        products = data.get("/api/san_pham/", [])
        contacts = data.get("/api/lien_he/", [])
        c1, c2 = st.columns(2)
        with c1: st.metric("TỔNG SẢN PHẨM", len(products) if products else 0)
        with c2: st.metric("LIÊN HỆ MỚI", len([c for c in (contacts or []) if c.get('status') == 'pending']))
    
    st.markdown("---")
    
    # === CẢNH BÁO ĐÁNH GIÁ TIÊU CỰC ===
    danh_gia_list = None
    if HAS_ANALYTICS:
        danh_gia_list = fetch_api_data("/api/san_pham/admin/danh_gia_cho_duyet")
        if danh_gia_list:
            _, canh_bao = phan_tich_danh_gia_list(danh_gia_list)
            if canh_bao:
                st.markdown(f"""
                    <div style="background:#e74c3c20; border:1px solid #e74c3c; border-radius:8px; padding:15px; margin-bottom:20px;">
                        <h4 style="color:#e74c3c; margin:0;">⚠️ CẢNH BÁO: Có {len(canh_bao)} đánh giá tiêu cực cần xử lý!</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔍 Xem chi tiết đánh giá tiêu cực"):
                    for cb in canh_bao[:5]:
                        st.markdown(f"""
                            <div style="background:#111; padding:10px; border-radius:4px; margin:5px 0; border-left:3px solid #e74c3c;">
                                <strong>⭐ {cb.get('rating', 'N/A')}/5</strong> - {cb.get('user_name', 'Ẩn danh')}<br>
                                <span style="color:#888;">{cb.get('comment', '')}</span>
                            </div>
                        """, unsafe_allow_html=True)
    
    # === TABS CHO DASHBOARD ===
    tab_overview, tab_forecast, tab_customers = st.tabs([
        "📈 Biểu đồ tổng quan", 
        "🔮 Dự báo doanh thu", 
        "👥 Phân tích khách hàng"
    ])
    
    # === TAB 1: BIỂU ĐỒ TỔNG QUAN ===
    with tab_overview:
        _render_overview_charts(don_hang_list, danh_gia_list, HAS_ANALYTICS)
    
    # === TAB 2: DỰ BÁO DOANH THU ===
    with tab_forecast:
        _render_forecast(don_hang_list, HAS_ANALYTICS)
    
    # === TAB 3: PHÂN TÍCH KHÁCH HÀNG ===
    with tab_customers:
        _render_customer_analysis(don_hang_list, HAS_ANALYTICS)
    
    st.markdown("---")
    
    # === ĐƠN HÀNG GẦN ĐÂY ===
    _render_recent_orders(don_hang_list)


def _render_overview_charts(don_hang_list, danh_gia_list, HAS_ANALYTICS):
    """Render biểu đồ tổng quan"""
    import plotly.express as px
    
    chart_col1, chart_col2 = st.columns(2)
    
    # PIE CHART: TRẠNG THÁI ĐƠN HÀNG
    with chart_col1:
        st.markdown("#### 🥧 Trạng thái đơn hàng")
        
        if don_hang_list:
            status_counts = {'pending': 0, 'processing': 0, 'shipped': 0, 'delivered': 0, 'cancelled': 0}
            for dh in don_hang_list:
                status = dh.get('status', 'pending')
                if status in status_counts:
                    status_counts[status] += 1
            
            status_labels = {
                'pending': 'Chờ xử lý', 'processing': 'Đang xử lý',
                'shipped': 'Đang giao', 'delivered': 'Đã giao', 'cancelled': 'Đã hủy'
            }
            
            pie_data = pd.DataFrame({
                'Trạng thái': [status_labels.get(k, k) for k, v in status_counts.items() if v > 0],
                'Số lượng': [v for v in status_counts.values() if v > 0]
            })
            
            if not pie_data.empty:
                fig_pie = px.pie(
                    pie_data, values='Số lượng', names='Trạng thái',
                    color='Trạng thái',
                    color_discrete_map={
                        'Chờ xử lý': '#FFA500', 'Đang xử lý': '#3498db',
                        'Đang giao': '#9b59b6', 'Đã giao': '#2ecc71', 'Đã hủy': '#e74c3c'
                    },
                    hole=0.4
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white', showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu đơn hàng")
        else:
            st.info("Chưa có dữ liệu đơn hàng")
    
    # BAR CHART: DOANH THU THEO TUẦN
    with chart_col2:
        st.markdown("#### 📊 Doanh thu 7 ngày gần nhất")
        
        if don_hang_list:
            today = datetime.now()
            revenue_by_day = {}
            
            for i in range(7):
                day = today - timedelta(days=i)
                day_str = day.strftime('%d/%m')
                revenue_by_day[day_str] = 0
            
            for dh in don_hang_list:
                if dh.get('status') in ['delivered', 'shipped', 'processing']:
                    order_date_str = dh.get('order_date', '')
                    if order_date_str:
                        try:
                            order_date = datetime.fromisoformat(order_date_str.replace('Z', '+00:00'))
                            day_str = order_date.strftime('%d/%m')
                            if day_str in revenue_by_day:
                                revenue_by_day[day_str] += dh.get('total_amount', 0)
                        except:
                            pass
            
            bar_data = pd.DataFrame({
                'Ngày': list(reversed(list(revenue_by_day.keys()))),
                'Doanh thu': list(reversed(list(revenue_by_day.values())))
            })
            
            fig_bar = px.bar(bar_data, x='Ngày', y='Doanh thu', color_discrete_sequence=['#3498db'])
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color='white', xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu doanh thu")
    
    # SENTIMENT ANALYSIS
    if HAS_ANALYTICS and danh_gia_list:
        from analytics import thong_ke_cam_xuc
        st.markdown("#### 😊 Phân tích cảm xúc đánh giá")
        sentiment_stats = thong_ke_cam_xuc(danh_gia_list)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div style="text-align:center; padding:15px; background:#2ecc7115; border-radius:8px; border:1px solid #2ecc7150;">
                    <div style="font-size:2em; font-weight:bold; color:#2ecc71;">{sentiment_stats.get('Tích cực', 0)}</div>
                    <div style="color:#888;">😊 Tích cực</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="text-align:center; padding:15px; background:#f39c1215; border-radius:8px; border:1px solid #f39c1250;">
                    <div style="font-size:2em; font-weight:bold; color:#f39c12;">{sentiment_stats.get('Trung lập', 0)}</div>
                    <div style="color:#888;">😐 Trung lập</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style="text-align:center; padding:15px; background:#e74c3c15; border-radius:8px; border:1px solid #e74c3c50;">
                    <div style="font-size:2em; font-weight:bold; color:#e74c3c;">{sentiment_stats.get('Tiêu cực', 0)}</div>
                    <div style="color:#888;">😞 Tiêu cực</div>
                </div>
            """, unsafe_allow_html=True)


def _render_forecast(don_hang_list, HAS_ANALYTICS):
    """Render dự báo doanh thu"""
    st.markdown("### 🔮 Dự báo doanh thu với Moving Average")
    
    if not HAS_ANALYTICS:
        st.warning("Module analytics chưa được cài đặt.")
        return
    
    if not don_hang_list:
        st.info("Chưa có dữ liệu đơn hàng.")
        return
    
    from analytics import tinh_doanh_thu_theo_thang, du_bao_moving_average, tinh_tang_truong
    import plotly.express as px
    
    doanh_thu_df = tinh_doanh_thu_theo_thang(don_hang_list)
    
    if doanh_thu_df.empty:
        st.info("Chưa đủ dữ liệu để dự báo.")
        return
    
    # Tính tăng trưởng
    doanh_thu_tang_truong = tinh_tang_truong(doanh_thu_df)
    
    st.markdown("#### 📈 Tăng trưởng theo tháng")
    
    for idx, row in doanh_thu_tang_truong.iterrows():
        tang_truong = row.get('tang_truong_phan_tram', 0)
        if pd.isna(tang_truong):
            tang_truong_text = "N/A"
            color = "#888"
        elif tang_truong > 0:
            tang_truong_text = f"+{tang_truong}%"
            color = "#2ecc71"
        elif tang_truong < 0:
            tang_truong_text = f"{tang_truong}%"
            color = "#e74c3c"
        else:
            tang_truong_text = "0%"
            color = "#f39c12"
        
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:8px; background:#111; border-radius:4px; margin:4px 0;">
                <span>{row['thang']}</span>
                <span>{row['doanh_thu']:,.0f}đ</span>
                <span style="color:{color}; font-weight:bold;">{tang_truong_text}</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 🔮 Dự báo 3 tháng tới")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        window_size = st.slider("Cửa sổ MA", 2, 6, 3, help="Số tháng để tính Moving Average")
    
    du_bao_df = du_bao_moving_average(doanh_thu_df, so_thang_du_bao=3, window=window_size)
    
    if not du_bao_df.empty:
        fig_forecast = px.line(
            du_bao_df, x='thang', y='doanh_thu', color='loai',
            markers=True,
            color_discrete_map={'Thực tế': '#3498db', 'Dự báo': '#e74c3c'}
        )
        fig_forecast.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False, title='Tháng'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Doanh thu (VNĐ)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        du_bao_rows = du_bao_df[du_bao_df['loai'] == 'Dự báo']
        if not du_bao_rows.empty:
            st.markdown("**📊 Dự báo chi tiết:**")
            for _, row in du_bao_rows.iterrows():
                st.markdown(f"""
                    <div style="display:inline-block; padding:10px 20px; background:#e74c3c20; border-radius:8px; margin:5px; border:1px solid #e74c3c50;">
                        <strong>{row['thang']}</strong>: {row['doanh_thu']:,.0f}đ
                    </div>
                """, unsafe_allow_html=True)


def _render_customer_analysis(don_hang_list, HAS_ANALYTICS):
    """Render phân tích khách hàng RFM"""
    st.markdown("### 👥 Phân loại khách hàng (RFM Analysis)")
    
    if not HAS_ANALYTICS:
        st.warning("Module analytics chưa được cài đặt.")
        return
    
    if not don_hang_list:
        st.info("Chưa có dữ liệu đơn hàng.")
        return
    
    from analytics import phan_tich_rfm, thong_ke_rfm
    import plotly.express as px
    
    rfm_df = phan_tich_rfm(don_hang_list)
    
    if rfm_df.empty:
        st.info("Chưa đủ dữ liệu để phân tích RFM.")
        return
    
    rfm_stats = thong_ke_rfm(rfm_df)
    
    st.markdown("#### 📊 Phân bố khách hàng")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div style="text-align:center; padding:15px; background:#FFD70015; border-radius:8px; border:1px solid #FFD70050;">
                <div style="font-size:2em; font-weight:bold; color:#FFD700;">{rfm_stats.get('VIP', 0)}</div>
                <div style="color:#888;">👑 VIP</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style="text-align:center; padding:15px; background:#2ecc7115; border-radius:8px; border:1px solid #2ecc7150;">
                <div style="font-size:2em; font-weight:bold; color:#2ecc71;">{rfm_stats.get('Tiềm năng', 0)}</div>
                <div style="color:#888;">🌱 Tiềm năng</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div style="text-align:center; padding:15px; background:#e74c3c15; border-radius:8px; border:1px solid #e74c3c50;">
                <div style="font-size:2em; font-weight:bold; color:#e74c3c;">{rfm_stats.get('Cần giữ chân', 0)}</div>
                <div style="color:#888;">⚠️ Cần giữ chân</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div style="text-align:center; padding:15px; background:#95a5a615; border-radius:8px; border:1px solid #95a5a650;">
                <div style="font-size:2em; font-weight:bold; color:#95a5a6;">{rfm_stats.get('Khách vãng lai', 0)}</div>
                <div style="color:#888;">👤 Vãng lai</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📋 Danh sách khách hàng theo phân loại")
    
    filter_segment = st.selectbox(
        "Lọc theo phân loại",
        ["Tất cả", "VIP", "Tiềm năng", "Cần giữ chân", "Khách vãng lai"]
    )
    
    display_df = rfm_df.copy()
    if filter_segment != "Tất cả":
        display_df = display_df[display_df['phan_loai'] == filter_segment]
    
    for _, row in display_df.head(20).iterrows():
        color = row['mau']
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding:10px; background:#111; border-radius:4px; margin:4px 0; border-left:3px solid {color};">
                <div>
                    <strong>{row.get('ten', 'N/A')}</strong><br>
                    <span style="color:#888; font-size:0.9em;">{row['email']} | {row.get('dien_thoai', 'N/A')}</span>
                </div>
                <div style="text-align:right;">
                    <span style="color:{color}; font-weight:bold;">{row['phan_loai']}</span><br>
                    <span style="color:#888; font-size:0.9em;">{row['frequency']} đơn | {row['monetary']:,.0f}đ</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Pie chart
    st.markdown("---")
    fig_rfm = px.pie(
        names=list(rfm_stats.keys()),
        values=list(rfm_stats.values()),
        color=list(rfm_stats.keys()),
        color_discrete_map={
            'VIP': '#FFD700', 'Tiềm năng': '#2ecc71',
            'Cần giữ chân': '#e74c3c', 'Khách vãng lai': '#95a5a6'
        },
        hole=0.4
    )
    fig_rfm.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_rfm, use_container_width=True)


def _render_recent_orders(don_hang_list):
    """Render đơn hàng gần đây"""
    st.subheader("🕐 Đơn hàng gần đây")
    
    if not don_hang_list:
        st.info("Chưa có đơn hàng nào")
        return
    
    recent_orders = sorted(don_hang_list, key=lambda x: x.get('order_date', ''), reverse=True)[:5]
    
    for dh in recent_orders:
        status = dh.get('status', 'pending')
        status_styles = {
            'pending': ('🟡', '#FFA500', 'Chờ xử lý'),
            'processing': ('🔵', '#3498db', 'Đang xử lý'),
            'shipped': ('🟣', '#9b59b6', 'Đang giao'),
            'delivered': ('🟢', '#2ecc71', 'Đã giao'),
            'cancelled': ('🔴', '#e74c3c', 'Đã hủy')
        }
        icon, color, text = status_styles.get(status, ('⚪', '#888', status))
        
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1, 3, 2, 2])
            with c1:
                st.write(f"**#{dh.get('id')}**")
            with c2:
                st.write(f"{dh.get('customer_name', 'N/A')}")
                st.caption(f"📞 {dh.get('customer_phone', '')}")
            with c3:
                st.write(f"💰 **{dh.get('total_amount', 0):,.0f}đ**")
            with c4:
                st.markdown(f"""
                    <span style="
                        background-color: {color}20;
                        color: {color};
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-size: 0.85em;
                        font-weight: 500;
                        border: 1px solid {color};
                    ">{icon} {text}</span>
                """, unsafe_allow_html=True)
