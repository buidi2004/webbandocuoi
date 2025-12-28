import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình Email
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")  # Email gửi (vd: your-email@gmail.com)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # App Password
RECEIVER_EMAIL = "buidi7170@gmail.com"

def gui_email_thong_bao(tieu_de: str, noi_dung: str):
    """Gửi email thông báo khi có khách liên hệ hoặc đặt lịch"""
    if not SMTP_USER or not SMTP_PASSWORD:
        print("CẢNH BÁO: Chưa cấu hình SMTP_USER hoặc SMTP_PASSWORD. Không thể gửi email.")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = tieu_de

        msg.attach(MIMEText(noi_dung, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USER, RECEIVER_EMAIL, text)
        server.quit()
        return True
    except Exception as e:
        print(f"LỖI GỬI EMAIL: {e}")
        return False
