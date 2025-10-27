"""
Setup script for Study Organiser
This script helps you generate a .env file with a secure SECRET_KEY
"""

import secrets
import os

print("=" * 60)
print("Study Organiser - Environment Setup")
print("=" * 60)
print()

# Check if .env already exists
if os.path.exists('.env'):
    response = input(".env file already exists. Overwrite? (y/n): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        exit(0)

# Generate secure secret key
secret_key = secrets.token_hex(32)

print("Generating secure SECRET_KEY...")
print()

# Get Google OAuth credentials
print("You need to set up Google OAuth credentials.")
print("Follow these steps:")
print()
print("1. Go to: https://console.cloud.google.com/")
print("2. Create a new project")
print("3. Enable Google+ API")
print("4. Create OAuth 2.0 Client ID")
print("5. Add redirect URI: http://127.0.0.1:5000/login/google/callback")
print()

google_client_id = input("Enter your GOOGLE_CLIENT_ID: ").strip()
google_client_secret = input("Enter your GOOGLE_CLIENT_SECRET: ").strip()

if not google_client_id or not google_client_secret:
    print()
    print("ERROR: Both Client ID and Client Secret are required.")
    print("Creating .env with placeholders...")
    google_client_id = "your-google-client-id-here.apps.googleusercontent.com"
    google_client_secret = "your-google-client-secret-here"

# Create .env file
env_content = f"""# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development

# Google OAuth Configuration
# Get these from: https://console.cloud.google.com/
GOOGLE_CLIENT_ID={google_client_id}
GOOGLE_CLIENT_SECRET={google_client_secret}
"""

with open('.env', 'w') as f:
    f.write(env_content)

print()
print("=" * 60)
print("✅ .env file created successfully!")
print("=" * 60)
print()

if "your-google-client" in google_client_id:
    print("⚠️  WARNING: You still need to add real Google OAuth credentials!")
    print("   Edit the .env file and replace the placeholder values.")
    print()
else:
    print("✅ Google OAuth credentials configured!")
    print()

print("Next steps:")
print("1. If needed, edit .env to add/update Google credentials")
print("2. Delete old database: Remove-Item documents.db")
print("3. Run the app: python app.py")
print("4. Open browser: http://127.0.0.1:5000/")
print()
print("=" * 60)
