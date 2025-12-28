from fastapi import APIRouter, UploadFile, File
import shutil
import os
import uuid

bo_dinh_tuyen = APIRouter(
    prefix="/api/tap_tin",
    tags=["tap_tin"]
)

# Đường dẫn đến thư mục public/images của frontend
# Lưu ý: Đường dẫn này phụ thuộc vào cấu trúc thư mục hiện tại
THU_MUC_ANH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../frontend/public/images"))

@bo_dinh_tuyen.post("/upload")
async def tai_len_anh(file: UploadFile = File(...)):
    """Tải lên hình ảnh và lưu vào thư mục public của frontend"""
    # Tạo tên file duy nhất để tránh trùng lặp
    duoi_file = os.path.splitext(file.filename)[1]
    ten_file_moi = f"{uuid.uuid4()}{duoi_file}"
    
    duong_dan_luu = os.path.join(THU_MUC_ANH, ten_file_moi)
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(THU_MUC_ANH, exist_ok=True)
    
    # Lưu file
    with open(duong_dan_luu, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Trả về đường dẫn tương đối để frontend sử dụng
    return {"url": f"/images/{ten_file_moi}"}
