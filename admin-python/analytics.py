"""
IVIE Admin - Analytics & AI Module
===================================
Các tính năng phân tích thông minh:
1. Dashboard dự báo doanh thu (Moving Average)
2. RFM Customer Segmentation
3. Product Recommendation (Association Rules)
4. Sentiment Analysis cho đánh giá
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import json

# ============ 1. DASHBOARD DỰ BÁO DOANH THU ============

def tinh_doanh_thu_theo_thang(don_hang_list):
    """
    Tính doanh thu theo tháng từ danh sách đơn hàng
    Input: List đơn hàng từ API
    Output: DataFrame với cột 'thang' và 'doanh_thu'
    """
    if not don_hang_list:
        return pd.DataFrame(columns=['thang', 'doanh_thu'])
    
    # Chuyển sang DataFrame
    df = pd.DataFrame(don_hang_list)
    
    # Chỉ tính đơn hàng đã giao hoặc đang xử lý
    df = df[df['status'].isin(['delivered', 'shipped', 'processing'])]
    
    if df.empty:
        return pd.DataFrame(columns=['thang', 'doanh_thu'])
    
    # Parse ngày
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    
    # Tạo cột tháng
    df['thang'] = df['order_date'].dt.to_period('M')
    
    # Group by tháng
    doanh_thu = df.groupby('thang')['total_amount'].sum().reset_index()
    doanh_thu.columns = ['thang', 'doanh_thu']
    doanh_thu['thang'] = doanh_thu['thang'].astype(str)
    
    return doanh_thu


def du_bao_moving_average(doanh_thu_df, so_thang_du_bao=3, window=3):
    """
    Dự báo doanh thu bằng Moving Average
    Input: DataFrame doanh thu theo tháng
    Output: DataFrame với dự báo cho các tháng tới
    """
    if doanh_thu_df.empty or len(doanh_thu_df) < window:
        return pd.DataFrame(columns=['thang', 'doanh_thu', 'loai'])
    
    # Tính Moving Average
    doanh_thu_df = doanh_thu_df.copy()
    doanh_thu_df['ma'] = doanh_thu_df['doanh_thu'].rolling(window=window, min_periods=1).mean()
    doanh_thu_df['loai'] = 'Thực tế'
    
    # Dự báo các tháng tới
    last_ma = doanh_thu_df['ma'].iloc[-1]
    last_month = pd.to_datetime(doanh_thu_df['thang'].iloc[-1])
    
    du_bao_list = []
    for i in range(1, so_thang_du_bao + 1):
        next_month = last_month + pd.DateOffset(months=i)
        du_bao_list.append({
            'thang': next_month.strftime('%Y-%m'),
            'doanh_thu': last_ma,
            'loai': 'Dự báo'
        })
    
    # Kết hợp
    result = pd.concat([
        doanh_thu_df[['thang', 'doanh_thu', 'loai']],
        pd.DataFrame(du_bao_list)
    ], ignore_index=True)
    
    return result


def tinh_tang_truong(doanh_thu_df):
    """
    Tính tỷ lệ tăng trưởng so với tháng trước
    Output: DataFrame với cột 'tang_truong_phan_tram'
    """
    if doanh_thu_df.empty or len(doanh_thu_df) < 2:
        return doanh_thu_df
    
    df = doanh_thu_df.copy()
    df['tang_truong'] = df['doanh_thu'].diff()
    df['tang_truong_phan_tram'] = (df['tang_truong'] / df['doanh_thu'].shift(1) * 100).round(1)
    
    return df


# ============ 2. RFM CUSTOMER SEGMENTATION ============

def phan_tich_rfm(don_hang_list, ngay_hien_tai=None):
    """
    Phân tích RFM (Recency, Frequency, Monetary) cho khách hàng
    
    Input: List đơn hàng từ API
    Output: DataFrame với phân loại khách hàng
    
    Phân loại:
    - VIP: Mua nhiều, chi đậm, gần đây
    - Tiềm năng: Mới mua, ít đơn
    - Cần giữ chân: Đã lâu không quay lại
    - Khách vãng lai: Mua ít, chi ít
    """
    if not don_hang_list:
        return pd.DataFrame()
    
    if ngay_hien_tai is None:
        ngay_hien_tai = datetime.now()
    
    df = pd.DataFrame(don_hang_list)
    
    # Chỉ tính đơn hàng thành công
    df = df[df['status'].isin(['delivered', 'shipped', 'processing'])]
    
    if df.empty:
        return pd.DataFrame()
    
    # Parse ngày
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    
    # Tính RFM cho mỗi khách hàng (theo email hoặc phone)
    rfm = df.groupby('customer_email').agg({
        'order_date': lambda x: (ngay_hien_tai - x.max()).days,  # Recency
        'id': 'count',  # Frequency
        'total_amount': 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = ['email', 'recency', 'frequency', 'monetary']
    
    # Thêm thông tin khách hàng
    customer_info = df.groupby('customer_email').agg({
        'customer_name': 'first',
        'customer_phone': 'first'
    }).reset_index()
    customer_info.columns = ['email', 'ten', 'dien_thoai']
    
    rfm = rfm.merge(customer_info, on='email', how='left')
    
    # Tính điểm RFM (1-5)
    rfm['r_score'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    
    # Chuyển sang số
    rfm['r_score'] = rfm['r_score'].astype(int)
    rfm['f_score'] = rfm['f_score'].astype(int)
    rfm['m_score'] = rfm['m_score'].astype(int)
    
    # Tính tổng điểm
    rfm['rfm_score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']
    
    # Phân loại khách hàng
    def phan_loai(row):
        r, f, m = row['r_score'], row['f_score'], row['m_score']
        
        # VIP: Điểm cao ở cả 3 tiêu chí
        if r >= 4 and f >= 4 and m >= 4:
            return 'VIP'
        
        # Tiềm năng: Mới mua (R cao), ít đơn (F thấp)
        if r >= 4 and f <= 2:
            return 'Tiềm năng'
        
        # Cần giữ chân: Đã lâu không quay lại (R thấp), từng mua nhiều
        if r <= 2 and (f >= 3 or m >= 3):
            return 'Cần giữ chân'
        
        # Khách vãng lai: Còn lại
        return 'Khách vãng lai'
    
    rfm['phan_loai'] = rfm.apply(phan_loai, axis=1)
    
    # Màu sắc cho từng loại
    mau_sac = {
        'VIP': '#FFD700',  # Vàng
        'Tiềm năng': '#2ecc71',  # Xanh lá
        'Cần giữ chân': '#e74c3c',  # Đỏ
        'Khách vãng lai': '#95a5a6'  # Xám
    }
    rfm['mau'] = rfm['phan_loai'].map(mau_sac)
    
    return rfm


def thong_ke_rfm(rfm_df):
    """
    Thống kê số lượng khách theo từng phân loại
    """
    if rfm_df.empty:
        return {}
    
    stats = rfm_df['phan_loai'].value_counts().to_dict()
    return stats


# ============ 3. PRODUCT RECOMMENDATION (Association Rules) ============

def phan_tich_ket_hop(don_hang_list, chi_tiet_don_hang_list):
    """
    Phân tích quy luật kết hợp sản phẩm
    Tìm các sản phẩm thường được mua cùng nhau
    
    Input: 
    - don_hang_list: Danh sách đơn hàng
    - chi_tiet_don_hang_list: Chi tiết đơn hàng (product_id, order_id)
    
    Output: Dict với key là product_id, value là list các product_id thường đi kèm
    """
    if not chi_tiet_don_hang_list:
        return {}
    
    # Group sản phẩm theo đơn hàng
    order_products = defaultdict(set)
    for item in chi_tiet_don_hang_list:
        order_id = item.get('order_id')
        product_id = item.get('product_id')
        if order_id and product_id:
            order_products[order_id].add(product_id)
    
    # Đếm số lần các cặp sản phẩm xuất hiện cùng nhau
    pair_counts = defaultdict(int)
    product_counts = defaultdict(int)
    
    for order_id, products in order_products.items():
        products = list(products)
        for p in products:
            product_counts[p] += 1
        
        # Đếm cặp
        for i in range(len(products)):
            for j in range(i + 1, len(products)):
                pair = tuple(sorted([products[i], products[j]]))
                pair_counts[pair] += 1
    
    # Tính confidence cho mỗi cặp
    recommendations = defaultdict(list)
    
    for (p1, p2), count in pair_counts.items():
        if count >= 2:  # Ít nhất 2 lần xuất hiện cùng nhau
            # Confidence: P(p2|p1) = count(p1,p2) / count(p1)
            conf_1_to_2 = count / product_counts[p1] if product_counts[p1] > 0 else 0
            conf_2_to_1 = count / product_counts[p2] if product_counts[p2] > 0 else 0
            
            if conf_1_to_2 >= 0.3:  # Threshold 30%
                recommendations[p1].append({
                    'product_id': p2,
                    'confidence': round(conf_1_to_2 * 100, 1),
                    'count': count
                })
            
            if conf_2_to_1 >= 0.3:
                recommendations[p2].append({
                    'product_id': p1,
                    'confidence': round(conf_2_to_1 * 100, 1),
                    'count': count
                })
    
    # Sắp xếp theo confidence
    for p_id in recommendations:
        recommendations[p_id] = sorted(
            recommendations[p_id], 
            key=lambda x: x['confidence'], 
            reverse=True
        )[:5]  # Top 5
    
    return dict(recommendations)


def goi_y_san_pham(product_id, recommendations, san_pham_list):
    """
    Lấy gợi ý sản phẩm cho một sản phẩm cụ thể
    
    Output: List các sản phẩm gợi ý với thông tin chi tiết
    """
    if product_id not in recommendations:
        return []
    
    # Tạo dict sản phẩm để lookup nhanh
    product_dict = {p['id']: p for p in san_pham_list}
    
    result = []
    for rec in recommendations[product_id]:
        rec_id = rec['product_id']
        if rec_id in product_dict:
            product = product_dict[rec_id]
            result.append({
                'id': rec_id,
                'name': product.get('name', ''),
                'image_url': product.get('image_url', ''),
                'price': product.get('rental_price_day', 0),
                'confidence': rec['confidence'],
                'message': f"{rec['confidence']}% khách hàng cũng thuê sản phẩm này"
            })
    
    return result


# ============ 4. SENTIMENT ANALYSIS ============

# Từ điển cảm xúc tiếng Việt đơn giản
TU_TICH_CUC = [
    'tuyệt vời', 'xuất sắc', 'đẹp', 'tốt', 'hài lòng', 'thích', 'yêu', 
    'chất lượng', 'nhanh', 'chu đáo', 'nhiệt tình', 'chuyên nghiệp',
    'ưng ý', 'hoàn hảo', 'tận tâm', 'ok', 'good', 'nice', 'great',
    'recommend', 'giới thiệu', 'quay lại', 'ủng hộ', 'cảm ơn', 'thanks'
]

TU_TIEU_CUC = [
    'tệ', 'xấu', 'chán', 'thất vọng', 'không hài lòng', 'chậm', 'lâu',
    'kém', 'dở', 'tồi', 'phàn nàn', 'khiếu nại', 'hoàn tiền', 'hủy',
    'bad', 'poor', 'terrible', 'worst', 'không tốt', 'không đẹp',
    'không ưng', 'không thích', 'không recommend', 'không giới thiệu',
    'lừa đảo', 'gian lận', 'fake', 'giả', 'rách', 'hỏng', 'bẩn'
]


def phan_tich_cam_xuc(text, rating=None):
    """
    Phân tích cảm xúc của một đánh giá
    
    Input:
    - text: Nội dung đánh giá
    - rating: Số sao (1-5), optional
    
    Output: Dict với sentiment và score
    """
    if not text:
        if rating:
            if rating >= 4:
                return {'sentiment': 'Tích cực', 'score': 0.7, 'color': '#2ecc71'}
            elif rating <= 2:
                return {'sentiment': 'Tiêu cực', 'score': -0.7, 'color': '#e74c3c'}
        return {'sentiment': 'Trung lập', 'score': 0, 'color': '#f39c12'}
    
    text_lower = text.lower()
    
    # Đếm từ tích cực và tiêu cực
    positive_count = sum(1 for word in TU_TICH_CUC if word in text_lower)
    negative_count = sum(1 for word in TU_TIEU_CUC if word in text_lower)
    
    # Tính score (-1 đến 1)
    total = positive_count + negative_count
    if total == 0:
        score = 0
    else:
        score = (positive_count - negative_count) / total
    
    # Kết hợp với rating nếu có
    if rating:
        rating_score = (rating - 3) / 2  # Chuyển 1-5 thành -1 đến 1
        score = (score + rating_score) / 2
    
    # Phân loại
    if score > 0.2:
        return {'sentiment': 'Tích cực', 'score': round(score, 2), 'color': '#2ecc71'}
    elif score < -0.2:
        return {'sentiment': 'Tiêu cực', 'score': round(score, 2), 'color': '#e74c3c'}
    else:
        return {'sentiment': 'Trung lập', 'score': round(score, 2), 'color': '#f39c12'}


def phan_tich_danh_gia_list(danh_gia_list):
    """
    Phân tích cảm xúc cho danh sách đánh giá
    
    Output: List đánh giá với thêm trường sentiment
    """
    result = []
    canh_bao = []
    
    for dg in danh_gia_list:
        sentiment = phan_tich_cam_xuc(
            dg.get('comment', ''),
            dg.get('rating')
        )
        
        dg_copy = dg.copy()
        dg_copy['sentiment'] = sentiment['sentiment']
        dg_copy['sentiment_score'] = sentiment['score']
        dg_copy['sentiment_color'] = sentiment['color']
        
        result.append(dg_copy)
        
        # Cảnh báo nếu tiêu cực
        if sentiment['sentiment'] == 'Tiêu cực' or dg.get('rating', 5) <= 2:
            canh_bao.append({
                'id': dg.get('id'),
                'product_id': dg.get('product_id'),
                'user_name': dg.get('user_name'),
                'rating': dg.get('rating'),
                'comment': dg.get('comment', '')[:100],
                'sentiment': sentiment['sentiment']
            })
    
    return result, canh_bao


def thong_ke_cam_xuc(danh_gia_list):
    """
    Thống kê tổng quan cảm xúc
    """
    if not danh_gia_list:
        return {'Tích cực': 0, 'Trung lập': 0, 'Tiêu cực': 0}
    
    analyzed, _ = phan_tich_danh_gia_list(danh_gia_list)
    
    stats = {'Tích cực': 0, 'Trung lập': 0, 'Tiêu cực': 0}
    for dg in analyzed:
        sentiment = dg.get('sentiment', 'Trung lập')
        if sentiment in stats:
            stats[sentiment] += 1
    
    return stats
