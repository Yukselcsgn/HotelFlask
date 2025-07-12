#!/usr/bin/env python3
"""
Script to create database tables
"""

import sqlite3

def create_database():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    try:
        print("🔄 Creating database tables...")
        
        # Create images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename VARCHAR(255) NOT NULL,
                category VARCHAR(50) NOT NULL,
                room_type VARCHAR(80),
                display_order INTEGER,
                is_active BOOLEAN DEFAULT 1,
                uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Images table created")
        
        # Create reservations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(120) NOT NULL,
                email VARCHAR(120) NOT NULL,
                room_type VARCHAR(80) NOT NULL,
                check_in DATE NOT NULL,
                check_out DATE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Reservations table created")
        
        # Create room_prices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS room_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_type VARCHAR(80) NOT NULL UNIQUE,
                price_per_night FLOAT NOT NULL,
                original_price FLOAT NOT NULL,
                discount_percentage FLOAT DEFAULT 0.0,
                is_discounted BOOLEAN DEFAULT 0,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Room prices table created")
        
        # Add default room prices
        default_prices = [
            ('Standart', 250.0, 250.0, 0.0, False, 'Konforlu yatak, modern banyo, klima ve ücretsiz Wi-Fi içeren standart oda.'),
            ('Standart Double', 350.0, 350.0, 0.0, False, 'Daha geniş alan, lüks dekorasyon ve ekstra oturma bölümü sunan deluxe oda.'),
            ('Standart Triple', 500.0, 500.0, 0.0, False, 'Özel salon, ayrı yatak odası ve jakuzi içeren en lüks oda seçeneği.')
        ]
        
        for price in default_prices:
            cursor.execute('''
                INSERT OR REPLACE INTO room_prices 
                (room_type, price_per_night, original_price, discount_percentage, is_discounted, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', price)
        
        print("✅ Default room prices added")
        
        conn.commit()
        print("\n🎉 Database created successfully!")
        
        # Verify tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📋 Created tables: {len(tables)}")
        for table in tables:
            print(f"  ✅ {table[0]}")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_database() 