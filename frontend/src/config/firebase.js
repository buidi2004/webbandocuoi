/**
 * Firebase Configuration - IVIE Wedding Studio
 * 
 * Để sử dụng đăng nhập Google/Facebook, bạn cần:
 * 1. Tạo project Firebase tại https://console.firebase.google.com
 * 2. Bật Authentication > Sign-in method > Google và Facebook
 * 3. Thay thế các giá trị config bên dưới bằng config từ Firebase Console
 * 4. Thêm domain vào Authorized domains (localhost và domain production)
 */

import { initializeApp } from 'firebase/app';
import { 
    getAuth, 
    GoogleAuthProvider, 
    FacebookAuthProvider,
    signInWithPopup,
    signOut
} from 'firebase/auth';

// Firebase configuration - IVIE Wedding
const firebaseConfig = {
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyCdC0NvFetnr_f4LmGbe-lwcKbhHM4c0o8",
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "ivie-wedding.firebaseapp.com",
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "ivie-wedding",
    storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "ivie-wedding.firebasestorage.app",
    messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "409138503650",
    appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:409138503650:web:5a03dbb4c7ba025e2523bb"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Providers
const googleProvider = new GoogleAuthProvider();
const facebookProvider = new FacebookAuthProvider();

// Thêm scope để lấy thêm thông tin
googleProvider.addScope('email');
googleProvider.addScope('profile');

facebookProvider.addScope('email');
facebookProvider.addScope('public_profile');

// Export functions
export { auth, googleProvider, facebookProvider, signInWithPopup, signOut };
