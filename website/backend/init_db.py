#!/usr/bin/env python3
"""
Database initialization script
"""
import sqlite3
import os

def init_db():
    """Initialize the database file"""
    db_path = "/app/novels.db"
    
    # Create the database file if it doesn't exist
    if not os.path.exists(db_path):
        print(f"Creating database file at {db_path}")
        # Create an empty database file
        conn = sqlite3.connect(db_path)
        conn.close()
        print("Database file created successfully")
    else:
        print(f"Database file already exists at {db_path}")
    
    # Set proper permissions
    os.chmod(db_path, 0o666)
    print(f"Set permissions on {db_path}")

if __name__ == "__main__":
    init_db()
