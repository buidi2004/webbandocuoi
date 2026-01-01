"""
Telegram Bot Integration cho IVIE Wedding Studio
Gửi thông báo khi có khách hàng mới đăng ký
"""
import os
import httpx
from typing import Optional

# Lấy config từ environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

async def gui_thong_bao_telegram(
    ten_khach: str,
    so_dien_thoai: str,
    email: Optional[str] = None,
    dia_chi: Optional[str] = None,
    noi_dung: Optional[str] = None,
    loai_form: str = "lien_he"
) -> bool:
    """
    Gửi thông báo về Telegram khi có khách mới
    
    Args:
        ten_khach: Tên khách hàng
        so_dien_thoai: Số điện thoại
        email: Email (optional)
        dia_chi: Địa chỉ (optional)
        noi_dung: Nội dung tin nhắn (optional)
        loai_form: Loại form (lien_he, dat_lich, khieu_nai)
    
    Returns:
        True nếu gửi thành công, False nếu thất bại
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram chưa được cấu hình (TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID)")
        return False
    
    # Emoji theo loại form
    emoji_map = {
        "lien_he": "📩",
        "dat_lich": "🗓️",
        "khieu_nai": "⚠️",
        "tu_van": "💬"
    }
    emoji = emoji_map.get(loai_form, "📩")
    
    # Format message
    message = f"""
{emoji} *KHÁCH HÀNG MỚI - IVIE WEDDING*

👤 *Họ tên:* {ten_khach}
📞 *SĐT:* `{so_dien_thoai}`
"""
    
    if email:
        message += f"✉️ *Email:* {email}\n"
    
    if dia_chi:
        message += f"📍 *Địa chỉ:* {dia_chi}\n"
    
    if noi_dung:
        message += f"\n💬 *Nội dung:*\n{noi_dung}\n"
    
    message += f"\n⏰ _Vui lòng liên hệ khách trong 15 phút!_"
    
    # Gửi request đến Telegram API
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Đã gửi thông báo Telegram cho khách: {ten_khach}")
                return True
            else:
                print(f"❌ Lỗi gửi Telegram: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Exception khi gửi Telegram: {str(e)}")
        return False


def gui_thong_bao_telegram_sync(
    ten_khach: str,
    so_dien_thoai: str,
    email: Optional[str] = None,
    dia_chi: Optional[str] = None,
    noi_dung: Optional[str] = None,
    loai_form: str = "lien_he"
) -> bool:
    """
    Phiên bản sync của gui_thong_bao_telegram
    Dùng cho các endpoint không async
    """
    import requests
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram chưa được cấu hình")
        return False
    
    emoji_map = {
        "lien_he": "📩",
        "dat_lich": "🗓️", 
        "khieu_nai": "⚠️",
        "tu_van": "💬"
    }
    emoji = emoji_map.get(loai_form, "📩")
    
    message = f"""
{emoji} *KHÁCH HÀNG MỚI - IVIE WEDDING*

👤 *Họ tên:* {ten_khach}
📞 *SĐT:* `{so_dien_thoai}`
"""
    
    if email:
        message += f"✉️ *Email:* {email}\n"
    if dia_chi:
        message += f"📍 *Địa chỉ:* {dia_chi}\n"
    if noi_dung:
        message += f"\n💬 *Nội dung:*\n{noi_dung}\n"
    
    message += f"\n⏰ _Vui lòng liên hệ khách trong 15 phút!_"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False
