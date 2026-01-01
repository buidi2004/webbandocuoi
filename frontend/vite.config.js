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
        // Tối ưu tên file cho caching
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]',
      },
    },
    // Tối ưu chunk size
    chunkSizeWarningLimit: 500,
    // Minify CSS
    cssMinify: true,
    // CSS code splitting
    cssCodeSplit: true,
    // Minify JS với esbuild (mặc định, nhanh hơn terser)
    minify: 'esbuild',
    // Source maps cho production (optional)
    sourcemap: false,
    // Target modern browsers
    target: 'es2020',
  },
  // Tối ưu dependencies
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom', 'axios'],
  },
  // Esbuild options để drop console
  esbuild: {
    drop: ['console', 'debugger'],
  },
})
