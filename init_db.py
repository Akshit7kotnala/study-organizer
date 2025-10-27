"""
Database initialization script for production deployment.
Run this once after deploying to create all database tables.
"""

from app import app, db

def init_db():
    """Initialize the database by creating all tables."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  - user")
        print("  - tag")
        print("  - collection")
        print("  - document")
        print("  - document_tags (association table)")
        print("  - document_collections (association table)")
        print("\n🎉 Database is ready to use!")

if __name__ == '__main__':
    init_db()
