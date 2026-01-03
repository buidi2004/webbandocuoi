# 📚 Index Tài Liệu - IVIE Wedding Studio

## 🚀 Chạy Local

### Quick Start
| File | Mục Đích | Khi Nào Dùng |
|------|----------|--------------|
| `BAT_DAU_NGAY.md` | Hướng dẫn bắt đầu ngày | Mỗi sáng trước khi code |
| `README_LOCAL.md` | Tổng quan chạy local | Lần đầu setup |
| `HUONG_DAN_CHAY_LOCAL.md` | Chi tiết đầy đủ | Khi gặp vấn đề |

### Scripts
| File | Chức Năng | Lệnh |
|------|-----------|------|
| `KIEM_TRA_LOCAL.bat` | Kiểm tra hệ thống | `KIEM_TRA_LOCAL.bat` |
| `CHAY_LOCAL.bat` | Khởi động tất cả | `CHAY_LOCAL.bat` |
| `DUNG_LOCAL.bat` | Dừng tất cả | `DUNG_LOCAL.bat` |

### Test
| File | Mục Đích |
|------|----------|
| `test-cors-locally.html` | Test kết nối API |
| `test-connection.html` | Test connection cũ |

## 🔧 Fixes & Troubleshooting

### Fixes Đã Áp Dụng
| File | Nội Dung |
|------|----------|
| `FIXES_APPLIED.md` | Tổng hợp tất cả fixes |
| `FIX_CORS_AND_DEPLOYMENT.md` | Fix CORS chi tiết |
| `QUICK_FIX_REFERENCE.md` | Tham khảo nhanh |

### Troubleshooting
| File | Giải Quyết |
|------|-----------|
| `FIX_FRONTEND_BACKEND_CONNECTION.md` | Lỗi kết nối FE-BE |
| `QUICK_FIX_BACKEND.md` | Lỗi backend nhanh |

## 🚢 Deployment

### Render
| File | Mục Đích |
|------|----------|
| `DEPLOYMENT_CHECKLIST.md` | Checklist deploy đầy đủ |
| `DEPLOY_RENDER.md` | Hướng dẫn deploy Render |
| `DEPLOY_RENDER_MANUAL.md` | Deploy thủ công |
| `DEPLOY_ADMIN_RENDER.md` | Deploy admin panel |
| `render.yaml` | Config Render |

### Vercel
| File | Mục Đích |
|------|----------|
| `DEPLOY_VERCEL.md` | Hướng dẫn deploy Vercel |
| `vercel.json` | Config Vercel |

### Alternatives
| File | Nội Dung |
|------|----------|
| `RENDER_FREE_ALTERNATIVES.md` | Các nền tảng thay thế |

## 📁 Cấu Hình

### Environment Files
| File | Service | Môi Trường |
|------|---------|------------|
| `backend/.env` | Backend | Local |
| `backend/.env.example` | Backend | Template |
| `frontend/.env` | Frontend | Local |
| `frontend/.env.production` | Frontend | Production |
| `admin-python/.env` | Admin | Local |
| `admin-python/.env.example` | Admin | Template |

### Config Files
| File | Mục Đích |
|------|----------|
| `render.yaml` | Render deployment |
| `vercel.json` | Vercel deployment |
| `docker-compose.yml` | Docker setup |

## 🎯 Workflow

### Development
```
BAT_DAU_NGAY.md
    ↓
KIEM_TRA_LOCAL.bat
    ↓
CHAY_LOCAL.bat
    ↓
Code & Test
    ↓
DUNG_LOCAL.bat
```

### Deployment
```
DEPLOYMENT_CHECKLIST.md
    ↓
git push origin main
    ↓
Render auto-deploy
    ↓
Verify production
```

### Troubleshooting
```
Gặp lỗi
    ↓
HUONG_DAN_CHAY_LOCAL.md (Section: Xử Lý Lỗi)
    ↓
Nếu vẫn lỗi → FIXES_APPLIED.md
    ↓
Nếu vẫn lỗi → FIX_CORS_AND_DEPLOYMENT.md
```

## 🔍 Tìm Nhanh

### "Làm sao chạy local?"
→ `BAT_DAU_NGAY.md` hoặc `README_LOCAL.md`

### "Gặp lỗi CORS"
→ `FIX_CORS_AND_DEPLOYMENT.md`

### "Làm sao deploy?"
→ `DEPLOYMENT_CHECKLIST.md`

### "Port đã được sử dụng"
→ `DUNG_LOCAL.bat`

### "Module not found"
→ `HUONG_DAN_CHAY_LOCAL.md` (Section: Xử Lý Lỗi)

### "Database không tồn tại"
→ `HUONG_DAN_CHAY_LOCAL.md` (Section: Xử Lý Lỗi)

### "Frontend không kết nối Backend"
→ `FIX_FRONTEND_BACKEND_CONNECTION.md`

### "Cần deploy lên Render"
→ `DEPLOY_RENDER.md`

### "Cần deploy lên Vercel"
→ `DEPLOY_VERCEL.md`

## 📊 Specs (Kiro)

### Git & Render Deployment
| File | Nội Dung |
|------|----------|
| `.kiro/specs/git-render-deployment/requirements.md` | Requirements |
| `.kiro/specs/git-render-deployment/design.md` | Design |
| `.kiro/specs/git-render-deployment/tasks.md` | Tasks |

## 🎨 Frontend

### Docs
| File | Nội Dung |
|------|----------|
| `frontend/huong_dan.md` | Hướng dẫn frontend |

## 🔧 Backend

### Scripts
| File | Mục Đích |
|------|----------|
| `backend/tao_du_lieu_mau.py` | Tạo dữ liệu mẫu |
| `backend/migrate_combo.py` | Migration combo |

## 👨‍💼 Admin

### Docs
| File | Nội Dung |
|------|----------|
| `admin-python/README.md` | Tổng quan admin |
| `admin-python/QUICK_START.md` | Quick start |
| `admin-python/OPTIMIZATION_GUIDE.md` | Tối ưu hóa |
| `admin-python/DEPLOYMENT_CHECKLIST.md` | Deploy checklist |

## 🆘 Cần Trợ Giúp?

### Bước 1: Xác định vấn đề
- Lỗi khi chạy local? → `HUONG_DAN_CHAY_LOCAL.md`
- Lỗi CORS? → `FIX_CORS_AND_DEPLOYMENT.md`
- Lỗi deploy? → `DEPLOYMENT_CHECKLIST.md`

### Bước 2: Tìm giải pháp
- Dùng Ctrl+F trong file tài liệu
- Hoặc xem section "Xử Lý Lỗi"

### Bước 3: Vẫn không được?
- Kiểm tra logs trong terminal
- Chạy `test-cors-locally.html`
- Reset lại: `DUNG_LOCAL.bat` → `CHAY_LOCAL.bat`

---

## 📌 Files Quan Trọng Nhất

### Top 5 - Phải Đọc
1. `BAT_DAU_NGAY.md` - Bắt đầu mỗi ngày
2. `README_LOCAL.md` - Tổng quan local
3. `DEPLOYMENT_CHECKLIST.md` - Deploy production
4. `FIXES_APPLIED.md` - Các fix đã áp dụng
5. `HUONG_DAN_CHAY_LOCAL.md` - Chi tiết đầy đủ

### Top 3 - Scripts
1. `CHAY_LOCAL.bat` - Chạy tất cả
2. `DUNG_LOCAL.bat` - Dừng tất cả
3. `KIEM_TRA_LOCAL.bat` - Kiểm tra hệ thống

---

**Cập nhật:** 2026-01-03
**Version:** 1.0
