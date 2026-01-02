"""
Utils Module - Helper functions for IVIE Wedding Admin
Contains pagination, formatting, and other utility functions
"""

from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple

import pandas as pd
import streamlit as st

# ============================================================
# PAGINATION HELPERS
# ============================================================


def paginate_list(items: List[Any], page_size: int = 20) -> Tuple[List[Any], int, int]:
    """
    Helper function for pagination - optimized

    Args:
        items: List of items to paginate
        page_size: Number of items per page

    Returns:
        Tuple of (paginated_items, current_page, total_pages)
    """
    if not items:
        return [], 1, 1

    # Sử dụng hash đơn giản hơn
    page_key = f"page_{id(items)}"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1

    total_pages = max(1, -(-len(items) // page_size))  # Ceiling division

    # Ensure current page is valid
    current = st.session_state[page_key]
    if current > total_pages:
        st.session_state[page_key] = total_pages
        current = total_pages

    start_idx = (current - 1) * page_size
    end_idx = start_idx + page_size

    return items[start_idx:end_idx], current, total_pages


def show_pagination(current_page: int, total_pages: int, key_prefix: str = "") -> None:
    """
    Display pagination controls - compact version

    Args:
        current_page: Current page number
        total_pages: Total number of pages
        key_prefix: Prefix for button keys to avoid conflicts
    """
    if total_pages <= 1:
        return

    # Sử dụng columns nhỏ gọn hơn
    c1, c2, c3, c4, c5 = st.columns([1, 1, 3, 1, 1])

    with c1:
        if st.button("⏮", disabled=current_page == 1, key=f"{key_prefix}first"):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = 1
            st.rerun()

    with c2:
        if st.button("◀", disabled=current_page == 1, key=f"{key_prefix}prev"):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = max(1, st.session_state[k] - 1)
            st.rerun()

    with c3:
        st.markdown(
            f"<p style='text-align:center;margin:8px 0;'>{current_page}/{total_pages}</p>",
            unsafe_allow_html=True,
        )

    with c4:
        if st.button(
            "▶", disabled=current_page == total_pages, key=f"{key_prefix}next"
        ):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = min(total_pages, st.session_state[k] + 1)
            st.rerun()

    with c5:
        if st.button(
            "⏭", disabled=current_page == total_pages, key=f"{key_prefix}last"
        ):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = total_pages
            st.rerun()


# ============================================================
# FORMATTING HELPERS
# ============================================================


def format_currency(amount: float) -> str:
    """
    Format number as Vietnamese currency

    Args:
        amount: Amount to format

    Returns:
        Formatted string (e.g., "1.000.000 đ")
    """
    try:
        return f"{int(amount):,}".replace(",", ".") + " đ"
    except (ValueError, TypeError):
        return "0 đ"


def format_date(date_str: str, format: str = "%d/%m/%Y") -> str:
    """
    Format date string to Vietnamese format

    Args:
        date_str: ISO date string
        format: Output format

    Returns:
        Formatted date string
    """
    try:
        if not date_str:
            return "N/A"
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime(format)
    except Exception:
        return date_str


def format_datetime(datetime_str: str) -> str:
    """
    Format datetime string to Vietnamese format

    Args:
        datetime_str: ISO datetime string

    Returns:
        Formatted datetime string (e.g., "01/01/2024 10:30")
    """
    return format_date(datetime_str, format="%d/%m/%Y %H:%M")


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to max length with ellipsis

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


# ============================================================
# STATUS HELPERS
# ============================================================


def get_status_badge(status: str) -> str:
    """
    Get HTML badge for status

    Args:
        status: Status string

    Returns:
        HTML string with colored badge
    """
    status_colors = {
        "Chờ xác nhận": "#ffc107",
        "Đã xác nhận": "#17a2b8",
        "Đang xử lý": "#007bff",
        "Hoàn thành": "#28a745",
        "Đã hủy": "#dc3545",
        "Chưa xử lý": "#6c757d",
        "Đã xử lý": "#28a745",
        "pending": "#ffc107",
        "approved": "#28a745",
        "rejected": "#dc3545",
    }

    color = status_colors.get(status, "#6c757d")

    return f"""
    <span style='
        background-color: {color};
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 500;
        display: inline-block;
    '>
        {status}
    </span>
    """


def get_priority_badge(priority: str) -> str:
    """
    Get HTML badge for priority

    Args:
        priority: Priority level (Cao, Trung bình, Thấp)

    Returns:
        HTML string with colored badge
    """
    priority_colors = {
        "Cao": "#dc3545",
        "Trung bình": "#ffc107",
        "Thấp": "#28a745",
    }

    color = priority_colors.get(priority, "#6c757d")

    return f"""
    <span style='
        background-color: {color};
        color: white;
        padding: 2px 8px;
        border-radius: 8px;
        font-size: 0.75em;
        font-weight: 500;
    '>
        {priority}
    </span>
    """


# ============================================================
# DATA HELPERS
# ============================================================


def filter_by_search(
    items: List[dict], search_term: str, fields: List[str]
) -> List[dict]:
    """
    Filter list of dictionaries by search term in specified fields

    Args:
        items: List of dictionaries to filter
        search_term: Search term
        fields: List of fields to search in

    Returns:
        Filtered list
    """
    if not search_term or not items:
        return items

    search_lower = search_term.lower()
    filtered = []

    for item in items:
        for field in fields:
            value = item.get(field, "")
            if value and search_lower in str(value).lower():
                filtered.append(item)
                break

    return filtered


def filter_by_status(
    items: List[dict], status_filter: str, status_field: str = "trang_thai"
) -> List[dict]:
    """
    Filter list by status

    Args:
        items: List of dictionaries to filter
        status_filter: Status to filter by ("Tất cả" for no filter)
        status_field: Field name containing status

    Returns:
        Filtered list
    """
    if not items or status_filter == "Tất cả":
        return items

    return [item for item in items if item.get(status_field) == status_filter]


def filter_by_date_range(
    items: List[dict],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    date_field: str = "ngay_tao",
) -> List[dict]:
    """
    Filter list by date range

    Args:
        items: List of dictionaries to filter
        start_date: Start date
        end_date: End date
        date_field: Field name containing date

    Returns:
        Filtered list
    """
    if not items:
        return items

    filtered = []
    for item in items:
        try:
            item_date_str = item.get(date_field)
            if not item_date_str:
                continue

            item_date = datetime.fromisoformat(item_date_str.replace("Z", "+00:00"))

            if start_date and item_date < start_date:
                continue
            if end_date and item_date > end_date:
                continue

            filtered.append(item)
        except Exception:
            continue

    return filtered


def sort_items(items: List[dict], sort_by: str, reverse: bool = False) -> List[dict]:
    """
    Sort list of dictionaries by field

    Args:
        items: List to sort
        sort_by: Field name to sort by
        reverse: Sort in descending order if True

    Returns:
        Sorted list
    """
    if not items:
        return items

    try:
        return sorted(items, key=lambda x: x.get(sort_by, ""), reverse=reverse)
    except Exception:
        return items


# ============================================================
# DATAFRAME HELPERS
# ============================================================


def list_to_dataframe(
    items: List[dict], columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Convert list of dictionaries to pandas DataFrame

    Args:
        items: List of dictionaries
        columns: Optional list of columns to include

    Returns:
        pandas DataFrame
    """
    if not items:
        return pd.DataFrame()

    df = pd.DataFrame(items)

    if columns:
        # Only include specified columns that exist
        available_cols = [col for col in columns if col in df.columns]
        df = df[available_cols]

    return df


def dataframe_to_excel(df: pd.DataFrame) -> bytes:
    """
    Convert DataFrame to Excel bytes

    Args:
        df: pandas DataFrame

    Returns:
        Excel file as bytes
    """
    import io

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return output.getvalue()


# ============================================================
# VALIDATION HELPERS
# ============================================================


def is_valid_email(email: str) -> bool:
    """
    Validate email format

    Args:
        email: Email string to validate

    Returns:
        True if valid, False otherwise
    """
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """
    Validate Vietnamese phone number

    Args:
        phone: Phone string to validate

    Returns:
        True if valid, False otherwise
    """
    import re

    # Vietnamese phone: 10 digits, starts with 0
    pattern = r"^0\d{9}$"
    cleaned = "".join(filter(str.isdigit, phone))
    return bool(re.match(pattern, cleaned))


def is_valid_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL string to validate

    Returns:
        True if valid, False otherwise
    """
    import re

    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, url))


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "paginate_list",
    "show_pagination",
    "format_currency",
    "format_date",
    "format_datetime",
    "truncate_text",
    "get_status_badge",
    "get_priority_badge",
    "filter_by_search",
    "filter_by_status",
    "filter_by_date_range",
    "sort_items",
    "list_to_dataframe",
    "dataframe_to_excel",
    "is_valid_email",
    "is_valid_phone",
    "is_valid_url",
]
