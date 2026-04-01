# Render.com Deployment Guide - Complete Instructions

## 🚀 Render Deployment Step-by-Step

### Prerequisites
- ✅ GitHub account with repo pushed (`git push origin main`)
- ✅ Render account (render.com)
- ✅ OpenAI API key ready

---

## Part 1: Prepare Your Repository

### 1. Commit All Changes
```powershell
git status
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Verify Files Exist (Should be done automatically)
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `.env` - Environment variables (NOT in Git)
- ✅ `.gitignore` - Excludes `.env` from Git

---

## Part 2: Deploy on Render.com

### Step 1: Sign Up on Render

1. Go to [render.com](https://render.com)
2. Click **"Sign up"**
3. Select **"Continue with GitHub"**
4. Authorize Render to access your GitHub repos

---

### Step 2: Create New Service from render.yaml

1. Click **"Dashboard"** (after signup)
2. Click **"New +"** → **"Blueprint"**
3. Select your `Data-Cleaning-Agent` repository
4. Configure:
   - **Blueprint Name**: `Data-Cleaning-Agent`
   - **Branch**: `main`
   - Click **"Deploy Blueprint"**

---

### Step 3: Wait for Auto-Deployment

Render will automatically:
- ✅ Deploy `data-cleaning-backend` (FastAPI)
- ✅ Deploy `data-cleaning-ui` (Streamlit)
- ✅ Assign unique domains
- Est. Time: 5-10 minutes

**You'll see:**
```
✓ Backend service live at: https://data-cleaning-backend.onrender.com
✓ Frontend service live at: https://data-cleaning-ui.onrender.com
```

---

## Part 3: Manual Configuration (If Needed)

### If Blueprint Deployment Fails, Deploy Manually:

#### Deploy Backend Service:

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub → Select your repo
3. **Basic Settings:**
   - Name: `data-cleaning-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn scripts.backend:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free** (sufficient for testing)

4. **Environment Variables:**
   Click **"Environment"** tab and add:

   | Key | Value |
   |-----|-------|
   | `OPENAI_API_KEY` | `sk-proj-pR3X...` (your full key) |
   | `PYTHONUNBUFFERED` | `1` |

5. Click **"Create Web Service"**
6. **Note the URL**: Something like `https://data-cleaning-backend.onrender.com`

#### Deploy Frontend Service:

1. Click **"New +"** → **"Web Service"** again
2. Select **same repo**
3. **Basic Settings:**
   - Name: `data-cleaning-ui`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0`
   - Plan: **Free**

4. **Environment Variables:**

   | Key | Value |
   |-----|-------|
   | `OPENAI_API_KEY` | `sk-proj-pR3X...` (same key) |
   | `FASTAPI_URL` | `https://data-cleaning-backend.onrender.com` (from step 3.6) |
   | `PYTHONUNBUFFERED` | `1` |

5. Click **"Create Web Service"**

---

## Part 4: Verify Deployment

### Check Services are Running:

1. **Backend Health Check:**
   ```
   https://data-cleaning-backend.onrender.com/docs
   ```
   Should show FastAPI Swagger UI

2. **Frontend:**
   ```
   https://data-cleaning-ui.onrender.com
   ```
   Should show Streamlit interface

3. **Check Logs:**
   - Dashboard → Service → **"Logs"** tab
   - Look for `Application startup complete`

---

## Part 5: Monitor & Manage

### View Real-Time Logs:
```
Dashboard → Select Service → Logs (auto-updates)
```

### Redeploy Changes:
```powershell
# Make code changes locally
git add .
git commit -m "Update: [description]"
git push origin main

# Render auto-deploys in 1-2 minutes
```

### Manual Redeploy (if needed):
- Dashboard → Service → **"Redeploy"** button

---

## Part 6: Production Environment Variables

### Update API URL in app/app.py:

The file already reads from `.env`:
```python
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8001")
```

**For Render**, the env var is set automatically in the dashboard.

---

## Part 7: Optional - Add PostgreSQL Database

### If you need a production database:

1. Dashboard → **"New +"** → **"PostgreSQL"**
2. Configure:
   - Name: `data-cleaning-db`
   - Region: Same as services
   - Plan: **Free**

3. Render auto-generates connection string
4. Add to Backend service environment:
   - `DATABASE_URL` (automatically set by Render)

---

## Part 8: Troubleshooting

### Issue: "Service failed to start"
**Solution:**
- Check logs for error message
- Verify `requirements.txt` has all dependencies
- Ensure Python version compatibility
- Command: View **Logs** tab

### Issue: "Frontend can't connect to backend"
**Solution:**
- Update `FASTAPI_URL` env var with correct backend domain
- No trailing slashes: `https://data-cleaning-backend.onrender.com`
- Recreate frontend service after updating

### Issue: "Module not found"
**Solution:**
- Add missing package to `requirements.txt`
- Commit and push
- Render will auto-redeploy

### Issue: "Timeout errors"
**Solution:**
- Upgrade from Free to Starter plan ($7/month)
- Or optimize code for faster execution
- Free tier has 15-min inactivity timeout

### Issue: "Service crashes after deployment"
**Solution:**
- Check environment variables are set correctly
- Verify OpenAI API key is valid
- Add `PYTHONUNBUFFERED=1` to prevent buffering issues

---

## Part 9: Costs & Limits

### Free Tier (Sufficient for Testing)
- ✅ $0/month base cost
- ⚠️ Services spin down after 15 min inactivity
- ⚠️ Limited compute power
- ⚠️ 750 hours/month

### Starter Plan ($7/month per service)
- ✅ Always-on services (no spin-down)
- ✅ Better performance
- ✅ Good for production
- **Cost**: $7 × 2 services = $14/month

### Production Recommendation:
- **Backend**: Starter ($7/month)
- **Frontend**: Starter ($7/month)
- **Total**: ~$14/month

---

## Part 10: Access Your Deployed App

| Component | URL |
|-----------|-----|
| **Streamlit UI** | `https://data-cleaning-ui.onrender.com` |
| **FastAPI Backend** | `https://data-cleaning-backend.onrender.com` |
| **API Documentation** | `https://data-cleaning-backend.onrender.com/docs` |
| **ReDoc** | `https://data-cleaning-backend.onrender.com/redoc` |

---

## Part 11: Push Future Updates

### Automatic Deployment:
```powershell
# Make any changes to your code
# Commit and push
git add .
git commit -m "Feature: [description]"
git push origin main

# Render auto-detects changes and redeploys
# Check status in Dashboard → Service → Deployments
```

---

## Part 12: Security Best Practices

✅ **What I've Done:**
- Remove `.env` from Git (via `.gitignore`)
- Store sensitive keys in Render environment variables
- Use HTTPS only (auto-enabled on render.com)

✅ **Still Do:**
- Don't share your OpenAI API key
- Rotate keys periodically
- Use environment variables for all secrets
- Add rate limiting to API (if needed)

---

## Quick Reference Commands

```powershell
# Check if all is ready
git status                    # Should show "nothing to commit"
git log -1                    # Last commit

# Deploy from terminal (optional)
npm install -g render       # If using Render CLI
render deploy               # Interactive deployment

# After deployment, test endpoints
$url = "https://data-cleaning-backend.onrender.com/docs"
Start-Process $url          # Open in browser
```

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Streamlit Docs**: https://docs.streamlit.io

---

## ✅ Deployment Checklist

- ✅ All code committed to GitHub
- ✅ `.env` NOT in Git (check `.gitignore`)
- ✅ `requirements.txt` updated
- ✅ `render.yaml` created
- ✅ Render account created
- ✅ Services deployed and running
- ✅ Environment variables set
- ✅ Both services accessible via URLs
- ✅ Backend and frontend connected
- ✅ Testing completed

---

## 🎉 You're Live!

Your AI Data Cleaning Agent is now deployed and accessible from anywhere!

Next Steps:
1. Test the Streamlit UI at your deployed URL
2. Try uploading a CSV/Excel file
3. Monitor logs for any issues
4. Upgrade plan if needed

**Questions?** Check [render.com/docs](https://render.com/docs)
