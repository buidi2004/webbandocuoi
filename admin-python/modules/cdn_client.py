"""
CDN Client Module - IVIE Wedding Admin
Cloudinary integration for ultra-fast image delivery

Features:
- Auto WebP/AVIF conversion
- Responsive images
- Global CDN delivery
- Image optimization
- Lazy loading support

Setup:
1. Sign up at https://cloudinary.com (Free: 25GB)
2. Set environment variables:
   - CLOUDINARY_CLOUD_NAME
   - CLOUDINARY_API_KEY
   - CLOUDINARY_API_SECRET
   - CDN_ENABLED=true

Usage:
    from modules.cdn_client import upload_to_cdn, get_cdn_url

    # Upload image
    url = upload_to_cdn(uploaded_file, folder="products")

    # Get optimized URL
    optimized_url = get_cdn_url(url, width=400, quality="auto")
"""

import io
import os
from typing import Dict, List, Optional, Tuple

from PIL import Image

# Cloudinary import with fallback
try:
    import cloudinary
    import cloudinary.uploader
    from cloudinary import CloudinaryImage

    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    print("⚠️  Cloudinary not installed. Run: pip install cloudinary")

# Configuration
CDN_ENABLED = os.getenv("CDN_ENABLED", "false").lower() == "true"
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

# Initialize Cloudinary
if CLOUDINARY_AVAILABLE and CDN_ENABLED:
    try:
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True,
        )
        print("✅ Cloudinary CDN initialized")
    except Exception as e:
        print(f"⚠️  Cloudinary config error: {e}")
        CDN_ENABLED = False


def is_cdn_available() -> bool:
    """
    Check if CDN is available and configured

    Returns:
        True if CDN is ready to use
    """
    return (
        CLOUDINARY_AVAILABLE
        and CDN_ENABLED
        and CLOUDINARY_CLOUD_NAME
        and CLOUDINARY_API_KEY
        and CLOUDINARY_API_SECRET
    )


def upload_to_cdn(
    file,
    folder: str = "uploads",
    public_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    width: int = 1000,
    quality: str = "auto",
) -> Optional[str]:
    """
    Upload image to Cloudinary CDN with optimization

    Args:
        file: File-like object or path
        folder: Cloudinary folder name
        public_id: Custom public ID (optional)
        tags: List of tags for organization
        width: Max width (default: 1000px)
        quality: Quality setting ("auto", 80-100, "auto:best")

    Returns:
        CDN URL if successful, None otherwise

    Example:
        url = upload_to_cdn(
            uploaded_file,
            folder="products",
            tags=["wedding", "dress"],
            width=1200
        )
    """
    if not is_cdn_available():
        return None

    try:
        # Prepare upload options
        upload_options = {
            "folder": folder,
            "transformation": [
                {"width": width, "crop": "limit"},  # Max width
                {"quality": quality},  # Auto quality
                {"fetch_format": "auto"},  # Auto format (WebP for supported browsers)
            ],
            "resource_type": "auto",
            "overwrite": False,
        }

        if public_id:
            upload_options["public_id"] = public_id

        if tags:
            upload_options["tags"] = tags

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(file, **upload_options)

        # Return secure URL
        return result.get("secure_url")

    except Exception as e:
        print(f"❌ Cloudinary upload error: {e}")
        return None


def upload_multiple_to_cdn(
    files: List,
    folder: str = "uploads",
    tags: Optional[List[str]] = None,
    width: int = 1000,
) -> List[str]:
    """
    Upload multiple images to CDN

    Args:
        files: List of file-like objects
        folder: Cloudinary folder
        tags: List of tags
        width: Max width

    Returns:
        List of CDN URLs

    Example:
        urls = upload_multiple_to_cdn(
            [file1, file2, file3],
            folder="gallery",
            tags=["wedding"]
        )
    """
    urls = []
    for file in files:
        url = upload_to_cdn(file, folder=folder, tags=tags, width=width)
        if url:
            urls.append(url)
    return urls


def get_cdn_url(
    public_id_or_url: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: str = "fill",
    quality: str = "auto",
    format: str = "auto",
    dpr: str = "auto",
) -> str:
    """
    Get optimized CDN URL with transformations

    Args:
        public_id_or_url: Cloudinary public ID or existing URL
        width: Target width in pixels
        height: Target height in pixels
        crop: Crop mode ("fill", "fit", "limit", "scale", "thumb")
        quality: Quality ("auto", "auto:best", "auto:good", 50-100)
        format: Format ("auto", "webp", "avif", "jpg", "png")
        dpr: Device pixel ratio ("auto", "1.0", "2.0", "3.0")

    Returns:
        Optimized CDN URL

    Example:
        # Responsive thumbnail
        thumb_url = get_cdn_url(
            "products/dress123",
            width=400,
            height=400,
            crop="fill",
            quality="auto"
        )
    """
    if not is_cdn_available():
        return public_id_or_url

    try:
        # Extract public_id from URL if needed
        if public_id_or_url.startswith("http"):
            # Extract public_id from Cloudinary URL
            parts = public_id_or_url.split("/upload/")
            if len(parts) == 2:
                # Get everything after /upload/ and before file extension
                public_id = parts[1].split(".")[0]
            else:
                return public_id_or_url
        else:
            public_id = public_id_or_url

        # Build transformation options
        transformation = {"fetch_format": format}

        if width:
            transformation["width"] = width
        if height:
            transformation["height"] = height
        if crop:
            transformation["crop"] = crop
        if quality:
            transformation["quality"] = quality
        if dpr:
            transformation["dpr"] = dpr

        # Generate URL
        url = CloudinaryImage(public_id).build_url(**transformation)

        return url

    except Exception as e:
        print(f"❌ CDN URL generation error: {e}")
        return public_id_or_url


def get_responsive_urls(
    public_id: str, sizes: List[int] = [320, 640, 1024, 1920]
) -> Dict[int, str]:
    """
    Generate responsive image URLs for different screen sizes

    Args:
        public_id: Cloudinary public ID
        sizes: List of widths to generate

    Returns:
        Dictionary mapping width to URL

    Example:
        urls = get_responsive_urls("products/dress123")
        # {320: "url1", 640: "url2", 1024: "url3", 1920: "url4"}
    """
    if not is_cdn_available():
        return {}

    responsive_urls = {}
    for size in sizes:
        url = get_cdn_url(public_id, width=size, quality="auto")
        responsive_urls[size] = url

    return responsive_urls


def get_responsive_srcset(public_id: str, sizes: List[int] = [320, 640, 1024]) -> str:
    """
    Generate srcset attribute for responsive images

    Args:
        public_id: Cloudinary public ID
        sizes: List of widths

    Returns:
        srcset string for HTML

    Example:
        srcset = get_responsive_srcset("products/dress123")
        # "url1 320w, url2 640w, url3 1024w"
    """
    if not is_cdn_available():
        return ""

    urls = get_responsive_urls(public_id, sizes)
    srcset_parts = [f"{url} {width}w" for width, url in urls.items()]
    return ", ".join(srcset_parts)


def get_lazy_image_html(
    public_id_or_url: str,
    width: int = 400,
    height: int = 300,
    alt: str = "Image",
    css_class: str = "",
    lazy: bool = True,
) -> str:
    """
    Generate HTML for lazy-loaded image with blur placeholder

    Args:
        public_id_or_url: Cloudinary public ID or URL
        width: Image width
        height: Image height
        alt: Alt text
        css_class: CSS class name
        lazy: Enable lazy loading

    Returns:
        HTML string with lazy loading

    Example:
        html = get_lazy_image_html(
            "products/dress123",
            width=400,
            height=400,
            alt="Wedding Dress"
        )
    """
    # Get optimized URLs
    main_url = get_cdn_url(public_id_or_url, width=width, height=height)
    placeholder_url = get_cdn_url(
        public_id_or_url, width=20, height=20, quality="auto:low"
    )

    loading = 'loading="lazy"' if lazy else ""

    html = f"""
    <img
        src="{placeholder_url}"
        data-src="{main_url}"
        alt="{alt}"
        width="{width}"
        height="{height}"
        class="lazy-image {css_class}"
        {loading}
        style="filter: blur(5px); transition: filter 0.3s;"
        onload="this.style.filter='none'; this.src=this.dataset.src;"
    />
    """

    return html.strip()


def get_picture_html(
    public_id_or_url: str,
    width: int = 800,
    height: int = 600,
    alt: str = "Image",
    formats: List[str] = ["avif", "webp", "jpg"],
) -> str:
    """
    Generate <picture> element with multiple format sources

    Args:
        public_id_or_url: Cloudinary public ID or URL
        width: Image width
        height: Image height
        alt: Alt text
        formats: List of formats to include

    Returns:
        HTML <picture> element

    Example:
        html = get_picture_html(
            "products/dress123",
            width=800,
            formats=["avif", "webp", "jpg"]
        )
    """
    sources = []

    for fmt in formats[:-1]:  # All except last (fallback)
        url = get_cdn_url(
            public_id_or_url, width=width, height=height, format=fmt, quality="auto"
        )
        mime_type = f"image/{fmt}"
        sources.append(f'<source srcset="{url}" type="{mime_type}">')

    # Fallback image (last format)
    fallback_fmt = formats[-1]
    fallback_url = get_cdn_url(
        public_id_or_url, width=width, height=height, format=fallback_fmt
    )

    html = f"""
    <picture>
        {chr(10).join(sources)}
        <img src="{fallback_url}" alt="{alt}" width="{width}" height="{height}" loading="lazy">
    </picture>
    """

    return html.strip()


def delete_from_cdn(public_id: str) -> bool:
    """
    Delete image from CDN

    Args:
        public_id: Cloudinary public ID

    Returns:
        True if deleted successfully

    Example:
        deleted = delete_from_cdn("products/dress123")
    """
    if not is_cdn_available():
        return False

    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get("result") == "ok"
    except Exception as e:
        print(f"❌ CDN delete error: {e}")
        return False


def get_cdn_stats() -> Dict:
    """
    Get CDN usage statistics

    Returns:
        Dictionary with CDN stats

    Example:
        stats = get_cdn_stats()
        print(f"Available: {stats['available']}")
    """
    if not is_cdn_available():
        return {
            "available": False,
            "reason": "CDN not configured or not available",
        }

    try:
        # Get account usage info
        usage = cloudinary.api.usage()

        return {
            "available": True,
            "plan": usage.get("plan", "unknown"),
            "credits_used": usage.get("credits", {}).get("used", 0),
            "credits_limit": usage.get("credits", {}).get("limit", 0),
            "bandwidth_used": usage.get("bandwidth", {}).get("used", 0),
            "bandwidth_limit": usage.get("bandwidth", {}).get("limit", 0),
            "storage_used": usage.get("storage", {}).get("used", 0),
            "storage_limit": usage.get("storage", {}).get("limit", 0),
            "transformations": usage.get("transformations", {}).get("used", 0),
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


def optimize_local_image(
    file, max_width: int = 1000, quality: int = 85, format: str = "JPEG"
) -> io.BytesIO:
    """
    Optimize image locally (fallback when CDN not available)

    Args:
        file: File-like object
        max_width: Maximum width
        quality: Quality (1-100)
        format: Output format

    Returns:
        Optimized image as BytesIO

    Example:
        optimized = optimize_local_image(uploaded_file, max_width=800)
    """
    img = Image.open(file)

    # Resize if needed
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

    # Convert mode if needed
    if format == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Save to buffer
    buffer = io.BytesIO()
    img.save(buffer, format=format, quality=quality, optimize=True)
    buffer.seek(0)

    return buffer


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    # Core functions
    "is_cdn_available",
    "upload_to_cdn",
    "upload_multiple_to_cdn",
    "delete_from_cdn",
    # URL generation
    "get_cdn_url",
    "get_responsive_urls",
    "get_responsive_srcset",
    # HTML helpers
    "get_lazy_image_html",
    "get_picture_html",
    # Stats
    "get_cdn_stats",
    # Fallback
    "optimize_local_image",
    # Config
    "CDN_ENABLED",
    "CLOUDINARY_AVAILABLE",
]
