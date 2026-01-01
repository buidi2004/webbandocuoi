/**
 * Google Analytics 4 Tracking Utilities
 * 
 * HƯỚNG DẪN CÀI ĐẶT:
 * 1. Tạo tài khoản GA4 tại https://analytics.google.com
 * 2. Lấy Measurement ID (format: G-XXXXXXXXXX)
 * 3. Thay GA_MEASUREMENT_ID bên dưới bằng ID của bạn
 * 4. Thêm script GA4 vào index.html (đã có sẵn placeholder)
 */

// Placeholder - Thay bằng GA4 Measurement ID thật
const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';

/**
 * Check if gtag is available
 */
const isGtagAvailable = () => {
    return typeof window !== 'undefined' && typeof window.gtag === 'function';
};

/**
 * Track page view
 * @param {string} pagePath - Đường dẫn trang
 * @param {string} pageTitle - Tiêu đề trang
 */
export const trackPageView = (pagePath, pageTitle) => {
    if (!isGtagAvailable()) {
        console.log('[GA4 Debug] Page view:', pagePath, pageTitle);
        return;
    }
    
    window.gtag('config', GA_MEASUREMENT_ID, {
        page_path: pagePath,
        page_title: pageTitle
    });
};

/**
 * Track view item (xem chi tiết sản phẩm)
 * @param {object} product - Thông tin sản phẩm
 */
export const trackViewItem = (product) => {
    if (!isGtagAvailable()) {
        console.log('[GA4 Debug] View item:', product);
        return;
    }

    window.gtag('event', 'view_item', {
        currency: 'VND',
        value: product.price || 0,
        items: [{
            item_id: product.id?.toString() || '',
            item_name: product.name || '',
            item_category: product.category || 'Váy cưới',
            price: product.price || 0
        }]
    });
};

/**
 * Track add to cart
 * @param {object} product - Thông tin sản phẩm
 * @param {number} quantity - Số lượng
 */
export const trackAddToCart = (product, quantity = 1) => {
    if (!isGtagAvailable()) {
        console.log('[GA4 Debug] Add to cart:', product, quantity);
        return;
    }

    window.gtag('event', 'add_to_cart', {
        currency: 'VND',
        value: (product.price || 0) * quantity,
        items: [{
            item_id: product.id?.toString() || '',
            item_name: product.name || '',
            item_category: product.category || 'Váy cưới',
            price: product.price || 0,
            quantity: quantity
        }]
    });
};

/**
 * Track generate lead (gửi form liên hệ)
 * @param {string} formType - Loại form (contact, booking, complaint)
 * @param {object} additionalData - Dữ liệu bổ sung
 */
export const trackGenerateLead = (formType, additionalData = {}) => {
    if (!isGtagAvailable()) {
        console.log('[GA4 Debug] Generate lead:', formType, additionalData);
        return;
    }

    window.gtag('event', 'generate_lead', {
        form_type: formType,
        ...additionalData
    });
};

/**
 * Track conversion (hoàn thành mục tiêu)
 * @param {string} conversionType - Loại conversion
 * @param {object} additionalData - Dữ liệu bổ sung
 */
export const trackConversion = (conversionType, additionalData = {}) => {
    if (!isGtagAvailable()) {
        console.log('[GA4 Debug] Conversion:', conversionType, additionalData);
        return;
    }

    window.gtag('event', 'conversion', {
        send_to: GA_MEASUREMENT_ID,
        conversion_type: conversionType,
        ...additionalData
    });
};

/**
 * Track custom event
 * @param {string} eventName - Tên event
 * @param {object} eventParams - Tham số event
 */
export const trackEvent = (eventName, eventParams = {}) => {
    if (!isGtagAvailable()) {
        console.log('[GA4 Debug] Custom event:', eventName, eventParams);
        return;
    }

    window.gtag('event', eventName, eventParams);
};

/**
 * Track search
 * @param {string} searchTerm - Từ khóa tìm kiếm
 */
export const trackSearch = (searchTerm) => {
    if (!isGtagAvailable()) {
        console.log('[GA4 Debug] Search:', searchTerm);
        return;
    }

    window.gtag('event', 'search', {
        search_term: searchTerm
    });
};

export default {
    trackPageView,
    trackViewItem,
    trackAddToCart,
    trackGenerateLead,
    trackConversion,
    trackEvent,
    trackSearch
};
