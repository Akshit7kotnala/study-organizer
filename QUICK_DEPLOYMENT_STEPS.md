# 🚀 Quick Deployment Guide - Let's Deploy Your App!

## ✅ Step 1: Git Repository Setup (COMPLETE!)

Your code is now ready in a Git repository with 40 files committed! ✅

---

## 📝 Step 2: Create GitHub Repository

### Option A: Using GitHub Website (Recommended)

1. **Go to GitHub**: https://github.com
2. **Sign in** (or create an account if you don't have one)
3. **Click the "+" icon** in the top right → **"New repository"**
4. **Fill in the details**:
   - **Repository name**: `study-organizer` (or any name you prefer)
   - **Description**: "A Flask-based study document organizer with collections, cloud storage, and mobile support"
   - **Visibility**: Choose **Public** (or Private if you prefer)
   - ⚠️ **DO NOT** check "Initialize with README, .gitignore, or license" (we already have these)
5. **Click "Create repository"**

### After creating the repository, GitHub will show you commands. Copy them and paste here in the terminal.

---

## 🔗 Step 3: Connect Your Local Repo to GitHub

After creating the GitHub repository, run these commands (GitHub will show them to you):

```powershell
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/study-organizer.git

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**📌 Note**: Replace `YOUR_USERNAME` with your actual GitHub username!

---

## 🎨 Step 4: Deploy to Render.com

### 4.1. Create Render Account

1. **Go to**: https://render.com
2. **Click "Get Started"**
3. **Sign up with GitHub** (easiest option - one click!)
4. **Authorize Render** to access your GitHub repositories

### 4.2. Create PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. **Configure**:
   - **Name**: `study-organizer-db`
   - **Database**: `study_organizer`
   - **Region**: Choose closest to you (e.g., Oregon USA, Frankfurt Europe, Singapore Asia)
   - **PostgreSQL Version**: 16 (or latest)
   - **Plan**: Select **FREE** ⭐
3. Click **"Create Database"**
4. ⏳ Wait 2-3 minutes for database creation
5. **IMPORTANT**: Once created, click on the database and copy the **"Internal Database URL"**
   - It looks like: `postgres://study_organizer_user:xxxx@dpg-xxxx/study_organizer_db`
   - **Save this URL** - you'll need it in the next step!

### 4.3. Create Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. **Connect Repository**:
   - Click "Connect account" if needed
   - Find and select your `study-organizer` repository
3. **Configure Service**:
   - **Name**: `study-organizer` (this will be your URL: study-organizer.onrender.com)
   - **Region**: **Same as your database!** (important for speed)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Select **FREE** ⭐ (Starter plan - 750 hours/month)

### 4.4. Add Environment Variables

Scroll down to **"Environment Variables"** section and click **"Add Environment Variable"**. Add these:

**Required Variables:**

```bash
# 1. Secret Key (generate a random string)
SECRET_KEY
your-super-secret-random-string-change-this-12345

# 2. Database URL (from Step 4.2)
DATABASE_URL
postgres://study_organizer_user:xxxx@dpg-xxxx/study_organizer_db

# 3. Google OAuth Client ID (your existing one)
GOOGLE_CLIENT_ID
your-google-client-id.apps.googleusercontent.com

# 4. Google OAuth Client Secret (your existing one)
GOOGLE_CLIENT_SECRET
your-google-client-secret

# 5. Python Version
PYTHON_VERSION
3.11.9
```

**Optional - Cloud Storage (Recommended):**

If using **Azure Blob Storage** (FREE for students):

```bash
STORAGE_TYPE
azure

AZURE_STORAGE_ACCOUNT_NAME
your-storage-account-name

AZURE_STORAGE_ACCOUNT_KEY
your-storage-key

AZURE_CONTAINER_NAME
study-documents
```

OR if using **AWS S3**:

```bash
STORAGE_TYPE
s3

AWS_ACCESS_KEY_ID
your-aws-key

AWS_SECRET_ACCESS_KEY
your-aws-secret

AWS_REGION
us-east-1

S3_BUCKET_NAME
your-bucket-name
```

OR use **local storage** (NOT recommended - files deleted on redeploy):

```bash
STORAGE_TYPE
local
```

4. Click **"Create Web Service"**

### 4.5. Wait for Deployment

- ⏳ First deployment takes **5-10 minutes**
- Watch the **"Logs"** tab to see progress
- You'll see:
  - Installing dependencies...
  - Building...
  - Starting Gunicorn...
  - ✅ Service live at https://study-organizer.onrender.com

---

## 🔐 Step 5: Update Google OAuth Settings

Your app is now live, but you need to tell Google about the new URL:

1. **Go to**: [Google Cloud Console](https://console.cloud.google.com)
2. **Select your project**
3. **Navigate to**: APIs & Services → Credentials
4. **Click on your OAuth 2.0 Client ID**
5. **Under "Authorized redirect URIs"**, click **"Add URI"**
6. **Add your Render URL**:
   ```
   https://your-app-name.onrender.com/callback
   ```
   Replace `your-app-name` with your actual Render app name
7. **Click "Save"**

---

## 🎉 Step 6: Test Your Deployed App!

1. **Visit your app**: `https://your-app-name.onrender.com`
2. **Test the features**:
   - ✅ Login with Google
   - ✅ Upload a document
   - ✅ Create a collection
   - ✅ Search for documents
   - ✅ Test on your phone! 📱

### First Visit Might Be Slow

- Free tier "sleeps" after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- After that, it's fast!

---

## 📱 Bonus: Test on Your Phone

1. **Visit your Render URL** on your phone
2. **Tap the menu icon** (☰) to test mobile navigation
3. **Try uploading** a photo from your phone
4. **Test collections** and search

Everything should work beautifully! 🎨

---

## 🔧 Troubleshooting

### "Application Error" on first visit

- Wait 1-2 minutes for app to wake up
- Check **Logs** in Render dashboard

### "Redirect URI mismatch" error

- Make sure you added the correct callback URL to Google Console
- Format: `https://your-app-name.onrender.com/callback`

### Database connection error

- Check that `DATABASE_URL` is set correctly in environment variables
- Make sure it starts with `postgresql://` (Render auto-converts from `postgres://`)

### Files not uploading

- If using local storage, files are deleted on redeploy (use Azure/S3!)
- Check storage credentials in environment variables

---

## 💰 Cost: $0/month!

- ✅ Render Web Service: **FREE** (750 hours)
- ✅ Render PostgreSQL: **FREE**
- ✅ Azure Storage: **FREE** (with student credits)
- ✅ Google OAuth: **FREE**

---

## 🚀 Auto-Deploy Updates

Every time you push to GitHub, Render automatically deploys:

```powershell
# Make changes to your code
# Then:
git add .
git commit -m "Your changes description"
git push

# Render automatically deploys! (takes 3-5 minutes)
```

---

## 📞 Need Help?

- **Render Status**: Check deployment logs in Render dashboard
- **Database Issues**: Make sure DATABASE_URL is set
- **OAuth Issues**: Verify redirect URIs match
- **Storage Issues**: Check Azure/S3 credentials

---

## ✅ Summary of What We Did

1. ✅ Initialized Git repository (40 files)
2. 🔄 Create GitHub repository (you'll do this)
3. 🔄 Push code to GitHub (you'll do this)
4. 🔄 Deploy to Render.com (you'll do this)
5. 🔄 Update Google OAuth (you'll do this)
6. 🎉 Test your live app!

---

**Next Step**: Go to https://github.com and create a new repository called `study-organizer`, then come back and I'll help you push the code! 🚀
