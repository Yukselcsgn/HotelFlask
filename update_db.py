#!/usr/bin/env python3
"""
Script to manually update database with discount fields
"""

import sqlite3

def update_database():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(room_prices)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print("Current columns:", columns)
        
        # Add new columns if they don't exist
        if 'original_price' not in columns:
            cursor.execute("ALTER TABLE room_prices ADD COLUMN original_price REAL")
            print("Added original_price column")
        
        if 'discount_percentage' not in columns:
            cursor.execute("ALTER TABLE room_prices ADD COLUMN discount_percentage REAL DEFAULT 0.0")
            print("Added discount_percentage column")
        
        if 'is_discounted' not in columns:
            cursor.execute("ALTER TABLE room_prices ADD COLUMN is_discounted BOOLEAN DEFAULT 0")
            print("Added is_discounted column")
        
        # Update existing records to set original_price = price_per_night
        cursor.execute("UPDATE room_prices SET original_price = price_per_night WHERE original_price IS NULL")
        print("Updated existing records with original_price")
        
        conn.commit()
        print("Database updated successfully!")
        
        # Show current data
        cursor.execute("SELECT room_type, price_per_night, original_price, discount_percentage, is_discounted FROM room_prices")
        rows = cursor.fetchall()
        print("\nCurrent room prices:")
        for row in rows:
            print(f"- {row[0]}: {row[1]}₺ (Original: {row[2]}₺, Discount: {row[3]}%, Active: {row[4]})")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_database() 