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

// Firebase configuration - THAY THẾ BẰNG CONFIG CỦA BẠN
const firebaseConfig = {
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "YOUR_API_KEY",
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "YOUR_PROJECT.firebaseapp.com",
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "YOUR_PROJECT_ID",
    storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "YOUR_PROJECT.appspot.com",
    messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "YOUR_SENDER_ID",
    appId: import.meta.env.VITE_FIREBASE_APP_ID || "YOUR_APP_ID"
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
