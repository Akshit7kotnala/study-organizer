# Study Organiser

A modern web application built with Flask that helps students organize their study materials by year, subject, and tags. Features include document upload, note creation, preview capabilities, and Google OAuth authentication.

## Features

- 📁 **Document Management**: Upload PDFs, images, Word docs, PowerPoint, and more
- 📝 **Note Creation**: Create text notes directly in the app without uploading files
- 🎯 **Organization**: Organize materials by academic year, subject, and custom tags
- 👁️ **Preview**: Preview PDFs, images, and text files directly in the browser
- 🔐 **Authentication**: Secure Google OAuth login
- 🎨 **Modern UI**: Beautiful purple gradient design with glassmorphism effects
- 📱 **Responsive**: Works seamlessly on desktop and mobile devices
- 👤 **Multi-User**: Each user has their own private document collection

## Tech Stack

- **Backend**: Python 3.7+, Flask 2.2+
- **Database**: SQLite with Flask-SQLAlchemy
- **Authentication**: Flask-Login, Authlib (Google OAuth)
- **Frontend**: Bootstrap 5, Google Fonts (Poppins), Bootstrap Icons
- **Testing**: pytest

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager
- Google Cloud Console account (for OAuth credentials)

### Step 1: Create a Virtual Environment (Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google+ API** (or **People API**)
4. Navigate to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure the OAuth consent screen if prompted
6. Choose **Web application** as application type
7. Add authorized redirect URI: `http://127.0.0.1:5000/login/google/callback`
8. Copy the **Client ID** and **Client Secret**

### Step 4: Configure Environment Variables

1. Copy the example environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your Google OAuth credentials:

   ```
   SECRET_KEY=your-secret-key-here-change-this-in-production
   FLASK_ENV=development
   GOOGLE_CLIENT_ID=your-google-client-id-here.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-google-client-secret-here
   ```

3. **IMPORTANT**: Generate a strong `SECRET_KEY` for production:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Step 5: Initialize the Database

```powershell
python app.py
```

The database will be created automatically on first run.

## Usage

### Running the Application

```powershell
python app.py
```

The app will be available at: `http://127.0.0.1:5000/`

### First Time Setup

1. Navigate to `http://127.0.0.1:5000/`
2. Click **"Sign in with Google"**
3. Authorize the application
4. You'll be redirected to the dashboard

### Uploading Documents

1. Click **"Upload"** in the navigation bar
2. Select a file from your computer
3. Choose the academic year (1, 2, 3, 4)
4. Enter the subject name
5. Optionally add comma-separated tags
6. Click **"Upload"**

### Creating Notes

1. Click **"Create Note"** in the navigation bar
2. Enter a title for your note
3. Write your content in the text area
4. Choose year, subject, and tags
5. Click **"Create Note"**

## Running Tests

```powershell
pytest test_app.py -v
```

## Project Structure

```
Study organiser/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example           # Example environment variables
├── documents.db           # SQLite database (created on first run)
├── uploads/               # Uploaded files directory (created on first run)
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar and styling
│   ├── login.html        # Login page
│   ├── index.html        # Home page with year cards
│   ├── upload.html       # Upload form
│   ├── create_note.html  # Note creation form
│   ├── year.html         # Year view with documents
│   └── preview.html      # Document preview page
└── test_app.py           # Unit tests
```

## Database Schema

### User Model

- `id`: Primary key
- `email`: User's email (from Google)
- `name`: User's full name
- `google_id`: Google account identifier (unique)
- `profile_pic`: Profile picture URL
- `created_at`: Account creation timestamp

### Document Model

- `id`: Primary key
- `original_filename`: Original uploaded filename
- `stored_filename`: Unique filename on server
- `year`: Academic year (1-4)
- `subject`: Subject name
- `tags`: Comma-separated tags
- `mimetype`: File MIME type
- `size`: File size in bytes
- `upload_date`: Upload timestamp
- `user_id`: Foreign key to User

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
