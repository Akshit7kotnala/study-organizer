import os
from datetime import datetime
from uuid import uuid4

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    flash,
    session,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from PIL import Image
from pdf2image import convert_from_path
import boto3
from botocore.exceptions import ClientError
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import AzureError
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me-in-production')

# Database configuration - use PostgreSQL in production, SQLite in development
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Fix for Render.com PostgreSQL URL format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Development - use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'documents.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Google OAuth config - get these from Google Cloud Console
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', '')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', '')

# AWS S3 Configuration
app.config['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID', '')
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
app.config['AWS_REGION'] = os.environ.get('AWS_REGION', 'us-east-1')
app.config['S3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAME', '')

# Azure Blob Storage Configuration
app.config['AZURE_STORAGE_ACCOUNT_NAME'] = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME', '')
app.config['AZURE_STORAGE_ACCOUNT_KEY'] = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY', '')
app.config['AZURE_CONTAINER_NAME'] = os.environ.get('AZURE_CONTAINER_NAME', 'study-documents')

# Storage Configuration: 'local', 's3', or 'azure'
app.config['STORAGE_TYPE'] = os.environ.get('STORAGE_TYPE', 'local')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize S3 client if using S3 storage
s3_client = None
if app.config['STORAGE_TYPE'] == 's3' and app.config['AWS_ACCESS_KEY_ID']:
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=app.config['AWS_REGION']
        )
        print(f"✓ S3 client initialized for bucket: {app.config['S3_BUCKET_NAME']}")
    except Exception as e:
        print(f"✗ Failed to initialize S3 client: {e}")
        print("  Falling back to local storage")
        app.config['STORAGE_TYPE'] = 'local'

# Initialize Azure Blob Service Client if using Azure storage
blob_service_client = None
if app.config['STORAGE_TYPE'] == 'azure' and app.config['AZURE_STORAGE_ACCOUNT_NAME']:
    try:
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={app.config['AZURE_STORAGE_ACCOUNT_NAME']};AccountKey={app.config['AZURE_STORAGE_ACCOUNT_KEY']};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Create container if it doesn't exist
        container_client = blob_service_client.get_container_client(app.config['AZURE_CONTAINER_NAME'])
        try:
            container_client.create_container()
            print(f"✓ Created Azure container: {app.config['AZURE_CONTAINER_NAME']}")
        except:
            pass  # Container already exists
        
        print(f"✓ Azure Blob Storage initialized for account: {app.config['AZURE_STORAGE_ACCOUNT_NAME']}")
    except Exception as e:
        print(f"✗ Failed to initialize Azure Blob Storage: {e}")
        print("  Falling back to local storage")
        app.config['STORAGE_TYPE'] = 'local'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


# Models
# Association table for many-to-many relationship between Document and Tag
document_tags = db.Table('document_tags',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# Association table for many-to-many relationship between Document and Collection
document_collections = db.Table('document_collections',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    profile_pic = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    documents = db.relationship('Document', backref='owner', lazy=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    documents = db.relationship('Document', secondary=document_tags, back_populates='tag_objects')
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    @staticmethod
    def slugify(text):
        """Convert tag name to URL-friendly slug."""
        return text.lower().strip().replace(' ', '-').replace('_', '-')


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    color = db.Column(db.String(7), default='#667eea')  # Hex color for visual distinction
    icon = db.Column(db.String(32), default='bi-folder')  # Bootstrap icon class
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-many relationship with Document
    documents = db.relationship('Document', secondary=document_collections, backref='collections', lazy='dynamic')
    
    def __repr__(self):
        return f'<Collection {self.name}>'
    
    def document_count(self):
        """Return the number of documents in this collection."""
        return self.documents.count()


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    original_filename = db.Column(db.String(512), nullable=False)
    stored_filename = db.Column(db.String(512), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    tags = db.Column(db.String(256), nullable=True)  # Keep for backward compatibility
    mimetype = db.Column(db.String(128), nullable=True)
    size = db.Column(db.Integer, nullable=True)
    thumbnail_filename = db.Column(db.String(512), nullable=True)  # Thumbnail image
    storage_type = db.Column(db.String(16), default='local', nullable=False)  # 'local' or 's3'
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with Tag
    tag_objects = db.relationship('Tag', secondary=document_tags, back_populates='documents')

    def tag_list(self):
        """Return list of tag names (from tag_objects relationship)."""
        if self.tag_objects:
            return [tag.name for tag in self.tag_objects]
        # Fallback to old tags field if no tag_objects
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
    
    def get_tags(self):
        """Return list of tag objects with name and slug."""
        if self.tag_objects:
            return [{'name': tag.name, 'slug': tag.slug} for tag in self.tag_objects]
        # Fallback for old comma-separated tags
        if not self.tags:
            return []
        return [{'name': t.strip(), 'slug': Tag.slugify(t.strip())} for t in self.tags.split(',') if t.strip()]
    
    def set_tags_from_string(self, tags_string):
        """Parse comma-separated tags and create/associate Tag objects."""
        if not tags_string or not tags_string.strip():
            self.tag_objects = []
            return
        
        tag_names = [t.strip().lower() for t in tags_string.split(',') if t.strip()]
        self.tag_objects = []
        
        for tag_name in tag_names:
            # Check if tag exists
            tag = Tag.query.filter_by(slug=Tag.slugify(tag_name)).first()
            if not tag:
                # Create new tag
                tag = Tag(name=tag_name, slug=Tag.slugify(tag_name))
                db.session.add(tag)
            self.tag_objects.append(tag)
    
    def format_size(self):
        """Return human-readable file size."""
        if not self.size:
            return 'Unknown'
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.size < 1024.0:
                return f"{self.size:.1f} {unit}"
            self.size /= 1024.0
        return f"{self.size:.1f} TB"
    
    def file_icon(self):
        """Return Bootstrap icon class based on file type."""
        ext = os.path.splitext(self.original_filename)[1].lower()
        icon_map = {
            '.pdf': 'bi-file-earmark-pdf-fill text-danger',
            '.doc': 'bi-file-earmark-word-fill text-primary',
            '.docx': 'bi-file-earmark-word-fill text-primary',
            '.xls': 'bi-file-earmark-excel-fill text-success',
            '.xlsx': 'bi-file-earmark-excel-fill text-success',
            '.ppt': 'bi-file-earmark-ppt-fill text-warning',
            '.pptx': 'bi-file-earmark-ppt-fill text-warning',
            '.jpg': 'bi-file-earmark-image-fill text-info',
            '.jpeg': 'bi-file-earmark-image-fill text-info',
            '.png': 'bi-file-earmark-image-fill text-info',
            '.gif': 'bi-file-earmark-image-fill text-info',
            '.zip': 'bi-file-earmark-zip-fill text-secondary',
            '.txt': 'bi-file-earmark-text-fill',
        }
        return icon_map.get(ext, 'bi-file-earmark-fill')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename: str) -> bool:
    # allow common document/image types; be permissive
    return '.' in filename


def human_year_label(y: int) -> str:
    mapping = {1: '1st Year', 2: '2nd Year', 3: '3rd Year', 4: '4th Year'}
    return mapping.get(y, f'{y} Year')


def get_subject_color_class(subject: str) -> str:
    """Get the color class for a subject."""
    subject_lower = subject.lower()
    
    color_mapping = {
        'math': 'math',
        'mathematics': 'math',
        'science': 'science',
        'english': 'english',
        'history': 'history',
        'physics': 'physics',
        'chemistry': 'chemistry',
        'biology': 'biology',
        'geography': 'geography',
        'computer': 'computer',
        'cs': 'computer',
        'programming': 'computer',
    }
    
    for key, value in color_mapping.items():
        if key in subject_lower:
            return value
    
    return 'default'


def generate_thumbnail(file_path: str, mimetype: str) -> str:
    """
    Generate a thumbnail for an uploaded file (image or PDF).
    Returns the thumbnail filename or None if generation fails.
    """
    try:
        thumbnail_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)
        
        # Generate thumbnail filename
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        thumbnail_filename = f'thumb_{name}.jpg'
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_filename)
        
        # Check if it's an image
        if mimetype.startswith('image/'):
            # Open and resize the image
            img = Image.open(file_path)
            # Convert RGBA to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create thumbnail (200x200 max, maintaining aspect ratio)
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=85)
            return thumbnail_filename
            
        # Check if it's a PDF
        elif mimetype == 'application/pdf':
            # Convert first page of PDF to image
            images = convert_from_path(file_path, first_page=1, last_page=1, dpi=100)
            if images:
                img = images[0]
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Create thumbnail
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                img.save(thumbnail_path, 'JPEG', quality=85)
                return thumbnail_filename
        
        return None
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None


# ============================================================================
# S3 Storage Helper Functions
# ============================================================================

def upload_to_s3(file_path: str, s3_key: str, mimetype: str = None) -> bool:
    """
    Upload a file to S3 bucket.
    Returns True if successful, False otherwise.
    """
    if not s3_client or app.config['STORAGE_TYPE'] != 's3':
        return False
    
    try:
        extra_args = {}
        if mimetype:
            extra_args['ContentType'] = mimetype
        
        with open(file_path, 'rb') as file_data:
            s3_client.upload_fileobj(
                file_data,
                app.config['S3_BUCKET_NAME'],
                s3_key,
                ExtraArgs=extra_args
            )
        print(f"✓ Uploaded to S3: {s3_key}")
        return True
    except ClientError as e:
        print(f"✗ S3 upload failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during S3 upload: {e}")
        return False


def download_from_s3(s3_key: str, local_path: str) -> bool:
    """
    Download a file from S3 to local filesystem.
    Returns True if successful, False otherwise.
    """
    if not s3_client:
        return False
    
    try:
        s3_client.download_file(
            app.config['S3_BUCKET_NAME'],
            s3_key,
            local_path
        )
        print(f"✓ Downloaded from S3: {s3_key}")
        return True
    except ClientError as e:
        print(f"✗ S3 download failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during S3 download: {e}")
        return False


def delete_from_s3(s3_key: str) -> bool:
    """
    Delete a file from S3 bucket.
    Returns True if successful, False otherwise.
    """
    if not s3_client:
        return False
    
    try:
        s3_client.delete_object(
            Bucket=app.config['S3_BUCKET_NAME'],
            Key=s3_key
        )
        print(f"✓ Deleted from S3: {s3_key}")
        return True
    except ClientError as e:
        print(f"✗ S3 deletion failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during S3 deletion: {e}")
        return False


def generate_presigned_url(s3_key: str, expiration: int = 3600, as_attachment: bool = False, download_name: str = None) -> str:
    """
    Generate a presigned URL for accessing an S3 object.
    Returns the URL string or None if failed.
    
    Args:
        s3_key: The S3 object key
        expiration: URL expiration time in seconds (default 1 hour)
        as_attachment: Whether to force download
        download_name: Custom filename for download
    """
    if not s3_client:
        return None
    
    try:
        params = {
            'Bucket': app.config['S3_BUCKET_NAME'],
            'Key': s3_key
        }
        
        # Add response headers for download
        if as_attachment or download_name:
            response_disposition = f'attachment; filename="{download_name}"' if download_name else 'attachment'
            params['ResponseContentDisposition'] = response_disposition
        
        url = s3_client.generate_presigned_url(
            'get_object',
            Params=params,
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        print(f"✗ Failed to generate presigned URL: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error generating presigned URL: {e}")
        return None


# ============================================================================
# Azure Blob Storage Helper Functions
# ============================================================================

def upload_to_azure(file_path: str, blob_name: str, mimetype: str = None) -> bool:
    """
    Upload a file to Azure Blob Storage.
    Returns True if successful, False otherwise.
    """
    if not blob_service_client or app.config['STORAGE_TYPE'] != 'azure':
        return False
    
    try:
        blob_client = blob_service_client.get_blob_client(
            container=app.config['AZURE_CONTAINER_NAME'],
            blob=blob_name
        )
        
        content_settings = None
        if mimetype:
            from azure.storage.blob import ContentSettings
            content_settings = ContentSettings(content_type=mimetype)
        
        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
        
        print(f"✓ Uploaded to Azure: {blob_name}")
        return True
    except AzureError as e:
        print(f"✗ Azure upload failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during Azure upload: {e}")
        return False


def download_from_azure(blob_name: str, local_path: str) -> bool:
    """
    Download a file from Azure Blob Storage to local filesystem.
    Returns True if successful, False otherwise.
    """
    if not blob_service_client:
        return False
    
    try:
        blob_client = blob_service_client.get_blob_client(
            container=app.config['AZURE_CONTAINER_NAME'],
            blob=blob_name
        )
        
        with open(local_path, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())
        
        print(f"✓ Downloaded from Azure: {blob_name}")
        return True
    except AzureError as e:
        print(f"✗ Azure download failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during Azure download: {e}")
        return False


def delete_from_azure(blob_name: str) -> bool:
    """
    Delete a file from Azure Blob Storage.
    Returns True if successful, False otherwise.
    """
    if not blob_service_client:
        return False
    
    try:
        blob_client = blob_service_client.get_blob_client(
            container=app.config['AZURE_CONTAINER_NAME'],
            blob=blob_name
        )
        blob_client.delete_blob()
        
        print(f"✓ Deleted from Azure: {blob_name}")
        return True
    except AzureError as e:
        print(f"✗ Azure deletion failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during Azure deletion: {e}")
        return False


def generate_azure_sas_url(blob_name: str, expiration: int = 3600, as_attachment: bool = False, download_name: str = None) -> str:
    """
    Generate a SAS (Shared Access Signature) URL for accessing an Azure blob.
    Returns the URL string or None if failed.
    
    Args:
        blob_name: The blob name
        expiration: URL expiration time in seconds (default 1 hour)
        as_attachment: Whether to force download
        download_name: Custom filename for download
    """
    if not blob_service_client:
        return None
    
    try:
        blob_client = blob_service_client.get_blob_client(
            container=app.config['AZURE_CONTAINER_NAME'],
            blob=blob_name
        )
        
        # Generate SAS token
        sas_token = generate_blob_sas(
            account_name=app.config['AZURE_STORAGE_ACCOUNT_NAME'],
            container_name=app.config['AZURE_CONTAINER_NAME'],
            blob_name=blob_name,
            account_key=app.config['AZURE_STORAGE_ACCOUNT_KEY'],
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(seconds=expiration)
        )
        
        # Construct URL
        url = f"{blob_client.url}?{sas_token}"
        
        # Add content disposition for downloads
        if as_attachment and download_name:
            url += f"&response-content-disposition=attachment; filename=\"{download_name}\""
        elif as_attachment:
            url += "&response-content-disposition=attachment"
        
        return url
    except AzureError as e:
        print(f"✗ Failed to generate Azure SAS URL: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error generating Azure SAS URL: {e}")
        return None


# Authentication routes
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login/google')
def login_google():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Failed to get user info from Google', 'danger')
            return redirect(url_for('login'))
        
        # Check if user exists
        user = User.query.filter_by(google_id=user_info['sub']).first()
        
        if not user:
            # Create new user
            user = User(
                email=user_info['email'],
                name=user_info.get('name'),
                google_id=user_info['sub'],
                profile_pic=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {user.name}! Your account has been created.', 'success')
        else:
            # Update existing user info
            user.name = user_info.get('name')
            user.profile_pic = user_info.get('picture')
            db.session.commit()
            flash(f'Welcome back, {user.name}!', 'success')
        
        login_user(user)
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Authentication failed: {str(e)}', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    years = [r[0] for r in db.session.query(Document.year).filter_by(user_id=current_user.id).distinct().order_by(Document.year).all()]
    years = sorted([y for y in years if y is not None])
    
    # Get total document count for current user
    total_docs = Document.query.filter_by(user_id=current_user.id).count()
    
    return render_template('index.html', years=years, human_year_label=human_year_label, total_docs=total_docs)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        year = request.form.get('year')
        subject = request.form.get('subject')
        tags = request.form.get('tags')

        if not file or file.filename == '':
            flash('No file selected', 'warning')
            return redirect(request.url)

        try:
            year_int = int(year)
        except Exception:
            flash('Year must be a number (e.g., 1, 2, 3, 4)', 'warning')
            return redirect(request.url)

        if not subject:
            flash('Subject is required', 'warning')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            orig = secure_filename(file.filename)
            ext = os.path.splitext(orig)[1]
            stored = f"{uuid4().hex}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], stored)
            file.save(save_path)

            # Get file size
            file_size = os.path.getsize(save_path)
            
            # Generate thumbnail for images and PDFs
            thumbnail = generate_thumbnail(save_path, file.mimetype)
            
            # Upload to cloud storage if configured
            storage_type = app.config['STORAGE_TYPE']
            
            if storage_type == 's3':
                # Upload thumbnail to S3
                if thumbnail:
                    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                    s3_thumbnail_key = f"thumbnails/{thumbnail}"
                    upload_to_s3(thumbnail_path, s3_thumbnail_key, 'image/jpeg')
                
                # Upload main file to S3
                s3_key = f"documents/{stored}"
                success = upload_to_s3(save_path, s3_key, file.mimetype)
                if success:
                    # Remove local file after successful S3 upload
                    os.remove(save_path)
                    if thumbnail:
                        # Also remove local thumbnail
                        thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                        if os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                else:
                    flash('Failed to upload to cloud storage', 'danger')
                    storage_type = 'local'  # Fall back to local
                    
            elif storage_type == 'azure':
                # Upload thumbnail to Azure
                if thumbnail:
                    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                    azure_thumbnail_blob = f"thumbnails/{thumbnail}"
                    upload_to_azure(thumbnail_path, azure_thumbnail_blob, 'image/jpeg')
                
                # Upload main file to Azure
                azure_blob_name = f"documents/{stored}"
                success = upload_to_azure(save_path, azure_blob_name, file.mimetype)
                if success:
                    # Remove local file after successful Azure upload
                    os.remove(save_path)
                    if thumbnail:
                        # Also remove local thumbnail
                        thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                        if os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                else:
                    flash('Failed to upload to cloud storage', 'danger')
                    storage_type = 'local'  # Fall back to local

            doc = Document(
                original_filename=orig,
                stored_filename=stored,
                year=year_int,
                subject=subject,
                mimetype=file.mimetype,
                size=file_size,
                thumbnail_filename=thumbnail,
                storage_type=storage_type,
                user_id=current_user.id
            )
            # Set tags using the new tag system
            doc.set_tags_from_string(tags)
            db.session.add(doc)
            db.session.commit()
            flash('File uploaded successfully', 'success')
            return redirect(url_for('year_view', year=year_int))

    # GET -> show form
    return render_template('upload.html')


@app.route('/upload-multiple', methods=['POST'])
@login_required
def upload_multiple():
    """Handle multiple file uploads via AJAX and return JSON response."""
    files = request.files.getlist('files[]')
    year = request.form.get('year')
    subject = request.form.get('subject')
    tags = request.form.get('tags')
    
    # Validation
    if not files or len(files) == 0:
        return jsonify({'success': False, 'error': 'No files selected'}), 400
    
    try:
        year_int = int(year)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid year value'}), 400
    
    if not subject:
        return jsonify({'success': False, 'error': 'Subject is required'}), 400
    
    results = []
    success_count = 0
    
    for file in files:
        result = {
            'filename': file.filename,
            'success': False,
            'error': None
        }
        
        try:
            if not file or file.filename == '':
                result['error'] = 'Empty file'
                results.append(result)
                continue
            
            if not allowed_file(file.filename):
                result['error'] = 'File type not allowed'
                results.append(result)
                continue
            
            # Process the file
            orig = secure_filename(file.filename)
            ext = os.path.splitext(orig)[1]
            stored = f"{uuid4().hex}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], stored)
            file.save(save_path)
            
            # Get file size
            file_size = os.path.getsize(save_path)
            
            # Generate thumbnail for images and PDFs
            thumbnail = generate_thumbnail(save_path, file.mimetype)
            
            # Upload to cloud storage if configured
            storage_type = app.config['STORAGE_TYPE']
            
            if storage_type == 's3':
                # Upload thumbnail to S3
                if thumbnail:
                    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                    s3_thumbnail_key = f"thumbnails/{thumbnail}"
                    upload_to_s3(thumbnail_path, s3_thumbnail_key, 'image/jpeg')
                
                # Upload main file to S3
                s3_key = f"documents/{stored}"
                success = upload_to_s3(save_path, s3_key, file.mimetype)
                if success:
                    os.remove(save_path)
                    if thumbnail:
                        thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                        if os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                else:
                    storage_type = 'local'
                    
            elif storage_type == 'azure':
                # Upload thumbnail to Azure
                if thumbnail:
                    thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                    azure_thumbnail_blob = f"thumbnails/{thumbnail}"
                    upload_to_azure(thumbnail_path, azure_thumbnail_blob, 'image/jpeg')
                
                # Upload main file to Azure
                azure_blob_name = f"documents/{stored}"
                success = upload_to_azure(save_path, azure_blob_name, file.mimetype)
                if success:
                    os.remove(save_path)
                    if thumbnail:
                        thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail)
                        if os.path.exists(thumbnail_path):
                            os.remove(thumbnail_path)
                else:
                    storage_type = 'local'
            
            # Save to database
            doc = Document(
                original_filename=orig,
                stored_filename=stored,
                year=year_int,
                subject=subject,
                mimetype=file.mimetype,
                size=file_size,
                thumbnail_filename=thumbnail,
                storage_type=storage_type,
                user_id=current_user.id
            )
            doc.set_tags_from_string(tags)
            db.session.add(doc)
            db.session.commit()
            
            result['success'] = True
            success_count += 1
            
        except Exception as e:
            result['error'] = str(e)
            print(f"Error uploading {file.filename}: {e}")
        
        results.append(result)
    
    return jsonify({
        'success': True,
        'total': len(files),
        'successful': success_count,
        'failed': len(files) - success_count,
        'results': results
    })


@app.route('/create-note', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        year = request.form.get('year')
        subject = request.form.get('subject')
        tags = request.form.get('tags')

        if not title or not title.strip():
            flash('Note title is required', 'warning')
            return redirect(request.url)

        if not content or not content.strip():
            flash('Note content is required', 'warning')
            return redirect(request.url)

        try:
            year_int = int(year)
        except Exception:
            flash('Year must be a number (e.g., 1, 2, 3, 4)', 'warning')
            return redirect(request.url)

        if not subject:
            flash('Subject is required', 'warning')
            return redirect(request.url)

        # Create a text file with the note content
        safe_title = secure_filename(title)
        if not safe_title.endswith('.txt'):
            safe_title += '.txt'
        
        stored = f"{uuid4().hex}.txt"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], stored)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)

        doc = Document(
            original_filename=safe_title,
            stored_filename=stored,
            year=year_int,
            subject=subject,
            mimetype='text/plain',
            size=os.path.getsize(save_path),
            user_id=current_user.id
        )
        # Set tags using the new tag system
        doc.set_tags_from_string(tags)
        db.session.add(doc)
        db.session.commit()
        flash('Note created successfully', 'success')
        return redirect(url_for('year_view', year=year_int))

    # GET -> show form
    return render_template('create_note.html')


@app.route('/year/<int:year>')
@login_required
def year_view(year: int):
    subject = request.args.get('subject', type=str)
    tags = request.args.get('tags', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    q = Document.query.filter_by(year=year, user_id=current_user.id)
    if subject:
        q = q.filter(Document.subject.ilike(f'%{subject}%'))
    if tags:
        # simple tags search: every provided tag must appear in stored tags string
        for t in [t.strip() for t in tags.split(',') if t.strip()]:
            q = q.filter(Document.tags.ilike(f'%{t}%'))

    pagination = q.order_by(Document.upload_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    documents = pagination.items
    
    # collect distinct subjects for a quick filter UI
    subjects = [r[0] for r in db.session.query(Document.subject).filter_by(year=year, user_id=current_user.id).distinct().order_by(Document.subject).all()]
    
    return render_template(
        'year.html', 
        year=year, 
        documents=documents, 
        pagination=pagination,
        subjects=subjects, 
        human_year_label=human_year_label,
        get_subject_color_class=get_subject_color_class
    )


@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    if not query:
        flash('Please enter a search term', 'warning')
        return redirect(url_for('index'))
    
    # Search across multiple fields
    search_term = f'%{query}%'
    q = Document.query.filter_by(user_id=current_user.id).filter(
        db.or_(
            Document.original_filename.ilike(search_term),
            Document.subject.ilike(search_term),
            Document.tags.ilike(search_term)
        )
    )
    
    # For text files, also search content
    text_docs = Document.query.filter_by(user_id=current_user.id, mimetype='text/plain').all()
    matching_text_doc_ids = []
    
    for doc in text_docs:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.stored_filename)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if query.lower() in content.lower():
                    matching_text_doc_ids.append(doc.id)
        except Exception:
            pass
    
    # Combine results
    if matching_text_doc_ids:
        q = q.union(
            Document.query.filter(Document.id.in_(matching_text_doc_ids))
        )
    
    pagination = q.order_by(Document.upload_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    documents = pagination.items
    
    return render_template(
        'search.html',
        query=query,
        documents=documents,
        pagination=pagination,
        human_year_label=human_year_label,
        get_subject_color_class=get_subject_color_class
    )


@app.route('/tags')
@login_required
def tags_list():
    """Show all tags with document counts."""
    # Get all tags that have documents belonging to current user
    tags_with_counts = db.session.query(
        Tag.id, Tag.name, Tag.slug, db.func.count(Document.id).label('count')
    ).select_from(Tag).join(document_tags, Tag.id == document_tags.c.tag_id).join(
        Document, Document.id == document_tags.c.document_id
    ).filter(
        Document.user_id == current_user.id
    ).group_by(Tag.id, Tag.name, Tag.slug).order_by(db.desc('count')).all()
    
    return render_template('tags.html', tags=tags_with_counts)


@app.route('/tag/<slug>')
@login_required
def tag_view(slug):
    """Show all documents with a specific tag."""
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get documents with this tag that belong to current user
    q = Document.query.join(document_tags).join(Tag).filter(
        Tag.slug == slug,
        Document.user_id == current_user.id
    )
    
    pagination = q.order_by(Document.upload_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    documents = pagination.items
    
    return render_template(
        'tag.html',
        tag=tag,
        documents=documents,
        pagination=pagination,
        human_year_label=human_year_label,
        get_subject_color_class=get_subject_color_class
    )


@app.route('/download/<int:doc_id>')
@login_required
def download(doc_id: int):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    
    # If file is in S3, generate presigned URL and redirect
    if doc.storage_type == 's3':
        s3_key = f"documents/{doc.stored_filename}"
        url = generate_presigned_url(s3_key, expiration=300, as_attachment=True, download_name=doc.original_filename)
        if url:
            return redirect(url)
        else:
            flash('Failed to generate download link', 'danger')
            return redirect(request.referrer or url_for('index'))
    
    # If file is in Azure, generate SAS URL and redirect
    elif doc.storage_type == 'azure':
        azure_blob_name = f"documents/{doc.stored_filename}"
        url = generate_azure_sas_url(azure_blob_name, expiration=300, as_attachment=True, download_name=doc.original_filename)
        if url:
            return redirect(url)
        else:
            flash('Failed to generate download link', 'danger')
            return redirect(request.referrer or url_for('index'))
    
    # Otherwise serve from local storage
    return send_from_directory(app.config['UPLOAD_FOLDER'], doc.stored_filename, as_attachment=True, download_name=doc.original_filename)


@app.route('/preview/<int:doc_id>')
@login_required
def preview(doc_id: int):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    previewable = False
    view_type = 'other'
    text_content = None
    file_url = None
    
    if doc.mimetype and doc.mimetype.startswith('image/'):
        previewable = True
        view_type = 'image'
    elif doc.mimetype == 'application/pdf' or (doc.original_filename.lower().endswith('.pdf')):
        previewable = True
        view_type = 'pdf'
    elif doc.mimetype == 'text/plain' or (doc.original_filename.lower().endswith('.txt')):
        previewable = True
        view_type = 'text'
        # Read the text file content
        if doc.storage_type == 's3':
            # Download from S3 to temporary location
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
            s3_key = f"documents/{doc.stored_filename}"
            if download_from_s3(s3_key, temp_file.name):
                try:
                    with open(temp_file.name, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                    os.remove(temp_file.name)
                except Exception as e:
                    text_content = f"Error reading file: {str(e)}"
            else:
                text_content = "Error downloading file from cloud storage"
        elif doc.storage_type == 'azure':
            # Download from Azure to temporary location
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
            azure_blob_name = f"documents/{doc.stored_filename}"
            if download_from_azure(azure_blob_name, temp_file.name):
                try:
                    with open(temp_file.name, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                    os.remove(temp_file.name)
                except Exception as e:
                    text_content = f"Error reading file: {str(e)}"
            else:
                text_content = "Error downloading file from cloud storage"
        else:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.stored_filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
            except Exception as e:
                text_content = f"Error reading file: {str(e)}"
    
    # Generate file URL for preview
    if doc.storage_type == 's3' and view_type in ['image', 'pdf']:
        s3_key = f"documents/{doc.stored_filename}"
        file_url = generate_presigned_url(s3_key, expiration=3600)
    elif doc.storage_type == 'azure' and view_type in ['image', 'pdf']:
        azure_blob_name = f"documents/{doc.stored_filename}"
        file_url = generate_azure_sas_url(azure_blob_name, expiration=3600)
    else:
        file_url = url_for('uploaded_file', filename=doc.stored_filename)

    return render_template('preview.html', doc=doc, previewable=previewable, view_type=view_type, text_content=text_content, file_url=file_url)


@app.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def edit_document(doc_id: int):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        year = request.form.get('year')
        subject = request.form.get('subject')
        tags = request.form.get('tags')
        
        try:
            year_int = int(year)
        except Exception:
            flash('Year must be a number (e.g., 1, 2, 3, 4)', 'warning')
            return redirect(request.url)
        
        if not subject:
            flash('Subject is required', 'warning')
            return redirect(request.url)
        
        # Update document metadata
        doc.year = year_int
        doc.subject = subject
        
        # Update tags using the new tag system
        doc.set_tags_from_string(tags)
        
        db.session.commit()
        flash('Document updated successfully', 'success')
        return redirect(url_for('year_view', year=year_int))
    
    # GET -> show edit form
    tags_string = ', '.join([tag.name for tag in doc.tag_objects]) if doc.tag_objects else ''
    return render_template('edit.html', doc=doc, tags_string=tags_string, human_year_label=human_year_label)


@app.route('/delete/<int:doc_id>', methods=['POST'])
@login_required
def delete_document(doc_id: int):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    
    # Delete the file from storage (S3, Azure, or local)
    if doc.storage_type == 's3':
        # Delete from S3
        s3_key = f"documents/{doc.stored_filename}"
        delete_from_s3(s3_key)
        
        # Delete thumbnail from S3 if exists
        if doc.thumbnail_filename:
            s3_thumbnail_key = f"thumbnails/{doc.thumbnail_filename}"
            delete_from_s3(s3_thumbnail_key)
            
    elif doc.storage_type == 'azure':
        # Delete from Azure
        azure_blob_name = f"documents/{doc.stored_filename}"
        delete_from_azure(azure_blob_name)
        
        # Delete thumbnail from Azure if exists
        if doc.thumbnail_filename:
            azure_thumbnail_blob = f"thumbnails/{doc.thumbnail_filename}"
            delete_from_azure(azure_thumbnail_blob)
            
    else:
        # Delete from local storage
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc.stored_filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            flash(f'Error deleting file: {str(e)}', 'danger')
            return redirect(request.referrer or url_for('index'))
        
        # Delete thumbnail from local storage if exists
        if doc.thumbnail_filename:
            thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails', doc.thumbnail_filename)
            try:
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
            except Exception as e:
                print(f"Error deleting thumbnail: {e}")
    
    # Delete from database
    db.session.delete(doc)
    db.session.commit()
    
    flash('Document deleted successfully', 'success')
    return redirect(request.referrer or url_for('index'))


# ===== COLLECTIONS ROUTES =====

@app.route('/collections')
@login_required
def collections():
    """List all collections for the current user."""
    user_collections = Collection.query.filter_by(user_id=current_user.id).order_by(Collection.updated_at.desc()).all()
    
    # Calculate document count for each collection
    collections_data = []
    for collection in user_collections:
        collections_data.append({
            'collection': collection,
            'document_count': collection.document_count()
        })
    
    return render_template('collections.html', collections=collections_data)


@app.route('/collection/create', methods=['GET', 'POST'])
@login_required
def create_collection():
    """Create a new collection."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '#667eea').strip()
        icon = request.form.get('icon', 'bi-folder').strip()
        
        if not name:
            flash('Collection name is required', 'danger')
            return redirect(url_for('create_collection'))
        
        # Create new collection
        new_collection = Collection(
            name=name,
            description=description,
            color=color,
            icon=icon,
            user_id=current_user.id
        )
        
        db.session.add(new_collection)
        db.session.commit()
        
        flash(f'Collection "{name}" created successfully!', 'success')
        return redirect(url_for('collections'))
    
    return render_template('collection_create.html')


@app.route('/collection/<int:collection_id>')
@login_required
def view_collection(collection_id):
    """View documents in a specific collection."""
    collection = Collection.query.filter_by(id=collection_id, user_id=current_user.id).first_or_404()
    documents = collection.documents.all()
    
    return render_template('collection_view.html', collection=collection, documents=documents)


@app.route('/collection/<int:collection_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_collection(collection_id):
    """Edit collection details."""
    collection = Collection.query.filter_by(id=collection_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '#667eea').strip()
        icon = request.form.get('icon', 'bi-folder').strip()
        
        if not name:
            flash('Collection name is required', 'danger')
            return redirect(url_for('edit_collection', collection_id=collection_id))
        
        collection.name = name
        collection.description = description
        collection.color = color
        collection.icon = icon
        collection.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Collection "{name}" updated successfully!', 'success')
        return redirect(url_for('view_collection', collection_id=collection_id))
    
    return render_template('collection_create.html', collection=collection, edit_mode=True)


@app.route('/collection/<int:collection_id>/delete', methods=['POST'])
@login_required
def delete_collection(collection_id):
    """Delete a collection (not the documents)."""
    collection = Collection.query.filter_by(id=collection_id, user_id=current_user.id).first_or_404()
    
    collection_name = collection.name
    db.session.delete(collection)
    db.session.commit()
    
    flash(f'Collection "{collection_name}" deleted successfully', 'success')
    return redirect(url_for('collections'))


@app.route('/collection/<int:collection_id>/add', methods=['POST'])
@login_required
def add_to_collection(collection_id):
    """Add documents to a collection."""
    collection = Collection.query.filter_by(id=collection_id, user_id=current_user.id).first_or_404()
    
    # Get document IDs from form (supports multiple)
    doc_ids = request.form.getlist('document_ids')
    
    if not doc_ids:
        return jsonify({'success': False, 'message': 'No documents selected'}), 400
    
    added_count = 0
    for doc_id in doc_ids:
        doc = Document.query.filter_by(id=int(doc_id), user_id=current_user.id).first()
        if doc and doc not in collection.documents:
            collection.documents.append(doc)
            added_count += 1
    
    collection.updated_at = datetime.utcnow()
    db.session.commit()
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': f'Added {added_count} document(s) to "{collection.name}"',
            'added_count': added_count
        })
    
    flash(f'Added {added_count} document(s) to "{collection.name}"', 'success')
    return redirect(request.referrer or url_for('view_collection', collection_id=collection_id))


@app.route('/collection/<int:collection_id>/remove/<int:doc_id>', methods=['POST'])
@login_required
def remove_from_collection(collection_id, doc_id):
    """Remove a document from a collection."""
    collection = Collection.query.filter_by(id=collection_id, user_id=current_user.id).first_or_404()
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    
    if doc in collection.documents:
        collection.documents.remove(doc)
        collection.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Document removed from "{collection.name}"', 'success')
    else:
        flash('Document not in this collection', 'warning')
    
    return redirect(url_for('view_collection', collection_id=collection_id))


@app.route('/api/documents')
@login_required
def api_get_documents():
    """API endpoint to get all user documents for collection management."""
    documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.upload_date.desc()).all()
    
    documents_list = []
    for doc in documents:
        documents_list.append({
            'id': doc.id,
            'original_filename': doc.original_filename,
            'year': doc.year,
            'subject': doc.subject,
            'tags': doc.tags,
            'upload_date': doc.upload_date.strftime('%Y-%m-%d')
        })
    
    return jsonify({'documents': documents_list})


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # serve stored files; keep simple for a small app
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/thumbnails/<path:filename>')
def thumbnail_file(filename):
    # If using S3, generate presigned URL and redirect
    if app.config['STORAGE_TYPE'] == 's3':
        s3_key = f"thumbnails/{filename}"
        url = generate_presigned_url(s3_key, expiration=3600)
        if url:
            return redirect(url)
    
    # Otherwise serve from local thumbnails directory
    thumbnail_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails')
    return send_from_directory(thumbnail_dir, filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
