"""
Migration script to add analytics columns to existing database.
Run this once to update your database schema.
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'documents.db')

def migrate_database():
    """Add new analytics columns to existing tables."""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🔄 Starting database migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(document)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add analytics columns to Document table if they don't exist
        if 'view_count' not in columns:
            print("  ➕ Adding view_count column to document table...")
            cursor.execute("ALTER TABLE document ADD COLUMN view_count INTEGER DEFAULT 0")
            print("  ✅ view_count column added")
        else:
            print("  ℹ️  view_count column already exists")
        
        if 'last_accessed' not in columns:
            print("  ➕ Adding last_accessed column to document table...")
            cursor.execute("ALTER TABLE document ADD COLUMN last_accessed DATETIME")
            print("  ✅ last_accessed column added")
        else:
            print("  ℹ️  last_accessed column already exists")
        
        if 'download_count' not in columns:
            print("  ➕ Adding download_count column to document table...")
            cursor.execute("ALTER TABLE document ADD COLUMN download_count INTEGER DEFAULT 0")
            print("  ✅ download_count column added")
        else:
            print("  ℹ️  download_count column already exists")
        
        # Create ActivityLog table if it doesn't exist
        print("  ➕ Creating activity_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type VARCHAR(64) NOT NULL,
                document_id INTEGER,
                meta_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (document_id) REFERENCES document(id)
            )
        """)
        print("  ✅ activity_log table created")
        
        # Create index on created_at for faster queries
        print("  ➕ Creating index on activity_log.created_at...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_activity_log_created_at 
            ON activity_log(created_at)
        """)
        print("  ✅ Index created")
        
        # Create index on user_id for faster queries
        print("  ➕ Creating index on activity_log.user_id...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_activity_log_user_id 
            ON activity_log(user_id)
        """)
        print("  ✅ Index created")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Migration completed successfully!")
        print("🚀 You can now restart your Flask app.")
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Analytics Database Migration")
    print("=" * 60)
    migrate_database()
