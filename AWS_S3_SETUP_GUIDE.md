# AWS S3 Cloud Storage Setup Guide

This guide will help you set up AWS S3 for cloud storage in your Study Organizer application.

## Why Use S3?

- **Scalability**: Store unlimited documents without worrying about local disk space
- **Reliability**: 99.999999999% (11 9's) durability
- **Accessibility**: Access your documents from anywhere
- **Cost-Effective**: Pay only for what you use (~$0.023 per GB/month)
- **Automatic Backups**: Built-in redundancy and versioning
- **Security**: Encrypted storage with fine-grained access control

## Step 1: Create an AWS Account

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the registration process (requires credit card, but free tier is generous)

## Step 2: Create an S3 Bucket

1. Log into AWS Console: https://console.aws.amazon.com/
2. Search for "S3" in the services search bar
3. Click "Create bucket"
4. Configure your bucket:
   - **Bucket name**: `study-organizer-bucket` (must be globally unique, so add your name/numbers)
   - **AWS Region**: Choose the closest region (e.g., `us-east-1` for US East Coast)
   - **Block Public Access**: Keep ALL boxes CHECKED (for security)
   - **Bucket Versioning**: Enable (optional, but recommended for backup)
   - **Tags**: Add any tags you want (optional)
5. Click "Create bucket"

## Step 3: Create an IAM User with S3 Access

1. Search for "IAM" in the services search bar
2. Click "Users" in the left sidebar
3. Click "Create user"
4. Enter username: `study-organizer-app`
5. Click "Next"
6. Select "Attach policies directly"
7. Search for and select: `AmazonS3FullAccess` (or create custom policy for more security)
8. Click "Next" then "Create user"

## Step 4: Generate Access Keys

1. Click on the newly created user
2. Go to "Security credentials" tab
3. Scroll to "Access keys" section
4. Click "Create access key"
5. Select "Application running outside AWS"
6. Click "Next"
7. Add description: "Study Organizer App"
8. Click "Create access key"
9. **IMPORTANT**: Copy both:
   - **Access key ID**: `AKIA...` (looks like: `AKIAIOSFODNN7EXAMPLE`)
   - **Secret access key**: `wJal...` (looks like: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)
10. Click "Done"

⚠️ **WARNING**: Never share or commit your secret access key! Treat it like a password.

## Step 5: Configure Your Application

1. Open your `.env` file
2. Update the AWS configuration section:

```env
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=study-organizer-bucket

# Storage Configuration
STORAGE_TYPE=s3
```

3. Replace:
   - `your_access_key_id_here` with your Access key ID from Step 4
   - `your_secret_access_key_here` with your Secret access key from Step 4
   - `us-east-1` with your chosen region from Step 2
   - `study-organizer-bucket` with your bucket name from Step 2

## Step 6: Run Database Migration

Run this command to update your database schema:

```bash
python migrate_add_storage_type.py
```

## Step 7: Test the Integration

1. Start your application:

   ```bash
   python app.py
   ```

2. Look for the success message:

   ```
   ✓ S3 client initialized for bucket: study-organizer-bucket
   ```

3. Try uploading a document
4. Check your S3 bucket in the AWS Console - you should see:
   - `documents/` folder with your uploaded files
   - `thumbnails/` folder with generated thumbnails

## Switching Between Local and S3 Storage

To switch storage types, simply change the `STORAGE_TYPE` in your `.env` file:

- **Use S3 (Cloud)**: `STORAGE_TYPE=s3`
- **Use Local Storage**: `STORAGE_TYPE=local`

**Note**: Existing documents will remain in their original storage location. Only new uploads will use the configured storage type.

## Cost Estimation

AWS S3 Free Tier (first 12 months):

- 5 GB of standard storage
- 20,000 GET requests
- 2,000 PUT requests

After free tier, approximate costs:

- **Storage**: $0.023 per GB/month
- **Requests**: $0.0004 per 1,000 GET requests, $0.005 per 1,000 PUT requests
- **Data transfer**: First 100 GB/month is free

**Example**: Storing 100 GB of study documents costs ~$2.30/month

## Security Best Practices

1. **Never commit `.env` file** to version control (already in .gitignore)
2. **Use IAM policies** with minimum required permissions
3. **Enable MFA** on your AWS root account
4. **Rotate access keys** periodically
5. **Enable S3 bucket encryption** (optional but recommended)
6. **Monitor usage** with AWS CloudWatch

## Troubleshooting

### "Failed to initialize S3 client"

- Check your AWS credentials are correct
- Verify your AWS account is active
- Ensure you have internet connection

### "S3 upload failed"

- Verify the bucket name is correct
- Check the IAM user has S3 permissions
- Ensure the bucket is in the correct region

### "Access Denied" errors

- Confirm the IAM user has `AmazonS3FullAccess` policy
- Check bucket permissions (should NOT be public)
- Verify access keys are not expired

### Application falls back to local storage

- Check console output for error messages
- Verify `.env` file has correct values
- Ensure `STORAGE_TYPE=s3` is set

## Migrating Existing Local Files to S3

If you have existing documents stored locally and want to move them to S3:

1. Create a migration script or manually upload via AWS Console
2. Update the `storage_type` column in the database for migrated documents
3. Consider keeping local files as backup during transition

## Need Help?

- AWS S3 Documentation: https://docs.aws.amazon.com/s3/
- AWS Support: https://console.aws.amazon.com/support/
- IAM Best Practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

---

**Congratulations!** Your Study Organizer is now using cloud storage! 🎉
