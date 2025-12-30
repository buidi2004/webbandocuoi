# Hướng Dẫn Cấu Hình Firebase Authentication

## Bước 1: Tạo Project Firebase

1. Truy cập [Firebase Console](https://console.firebase.google.com)
2. Click "Add project" (Thêm dự án)
3. Đặt tên project: `ivie-wedding-studio`
4. Bỏ chọn Google Analytics (không cần thiết)
5. Click "Create project"

## Bước 2: Bật Authentication

1. Trong Firebase Console, chọn project vừa tạo
2. Click "Authentication" ở menu bên trái
3. Click "Get started"
4. Chọn tab "Sign-in method"

### Bật Google Sign-in:
1. Click vào "Google"
2. Toggle "Enable" sang ON
3. Chọn "Project support email" (email của bạn)
4. Click "Save"

### Bật Facebook Sign-in:
1. Click vào "Facebook"
2. Toggle "Enable" sang ON
3. Bạn cần tạo Facebook App:
   - Truy cập [Facebook Developers](https://developers.facebook.com)
   - Tạo App mới
   - Lấy App ID và App Secret
4. Điền App ID và App Secret vào Firebase
5. Copy "OAuth redirect URI" từ Firebase
6. Paste vào Facebook App > Facebook Login > Settings > Valid OAuth Redirect URIs
7. Click "Save"

## Bước 3: Thêm Domain vào Authorized Domains

1. Trong Authentication > Settings > Authorized domains
2. Thêm các domain:
   - `localhost` (đã có sẵn)
   - `ivie-frontend.onrender.com` (domain production)

## Bước 4: Lấy Firebase Config

1. Click vào biểu tượng ⚙️ (Settings) > Project settings
2. Scroll xuống "Your apps"
3. Click vào biểu tượng `</>` (Web)
4. Đặt tên app: `ivie-web`
5. Click "Register app"
6. Copy đoạn config:

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

## Bước 5: Cấu Hình Environment Variables

### Local Development:
Tạo file `frontend/.env.local`:
```env
VITE_FIREBASE_API_KEY=AIza...
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abc123
```

### Production (Render):
1. Vào Render Dashboard > ivie-frontend > Environment
2. Thêm các biến môi trường:
   - `VITE_FIREBASE_API_KEY`
   - `VITE_FIREBASE_AUTH_DOMAIN`
   - `VITE_FIREBASE_PROJECT_ID`
   - `VITE_FIREBASE_STORAGE_BUCKET`
   - `VITE_FIREBASE_MESSAGING_SENDER_ID`
   - `VITE_FIREBASE_APP_ID`

## Bước 6: Test

1. Chạy frontend local: `npm run dev`
2. Truy cập trang đăng nhập
3. Click "Đăng nhập với Google" hoặc "Đăng nhập với Facebook"
4. Hoàn tất đăng nhập

## Lưu Ý

- Firebase Authentication miễn phí cho 10,000 xác thực/tháng
- Không cần backend riêng cho authentication
- Token được tạo bởi backend IVIE, không phải Firebase
- User được lưu trong database PostgreSQL của IVIE

## Troubleshooting

### Lỗi "auth/configuration-not-found"
- Kiểm tra lại Firebase config
- Đảm bảo đã bật Google/Facebook trong Sign-in method

### Lỗi "auth/popup-closed-by-user"
- User đã đóng popup đăng nhập
- Không phải lỗi, chỉ là user hủy

### Lỗi "auth/unauthorized-domain"
- Thêm domain vào Authorized domains trong Firebase Console

### Facebook Login không hoạt động
- Kiểm tra App ID và App Secret
- Đảm bảo đã thêm OAuth redirect URI vào Facebook App
- Facebook App phải ở chế độ "Live" (không phải Development)
