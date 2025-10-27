"""
Sample Data Generator for Study Organizer

This script creates sample documents in the database for testing/demo purposes.
It creates mock PDF files and adds them to the database with realistic metadata.

Usage:
    python demo_data.py
"""

import os
import sys
from datetime import datetime, timedelta
from uuid import uuid4
import random

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Document

# Sample data
SUBJECTS = {
    1: ['Mathematics I', 'Physics I', 'Chemistry', 'Engineering Drawing', 'Programming Basics'],
    2: ['Mathematics II', 'Physics II', 'Data Structures', 'Digital Logic', 'Electronics'],
    3: ['Algorithms', 'Database Systems', 'Operating Systems', 'Computer Networks', 'Software Engineering'],
    4: ['Machine Learning', 'Artificial Intelligence', 'Distributed Systems', 'Cloud Computing', 'Cybersecurity']
}

TAG_OPTIONS = [
    ['lecture', 'notes'],
    ['exam', 'preparation'],
    ['assignment', 'homework'],
    ['lab', 'practical'],
    ['tutorial', 'practice'],
    ['project', 'report'],
    ['midterm', 'study guide'],
    ['final', 'revision']
]

FILE_TYPES = [
    ('lecture-notes.pdf', 'application/pdf'),
    ('assignment.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
    ('lab-report.pdf', 'application/pdf'),
    ('slides.pptx', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'),
    ('diagram.png', 'image/png'),
    ('problem-set.pdf', 'application/pdf'),
]


def create_sample_file(filename: str, upload_folder: str) -> str:
    """Create a sample file with dummy content."""
    ext = os.path.splitext(filename)[1]
    stored_name = f"{uuid4().hex}{ext}"
    file_path = os.path.join(upload_folder, stored_name)
    
    # Create dummy content
    content = f"Sample document content for {filename}\n"
    content += f"Generated on {datetime.now()}\n"
    content += "This is a demo file created by demo_data.py\n" * 10
    
    with open(file_path, 'wb') as f:
        f.write(content.encode('utf-8'))
    
    return stored_name


def generate_sample_data(num_docs_per_year: int = 5):
    """Generate sample documents for all years."""
    print("🚀 Generating sample data for Study Organizer...")
    print(f"   Creating {num_docs_per_year} documents per year")
    print()
    
    with app.app_context():
        # Create uploads folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        # Document.query.delete()
        # db.session.commit()
        # print("   Cleared existing documents")
        
        total_created = 0
        
        for year, subjects in SUBJECTS.items():
            print(f"📚 Year {year}:")
            
            for i in range(num_docs_per_year):
                # Select random subject
                subject = random.choice(subjects)
                
                # Select random file type
                original_filename, mimetype = random.choice(FILE_TYPES)
                filename_parts = original_filename.rsplit('.', 1)
                original_filename = f"{subject.replace(' ', '-')}-{filename_parts[0]}-{i+1}.{filename_parts[1]}"
                
                # Create actual file
                stored_filename = create_sample_file(original_filename, app.config['UPLOAD_FOLDER'])
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
                file_size = os.path.getsize(file_path)
                
                # Select random tags
                tags = ', '.join(random.choice(TAG_OPTIONS))
                
                # Create random upload date (within last 6 months)
                days_ago = random.randint(0, 180)
                upload_date = datetime.utcnow() - timedelta(days=days_ago)
                
                # Create document record
                doc = Document(
                    original_filename=original_filename,
                    stored_filename=stored_filename,
                    year=year,
                    subject=subject,
                    tags=tags,
                    mimetype=mimetype,
                    size=file_size,
                    upload_date=upload_date
                )
                
                db.session.add(doc)
                total_created += 1
                
                print(f"   ✅ Created: {original_filename} ({subject})")
            
            print()
        
        # Commit all documents
        db.session.commit()
        
        print("=" * 60)
        print(f"✨ Successfully created {total_created} sample documents!")
        print("=" * 60)
        print()
        print("You can now:")
        print("  1. Run the app: python app.py")
        print("  2. Open browser: http://127.0.0.1:5000/")
        print("  3. Browse the sample documents by year")
        print()


if __name__ == '__main__':
    print()
    print("=" * 60)
    print("  Study Organizer - Sample Data Generator")
    print("=" * 60)
    print()
    
    # Check if database exists
    db_path = os.path.join(os.path.dirname(__file__), 'documents.db')
    if not os.path.exists(db_path):
        print("⚠️  Database not found. Creating...")
        with app.app_context():
            db.create_all()
        print("✅ Database created successfully!")
        print()
    
    try:
        generate_sample_data(num_docs_per_year=5)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
