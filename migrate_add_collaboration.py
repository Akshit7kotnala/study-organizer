"""
Migration script to add collaboration features to the database.
This adds SharePermission, Comment, StudyGroup, Notification models and group_members table.
"""
from app import app, db
import sys

def migrate():
    with app.app_context():
        try:
            print("Starting migration to add collaboration features...")
            
            # Create all tables defined in models
            db.create_all()
            
            print("✓ Migration completed successfully!")
            print("✓ Added tables:")
            print("  - share_permission (for sharing documents/collections)")
            print("  - comment (for document annotations)")
            print("  - study_group (for study groups)")
            print("  - group_members (association table)")
            print("  - notification (for user notifications)")
            
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            sys.exit(1)

if __name__ == '__main__':
    migrate()
