# Microsoft Azure for Students - Cloud Storage Setup Guide

This guide will help you set up **Microsoft Azure Blob Storage** for FREE using your GitHub Student Pack!

## 🎓 Why Azure for Students is PERFECT for You

- **$100 FREE Credit** - No credit card required!
- **Renews Annually** - Get another $100 every year while you're a student
- **No Surprise Charges** - Cannot be charged without upgrading
- **Student-Friendly** - Made specifically for students
- **Professional Experience** - Learn industry-standard cloud platform

## 💰 What You Get FREE

- **$100 Azure Credit per year** (enough for ~200GB storage for a year!)
- **Popular services FREE forever** (even after credit expires)
- **No credit card needed** to sign up
- **Renews every year** as long as you're a verified student

---

## 📋 Prerequisites

1. **Valid student email** (.edu or verified through school)
2. **GitHub Student Developer Pack** (get it at: https://education.github.com/pack)
3. **5 minutes** of your time!

---

## Step 1: Activate Azure for Students

### 1.1 Visit Azure for Students Page

1. Go to: **https://azure.microsoft.com/en-us/free/students/**
2. Click the big green "**Activate now**" button

### 1.2 Sign In with Microsoft Account

1. Sign in with your **school email** (recommended) or personal Microsoft account
2. If you don't have a Microsoft account, create one (it's free!)

### 1.3 Verify Student Status

1. Azure will ask you to verify you're a student
2. Options:

   - **School email verification** (easiest - instant)
   - **Upload student ID** or enrollment document
   - **International Student Identity Card (ISIC)**

3. **Wait for approval** (usually instant with .edu email, or within 24 hours)

### 1.4 Activation Complete! 🎉

You should see: "**You have $100 in Azure credits!**"

---

## Step 2: Create a Storage Account

### 2.1 Go to Azure Portal

1. Navigate to: **https://portal.azure.com/**
2. Sign in with your student account

### 2.2 Create Storage Account

1. Click "**Create a resource**" (top left, or search bar)
2. Search for "**Storage account**" and click it
3. Click "**Create**"

### 2.3 Configure Storage Account

Fill in the form:

**Basics Tab:**

- **Subscription**: Azure for Students
- **Resource group**: Click "Create new" → Name it `study-organizer-resources`
- **Storage account name**: `studyorg<yourname>` (must be globally unique, lowercase, no spaces)
  - Example: `studyorgakshi`, `studyorgjohn123`
- **Region**: Choose closest to you (e.g., `(US) East US`, `(Europe) West Europe`)
- **Performance**: **Standard** (cheaper, perfect for documents)
- **Redundancy**: **Locally-redundant storage (LRS)** (cheapest, good enough)

**Leave other tabs as default** and click "**Review + create**"

### 2.4 Create Container

1. Wait for deployment (30 seconds)
2. Click "**Go to resource**"
3. In the left sidebar, click "**Containers**" (under Data storage)
4. Click "+ **Container**" at the top
5. Name it: `study-documents`
6. **Public access level**: **Private** (keep your docs secure!)
7. Click "**Create**"

---

## Step 3: Get Your Access Keys

### 3.1 Find Access Keys

1. In your storage account, look at the left sidebar
2. Under "Security + networking", click "**Access keys**"
3. You'll see two keys (key1 and key2)

### 3.2 Copy Credentials

1. **Storage account name**: At the top (e.g., `studyorgakshi`)
2. Click "**Show**" next to key1
3. **Copy the Key value** (looks like: `abc123XYZ...` very long string)

⚠️ **IMPORTANT**: Keep these keys secret! They're like passwords to your storage.

---

## Step 4: Configure Your Application

### 4.1 Open Your .env File

Navigate to your project folder and open `.env`

### 4.2 Update Azure Configuration

Find the Azure section and update:

```env
# Azure Blob Storage Configuration (RECOMMENDED FOR STUDENTS)
# Get these from Azure Portal after creating storage account
# FREE: $100 credit/year with GitHub Student Pack, no credit card needed!
AZURE_STORAGE_ACCOUNT_NAME=studyorgakshi
AZURE_STORAGE_ACCOUNT_KEY=your_very_long_access_key_here
AZURE_CONTAINER_NAME=study-documents

# Storage Configuration
# Set to 'azure' for Azure Blob Storage, 's3' for AWS S3, or 'local' for local filesystem
STORAGE_TYPE=azure
```

### 4.3 Replace Values

- **AZURE_STORAGE_ACCOUNT_NAME**: Your storage account name from Step 2.3
- **AZURE_STORAGE_ACCOUNT_KEY**: The key1 value from Step 3.2
- **AZURE_CONTAINER_NAME**: `study-documents` (or whatever you named it)
- **STORAGE_TYPE**: Change from `local` to `azure`

---

## Step 5: Test Your Setup!

### 5.1 Start the Application

```bash
python app.py
```

### 5.2 Look for Success Message

You should see:

```
✓ Azure Blob Storage initialized for account: studyorgakshi
```

### 5.3 Upload a Test Document

1. Open http://127.0.0.1:5000 in your browser
2. Log in with Google
3. Upload a document
4. Success! Your file is now in the cloud! ☁️

### 5.4 Verify in Azure Portal

1. Go back to Azure Portal
2. Navigate to your storage account
3. Click "Containers" → "study-documents"
4. You should see folders:
   - `documents/` - Your uploaded files
   - `thumbnails/` - Generated thumbnails

---

## 💡 Pro Tips for Students

### Monitor Your Spending

1. In Azure Portal, go to "Cost Management + Billing"
2. Check "Cost analysis" to see credit usage
3. Set up spending alerts (optional)

### Your $100 Lasts a LONG Time!

**Example costs with Azure Blob Storage:**

- Storage: ~$0.018 per GB/month
- $100 = Store **555 GB** for a month, OR
- $100 = Store **50 GB** for **10 months**, OR
- $100 = Store **10 GB** for **55 months** (4.5 years!)

**Reality check**: Most students use 5-20 GB → Your credit lasts 1-2 years easily!

### What Happens After Credit Expires?

- You can keep using free services (many services have always-free tiers)
- You can upgrade to pay-as-you-go (with approval)
- You can renew for another year if still a student!

---

## 🔄 Switching Between Storage Types

Want to test locally first? No problem!

### Use Local Storage:

```env
STORAGE_TYPE=local
```

### Use Azure Cloud Storage:

```env
STORAGE_TYPE=azure
```

### Use AWS S3:

```env
STORAGE_TYPE=s3
```

Just change `STORAGE_TYPE` and restart your app!

**Note**: Existing documents stay where they were uploaded. Only new uploads use the new storage type.

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to Git (already in .gitignore)
2. **Rotate keys periodically** (Azure lets you regenerate keys)
3. **Use separate containers** for different apps
4. **Enable soft delete** (in container settings - recovers deleted files for 7 days)
5. **Monitor access logs** in Azure Portal

---

## 🐛 Troubleshooting

### "Failed to initialize Azure Blob Storage"

**Solutions:**

- ✓ Check storage account name is correct (no typos!)
- ✓ Verify access key is complete (it's very long, ~88 characters)
- ✓ Ensure no extra spaces in .env file
- ✓ Confirm you're using the key1 value, not the connection string

### "Container not found"

**Solutions:**

- ✓ Check container name matches exactly (case-sensitive!)
- ✓ Verify container exists in Azure Portal
- ✓ Make sure you're looking at the right storage account

### "Application falls back to local storage"

**Solutions:**

- ✓ Check console output for detailed error message
- ✓ Verify `STORAGE_TYPE=azure` in .env
- ✓ Restart the application after changing .env

### "Cannot create container"

**Solutions:**

- ✓ Container may already exist (this is fine!)
- ✓ Check if you have permissions on the storage account
- ✓ Ensure storage account is activated

### Files not appearing in Azure Portal

**Solutions:**

- ✓ Refresh the containers view
- ✓ Click into `documents/` folder
- ✓ Check console output for upload errors
- ✓ Verify STORAGE_TYPE is set to 'azure'

---

## 📊 Cost Comparison

| Service                | Free Tier          | After Free Tier  | Best For            |
| ---------------------- | ------------------ | ---------------- | ------------------- |
| **Azure for Students** | $100/year, no card | ~$0.018/GB/month | Students (YOU!)     |
| AWS S3                 | 5GB for 12 months  | $0.023/GB/month  | After graduation    |
| Local Storage          | FREE               | FREE disk space  | Development/testing |

**Winner for students**: Azure! 🎓

---

## 🎓 Learning Resources

- **Azure Documentation**: https://docs.microsoft.com/en-us/azure/storage/
- **Azure for Students FAQ**: https://azure.microsoft.com/en-us/free/students/faq/
- **Blob Storage Tutorial**: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
- **GitHub Student Pack**: https://education.github.com/pack

---

## 🆘 Need Help?

1. **Azure Support for Students**: https://azure.microsoft.com/en-us/support/options/
2. **Azure Community Forum**: https://docs.microsoft.com/en-us/answers/products/azure
3. **GitHub Education Support**: https://support.github.com/

---

## ✨ Next Steps

Once you're comfortable with Azure:

1. **Enable versioning** for automatic backups
2. **Set up lifecycle management** (auto-delete old files)
3. **Use Azure CDN** for faster downloads
4. **Explore Azure Functions** for serverless computing
5. **Add Azure Key Vault** for even better security

---

**Congratulations!** You're now using professional cloud storage for FREE! 🚀☁️

Your study documents are:

- ✅ Safely backed up in Microsoft's data centers
- ✅ Accessible from anywhere in the world
- ✅ Costing you $0 thanks to your student status
- ✅ Helping you learn real-world cloud skills!

Happy studying! 📚✨
