# Railway Deployment Guide - AI Data Cleaning Agent

## Complete Step-by-Step Deployment Instructions

### Prerequisites
1. ✅ GitHub account with your repo pushed
2. ✅ Railway account (railway.app)
3. ✅ OpenAI API key
4. ✅ PostgreSQL database (optional, for production data)

---

## Part 1: Initial Repository Setup

### 1. Verify Git Setup
```powershell
git status
git log --oneline -3
```

### 2. Push Latest Changes
```powershell
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

---

## Part 2: Deploy on Railway

### Step 1: Create Railway Account & Project

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Connect your GitHub account
6. Select `Data-Cleaning-Agent` repo

---

### Step 2: Deploy Backend Service (FastAPI)

Once the project is created:

1. **Click "Add Service"** → **"GitHub Repo"**
2. Select your repo again
3. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `backend` |
| **Root Directory** | `/` (leave empty) |
| **Buildpack** | Python |
| **Start Command** | `uvicorn scripts.backend:app --host 0.0.0.0 --port $PORT` |

#### Add Environment Variables for Backend:

Click **"Variables"** and add:

| Key | Value | Scope |
|-----|-------|-------|
| `OPENAI_API_KEY` | `sk-proj-pR3X...` (your key) | Production |
| `PYTHONUNBUFFERED` | `1` | Production |
| `PORT` | `8000` | Production |

#### Domain Setup:
- Railway auto-generates a domain: `https://backend-[random].railway.app`
- Save this URL for later (needed for frontend)

---

### Step 3: Deploy Frontend Service (Streamlit)

1. **Click "Add Service"** → **"GitHub Repo"**
2. Select repo once more
3. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `frontend` |
| **Root Directory** | `/` |
| **Buildpack** | Python |
| **Start Command** | `streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0 --logger.level=error` |

#### Add Environment Variables for Frontend:

| Key | Value | Scope |
|-----|-------|-------|
| `OPENAI_API_KEY` | `sk-proj-pR3X...` (same key) | Production |
| `FASTAPI_URL` | `https://backend-[random].railway.app` | Production |
| `PYTHONUNBUFFERED` | `1` | Production |
| `PORT` | `8501` | Production |

---

### Step 4: (Optional) Deploy PostgreSQL Database

If you need production database:

1. Click **"Add Service"** → **"Database"** → **"PostgreSQL"**
2. Railway auto-configures it
3. Environment variables are automatically set:
   - `DATABASE_URL` (connection string)
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

#### Connect Database to Backend:

1. Go to Backend service → **"Variables"**
2. Add:

| Key | Value |
|-----|-------|
| `DB_HOST` | Get from DATABASE_URL |
| `DB_PORT` | `5432` |
| `DB_USER` | Get from PGUSER |
| `DB_PASSWORD` | Get from PGPASSWORD |
| `DB_NAME` | Get from PGDATABASE |

---

## Part 3: Configuration Details

### Backend Service Config (railway.json)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "paketo"
  },
  "deploy": {
    "startCommand": "uvicorn scripts.backend:app --host 0.0.0.0 --port $PORT",
    "restartPolicyMaxRetries": 3,
    "restartPolicyWindowMs": 60000
  }
}
```

### Python Version (runtime.txt)
```
python-3.11.8
```

---

## Part 4: Monitoring & Troubleshooting

### View Logs
1. Go to each service in Railway dashboard
2. Click **"Logs"** tab
3. Monitor deployment progress

### Common Issues & Solutions

**Issue: "ModuleNotFoundError"**
- Solution: Check `requirements.txt` includes all dependencies
- Run locally: `pip install -r requirements.txt`

**Issue: "Connection refused to backend"**
- Solution: Update Streamlit `FASTAPI_URL` to correct backend domain
- Check it doesn't have trailing slash

**Issue: "Port already in use"**
- Solution: Railway automatically handles port assignment via `$PORT` variable
- Don't hardcode ports

**Issue: Services timing out**
- Solution: Increase Railway plan or optimize code
- Check for long-running operations in `app/app.py`

---

## Part 5: Access Your Deployment

### URLs After Deployment

| Service | URL |
|---------|-----|
| **FastAPI Backend** | `https://backend-[random].railway.app` |
| **API Docs** | `https://backend-[random].railway.app/docs` |
| **Streamlit UI** | `https://frontend-[random].railway.app` |
| **Optional DB** | PostgreSQL hosted on Railway |

---

## Part 6: Continuous Deployment

### Automatic Updates
- Whenever you push to `main` branch, Railway automatically redeploys
- Deployments take 2-5 minutes

### Manual Redeploy
1. Go to service in dashboard
2. Click **"Redeploy"** button

---

## Part 7: Environment Variables Reference

### Backend (.env locally)
```
OPENAI_API_KEY=sk-proj-...
BACKEND_PORT=8001
BACKEND_HOST=0.0.0.0
DATABASE_URL=postgresql://...
```

### Frontend (.env locally)
```
OPENAI_API_KEY=sk-proj-...
FASTAPI_URL=http://127.0.0.1:8001
```

### Railway (automatically set)
```
PORT (auto-assigned)
RAILWAY_ENVIRONMENT_NAME (production)
RAILWAY_PUBLIC_DOMAIN (auto-generated)
```

---

## Part 8: Production Checklist

Before final deployment:

- ✅ All dependencies in `requirements.txt`
- ✅ `.env` file NOT committed to Git (check `.gitignore`)
- ✅ Environment variables set in Railway dashboard
- ✅ Database migrations run (if applicable)
- ✅ Error handling in place
- ✅ Logging configured
- ✅ CORS configured for cross-domain requests
- ✅ API rate limiting set
- ✅ Security headers added

---

## Part 9: Cost Information

### Railway Free Tier
- $5/month promotional credits
- Auto-scales down when idle

### Pricing
- **Backend Service**: ~$5-10/month
- **Frontend Service**: ~$5-10/month
- **PostgreSQL Database**: ~$15/month (if used)

---

## Quick Command Reference

```powershell
# Test locally before deploying
& .\.venv\Scripts\Activate.ps1
uvicorn scripts.backend:app --reload --port 8001
streamlit run app/app.py

# Push to GitHub (auto-deploys on Railway)
git add .
git commit -m "Production updates"
git push origin main

# Check Railway logs
# Use Railway dashboard → Service → Logs
```

---

## Support

- **Railway Docs**: https://docs.railway.app
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Streamlit Docs**: https://docs.streamlit.io

---

**🎉 Your app is now ready for production deployment!**
