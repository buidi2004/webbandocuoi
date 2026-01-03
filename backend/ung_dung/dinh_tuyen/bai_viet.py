from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ..co_so_du_lieu import lay_csdl, BaiViet as BaiVietDB
import re

bo_dinh_tuyen = APIRouter(
    prefix="/api/blog",
    tags=["blog"]
)

# Pydantic models
class BaiVietTao(BaseModel):
    title: str
    excerpt: str | None = None
    content: str
    image_url: str | None = None
    category: str = "tips"
    is_published: bool = False

class BaiVietPhanHoi(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str | None
    content: str
    image_url: str | None
    category: str
    is_published: bool
    views: int
    created_at: datetime | None
    
    class Config:
        from_attributes = True

def tao_slug(title: str) -> str:
    """Tạo slug từ tiêu đề"""
    slug = title.lower()
    slug = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', slug)
    slug = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', slug)
    slug = re.sub(r'[ìíịỉĩ]', 'i', slug)
    slug = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', slug)
    slug = re.sub(r'[ùúụủũưừứựửữ]', 'u', slug)
    slug = re.sub(r'[ỳýỵỷỹ]', 'y', slug)
    slug = re.sub(r'đ', 'd', slug)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = slug.strip('-')
    return slug

# API endpoints
@bo_dinh_tuyen.get("/", response_model=List[BaiVietPhanHoi])
def lay_danh_sach_bai_viet(category: Optional[str] = None, published_only: bool = True, csdl: Session = Depends(lay_csdl)):
    """Lấy danh sách bài viết blog"""
    query = csdl.query(BaiVietDB)
    if published_only:
        query = query.filter(BaiVietDB.is_published == True)
    if category:
        query = query.filter(BaiVietDB.category == category)
    return query.order_by(BaiVietDB.created_at.desc()).all()

@bo_dinh_tuyen.get("/{slug}", response_model=BaiVietPhanHoi)
def lay_bai_viet(slug: str, csdl: Session = Depends(lay_csdl)):
    """Lấy chi tiết một bài viết theo slug"""
    bai_viet = csdl.query(BaiVietDB).filter(BaiVietDB.slug == slug).first()
    if not bai_viet:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    # Tăng lượt xem
    bai_viet.views += 1
    csdl.commit()
    return bai_viet

@bo_dinh_tuyen.post("/", response_model=BaiVietPhanHoi)
def tao_bai_viet(data: BaiVietTao, csdl: Session = Depends(lay_csdl)):
    """Tạo bài viết mới (Admin)"""
    slug = tao_slug(data.title)
    # Đảm bảo slug unique
    existing = csdl.query(BaiVietDB).filter(BaiVietDB.slug == slug).first()
    if existing:
        slug = f"{slug}-{int(datetime.now().timestamp())}"
    
    bai_viet = BaiVietDB(
        title=data.title,
        slug=slug,
        excerpt=data.excerpt,
        content=data.content,
        image_url=data.image_url,
        category=data.category,
        is_published=data.is_published
    )
    csdl.add(bai_viet)
    csdl.commit()
    csdl.refresh(bai_viet)
    return bai_viet

@bo_dinh_tuyen.put("/{id}", response_model=BaiVietPhanHoi)
def cap_nhat_bai_viet(id: int, data: BaiVietTao, csdl: Session = Depends(lay_csdl)):
    """Cập nhật bài viết (Admin)"""
    bai_viet = csdl.query(BaiVietDB).filter(BaiVietDB.id == id).first()
    if not bai_viet:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    
    bai_viet.title = data.title
    bai_viet.excerpt = data.excerpt
    bai_viet.content = data.content
    bai_viet.image_url = data.image_url
    bai_viet.category = data.category
    bai_viet.is_published = data.is_published
    csdl.commit()
    csdl.refresh(bai_viet)
    return bai_viet

@bo_dinh_tuyen.delete("/{id}")
def xoa_bai_viet(id: int, csdl: Session = Depends(lay_csdl)):
    """Xóa bài viết (Admin)"""
    bai_viet = csdl.query(BaiVietDB).filter(BaiVietDB.id == id).first()
    if not bai_viet:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    csdl.delete(bai_viet)
    csdl.commit()
    return {"message": "Đã xóa bài viết"}
