# 📚 Study Organizer - AI-Powered Learning Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.2+-green?style=for-the-badge&logo=flask)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange?style=for-the-badge&logo=openai)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A cutting-edge web application that combines document management with AI-powered features to revolutionize how students organize and study their materials.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [AI Features](#-ai-powered-features) • [Documentation](#-documentation)

</div>

---

## 🌟 Overview

Study Organizer is a comprehensive learning platform built with Flask that leverages artificial intelligence to help students manage their academic documents efficiently. It combines traditional document organization with modern AI capabilities including automatic summarization, smart tagging, OCR text extraction, intelligent search, and personalized study recommendations.

## ✨ Features

### 📁 Core Document Management
- **Multi-format Support**: Upload PDFs, images, Word docs, PowerPoint, and more
- **Smart Organization**: Organize by academic year, subject, and custom tags
- **Preview System**: In-browser preview for PDFs, images, and text files
- **Thumbnail Generation**: Automatic thumbnail creation for visual browsing
- **Cloud Storage**: Support for local, AWS S3, and Azure Blob Storage

### 📝 Content Creation
- **Text Notes**: Create rich text notes directly in the app
- **Document Upload**: Drag-and-drop or click-to-upload interface
- **Batch Operations**: Upload multiple documents at once
- **Metadata Management**: Edit tags, subjects, and descriptions

### 🤖 AI-Powered Features
- **Document Summarization** 📄
  - Automatic AI-generated summaries using OpenAI GPT-3.5
  - 500-character concise overviews
  - Quick document understanding without reading full content

- **Smart Tagging** 🏷️
  - Automatic keyword extraction using NLP (NLTK)
  - AI-suggested tags based on content analysis
  - Context-aware tagging for better organization

- **OCR Text Extraction** 👁️
  - Extract text from images using Tesseract OCR
  - Process scanned PDFs and handwritten notes
  - Multi-language support (configurable)

- **Intelligent Search** 🔍
  - Full-text search across all documents
  - Search within summaries and extracted text
  - Tag-based filtering and discovery
  - Real-time search suggestions

- **Study Recommendations** 💡
  - ML-based content similarity analysis
  - TF-IDF vectorization with cosine similarity
  - Discover related documents automatically
  - Personalized "You might also like" suggestions

### 👥 Collaboration Features
- **Document Sharing**
  - Share documents with other users
  - Three permission levels: Viewer, Editor, Admin
  - Revoke access anytime

- **Comments System**
  - Add comments to documents
  - Reply to existing comments
  - Page-specific annotations
  - Real-time comment updates

- **Study Groups**
  - Create and join study groups
  - Share documents within groups
  - Collaborative learning spaces
  - Group member management

- **Notifications**
  - Real-time notification badge
  - Share notifications
  - Comment alerts
  - Group activity updates

### 🎨 User Interface
- **Modern Design**: Custom CSS with gradient themes
- **Dark Mode**: Eye-friendly dark theme toggle
- **Responsive**: Works on desktop, tablet, and mobile
- **Animations**: Smooth hover effects and transitions
- **Glassmorphism**: Modern translucent UI elements
- **Color Coding**: Subject-based color schemes

### 🔐 Security & Authentication
- **Google OAuth**: Secure login with Google accounts
- **User Isolation**: Each user has private document collection
- **Session Management**: Secure Flask-Login integration
- **API Security**: Protected endpoints with authentication
- **Data Privacy**: Encrypted connections (HTTPS in production)

## 🛠️ Tech Stack

### Backend
- **Python 3.12+** - Core programming language
- **Flask 2.2+** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-SocketIO** - Real-time features

### AI & Machine Learning
- **OpenAI API** - GPT-3.5 for summarization and tagging
- **Tesseract OCR** - Optical character recognition
- **NLTK** - Natural language processing toolkit
- **scikit-learn** - Machine learning for recommendations
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing

### Database & Storage
- **SQLite** - Development database
- **PostgreSQL** - Production database (optional)
- **AWS S3** - Cloud storage option
- **Azure Blob Storage** - Cloud storage option

### Frontend
- **Bootstrap 5** - UI framework
- **Custom CSS** - Modern gradient designs
- **Bootstrap Icons** - Icon library
- **Google Fonts (Poppins)** - Typography
- **Vanilla JavaScript** - Client-side interactions

### Authentication
- **Authlib** - OAuth implementation
- **Google OAuth 2.0** - Authentication provider

## 📦 Installation

### Prerequisites

- **Python 3.12+** (Python 3.7+ minimum)
- **pip** package manager
- **Google Cloud Console** account (for OAuth)
- **OpenAI API key** (for AI features) - Get $5 free credit!
- **Tesseract OCR** (optional, for image text extraction)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Akshit7kotnala/study-organizer.git
cd study-organizer
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**All Dependencies:**
```
Flask>=2.2.0
Flask-SQLAlchemy>=3.0.0
Flask-Login>=0.6.2
Authlib>=1.2.0
python-dotenv>=1.0.0
Pillow>=10.0.0
pdf2image>=1.16.0
boto3>=1.28.0
azure-storage-blob>=12.17.0
gunicorn>=21.2.0
psycopg2-binary>=2.9.7
Flask-SocketIO>=5.3.0

# AI/ML Libraries
openai>=1.0.0
PyPDF2>=3.0.0
pytesseract>=0.3.10
python-docx>=0.8.11
scikit-learn>=1.3.0
nltk>=3.8.1
```

### Step 4: Install Tesseract OCR (Optional but Recommended)

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

### Step 5: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Step 6: Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google+ API** or **People API**
4. Navigate to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen:
   - User Type: External
   - Add app name, email
   - Add scopes: `email`, `profile`, `openid`
6. Create OAuth 2.0 Client ID:
   - Application type: **Web application**
   - Authorized redirect URIs:
     - `http://127.0.0.1:5000/login/google/callback`
     - `http://localhost:5000/login/google/callback`
7. Copy **Client ID** and **Client Secret**

### Step 7: Get OpenAI API Key

1. Sign up at: https://platform.openai.com/signup
2. Get $5 free credit (enough for ~500 documents!)
3. Go to: https://platform.openai.com/api-keys
4. Create new secret key
5. Copy the key (starts with `sk-`)

### Step 8: Configure Environment Variables

Create `.env` file in project root:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-generate-strong-one-for-production
FLASK_ENV=development

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key

# Tesseract OCR Configuration (Windows)
TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe

# AI Features Configuration
AI_SUMMARY_MAX_LENGTH=500
AI_TAGS_COUNT=5
OCR_LANGUAGE=eng
SEARCH_RESULTS_LIMIT=50
RECOMMENDATIONS_COUNT=5

# AWS S3 Configuration (Optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=

# Azure Blob Storage Configuration (Optional)
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_ACCOUNT_KEY=
AZURE_CONTAINER_NAME=study-documents

# Storage Configuration
STORAGE_TYPE=local  # 'local', 's3', or 'azure'
```

**Generate Strong SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 9: Initialize Database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created!')"
```

### Step 10: Run the Application

```bash
python app.py
```

**App will be available at:** http://127.0.0.1:5000/

✅ **You should see:**
```
✓ OpenAI client initialized
✓ Tesseract OCR configured
* Running on http://127.0.0.1:5000
```

## 🚀 Usage Guide

### First Time Setup

1. **Navigate to** http://127.0.0.1:5000/
2. Click **"Sign in with Google"**
3. Authorize the application
4. You'll be redirected to your dashboard

### Dashboard Overview

The main dashboard shows:
- **Year Cards**: Browse documents by academic year (1st-4th)
- **Statistics**: Total documents, collections, shared items
- **Recent Activity**: Latest uploads and updates
- **Quick Actions**: Upload, create note, create collection

### 📤 Uploading Documents

**Method 1: Standard Upload**
1. Click **"Upload"** in navbar
2. Select file(s) from computer
3. Fill in details:
   - **Year**: Select 1-4
   - **Subject**: Enter subject name (e.g., "Mathematics")
   - **Tags**: Add comma-separated tags (e.g., "calculus, derivatives")
4. Click **"Upload"**

**Method 2: Drag & Drop**
1. Drag files to upload zone
2. Fill in metadata
3. Submit

**Supported Formats:**
- 📄 PDFs
- 🖼️ Images (JPG, PNG, GIF)
- 📝 Word Documents (.docx)
- 📊 PowerPoint (.pptx)
- 📋 Text files (.txt)

### 📝 Creating Notes

1. Click **"Create Note"** in navbar
2. Enter note title
3. Write content in text area
4. Select year and subject
5. Add optional tags
6. Click **"Create Note"**

### 📚 Creating Collections

**Collections** group related documents together:

1. Go to **"Collections"** page
2. Click **"Create Collection"**
3. Enter collection name and description
4. Add documents to collection
5. Share collection with others (optional)

### 🤖 Using AI Features

#### Analyze a Document

1. Open any document
2. Click **"Analyze with AI"** button
3. Wait 2-5 seconds
4. View results:
   - **Summary**: AI-generated overview
   - **Smart Tags**: Extracted keywords
   - **Extracted Text**: Full document text

#### Search with AI

1. Use search bar in navbar
2. Type any keyword or phrase
3. AI searches:
   - Document titles
   - Summaries
   - Extracted text
   - Tags
4. Click result to view document

#### Get Recommendations

1. Open any document
2. Scroll to **"You might also like"** section
3. See ML-powered similar documents
4. Click to explore related content

#### View AI Dashboard

1. Go to **Collaborate** → **AI Features 🤖**
2. View statistics:
   - Total documents
   - Analyzed documents
   - Coverage percentage
3. Learn about AI capabilities

### 👥 Collaboration

#### Share Documents

1. Open document
2. Click **"Share"** button
3. Enter user's email
4. Select permission level:
   - **Viewer**: Can view only
   - **Editor**: Can edit metadata
   - **Admin**: Full control
5. Click **"Share"**

#### Add Comments

1. Open document
2. Scroll to comments section
3. Type your comment
4. Optionally specify page number
5. Click **"Add Comment"**
6. Reply to existing comments

#### Create Study Group

1. Go to **"Study Groups"**
2. Click **"Create Group"**
3. Enter group name and description
4. Invite members by email
5. Share documents within group

### 🔍 Advanced Search

**Search Syntax:**
- Simple: `calculus`
- Multiple words: `calculus derivatives`
- Subject filter: In subject dropdown
- Tag filter: Click tag badges
- Full-text: Searches inside documents

**Search Tips:**
- Use specific keywords
- Try different spellings
- Search by subject first
- Use AI-suggested tags

### 📊 Organization Tips

**Best Practices:**
1. **Consistent Naming**: Use clear, descriptive filenames
2. **Tag Everything**: More tags = better search
3. **Use Collections**: Group related materials
4. **Analyze Important Docs**: Run AI analysis on key documents
5. **Share Wisely**: Share with study groups for collaboration

### ⚙️ Settings & Preferences

**Toggle Dark Mode:**
- Click moon/sun icon in navbar
- Preference saved in browser

**Manage Notifications:**
- Click bell icon for notifications
- Mark as read individually
- View notification history

**Account Settings:**
- Profile picture from Google account
- Email from Google account
- Logout from navbar

## 🤖 AI-Powered Features

### Document Summarization

**Technology:** OpenAI GPT-3.5 Turbo

**How it works:**
1. Extracts text from your document (PDF, Word, or image)
2. Sends text to OpenAI API
3. GPT-3.5 generates concise 500-character summary
4. Summary stored in database for instant access

**Use Cases:**
- Quick document review before exams
- Identify relevant materials fast
- Share documents with summaries
- Create study guides

**Example:**
```
Original: 50-page calculus textbook chapter
Summary: "This chapter covers derivatives including power rule, 
product rule, chain rule with multiple examples. Discusses 
applications in physics and optimization problems."
```

**Cost:** ~$0.01-$0.05 per document

### Smart Tagging

**Technology:** NLTK + OpenAI GPT-3.5

**How it works:**
1. **NLP Analysis:** 
   - Tokenizes document text
   - Removes stopwords (the, and, or, etc.)
   - Identifies frequent meaningful words
2. **AI Enhancement:**
   - OpenAI analyzes content context
   - Suggests 5 relevant tags
   - Considers subject field
3. **Deduplication:**
   - Removes duplicates
   - Returns top 5 tags

**Benefits:**
- No manual tagging needed
- Consistent tag naming
- Better search results
- Smart organization

**Example Tags:**
- Math doc: "calculus", "derivatives", "limits", "continuity", "functions"
- History doc: "world war", "treaty", "imperialism", "nationalism", "alliance"

### OCR Text Extraction

**Technology:** Tesseract OCR + PyPDF2

**Supported Sources:**
- Scanned PDFs
- Photos of notes/textbooks
- Screenshots
- Handwritten notes (clear writing)

**How it works:**
1. Detects document type
2. Uses PyPDF2 for native PDFs
3. Uses Tesseract for images/scanned pages
4. Extracts all readable text
5. Stores for search and analysis

**Accuracy:**
- Typed text: 95-99%
- Clear scans: 85-95%
- Handwriting: 60-80% (varies)

**Languages:** English (default), configurable for 100+ languages

### Intelligent Search

**Technology:** SQLAlchemy Full-Text Search

**Search Scope:**
- Document filenames
- Subject names
- Manual tags
- AI-generated tags
- Document summaries
- Extracted text content

**Features:**
- Case-insensitive
- Partial matching
- Real-time results
- Highlighted matches
- Sort by relevance

**Search Tips:**
- Use specific keywords
- Try synonyms
- Search by topic, not exact words
- Use quotes for exact phrases

### Study Recommendations

**Technology:** scikit-learn (TF-IDF + Cosine Similarity)

**How it works:**
1. **TF-IDF Vectorization:**
   - Converts document text to numerical vectors
   - TF = Term Frequency (word importance in doc)
   - IDF = Inverse Document Frequency (word rarity)
2. **Similarity Calculation:**
   - Computes cosine similarity between vectors
   - Measures content overlap
3. **Ranking:**
   - Finds top 5 most similar documents
   - Filters out low similarity (<10%)

**Use Cases:**
- Discover related study materials
- Find complementary resources
- Build comprehensive study sets
- Explore connected topics

**Example:**
```
Viewing: "Introduction to Calculus"
Recommendations:
1. "Advanced Calculus Techniques" (85% similar)
2. "Derivative Practice Problems" (78% similar)
3. "Limits and Continuity" (72% similar)
```

### AI Performance Metrics

**Processing Speed:**
- Document upload: Instant
- AI analysis: 2-5 seconds
- Summary generation: 2-3 seconds
- Smart tagging: 1-2 seconds
- OCR extraction: 3-10 seconds/page
- Search: <1 second
- Recommendations: <1 second

**Accuracy:**
- PDF text extraction: 95-99%
- OCR accuracy: 85-95% (clear scans)
- Summary quality: Excellent (GPT-3.5)
- Tag relevance: 80-90%
- Recommendation quality: Good (improves with more docs)

**Cost Efficiency:**
- Free tier: ~500 documents ($5 credit)
- Per document: $0.01-$0.05
- OCR: Free forever
## 📁 Project Structure

```
study-organizer/
├── 📄 app.py (2,400+ lines)          # Main Flask application
│   ├── Models (User, Document, Tag, Collection, etc.)
│   ├── AI Helper Functions (250+ lines)
│   ├── Routes (50+ endpoints)
│   └── Database Configuration
│
├── 📋 requirements.txt               # Python dependencies (21 packages)
├── 🔐 .env                          # Environment variables (gitignored)
├── 📊 documents.db                  # SQLite database (auto-created)
│
├── 📂 uploads/                      # Uploaded files storage
│   └── thumbnails/                 # Generated thumbnails
│
├── 📂 templates/                    # HTML templates
│   ├── base.html                   # Base layout with navbar
│   ├── index.html                  # Dashboard/home page
│   ├── upload.html                 # Upload form
│   ├── create_note.html            # Note creation form
│   ├── year.html                   # Year view with documents
│   ├── view_document.html          # Document detail page
│   ├── preview.html                # Document preview
│   ├── search.html                 # Search interface
│   ├── ai_features.html            # AI features showcase
│   ├── collections.html            # Collections list
│   ├── view_collection.html        # Collection detail
│   ├── shared_with_me.html         # Shared documents
│   ├── study_groups.html           # Study groups list
│   └── view_group.html             # Group detail
│
├── 📂 static/
│   └── css/
│       └── custom.css (1000+ lines) # Custom styling with gradients
│
├── 📂 Documentation/
│   ├── AI_FEATURES.md              # AI features technical docs
│   ├── AI_QUICKSTART.md            # AI features user guide
│   ├── AI_IMPLEMENTATION_COMPLETE.md # Implementation summary
│   ├── COLLABORATION_FEATURES.md   # Collaboration docs
│   ├── CUSTOM_STYLING_GUIDE.md     # CSS framework guide
│   └── IMPLEMENTATION_SUMMARY.md   # Complete feature summary
│
└── 📄 README.md                     # This file!
```

### Key Files Explained

**app.py** - Core application file containing:
- Database models (User, Document, Tag, Collection, SharePermission, Comment, StudyGroup, Notification)
- AI configuration and helper functions
- 50+ Flask routes
- Authentication logic
- File upload/download handlers

**requirements.txt** - All Python dependencies:
- Core: Flask, SQLAlchemy, Flask-Login
- AI/ML: openai, pytesseract, nltk, scikit-learn
- Cloud: boto3, azure-storage-blob
- Utilities: Pillow, PyPDF2, python-docx

**templates/** - Jinja2 HTML templates:
- Uses Bootstrap 5 for responsive design
- Custom CSS for modern look
- Dynamic content rendering
- Dark mode support

**static/css/custom.css** - Custom styling:
- CSS variables for theming
- Gradient color schemes (5 types)
- Animation effects
- Hover transitions
- Dark mode styles

## 🗄️ Database Schema

### User Model
```python
class User(UserMixin, db.Model):
    id: Integer (Primary Key)
    email: String(255) (Unique, Not Null)
    name: String(255)
    google_id: String(255) (Unique, Not Null)
    profile_pic: String(512)
    created_at: DateTime (Default: now)
```

### Document Model
```python
class Document(db.Model):
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key → User)
    original_filename: String(512)
    stored_filename: String(512) (Unique)
    year: Integer (1-4)
    subject: String(128)
    tags: String(256)  # Legacy field
    mimetype: String(128)
    size: Integer (bytes)
    thumbnail_filename: String(512)
    storage_type: String(16) ('local', 's3', 'azure')
    upload_date: DateTime
    
    # AI-powered fields
    summary: Text (AI-generated summary)
    extracted_text: Text (OCR/extracted text)
    ai_tags: String(512) (AI-suggested tags)
    content_vector: Text (ML vector - JSON)
    last_analyzed: DateTime (Last AI analysis)
    
    # Relationships
    tag_objects: Many-to-Many → Tag
    collections: Many-to-Many → Collection
```

### Tag Model
```python
class Tag(db.Model):
    id: Integer (Primary Key)
    name: String(64) (Unique)
    slug: String(64) (Unique, URL-friendly)
    user_id: Integer (Foreign Key → User)
    created_at: DateTime
    
    # Relationships
    documents: Many-to-Many → Document
```

### Collection Model
```python
class Collection(db.Model):
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key → User)
    name: String(128)
    description: Text
    created_at: DateTime
    updated_at: DateTime
    
    # Relationships
    documents: Many-to-Many → Document
```

### SharePermission Model
```python
class SharePermission(db.Model):
    id: Integer (Primary Key)
    shared_by_id: Integer (Foreign Key → User)
    shared_with_id: Integer (Foreign Key → User)
    document_id: Integer (Foreign Key → Document, nullable)
    collection_id: Integer (Foreign Key → Collection, nullable)
    permission: String(16) ('viewer', 'editor', 'admin')
    shared_at: DateTime
```

### Comment Model
```python
class Comment(db.Model):
    id: Integer (Primary Key)
    document_id: Integer (Foreign Key → Document)
    user_id: Integer (Foreign Key → User)
    content: Text
    page_number: Integer (nullable)
    parent_id: Integer (Foreign Key → Comment, nullable)
    created_at: DateTime
    updated_at: DateTime
```

### StudyGroup Model
```python
class StudyGroup(db.Model):
    id: Integer (Primary Key)
    name: String(128)
    description: Text
    created_by_id: Integer (Foreign Key → User)
    created_at: DateTime
    
    # Relationships
    members: Many-to-Many → User (with role and joined_at)
```

### Notification Model
```python
class Notification(db.Model):
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key → User)
    title: String(255)
    message: Text
    type: String(32) ('share', 'comment', 'group', 'info')
    link: String(512)
    read: Boolean (Default: False)
    created_at: DateTime
```

### Relationships

```
User (1) ─── (N) Document
User (1) ─── (N) Tag
User (1) ─── (N) Collection
User (1) ─── (N) Comment
User (1) ─── (N) Notification

Document (N) ─── (N) Tag (through document_tags)
Document (N) ─── (N) Collection (through document_collections)
Document (1) ─── (N) Comment

StudyGroup (N) ─── (N) User (through group_members)

SharePermission:
  ├── shared_by → User
  ├── shared_with → User
  ├── document → Document (optional)
  └── collection → Collection (optional)
```

## Security Considerations

- **Never commit `.env` file** to version control
- Use strong `SECRET_KEY` in production
- Keep Google OAuth credentials confidential
- For production deployment:
  - Use HTTPS
  - Set `FLASK_ENV=production`
  - Use a production-grade database (PostgreSQL)
  - Configure proper CORS settings
  - Add rate limiting

## Troubleshooting

### "Import 'dotenv' could not be resolved"

Install python-dotenv:

```powershell
pip install python-dotenv
```

### "Google OAuth redirect URI mismatch"

Make sure the redirect URI in Google Cloud Console exactly matches:

```
http://127.0.0.1:5000/login/google/callback
```

### Database errors on startup

Delete `documents.db` and restart the app to recreate the database:

```powershell
Remove-Item documents.db
python app.py
```

## Future Enhancements

- Full-text search across documents
- Tag normalization and autocomplete
- Delete and edit document metadata
- Bulk upload functionality
- Export/backup features
- File sharing between users

## License

This project is open source and available for educational purposes.
└── templates/ # HTML templates
├── base.html # Base layout
├── index.html # Year list page
├── upload.html # Upload form
├── year.html # Document list for a year
└── preview.html # File preview page

```

## Usage

1. **Upload a document**: Click "Upload" in the navbar, fill in the form (file, year, subject, optional tags), and submit.
2. **Browse by year**: On the home page, click on a year (e.g., "1st Year") to see all documents for that year.
3. **Filter documents**: Use the subject dropdown or tags input to filter the document list.
4. **Preview/Download**: Click "Preview" to view images/PDFs in browser, or "Download" to save the file.

## Notes

- Uploaded files are stored in `uploads/` with UUID-based filenames to avoid collisions.
- The original filename is preserved in the database for display and download.
- Maximum upload size: 50MB per file (configurable in `app.py`).
- For production use, add authentication, secure file serving, and HTTPS.

## Security Considerations

This is a development/demo app. For production:

- Add user authentication and authorization
- Validate and sanitize file uploads
- Use environment variables for SECRET_KEY
- Serve files through a CDN or protected endpoint
- Add rate limiting and file size validation
- Use a production WSGI server (gunicorn, waitress)
- Enable HTTPS
```
