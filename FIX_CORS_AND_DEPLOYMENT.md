# Fix CORS and Deployment Issues

## Issues Fixed

### 1. CORS Policy Errors
**Problem**: Backend was not configured to accept requests from frontend domain
**Solution**: Added `CORS_ORIGINS` environment variable to backend in `render.yaml`

### 2. Frontend API Connection
**Problem**: Frontend `.env` was pointing to `localhost:8000` instead of production backend
**Solution**: 
- Created `.env.production` with production backend URL
- Added environment variables to frontend service in `render.yaml`

### 3. Admin Panel API Connection
**Problem**: Admin panel had no API_BASE_URL configured
**Solution**: Added `API_BASE_URL` environment variable to admin service in `render.yaml`

## Changes Made

### 1. `render.yaml`
- Added `CORS_ORIGINS` to backend service (allows frontend domains)
- Added `VITE_API_BASE_URL` and `VITE_IMGBB_API_KEY` to frontend service
- Added `API_BASE_URL` to admin service

### 2. `frontend/.env.production`
- Created new file with production environment variables
- Points to production backend URL

## Deployment Steps

### Option 1: Deploy via Render Dashboard (Recommended)

1. **Commit and push changes**:
   ```bash
   git add .
   git commit -m "fix: Configure CORS and production environment variables"
   git push origin main
   ```

2. **Render will auto-deploy** all services based on `render.yaml`

3. **Verify deployment**:
   - Backend: https://ivie-be-final.onrender.com/docs
   - Frontend: https://ivie-fe-final.onrender.com
   - Admin: https://ivie-ad-final.onrender.com

### Option 2: Manual Environment Variable Update

If you don't want to redeploy everything, update environment variables manually:

#### Backend Service (ivie-be-final)
1. Go to Render Dashboard → ivie-be-final
2. Click "Environment" tab
3. Add new environment variable:
   - Key: `CORS_ORIGINS`
   - Value: `https://ivie-fe-final.onrender.com,https://ve-wedding-frontend.vercel.app`
4. Click "Save Changes" (will trigger redeploy)

#### Frontend Service (ivie-fe-final)
1. Go to Render Dashboard → ivie-fe-final
2. Click "Environment" tab
3. Add environment variables:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://ivie-be-final.onrender.com`
   - Key: `VITE_IMGBB_API_KEY`
   - Value: `c525fc0204b449b541b0f0a5a4f5d9c4`
4. Click "Save Changes" and trigger manual deploy

#### Admin Service (ivie-ad-final)
1. Go to Render Dashboard → ivie-ad-final
2. Click "Environment" tab
3. Add environment variable:
   - Key: `API_BASE_URL`
   - Value: `https://ivie-be-final.onrender.com`
4. Click "Save Changes" (will trigger redeploy)

## Verification

After deployment, check:

1. **Backend CORS**: Open browser console on frontend, should see no CORS errors
2. **API Connection**: Frontend should successfully fetch data from backend
3. **Health Check**: Visit https://ivie-be-final.onrender.com/api/health

## Additional Notes

### If using Vercel for Frontend

If you're deploying frontend to Vercel instead of Render:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   - `VITE_API_BASE_URL` = `https://ivie-be-final.onrender.com`
   - `VITE_IMGBB_API_KEY` = `c525fc0204b449b541b0f0a5a4f5d9c4`
3. Redeploy

### Update CORS_ORIGINS for Vercel

If using Vercel, update backend CORS_ORIGINS to include your Vercel domain:
```
CORS_ORIGINS=https://ivie-fe-final.onrender.com,https://your-vercel-domain.vercel.app
```

## Troubleshooting

### Still seeing CORS errors?
1. Check backend logs: `render.yaml` CORS_ORIGINS includes your frontend domain
2. Verify frontend is using correct API URL (check Network tab in DevTools)
3. Clear browser cache and hard reload (Ctrl+Shift+R)

### 404 Errors on assets?
1. Check if build completed successfully
2. Verify `dist` folder contains all assets
3. Check Render build logs for errors

### Backend not responding?
1. Check if backend service is running (Render Dashboard)
2. Visit `/api/health` endpoint to verify
3. Check backend logs for errors
