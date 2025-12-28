# Sử dụng Python 3.12 Slim để tối ưu dung lượng và tương thích Pydantic v2
FROM python:3.12-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn backend
COPY . .

# Mở port 8000
EXPOSE 8000

# Lệnh chạy ứng dụng
CMD ["uvicorn", "ung_dung.chinh:ung_dung", "--host", "0.0.0.0", "--port", "8000"]
