# 🚀 Quick Start: Deploy MediGuide AI to Render

## ✅ All Issues Fixed & Pushed to GitHub!

Your repository is now ready for deployment with all issues resolved:

### What Was Fixed:
1. ✅ **Numpy dependency conflict** - Removed conflicting `numpy>=2.0.0` line
2. ✅ **Python version specification** - Fixed `runtime.txt` to use `python-3.11.9`
3. ✅ **Render configuration** - Added `render.yaml` for automatic deployment
4. ✅ **Documentation** - Added comprehensive `DEPLOYMENT.md` guide

### Changes Pushed to GitHub:
- Commit: `Fix numpy dependency conflict in requirements.txt`
- Commit: `Fix Python version specification in runtime.txt`
- Commit: `Add Render deployment configuration and comprehensive deployment guide`

Repository: https://github.com/Errisuvarna/mediguide-ai

---

## 🎯 Deploy to Render in 3 Steps

### Step 1: Connect Repository to Render

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Blueprint"**
3. Click **"Connect account"** to link your GitHub
4. Search and select: **`Errisuvarna/mediguide-ai`**
5. Click **"Connect"**

Render will automatically detect `render.yaml` and set up:
- ✅ Backend API service
- ✅ Frontend static site
- ✅ All environment variables
- ✅ Build and start commands

### Step 2: Add Your Gemini API Key

After services are created:

1. Go to **Backend Service** in Render dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `your-actual-gemini-api-key-here`
5. Click **"Save Changes"**

> 💡 Get a Gemini API key at: https://makersuite.google.com/app/apikey

### Step 3: Update CORS (After Frontend Deploys)

1. Wait for both services to deploy (5-10 minutes)
2. Copy your **frontend URL** (e.g., `https://mediguide-frontend.onrender.com`)
3. Go to **Backend Service** → **Environment** tab
4. Update `FRONTEND_ORIGIN` with your frontend URL
5. Click **"Save Changes"** (backend will redeploy automatically)

---

## 🎉 That's It!

Your MediGuide AI application will be live at:
- **Frontend**: `https://mediguide-frontend-XXXX.onrender.com`
- **Backend API**: `https://mediguide-backend-XXXX.onrender.com`
- **API Docs**: `https://mediguide-backend-XXXX.onrender.com/docs`

---

## 📊 What Happens During Deployment

### Backend Service:
```
1. Render pulls latest code from GitHub
2. Installs Python 3.11.9
3. Runs: pip install -r backend/requirements.txt
4. Seeds database with 648 records from dataset/
5. Builds RAG index from knowledge_base/ (45 chunks)
6. Starts FastAPI server on port $PORT
7. Health check confirms service is ready
```

### Frontend Service:
```
1. Render pulls latest code from GitHub
2. Installs Node.js and dependencies
3. Runs: cd frontend && npm install && npm run build
4. Serves built static files from frontend/dist/
5. Configures redirect rules for React Router
```

---

## ⚠️ Important Notes

### Free Tier Behavior:
- Services **sleep after 15 minutes** of inactivity
- First request after sleep takes **30-50 seconds** to wake up
- You get **750 hours/month** of free compute time

### Data Persistence:
- Currently using **SQLite** (ephemeral on Render free tier)
- Data **resets on each deployment**
- For production: upgrade to Render PostgreSQL or another managed database

### No Gemini API Key?
- The app works without it! It will use **fallback mode**
- Fallback returns the **best-matching knowledge base chunk** directly
- Voice features and full chat experience still work

---

## 🔧 Troubleshooting

### Build Fails?
```bash
# Check logs in Render dashboard → "Logs" tab
# Common issues:
- Missing environment variables
- Dependency conflicts (we fixed numpy already!)
- Python version mismatch (we fixed this too!)
```

### Service Won't Start?
```bash
# Check:
1. Health check endpoint: /api/health
2. Backend logs for errors
3. All environment variables are set
```

### Frontend Can't Connect to Backend?
```bash
# Solution:
1. Verify VITE_BACKEND_URL in frontend environment
2. Update FRONTEND_ORIGIN in backend environment
3. Check CORS settings in backend logs
```

---

## 🔄 Future Updates

To update your deployment:
```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main
```

Render will **automatically detect** the push and **redeploy** both services!

---

## 📚 Need More Help?

- **Full Deployment Guide**: See `DEPLOYMENT.md` in repository
- **Render Documentation**: https://render.com/docs
- **Project Architecture**: See `docs/architecture.md`

---

## ✨ Success Checklist

After deployment completes, verify:
- [ ] Backend service shows "Live" status
- [ ] Frontend service shows "Live" status  
- [ ] Visit frontend URL - app loads
- [ ] Test chat feature - gets responses
- [ ] Check `/docs` endpoint - Swagger UI loads
- [ ] Voice input works (requires HTTPS - ✅ on Render)
- [ ] View departments, doctors, services
- [ ] Submit feedback works
- [ ] Admin login works (if credentials set)

---

**🎊 Your MediGuide AI application is ready for deployment!**

Any issues? Check the logs in Render dashboard or refer to `DEPLOYMENT.md` for detailed troubleshooting.
