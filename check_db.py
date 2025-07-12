#!/usr/bin/env python3
"""
Script to check database status
"""

import sqlite3

def check_database():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    try:
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 Database tables:")
        print("-" * 30)
        
        if tables:
            for table in tables:
                print(f"✅ {table[0]}")
        else:
            print("❌ No tables found!")
        
        print("\n" + "="*50)
        
        # Check each table structure
        for table in tables:
            table_name = table[0]
            print(f"\n📊 Table: {table_name}")
            print("-" * 20)
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # Count rows
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  Rows: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_database() 