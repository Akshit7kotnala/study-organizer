# Deployment Guide - Study Organizer

This guide will help you deploy your Study Organizer application to the web for free!

## Recommended Platform: Render.com (FREE)

**Why Render.com?**
- ✅ **100% FREE** for students (no credit card required!)
- ✅ Free PostgreSQL database included
- ✅ Automatic HTTPS
- ✅ Easy GitHub integration
- ✅ Auto-deploy on code changes
- ✅ 750 hours/month free (enough for 24/7 uptime)

## Prerequisites

1. **GitHub Account** - Create one at https://github.com if you don't have one
2. **Render Account** - Sign up at https://render.com (use your GitHub account)
3. **Google Cloud Console** - For OAuth (you already have this)
4. **Cloud Storage** (Optional):
   - Azure Blob Storage (FREE with GitHub Student Pack)
   - Or AWS S3 (if you have credits)
   - Or use local storage (not recommended for production)

---

## Step 1: Prepare Your Code

### 1.1. Create a `.gitignore` file

Create a file named `.gitignore` in your project root:

```gitignore
# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environment
venv/
env/
ENV/

# Database (local only)
*.db
*.sqlite
*.sqlite3

# Uploads folder (use cloud storage in production)
uploads/
!uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
htmlcov/
.coverage
```

### 1.2. Initialize Git Repository

Open PowerShell in your project folder:

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Study Organizer with Collections"
```

### 1.3. Push to GitHub

1. Go to https://github.com and create a new repository
2. Name it `study-organizer` (or any name you prefer)
3. **DO NOT** initialize with README, .gitignore, or license
4. Copy the commands shown and run them:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/study-organizer.git
git branch -M main
git push -u origin main
```

---

## Step 2: Set Up Render.com

### 2.1. Create a PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `study-organizer-db`
   - **Database**: `study_organizer`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 15 or latest
   - **Plan**: **FREE**
4. Click **"Create Database"**
5. Wait for it to be created (takes 2-3 minutes)
6. **IMPORTANT**: Copy the **Internal Database URL** (starts with `postgres://`)

### 2.2. Create a Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select `study-organizer` repository
4. Configure:
   - **Name**: `study-organizer` (or your choice)
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: **FREE**

---

## Step 3: Configure Environment Variables

In Render's web service settings, go to **"Environment"** tab and add these variables:

### Required Variables:

```bash
# Secret Key (generate a random string)
SECRET_KEY=your-super-secret-key-here-change-me

# Database (use the Internal Database URL from Step 2.1)
DATABASE_URL=postgres://...from-step-2.1...

# Google OAuth (from your Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Python Environment
PYTHON_VERSION=3.11.9
```

### Optional - Cloud Storage Variables:

**Option A: Azure Blob Storage (FREE for students)**
```bash
STORAGE_TYPE=azure
AZURE_STORAGE_ACCOUNT_NAME=your-storage-account-name
AZURE_STORAGE_ACCOUNT_KEY=your-storage-account-key
AZURE_CONTAINER_NAME=study-documents
```

**Option B: AWS S3**
```bash
STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

**Option C: Local Storage (Not Recommended)**
```bash
STORAGE_TYPE=local
```
⚠️ Note: Render's free tier has ephemeral storage - files will be deleted on each deploy!

---

## Step 4: Update Google OAuth Settings

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Edit your OAuth 2.0 Client ID
5. Add to **Authorized Redirect URIs**:
   ```
   https://your-app-name.onrender.com/callback
   ```
   Replace `your-app-name` with your actual Render app name

---

## Step 5: Deploy!

1. Click **"Create Web Service"** in Render
2. Wait for the build to complete (5-10 minutes first time)
3. Once deployed, click on your app URL (e.g., `https://your-app-name.onrender.com`)
4. 🎉 Your app is live!

---

## Step 6: Initialize Database (First Time Only)

Your database tables will be created automatically when the app starts. Flask-SQLAlchemy will detect the empty database and create all tables.

If you need to manually create tables, you can use Render's Shell:

1. Go to your web service in Render
2. Click **"Shell"** tab
3. Run:
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

---

## Step 7: Set Up Azure Blob Storage (Recommended for File Storage)

### 7.1. Get Azure for Students (FREE $100 credit)

1. Go to https://azure.microsoft.com/en-us/free/students
2. Sign up with your school email
3. **NO CREDIT CARD REQUIRED** for students!
4. Get $100/year free credit

### 7.2. Create Storage Account

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **"Create a resource"** → **"Storage account"**
3. Configure:
   - **Resource group**: Create new `study-organizer-rg`
   - **Storage account name**: `studyorganizerstorage` (must be globally unique)
   - **Region**: Same as Render service
   - **Performance**: Standard
   - **Redundancy**: LRS (cheapest)
4. Click **"Review + Create"** → **"Create"**

### 7.3. Create Container

1. Go to your storage account
2. Click **"Containers"**
3. Click **"+ Container"**
4. Name: `study-documents`
5. Public access level: **Private**
6. Click **"Create"**

### 7.4. Get Access Keys

1. In your storage account, go to **"Access keys"**
2. Click **"Show keys"**
3. Copy:
   - **Storage account name**
   - **Key1** (connection string or key)
4. Add these to Render environment variables (see Step 3)

---

## Monitoring & Maintenance

### View Logs
- Go to your Render web service
- Click **"Logs"** tab to see real-time logs

### Automatic Deploys
- Every time you push to GitHub, Render will automatically rebuild and deploy
- Takes 3-5 minutes per deploy

### Database Backups
- Render automatically backs up your PostgreSQL database
- Free tier: 7 days of backups

### Upgrade Plans (Optional)
If you outgrow the free tier:
- **Web Service**: $7/month (better performance, no sleep)
- **Database**: $7/month (more storage, backups)

---

## Troubleshooting

### "Application Error" on first visit
- Wait 1-2 minutes for the app to wake up (free tier sleeps after inactivity)
- Check logs in Render dashboard

### Database Connection Error
- Verify `DATABASE_URL` environment variable is set correctly
- Make sure it starts with `postgresql://` (not `postgres://`)

### OAuth Error / Redirect URI Mismatch
- Double-check Google OAuth redirect URI matches your Render URL
- Format: `https://your-app-name.onrender.com/callback`

### Files Not Uploading
- If using local storage: **NOT RECOMMENDED** - files are deleted on redeploy
- Switch to Azure Blob Storage or AWS S3
- Verify storage credentials in environment variables

### App is Slow
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- Upgrade to paid plan ($7/month) for 24/7 uptime

---

## Security Best Practices

### ✅ DO:
- Use strong, random `SECRET_KEY`
- Keep `.env` file private (never commit to Git)
- Use HTTPS (automatic on Render)
- Regularly update dependencies
- Use cloud storage for production files

### ❌ DON'T:
- Commit `.env` file to Git
- Use default secret keys
- Store files locally in production
- Share your database credentials

---

## Alternative Deployment Options

If Render doesn't work for you, here are alternatives:

### 1. Railway.app
- **Free**: $5/month credit
- Similar to Render
- https://railway.app

### 2. Fly.io
- **Free**: Limited resources
- Good for small apps
- https://fly.io

### 3. PythonAnywhere
- **Free**: Limited but forever free
- Easier setup
- https://www.pythonanywhere.com

### 4. Azure App Service (with Student Credits)
- **$100/year FREE** with student pack
- More powerful
- Requires more configuration
- https://azure.microsoft.com/free/students

---

## Cost Breakdown (FREE Setup)

- ✅ **Render Web Service**: FREE (750 hours/month)
- ✅ **Render PostgreSQL**: FREE (limited storage)
- ✅ **Azure Blob Storage**: FREE with student pack ($100/year credit)
- ✅ **Google OAuth**: FREE
- ✅ **Domain**: Use Render's subdomain (FREE) or buy custom domain

**Total Cost: $0/month** 🎉

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **Azure Docs**: https://docs.microsoft.com/azure
- **GitHub Student Pack**: https://education.github.com/pack

---

## Next Steps After Deployment

1. ✅ Test all features (upload, search, tags, collections)
2. ✅ Invite classmates to try your app
3. ✅ Add custom domain (optional, ~$12/year)
4. ✅ Set up monitoring (Render includes basic monitoring)
5. ✅ Create backups of your database regularly

---

**🎉 Congratulations! Your Study Organizer is now live on the web!**

Share your app URL with friends: `https://your-app-name.onrender.com`
