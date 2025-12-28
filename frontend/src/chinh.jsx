import React from 'react'
import ReactDOM from 'react-dom/client'
import UngDung from './UngDung.jsx'
import './index.css'
import { ToastProvider } from './thanh_phan/Toast'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ToastProvider>
      <UngDung />
    </ToastProvider>
  </React.StrictMode>,
)
