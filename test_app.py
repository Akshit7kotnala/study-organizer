import os
import tempfile
import pytest
import shutil
from app import app, db, Document
from io import BytesIO


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    db_fd, db_path = tempfile.mkstemp()
    upload_dir = tempfile.mkdtemp()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = upload_dir
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()
        
    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(upload_dir, ignore_errors=True)


def test_index_empty(client):
    """Test index page with no documents."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'No documents uploaded yet' in rv.data or b'Total Documents' in rv.data


def test_upload_page(client):
    """Test upload page loads."""
    rv = client.get('/upload')
    assert rv.status_code == 200
    assert b'Upload Document' in rv.data


def test_upload_document(client):
    """Test uploading a document."""
    data = {
        'file': (BytesIO(b'test content'), 'test.pdf'),
        'year': '1',
        'subject': 'Math',
        'tags': 'algebra, calculus'
    }
    rv = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert rv.status_code == 200
    
    # Check document was saved to DB
    with app.app_context():
        doc = Document.query.first()
        assert doc is not None
        assert doc.original_filename == 'test.pdf'
        assert doc.year == 1
        assert doc.subject == 'Math'
        assert doc.tags == 'algebra, calculus'


def test_upload_missing_file(client):
    """Test upload with missing file."""
    data = {
        'year': '1',
        'subject': 'Math',
    }
    rv = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert rv.status_code == 200
    assert b'No file selected' in rv.data


def test_upload_missing_subject(client):
    """Test upload with missing subject."""
    data = {
        'file': (BytesIO(b'test'), 'test.pdf'),
        'year': '1',
    }
    rv = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert rv.status_code == 200
    assert b'Subject is required' in rv.data


def test_year_view(client):
    """Test year view page."""
    # Upload a document first
    data = {
        'file': (BytesIO(b'test'), 'test.pdf'),
        'year': '2',
        'subject': 'Physics',
        'tags': 'mechanics'
    }
    client.post('/upload', data=data, content_type='multipart/form-data')
    
    # Visit year page
    rv = client.get('/year/2')
    assert rv.status_code == 200
    assert b'2nd Year' in rv.data
    assert b'Physics' in rv.data
    assert b'test.pdf' in rv.data


def test_year_view_filter_by_subject(client):
    """Test filtering by subject."""
    # Upload two documents
    client.post('/upload', data={
        'file': (BytesIO(b'test1'), 'math.pdf'),
        'year': '1',
        'subject': 'Math',
    }, content_type='multipart/form-data')
    
    client.post('/upload', data={
        'file': (BytesIO(b'test2'), 'physics.pdf'),
        'year': '1',
        'subject': 'Physics',
    }, content_type='multipart/form-data')
    
    # Filter by Math
    rv = client.get('/year/1?subject=Math')
    assert rv.status_code == 200
    assert b'math.pdf' in rv.data
    assert b'physics.pdf' not in rv.data


def test_download(client):
    """Test downloading a document."""
    # Upload a document
    data = {
        'file': (BytesIO(b'download test'), 'download.pdf'),
        'year': '1',
        'subject': 'Test',
    }
    client.post('/upload', data=data, content_type='multipart/form-data')
    
    # Get document ID from the test client's app context
    doc = Document.query.first()
    doc_id = doc.id
    
    # Download it
    rv = client.get(f'/download/{doc_id}')
    assert rv.status_code == 200
    assert rv.data == b'download test'


def test_preview_page(client):
    """Test preview page."""
    # Upload a document
    data = {
        'file': (BytesIO(b'preview test'), 'preview.pdf'),
        'year': '1',
        'subject': 'Test',
    }
    client.post('/upload', data=data, content_type='multipart/form-data')
    
    # Get document ID from the test client's app context
    doc = Document.query.first()
    doc_id = doc.id
    
    # Visit preview page
    rv = client.get(f'/preview/{doc_id}')
    assert rv.status_code == 200
    assert b'preview.pdf' in rv.data


def test_index_with_documents(client):
    """Test index shows years after upload."""
    # Upload documents in different years
    client.post('/upload', data={
        'file': (BytesIO(b'test1'), 'year1.pdf'),
        'year': '1',
        'subject': 'Math',
    }, content_type='multipart/form-data')
    
    client.post('/upload', data={
        'file': (BytesIO(b'test2'), 'year3.pdf'),
        'year': '3',
        'subject': 'Physics',
    }, content_type='multipart/form-data')
    
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'1st Year' in rv.data
    assert b'3rd Year' in rv.data


def test_create_note_page(client):
    """Test create note page loads."""
    rv = client.get('/create-note')
    assert rv.status_code == 200
    assert b'Create Note' in rv.data


def test_create_note(client):
    """Test creating a text note."""
    data = {
        'title': 'Math Formulas',
        'content': 'Pythagorean theorem: a^2 + b^2 = c^2\nQuadratic formula: x = (-b ± sqrt(b^2 - 4ac)) / 2a',
        'year': '2',
        'subject': 'Mathematics',
        'tags': 'formulas, reference'
    }
    rv = client.post('/create-note', data=data, follow_redirects=True)
    assert rv.status_code == 200
    
    # Check note was saved to DB
    doc = Document.query.filter_by(subject='Mathematics').first()
    assert doc is not None
    assert doc.original_filename.endswith('.txt')
    assert doc.year == 2
    assert doc.tags == 'formulas, reference'


def test_create_note_missing_title(client):
    """Test create note with missing title."""
    data = {
        'content': 'Some content',
        'year': '1',
        'subject': 'Test',
    }
    rv = client.post('/create-note', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Note title is required' in rv.data


def test_preview_text_note(client):
    """Test previewing a text note."""
    # Create a note
    data = {
        'title': 'Test Note',
        'content': 'This is a test note content.\nLine 2\nLine 3',
        'year': '1',
        'subject': 'Testing',
    }
    client.post('/create-note', data=data)
    
    # Get note ID
    doc = Document.query.first()
    doc_id = doc.id
    
    # Preview it
    rv = client.get(f'/preview/{doc_id}')
    assert rv.status_code == 200
    assert b'This is a test note content' in rv.data
