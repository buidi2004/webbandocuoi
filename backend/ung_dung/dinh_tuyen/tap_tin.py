from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import base64
import httpx

bo_dinh_tuyen = APIRouter(
    prefix="/api/tap_tin",
    tags=["tap_tin"]
)

# ImgBB API Key - Lấy từ biến môi trường hoặc dùng key demo
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "c525fc0204b449b541b0f0a5a4f5d9c4")

@bo_dinh_tuyen.post("/upload")
async def tai_len_anh(file: UploadFile = File(...)):
    """Tải lên hình ảnh lên ImgBB"""
    try:
        # Đọc file content
        contents = await file.read()
        
        # Encode sang base64
        base64_image = base64.b64encode(contents).decode('utf-8')
        
        # Upload lên ImgBB
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.imgbb.com/1/upload",
                data={
                    "key": IMGBB_API_KEY,
                    "image": base64_image,
                    "name": file.filename
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    image_url = result["data"]["url"]
                    return {"url": image_url}
                else:
                    raise HTTPException(status_code=500, detail="ImgBB upload failed")
            else:
                raise HTTPException(status_code=response.status_code, detail="ImgBB API error")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")
