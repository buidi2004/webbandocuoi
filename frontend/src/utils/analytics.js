/**
 * Analytics utilities for tracking conversions
 * Integrates with Google Analytics 4 (GA4)
 */

// Track conversion event
export const trackConversion = (eventName, params = {}) => {
    try {
        // Check if gtag is available (GA4)
        if (typeof window !== 'undefined' && window.gtag) {
            window.gtag('event', eventName, {
                ...params,
                send_to: 'default'
            });
        }
        
        // Also log to console in development
        if (import.meta.env.DEV) {
            console.log(`[Analytics] Event: ${eventName}`, params);
        }
    } catch (error) {
        console.warn('Analytics tracking failed:', error);
    }
};

// Track page view
export const trackPageView = (pagePath, pageTitle) => {
    try {
        if (typeof window !== 'undefined' && window.gtag) {
            window.gtag('event', 'page_view', {
                page_path: pagePath,
                page_title: pageTitle
            });
        }
    } catch (error) {
        console.warn('Page view tracking failed:', error);
    }
};

// Track button click
export const trackButtonClick = (buttonName, category = 'engagement') => {
    trackConversion('button_click', {
        button_name: buttonName,
        event_category: category
    });
};

// Track form submission
export const trackFormSubmission = (formName, formData = {}) => {
    trackConversion('form_submit', {
        form_name: formName,
        ...formData
    });
};

export default {
    trackConversion,
    trackPageView,
    trackButtonClick,
    trackFormSubmission
};
