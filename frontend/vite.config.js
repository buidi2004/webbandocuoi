import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Code splitting - tách chunks nhỏ hơn
    rollupOptions: {
      output: {
        manualChunks: {
          // Tách vendor libraries
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-animation': ['framer-motion', 'gsap'],
          'vendor-3d': ['three', '@react-three/fiber', '@react-three/drei'],
          'vendor-utils': ['axios', 'atropos'],
        },
      },
    },
    // Tối ưu chunk size
    chunkSizeWarningLimit: 500,
    // Minify CSS
    cssMinify: true,
    // Minify JS với terser
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Xóa console.log trong production
        drop_debugger: true,
      },
    },
    // Source maps cho production (optional)
    sourcemap: false,
  },
  // Tối ưu dependencies
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom', 'axios'],
  },
})
