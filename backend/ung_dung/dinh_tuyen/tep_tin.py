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
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=422, 
                detail=f"File type not allowed. Allowed: {', '.join(allowed_types)}. Got: {file.content_type}"
            )
        
        # Đọc file content
        contents = await file.read()
        
        # Validate file size (max 10MB)
        if len(contents) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=422,
                detail=f"File too large. Maximum size: 10MB. Got: {len(contents) / 1024 / 1024:.2f}MB"
            )
        
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
                    error_msg = result.get("error", {}).get("message", "Unknown error")
                    raise HTTPException(
                        status_code=500, 
                        detail=f"ImgBB upload failed: {error_msg}"
                    )
            else:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"ImgBB API error: {response.text[:200]}"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")
