#!/usr/bin/env python3
"""
Script to check images in database
"""

import sqlite3

def check_images():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    
    try:
        # Check if images table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='images'")
        if not cursor.fetchone():
            print("❌ Images table does not exist!")
            return
        
        # Get all images
        cursor.execute("SELECT id, filename, category, room_type, uploaded_at FROM images")
        images = cursor.fetchall()
        
        print(f"📸 Found {len(images)} images in database:")
        print("-" * 50)
        
        if images:
            for img in images:
                print(f"ID: {img[0]}")
                print(f"Filename: {img[1]}")
                print(f"Category: {img[2]}")
                print(f"Room Type: {img[3]}")
                print(f"Uploaded: {img[4]}")
                print("-" * 30)
        else:
            print("❌ No images found in database!")
        
        # Check room images specifically
        cursor.execute("SELECT COUNT(*) FROM images WHERE category='room'")
        room_count = cursor.fetchone()[0]
        print(f"\n🏠 Room images: {room_count}")
        
        # Check slider images specifically
        cursor.execute("SELECT COUNT(*) FROM images WHERE category='slider'")
        slider_count = cursor.fetchone()[0]
        print(f"🖼️ Slider images: {slider_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_images() 