#!/usr/bin/env python3
"""
Script to update room names in the database
"""

import sqlite3

def update_room_names():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    try:
        # Show current room names
        cursor.execute("SELECT room_type, price_per_night FROM room_prices")
        rows = cursor.fetchall()
        print("Current room names:")
        for row in rows:
            print(f"- {row[0]}: {row[1]}₺")
        
        # Update room names
        cursor.execute("UPDATE room_prices SET room_type = 'Standart' WHERE room_type = 'Standart'")
        cursor.execute("UPDATE room_prices SET room_type = 'Standart Double' WHERE room_type = 'Deluxe'")
        cursor.execute("UPDATE room_prices SET room_type = 'Standart Triple' WHERE room_type = 'Suit'")
        
        # Update images table room_type column
        cursor.execute("UPDATE images SET room_type = 'standart' WHERE room_type = 'standart'")
        cursor.execute("UPDATE images SET room_type = 'standart_double' WHERE room_type = 'deluxe'")
        cursor.execute("UPDATE images SET room_type = 'standart_triple' WHERE room_type = 'suit'")
        
        conn.commit()
        print("\nRoom names updated successfully!")
        
        # Show updated room names
        cursor.execute("SELECT room_type, price_per_night FROM room_prices")
        rows = cursor.fetchall()
        print("\nUpdated room names:")
        for row in rows:
            print(f"- {row[0]}: {row[1]}₺")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_room_names() 