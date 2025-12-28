"""
Di chuyển CSDL: Khởi tạo các bảng tính năng mới
(Khiếu nại và Hồ sơ đối tác)
"""
from ung_dung.co_so_du_lieu import khoi_tao_csdl, CoSo, dong_co
import os

print("Khởi tạo các bảng mới trong cơ sở dữ liệu...")
try:
    khoi_tao_csdl()
    print("Thành công: Đã tạo các bảng complaints và partner_applications (nếu chưa có).")
except Exception as loi:
    print(f"Lỗi khi khởi tạo CSDL: {loi}")
