# Deployment Guide for MediGuide AI

## Quick Deploy to Render

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub** (Already done!)
   ```bash
   git push origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository: `Errisuvarna/mediguide-ai`
   - Render will automatically detect `render.yaml` and create both services

3. **Configure Environment Variables**
   - After deployment, add your `GEMINI_API_KEY` in the Render dashboard:
     - Go to your backend service
     - Navigate to "Environment" tab
     - Add `GEMINI_API_KEY` with your Google Gemini API key

4. **Update CORS Settings** (if needed)
   - Once you have the frontend URL, update `FRONTEND_ORIGIN` in backend environment variables
   - Format: `https://your-frontend-name.onrender.com`

### Option 2: Manual Setup

#### Backend Deployment

1. **Create a New Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect repository: `Errisuvarna/mediguide-ai`
   - Configure:
     - **Name**: `mediguide-backend`
     - **Region**: Oregon (US West)
     - **Branch**: `main`
     - **Root Directory**: Leave empty (use root)
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   Add these in the Render dashboard:
   ```
   PYTHON_VERSION=3.11.9
   APP_NAME=MediGuide AI
   ENVIRONMENT=production
   SECRET_KEY=<generate-a-secure-random-string>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   DATABASE_URL=sqlite:///./mediguide.db
   GEMINI_API_KEY=<your-gemini-api-key>
   GEMINI_MODEL=gemini-1.5-flash
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   TOP_K_RESULTS=4
   FRONTEND_ORIGIN=https://your-frontend-url.onrender.com
   ```

3. **Health Check**
   - Path: `/api/health`
   - This ensures Render knows when your service is ready

#### Frontend Deployment

1. **Create a Static Site**
   - Go to Render Dashboard
   - Click "New +" → "Static Site"
   - Connect repository: `Errisuvarna/mediguide-ai`
   - Configure:
     - **Name**: `mediguide-frontend`
     - **Branch**: `main`
     - **Root Directory**: Leave empty
     - **Build Command**: `cd frontend && npm install && npm run build`
     - **Publish Directory**: `frontend/dist`

2. **Environment Variables**
   ```
   VITE_BACKEND_URL=https://your-backend-url.onrender.com
   ```

3. **Redirect Rules**
   Add this to handle React Router:
   - Source: `/*`
   - Destination: `/index.html`
   - Action: `Rewrite`

## Important Notes

### Database Persistence
- The current setup uses SQLite with ephemeral storage
- Data will be lost on service restarts
- For production, consider:
  - Using Render's PostgreSQL database
  - Updating `DATABASE_URL` environment variable
  - No code changes needed (SQLAlchemy handles both!)

### Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- First request after sleep takes 30-50 seconds to wake up
- 750 hours/month free compute time

### Monitoring
- Check logs in Render dashboard under "Logs" tab
- Monitor deployment status under "Events" tab
- Set up alerts for failed deployments

## Troubleshooting

### Build Fails
1. Check the build logs in Render dashboard
2. Verify `requirements.txt` has no conflicting dependencies
3. Ensure Python version matches `runtime.txt` (3.11.9)

### Service Won't Start
1. Check environment variables are set correctly
2. Verify health check endpoint is responding
3. Review application logs for errors

### CORS Errors
1. Update `FRONTEND_ORIGIN` in backend environment variables
2. Include the exact URL (with https://)
3. Redeploy backend service

### API Errors
1. Verify `GEMINI_API_KEY` is set
2. Check if the API key is valid
3. Review backend logs for specific error messages

## Updating the Deployment

```bash
# Make your changes
git add .
git commit -m "Your commit message"
git push origin main
```

Render will automatically detect the push and redeploy both services.

## Alternative Deployment Options

### Using Docker
The project includes a `Dockerfile` and `docker-compose.yml`:

```bash
docker compose up --build
```

### Using Vercel (Frontend Only)
```bash
cd frontend
npm install
vercel --prod
```

### Using Railway, Fly.io, or Heroku
Similar configuration as Render - adjust build/start commands accordingly.

## Post-Deployment Checklist

- [ ] Backend service is running and healthy
- [ ] Frontend service is deployed and accessible
- [ ] CORS is configured correctly
- [ ] GEMINI_API_KEY is set (or fallback mode is acceptable)
- [ ] Database is seeded with initial data
- [ ] RAG index is built successfully
- [ ] Health check endpoint responds
- [ ] API documentation is accessible at `/docs`
- [ ] Frontend can connect to backend API
- [ ] Test chat functionality
- [ ] Test voice input/output (requires HTTPS)

## Support

For issues:
1. Check Render service logs
2. Review application logs
3. Verify all environment variables
4. Test locally first: `uvicorn app.main:app --reload` (backend)
5. Check GitHub repository issues
