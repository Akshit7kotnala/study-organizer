"""
Migration script to add Collection model and document_collections association table.
This enables users to organize documents into custom collections/folders.

Run this script once to update your database schema.
"""

import sqlite3
from datetime import datetime

def migrate():
    # Connect to the database
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    
    try:
        # Check if collection table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='collection'
        """)
        
        if cursor.fetchone():
            print("✓ Collection table already exists. Skipping creation.")
        else:
            # Create collection table
            cursor.execute("""
                CREATE TABLE collection (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(128) NOT NULL,
                    description TEXT,
                    user_id INTEGER NOT NULL,
                    color VARCHAR(7) DEFAULT '#667eea',
                    icon VARCHAR(32) DEFAULT 'bi-folder',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            """)
            print("✓ Created collection table")
        
        # Check if document_collections table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='document_collections'
        """)
        
        if cursor.fetchone():
            print("✓ document_collections table already exists. Skipping creation.")
        else:
            # Create document_collections association table
            cursor.execute("""
                CREATE TABLE document_collections (
                    document_id INTEGER NOT NULL,
                    collection_id INTEGER NOT NULL,
                    PRIMARY KEY (document_id, collection_id),
                    FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE CASCADE,
                    FOREIGN KEY (collection_id) REFERENCES collection (id) ON DELETE CASCADE
                )
            """)
            print("✓ Created document_collections association table")
        
        # Create index for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_collections_user_id 
            ON collection (user_id)
        """)
        print("✓ Created index on collection.user_id")
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_document_collections_document_id 
            ON document_collections (document_id)
        """)
        print("✓ Created index on document_collections.document_id")
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_document_collections_collection_id 
            ON document_collections (collection_id)
        """)
        print("✓ Created index on document_collections.collection_id")
        
        # Commit all changes
        conn.commit()
        print("\n✅ Migration completed successfully!")
        print("\nYou can now:")
        print("  - Create collections to organize your documents")
        print("  - Add documents to multiple collections")
        print("  - Access collections at /collections route")
        
    except sqlite3.Error as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting migration to add Collections feature...\n")
    migrate()
