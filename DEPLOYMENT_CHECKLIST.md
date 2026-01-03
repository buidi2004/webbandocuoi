# Deployment Checklist - IVIE Wedding Studio

## Pre-Deployment

- [x] Fix CORS configuration in backend
- [x] Add production environment variables to render.yaml
- [x] Create .env.production for frontend
- [x] Update vercel.json for proper frontend deployment
- [ ] Test locally before deploying

## Deployment Steps

### 1. Commit Changes
```bash
git add .
git commit -m "fix: Configure CORS and production environment variables"
git push origin main
```

### 2. Deploy Backend (Render)
- Render will auto-deploy from render.yaml
- Or manually trigger deploy in Render Dashboard
- Wait for backend to be live (~5-10 minutes)
- Verify: https://ivie-be-final.onrender.com/api/health

### 3. Deploy Frontend

#### Option A: Render (Static Site)
- Render will auto-deploy from render.yaml
- Wait for build to complete (~3-5 minutes)
- Verify: https://ivie-fe-final.onrender.com

#### Option B: Vercel
```bash
cd frontend
vercel --prod
```
- Or push to GitHub and let Vercel auto-deploy
- Add environment variables in Vercel Dashboard:
  - `VITE_API_BASE_URL` = `https://ivie-be-final.onrender.com`
  - `VITE_IMGBB_API_KEY` = `c525fc0204b449b541b0f0a5a4f5d9c4`

### 4. Deploy Admin Panel (Render)
- Render will auto-deploy from render.yaml
- Wait for deployment (~5-10 minutes)
- Verify: https://ivie-ad-final.onrender.com

## Post-Deployment Verification

### Backend Health Check
- [ ] Visit https://ivie-be-final.onrender.com/api/health
- [ ] Should return: `{"status": "healthy"}`
- [ ] Check API docs: https://ivie-be-final.onrender.com/docs

### Frontend Verification
- [ ] Open frontend URL in browser
- [ ] Open browser DevTools → Console
- [ ] Should see NO CORS errors
- [ ] Should see NO 404 errors on assets
- [ ] Test navigation between pages
- [ ] Test API calls (products, services, etc.)

### Admin Panel Verification
- [ ] Open admin URL in browser
- [ ] Login with credentials
- [ ] Verify dashboard loads
- [ ] Test CRUD operations

## Common Issues & Solutions

### Issue: CORS Errors Still Appearing
**Solution**:
1. Check backend logs in Render Dashboard
2. Verify CORS_ORIGINS includes your frontend domain
3. Hard refresh browser (Ctrl+Shift+R)
4. Clear browser cache

### Issue: Frontend Shows "Cannot connect to backend"
**Solution**:
1. Check if backend is running (Render Dashboard)
2. Verify VITE_API_BASE_URL is correct
3. Check backend logs for errors
4. Test backend health endpoint directly

### Issue: 404 on CSS/JS Files
**Solution**:
1. Check build logs in Render/Vercel
2. Verify dist folder was created
3. Check vite.config.js base path
4. Trigger manual redeploy

### Issue: Admin Panel Not Loading
**Solution**:
1. Check admin service logs in Render
2. Verify API_BASE_URL is set correctly
3. Check if backend is accessible from admin service
4. Restart admin service

## Environment Variables Summary

### Backend (ivie-be-final)
```
DATABASE_URL=<from-render-database>
PORT=8000
PYTHON_VERSION=3.12.0
CORS_ORIGINS=https://ivie-fe-final.onrender.com,https://ve-wedding-frontend.vercel.app
```

### Frontend (ivie-fe-final or Vercel)
```
VITE_API_BASE_URL=https://ivie-be-final.onrender.com
VITE_IMGBB_API_KEY=c525fc0204b449b541b0f0a5a4f5d9c4
```

### Admin (ivie-ad-final)
```
PORT=8501
PYTHON_VERSION=3.11.0
STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=3
API_BASE_URL=https://ivie-be-final.onrender.com
```

## Monitoring

### Check Service Status
- Render Dashboard: https://dashboard.render.com
- View logs for each service
- Monitor resource usage (free tier limits)

### Performance Monitoring
- Check page load times
- Monitor API response times
- Watch for memory/CPU issues on free tier

## Rollback Plan

If deployment fails:
1. Revert git commit: `git revert HEAD`
2. Push to trigger redeploy: `git push origin main`
3. Or manually rollback in Render Dashboard

## Notes

- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Database has 90-day retention on free tier
- Consider upgrading to paid tier for production use
