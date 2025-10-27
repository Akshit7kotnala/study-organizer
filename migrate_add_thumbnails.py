"""
Migration script to add thumbnail_filename column to Document table.
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
        
        if 'thumbnail_filename' not in columns:
            print("Adding thumbnail_filename column to document table...")
            cursor.execute("ALTER TABLE document ADD COLUMN thumbnail_filename VARCHAR(512)")
            conn.commit()
            print("Migration successful! thumbnail_filename column added.")
        else:
            print("thumbnail_filename column already exists. No migration needed.")
    
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
