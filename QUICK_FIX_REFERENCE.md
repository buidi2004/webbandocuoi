# Quick Fix Reference Card

## 🚀 Deploy Now (Fastest)

```bash
git add .
git commit -m "fix: Configure CORS and production environment variables"
git push origin main
```

Wait 5-10 minutes. Done! ✅

## 🔍 Verify Deployment

1. **Backend**: https://ivie-be-final.onrender.com/api/health
   - Should return: `{"status": "healthy"}`

2. **Frontend**: https://ivie-fe-final.onrender.com
   - Open browser console
   - Should see NO CORS errors

3. **Admin**: https://ivie-ad-final.onrender.com
   - Should load dashboard

## 🧪 Test Before Deploy

Open `test-cors-locally.html` in browser and run all tests.

## 📋 What Was Fixed

| Issue | Fix |
|-------|-----|
| CORS errors | Added CORS_ORIGINS to backend |
| Frontend can't connect | Added VITE_API_BASE_URL |
| Admin can't connect | Added API_BASE_URL |
| Wrong build path | Fixed vercel.json paths |

## 🔧 Environment Variables

### Backend (ivie-be-final)
```
CORS_ORIGINS=https://ivie-fe-final.onrender.com,https://ve-wedding-frontend.vercel.app
```

### Frontend (ivie-fe-final)
```
VITE_API_BASE_URL=https://ivie-be-final.onrender.com
VITE_IMGBB_API_KEY=c525fc0204b449b541b0f0a5a4f5d9c4
```

### Admin (ivie-ad-final)
```
API_BASE_URL=https://ivie-be-final.onrender.com
```

## 🆘 Still Having Issues?

### CORS Errors?
1. Check backend logs in Render
2. Verify CORS_ORIGINS includes your domain
3. Hard refresh: Ctrl+Shift+R

### Can't Connect to Backend?
1. Check if backend is running
2. Visit health endpoint directly
3. Check backend logs

### 404 on Assets?
1. Check build logs
2. Verify dist folder exists
3. Trigger manual redeploy

## 📚 Full Documentation

- `FIXES_APPLIED.md` - What was fixed
- `FIX_CORS_AND_DEPLOYMENT.md` - Detailed guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step
- `test-cors-locally.html` - Testing tool

## 🎯 Success Criteria

✅ No CORS errors in console
✅ Frontend loads data from backend
✅ Images display correctly
✅ Admin panel works
✅ All pages navigate properly

---

**Need help?** Check the full documentation files listed above.
