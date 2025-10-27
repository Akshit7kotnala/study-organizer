# 🎓 Study Organizer - Complete Usage Guide

Welcome to your Study Documents Organizer! This guide will help you get started quickly.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Run the App

```powershell
python app.py
```

### Step 3: Open Browser

Navigate to: **http://127.0.0.1:5000/**

---

## 📚 Using the Application

### 1️⃣ Home Page

When you first open the app, you'll see:

- **Total Documents Counter** - shows how many documents you've uploaded
- **Year Cards** - click on any year (1st, 2nd, 3rd, 4th) to view documents

### 2️⃣ Uploading Documents

**Click "Upload" in the navigation bar**

Fill in the form:

- **File**: Click "Choose File" and select your document
  - Accepts: PDF, Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), images (.jpg, .png, .gif), and more
  - Max size: 50MB per file
- **Year**: Select your academic year (1-5)
- **Subject**: Enter the subject name
  - Examples: "Mathematics", "Physics", "Computer Science"
- **Tags** (Optional): Add comma-separated tags
  - Examples: "lecture, notes" or "exam, midterm, preparation"

**Click "Upload Document"**

After uploading, you'll be redirected to that year's document list.

### 3️⃣ Viewing Documents by Year

Click on any year card (e.g., "1st Year") to see all documents for that year.

**Features on this page:**

- **Filter by Subject** - dropdown with all subjects you've used
- **Filter by Tags** - enter tags to search
- **Document Cards** show:
  - File type icon (PDF, Word, Excel, etc.)
  - Filename
  - Subject (blue badge)
  - Tags (gray badges)
  - File size
  - Upload date/time
  - Action buttons (Download, Preview)

**Pagination:**

- 10 documents per page
- Navigation at the bottom (Previous, page numbers, Next)

### 4️⃣ Filtering Documents

Use the filter section at the top:

**Filter by Subject:**

1. Click the "Subject" dropdown
2. Select a subject
3. Click "Apply Filter"

**Filter by Tags:**

1. Enter tags in the "Tags" field (comma-separated)
2. Click "Apply Filter"

**Clear Filters:**

- Click "Clear" button to see all documents again

### 5️⃣ Previewing Files

**Click the "Preview" button** on any document.

**What you can preview:**

- **PDFs** - embedded in browser
- **Images** (PNG, JPG, GIF) - displayed inline
- **Other files** - shows download option

The preview page shows:

- File metadata (subject, tags, size, upload date)
- Download button
- Back button to return to year view

### 6️⃣ Downloading Files

**Click the "Download" button** on any document.

The file will download with its **original filename** (the name you uploaded it with).

---

## 🧪 Testing the App

### Run Unit Tests

```powershell
pytest test_app.py -v
```

All 10 tests should pass:

- Index page tests
- Upload functionality tests
- Filtering tests
- Download/preview tests

### Generate Sample Data

Want to see the app with sample documents?

```powershell
python demo_data.py
```

This will create:

- 5 sample documents per year (20 total)
- Realistic subjects (Math, Physics, CS, etc.)
- Various file types (PDF, Word, PowerPoint, images)
- Random tags and upload dates

Then run the app and browse the sample data!

---

## 🎨 Features Overview

### ✅ Core Features

- ✨ Upload files with metadata (year, subject, tags)
- 📁 Organize documents by academic year
- 🔍 Filter by subject and tags
- 👀 Preview images and PDFs in browser
- ⬇️ Download files with original filenames
- 📊 Pagination (10 documents per page)
- 📈 Total document counter on home page

### ✅ UI Features

- 🎨 Modern Bootstrap 5 design
- 📱 Responsive (works on mobile, tablet, desktop)
- 🎯 File type icons (PDF, Word, Excel, etc.)
- 📏 Human-readable file sizes (KB, MB, GB)
- ⚡ Hover effects on cards and lists
- 💬 Flash messages for user feedback
- 🎭 Beautiful footer with branding

---

## 🗂️ File Organization

### How Files Are Stored

**On Upload:**

1. Original filename is saved in database
2. File is renamed with a UUID (prevents conflicts)
3. File is stored in `uploads/` directory
4. Metadata is saved in SQLite database

**Example:**

- You upload: `Math-Lecture-Notes.pdf`
- Stored as: `a3f2c4d1e5b6789012345678.pdf`
- Database remembers original name
- When you download, you get: `Math-Lecture-Notes.pdf`

### Database Storage

SQLite database (`documents.db`) stores:

- Original filename
- Storage filename (UUID-based)
- Year
- Subject
- Tags
- File MIME type
- File size
- Upload timestamp

---

## 🔧 Configuration

### Customize Settings

Edit `app.py` to change:

**Upload Folder:**

```python
app.config['UPLOAD_FOLDER'] = 'uploads'  # Change path
```

**Max File Size:**

```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

**Pagination:**

```python
per_page = 10  # Documents per page (in year_view route)
```

**Secret Key (IMPORTANT for production):**

```python
app.config['SECRET_KEY'] = 'your-secure-random-key-here'
```

---

## 🆘 Troubleshooting

### App Won't Start

**Error: "No module named 'flask'"**

```powershell
pip install -r requirements.txt
```

**Error: "Address already in use"**

- Another app is using port 5000
- Stop the other app or change port in `app.py`:

```python
app.run(debug=True, port=5001)  # Use different port
```

### Upload Issues

**Error: "No file selected"**

- Make sure you clicked "Choose File" and selected a file
- File input cannot be empty

**Error: "Subject is required"**

- Fill in the subject field before uploading

**Upload is slow**

- Large files take time to upload
- Check your file size (max 50MB)

### Database Issues

**Delete and recreate database:**

```powershell
Remove-Item documents.db
python app.py  # Will auto-create new database
```

**View database content:**

```powershell
sqlite3 documents.db
.tables
SELECT * FROM document;
.quit
```

---

## 📖 Common Workflows

### Workflow 1: Organizing Semester Notes

1. **Upload all lecture notes** for current semester
   - Use consistent subject names
   - Tag with "lecture", "notes"
2. **Before exam:**
   - Go to your year
   - Filter by subject
   - Download or preview all notes

### Workflow 2: Assignment Management

1. **Upload completed assignments**
   - Subject: "Math 201"
   - Tags: "assignment, homework, completed"
2. **Later reference:**
   - Filter by "assignment" tag
   - Download for review

### Workflow 3: Exam Preparation

1. **Upload past exams and study guides**
   - Tags: "exam, midterm" or "exam, final"
2. **Filter by exam tags**
   - See all exam materials together
   - Preview PDFs in browser

---

## 🚨 Important Notes

### Security Warnings

⚠️ **This is a development app** - Not production-ready!

**For production use, you MUST:**

- Change the SECRET_KEY
- Add user authentication
- Validate file types and scan for malware
- Use HTTPS
- Add access controls
- Use a production WSGI server (not Flask dev server)

### File Safety

- ✅ Files are renamed with UUIDs (no conflicts)
- ✅ Original filenames preserved for download
- ⚠️ No virus scanning
- ⚠️ No file type restrictions
- ⚠️ No user quotas

---

## 🎓 Tips & Best Practices

### Naming Conventions

**Subjects:**

- Use consistent names: "Mathematics I" not sometimes "Math 1"
- Include course codes if helpful: "CS 101 - Programming"

**Tags:**

- Use lowercase for consistency
- Common tags: lecture, notes, exam, assignment, lab, project, tutorial
- Combine tags: "midterm, preparation, study-guide"

### Organization

**By Year:**

- Keep documents organized by academic year
- Update year when advancing

**By Subject:**

- Use full subject names
- Be consistent across uploads

**By Tags:**

- Tag everything for easy searching
- Use multiple tags per document

### Performance

**File Sizes:**

- Compress large PDFs before uploading
- Resize images if needed
- Split very large documents

**Database:**

- Backup `documents.db` regularly
- Test recovery procedures

---

## 📞 Need Help?

### Check These Files

1. **README.md** - Installation and setup
2. **PROJECT_SUMMARY.md** - Technical details and testing results
3. **This file (USAGE_GUIDE.md)** - How to use the app

### Run Demo Data

```powershell
python demo_data.py
```

Generates sample documents to explore the app's features.

---

## 🎉 Enjoy Your Study Organizer!

You now have everything you need to manage your study documents effectively!

**Quick Reminder:**

```powershell
# Start the app
python app.py

# Generate sample data
python demo_data.py

# Run tests
pytest test_app.py -v
```

**Access the app at:** http://127.0.0.1:5000/

Happy studying! 📚✨
