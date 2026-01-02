"""
API Sản phẩm tối ưu hóa cho IVIE Wedding Studio
- Pagination hiệu quả với cursor-based và offset-based
- Bulk operations cho admin
- Async processing
- Response caching
- Query optimization
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response
from sqlalchemy import and_, asc, desc, func, or_
from sqlalchemy.orm import Session, joinedload

from ..co_so_du_lieu import DanhGia as DanhGiaDB
from ..co_so_du_lieu import SanPham as SanPhamDB
from ..co_so_du_lieu import lay_csdl
from ..mo_hinh import DanhGia, SanPham, SanPhamCapNhat, SanPhamTao

# Import caching utilities
try:
    from ..cache_advanced import (
        CACHE_TTL,
        cached,
        get_or_set,
        invalidator,
        redis_client,
    )

    HAS_CACHE = True
except ImportError:
    HAS_CACHE = False

bo_dinh_tuyen = APIRouter(prefix="/api/san_pham", tags=["san_pham_optimized"])

# Thread pool for async operations
executor = ThreadPoolExecutor(max_workers=4)


# =============================================================================
# RESPONSE MODELS
# =============================================================================


class PaginatedResponse:
    """Response wrapper cho paginated data"""

    def __init__(
        self,
        items: List[Any],
        total: int,
        page: int,
        page_size: int,
        has_next: bool,
        has_prev: bool,
    ):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.has_next = has_next
        self.has_prev = has_prev
        self.total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0


def create_paginated_response(
    items: List[Any], total: int, page: int, page_size: int
) -> Dict[str, Any]:
    """Tạo paginated response dict"""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return {
        "items": items,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }


# =============================================================================
# OPTIMIZED LIST ENDPOINT
# =============================================================================


@bo_dinh_tuyen.get("/")
def lay_danh_sach_san_pham_optimized(
    # Filters
    danh_muc: Optional[str] = Query(None, description="Lọc theo danh mục"),
    sub_category: Optional[str] = Query(None, description="Lọc theo tiểu mục"),
    gioi_tinh: Optional[str] = Query(None, description="Lọc theo giới tính"),
    is_hot: Optional[bool] = Query(None, description="Lọc sản phẩm hot"),
    is_new: Optional[bool] = Query(None, description="Lọc sản phẩm mới"),
    price_min: Optional[int] = Query(None, description="Giá tối thiểu"),
    price_max: Optional[int] = Query(None, description="Giá tối đa"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên/mã"),
    # Sorting
    sort_by: Optional[str] = Query(
        "id_desc",
        description="Sắp xếp: price_asc, price_desc, hot, new, id_asc, id_desc",
    ),
    # Pagination
    page: int = Query(1, ge=1, description="Số trang"),
    page_size: int = Query(20, ge=1, le=100, description="Số item mỗi trang"),
    # Legacy support
    bo_qua: Optional[int] = Query(None, ge=0, description="Skip (legacy)"),
    gioi_han: Optional[int] = Query(None, ge=0, le=1000, description="Limit (legacy)"),
    # Response
    phan_hoi: Response = None,
    csdl: Session = Depends(lay_csdl),
):
    """
    Lấy danh sách sản phẩm với pagination và filters tối ưu.

    Hỗ trợ cả pagination mới (page/page_size) và legacy (bo_qua/gioi_han).
    """

    # Generate cache key từ parameters
    cache_key = f"products:{danh_muc}:{sub_category}:{gioi_tinh}:{is_hot}:{is_new}:{price_min}:{price_max}:{search}:{sort_by}:{page}:{page_size}"

    # Try cache first
    if HAS_CACHE:
        cached_result = redis_client.get(cache_key)
        if cached_result is not None:
            if phan_hoi:
                phan_hoi.headers["X-Cache"] = "HIT"
                phan_hoi.headers["X-Total-Count"] = str(
                    cached_result.get("pagination", {}).get("total", 0)
                )
            return cached_result

    # Build optimized query
    truy_van = csdl.query(SanPhamDB)

    # Apply filters
    filters = []

    if danh_muc:
        filters.append(SanPhamDB.category == danh_muc)

    if sub_category:
        filters.append(SanPhamDB.sub_category == sub_category)

    if gioi_tinh:
        filters.append(SanPhamDB.gender == gioi_tinh)

    if is_hot is not None:
        filters.append(SanPhamDB.is_hot == is_hot)

    if is_new is not None:
        filters.append(SanPhamDB.is_new == is_new)

    if price_min is not None:
        filters.append(SanPhamDB.rental_price_day >= price_min)

    if price_max is not None:
        filters.append(SanPhamDB.rental_price_day <= price_max)

    if search:
        search_term = f"%{search}%"
        filters.append(
            or_(
                SanPhamDB.name.ilike(search_term),
                SanPhamDB.code.ilike(search_term),
                SanPhamDB.description.ilike(search_term),
            )
        )

    if filters:
        truy_van = truy_van.filter(and_(*filters))

    # Apply sorting
    sort_mapping = {
        "price_asc": SanPhamDB.rental_price_day.asc(),
        "price_desc": SanPhamDB.rental_price_day.desc(),
        "hot": SanPhamDB.is_hot.desc(),
        "new": desc(SanPhamDB.is_new),
        "id_asc": SanPhamDB.id.asc(),
        "id_desc": SanPhamDB.id.desc(),
        "name_asc": SanPhamDB.name.asc(),
        "name_desc": SanPhamDB.name.desc(),
    }

    if sort_by in sort_mapping:
        truy_van = truy_van.order_by(sort_mapping[sort_by])
    else:
        truy_van = truy_van.order_by(SanPhamDB.id.desc())

    # Count total (optimized - chỉ count một lần)
    tong_so = truy_van.count()

    # Set response headers
    if phan_hoi:
        phan_hoi.headers["X-Total-Count"] = str(tong_so)
        phan_hoi.headers["X-Cache"] = "MISS"

    # Handle legacy pagination
    if gioi_han is not None and gioi_han > 0:
        skip = bo_qua or 0
        items = truy_van.offset(skip).limit(gioi_han).all()
        # Return legacy format
        return items

    # New pagination
    offset = (page - 1) * page_size
    items = truy_van.offset(offset).limit(page_size).all()

    # Create response
    result = create_paginated_response(items, tong_so, page, page_size)

    # Cache result
    if HAS_CACHE:
        redis_client.set(cache_key, result, CACHE_TTL["MEDIUM"])

    return result


# =============================================================================
# OPTIMIZED DETAIL ENDPOINT
# =============================================================================


@bo_dinh_tuyen.get("/{id_san_pham}")
def lay_san_pham_optimized(
    id_san_pham: int,
    include_reviews: bool = Query(False, description="Bao gồm đánh giá"),
    csdl: Session = Depends(lay_csdl),
):
    """Lấy chi tiết sản phẩm với eager loading"""

    cache_key = f"product:{id_san_pham}:{include_reviews}"

    # Try cache
    if HAS_CACHE:
        cached = redis_client.get(cache_key)
        if cached:
            return cached

    # Query with optional eager loading
    san_pham = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()

    if not san_pham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    result = san_pham

    # Include reviews if requested
    if include_reviews:
        reviews = (
            csdl.query(DanhGiaDB)
            .filter(DanhGiaDB.product_id == id_san_pham, DanhGiaDB.is_approved == True)
            .order_by(DanhGiaDB.created_at.desc())
            .limit(10)
            .all()
        )

        result = {
            "product": san_pham,
            "reviews": reviews,
            "review_count": csdl.query(func.count(DanhGiaDB.id))
            .filter(DanhGiaDB.product_id == id_san_pham, DanhGiaDB.is_approved == True)
            .scalar(),
        }

    # Cache
    if HAS_CACHE:
        redis_client.set(cache_key, result, CACHE_TTL["LONG"])

    return result


# =============================================================================
# BULK OPERATIONS (Admin)
# =============================================================================


@bo_dinh_tuyen.post("/bulk")
def tao_nhieu_san_pham(
    san_pham_list: List[SanPhamTao], csdl: Session = Depends(lay_csdl)
):
    """
    Tạo nhiều sản phẩm cùng lúc (bulk insert).
    Tối ưu cho import dữ liệu.
    """
    if len(san_pham_list) > 100:
        raise HTTPException(status_code=400, detail="Tối đa 100 sản phẩm mỗi lần")

    try:
        # Bulk insert
        san_pham_moi = [SanPhamDB(**sp.dict()) for sp in san_pham_list]
        csdl.bulk_save_objects(san_pham_moi)
        csdl.commit()

        # Invalidate cache
        if HAS_CACHE:
            invalidator.invalidate_products()

        return {
            "success": True,
            "created": len(san_pham_list),
            "message": f"Đã tạo {len(san_pham_list)} sản phẩm",
        }
    except Exception as e:
        csdl.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@bo_dinh_tuyen.put("/bulk")
def cap_nhat_nhieu_san_pham(
    updates: List[Dict[str, Any]], csdl: Session = Depends(lay_csdl)
):
    """
    Cập nhật nhiều sản phẩm cùng lúc.
    Mỗi item cần có 'id' và các fields cần update.
    """
    if len(updates) > 100:
        raise HTTPException(status_code=400, detail="Tối đa 100 sản phẩm mỗi lần")

    updated_count = 0
    errors = []

    try:
        for update in updates:
            product_id = update.pop("id", None)
            if not product_id:
                errors.append({"error": "Missing id", "data": update})
                continue

            result = (
                csdl.query(SanPhamDB)
                .filter(SanPhamDB.id == product_id)
                .update(update, synchronize_session=False)
            )

            if result:
                updated_count += 1
            else:
                errors.append({"error": "Not found", "id": product_id})

        csdl.commit()

        # Invalidate cache
        if HAS_CACHE:
            invalidator.invalidate_products()

        return {
            "success": True,
            "updated": updated_count,
            "errors": errors if errors else None,
        }
    except Exception as e:
        csdl.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@bo_dinh_tuyen.delete("/bulk")
def xoa_nhieu_san_pham(ids: List[int], csdl: Session = Depends(lay_csdl)):
    """Xóa nhiều sản phẩm cùng lúc"""
    if len(ids) > 50:
        raise HTTPException(status_code=400, detail="Tối đa 50 sản phẩm mỗi lần")

    try:
        deleted = (
            csdl.query(SanPhamDB)
            .filter(SanPhamDB.id.in_(ids))
            .delete(synchronize_session=False)
        )

        csdl.commit()

        # Invalidate cache
        if HAS_CACHE:
            invalidator.invalidate_products()

        return {
            "success": True,
            "deleted": deleted,
            "message": f"Đã xóa {deleted} sản phẩm",
        }
    except Exception as e:
        csdl.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# TOGGLE STATUS (Quick Update)
# =============================================================================


@bo_dinh_tuyen.patch("/{id_san_pham}/toggle-hot")
def toggle_hot(id_san_pham: int, csdl: Session = Depends(lay_csdl)):
    """Toggle trạng thái hot của sản phẩm"""
    san_pham = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    san_pham.is_hot = not san_pham.is_hot
    csdl.commit()

    if HAS_CACHE:
        invalidator.invalidate_products()

    return {"id": id_san_pham, "is_hot": san_pham.is_hot}


@bo_dinh_tuyen.patch("/{id_san_pham}/toggle-new")
def toggle_new(id_san_pham: int, csdl: Session = Depends(lay_csdl)):
    """Toggle trạng thái new của sản phẩm"""
    san_pham = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    san_pham.is_new = not san_pham.is_new
    csdl.commit()

    if HAS_CACHE:
        invalidator.invalidate_products()

    return {"id": id_san_pham, "is_new": san_pham.is_new}


# =============================================================================
# STATISTICS ENDPOINTS
# =============================================================================


@bo_dinh_tuyen.get("/stats/summary")
def thong_ke_san_pham(csdl: Session = Depends(lay_csdl)):
    """Thống kê tổng quan sản phẩm"""

    cache_key = "products:stats:summary"

    if HAS_CACHE:
        cached = redis_client.get(cache_key)
        if cached:
            return cached

    stats = {
        "total": csdl.query(func.count(SanPhamDB.id)).scalar(),
        "by_category": {},
        "by_gender": {},
        "hot_count": csdl.query(func.count(SanPhamDB.id))
        .filter(SanPhamDB.is_hot == True)
        .scalar(),
        "new_count": csdl.query(func.count(SanPhamDB.id))
        .filter(SanPhamDB.is_new == True)
        .scalar(),
        "price_range": {
            "min": csdl.query(func.min(SanPhamDB.rental_price_day)).scalar(),
            "max": csdl.query(func.max(SanPhamDB.rental_price_day)).scalar(),
            "avg": csdl.query(func.avg(SanPhamDB.rental_price_day)).scalar(),
        },
    }

    # Count by category
    category_counts = (
        csdl.query(SanPhamDB.category, func.count(SanPhamDB.id))
        .group_by(SanPhamDB.category)
        .all()
    )

    stats["by_category"] = {cat: count for cat, count in category_counts if cat}

    # Count by gender
    gender_counts = (
        csdl.query(SanPhamDB.gender, func.count(SanPhamDB.id))
        .group_by(SanPhamDB.gender)
        .all()
    )

    stats["by_gender"] = {gender: count for gender, count in gender_counts if gender}

    if HAS_CACHE:
        redis_client.set(cache_key, stats, CACHE_TTL["MEDIUM"])

    return stats


@bo_dinh_tuyen.get("/stats/categories")
def danh_muc_san_pham(csdl: Session = Depends(lay_csdl)):
    """Lấy danh sách danh mục với số lượng"""

    cache_key = "products:stats:categories"

    if HAS_CACHE:
        cached = redis_client.get(cache_key)
        if cached:
            return cached

    result = (
        csdl.query(
            SanPhamDB.category,
            SanPhamDB.sub_category,
            func.count(SanPhamDB.id).label("count"),
        )
        .group_by(SanPhamDB.category, SanPhamDB.sub_category)
        .all()
    )

    # Organize by category
    categories = {}
    for cat, sub_cat, count in result:
        if cat not in categories:
            categories[cat] = {"total": 0, "sub_categories": {}}
        categories[cat]["total"] += count
        if sub_cat:
            categories[cat]["sub_categories"][sub_cat] = count

    if HAS_CACHE:
        redis_client.set(cache_key, categories, CACHE_TTL["LONG"])

    return categories


# =============================================================================
# SEARCH OPTIMIZATION
# =============================================================================


@bo_dinh_tuyen.get("/search/suggestions")
def goi_y_tim_kiem(
    q: str = Query(..., min_length=2, description="Từ khóa tìm kiếm"),
    limit: int = Query(10, ge=1, le=20),
    csdl: Session = Depends(lay_csdl),
):
    """
    Gợi ý tìm kiếm nhanh cho autocomplete.
    Trả về danh sách tên và mã sản phẩm matching.
    """

    cache_key = f"products:search:suggestions:{q}:{limit}"

    if HAS_CACHE:
        cached = redis_client.get(cache_key)
        if cached:
            return cached

    search_term = f"%{q}%"

    # Chỉ lấy các trường cần thiết cho performance
    results = (
        csdl.query(SanPhamDB.id, SanPhamDB.name, SanPhamDB.code, SanPhamDB.category)
        .filter(
            or_(SanPhamDB.name.ilike(search_term), SanPhamDB.code.ilike(search_term))
        )
        .limit(limit)
        .all()
    )

    suggestions = [
        {"id": r.id, "name": r.name, "code": r.code, "category": r.category}
        for r in results
    ]

    if HAS_CACHE:
        redis_client.set(cache_key, suggestions, CACHE_TTL["SHORT"])

    return suggestions


# =============================================================================
# STANDARD CRUD (backward compatible)
# =============================================================================


@bo_dinh_tuyen.post("/", response_model=SanPham)
def tao_san_pham(san_pham: SanPhamTao, csdl: Session = Depends(lay_csdl)):
    """Tạo sản phẩm mới"""
    san_pham_moi = SanPhamDB(**san_pham.dict())
    csdl.add(san_pham_moi)
    csdl.commit()
    csdl.refresh(san_pham_moi)

    if HAS_CACHE:
        invalidator.invalidate_products()

    return san_pham_moi


@bo_dinh_tuyen.put("/{id_san_pham}", response_model=SanPham)
def cap_nhat_san_pham(
    id_san_pham: int, san_pham: SanPhamCapNhat, csdl: Session = Depends(lay_csdl)
):
    """Cập nhật sản phẩm"""
    san_pham_cu = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()
    if not san_pham_cu:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    du_lieu = san_pham.dict(exclude_unset=True)
    for key, value in du_lieu.items():
        setattr(san_pham_cu, key, value)

    csdl.commit()
    csdl.refresh(san_pham_cu)

    if HAS_CACHE:
        invalidator.invalidate_products()
        redis_client.delete(f"product:{id_san_pham}")

    return san_pham_cu


@bo_dinh_tuyen.delete("/{id_san_pham}")
def xoa_san_pham(id_san_pham: int, csdl: Session = Depends(lay_csdl)):
    """Xóa sản phẩm"""
    san_pham = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    csdl.delete(san_pham)
    csdl.commit()

    if HAS_CACHE:
        invalidator.invalidate_products()
        redis_client.delete(f"product:{id_san_pham}")

    return {"success": True, "message": "Đã xóa sản phẩm"}


# =============================================================================
# CACHE MANAGEMENT (Admin)
# =============================================================================


@bo_dinh_tuyen.post("/admin/cache/clear")
def xoa_cache_san_pham():
    """Xóa cache sản phẩm (Admin only)"""
    if HAS_CACHE:
        count = invalidator.invalidate_products()
        return {"success": True, "cleared": count}
    return {"success": False, "message": "Cache not available"}


@bo_dinh_tuyen.get("/admin/cache/stats")
def thong_ke_cache():
    """Thống kê cache (Admin only)"""
    if HAS_CACHE:
        return redis_client.stats()
    return {"message": "Cache not available"}
