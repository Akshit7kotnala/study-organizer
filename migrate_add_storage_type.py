"""
Migration script to add storage_type column to Document table.
Run this once to update your existing database.
"""
import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'documents.db')

def migrate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(document)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'storage_type' not in columns:
            print("Adding storage_type column to document table...")
            cursor.execute("ALTER TABLE document ADD COLUMN storage_type VARCHAR(16) DEFAULT 'local' NOT NULL")
            conn.commit()
            print("Migration successful! storage_type column added.")
            print("All existing documents are marked as 'local' storage.")
        else:
            print("storage_type column already exists. No migration needed.")
    
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
