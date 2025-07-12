#!/usr/bin/env python3
"""
Script to scan existing images and add them to database
"""

import os
from app import create_app, db
from app.models.reservation import Image

def scan_and_add_images():
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Scanning existing images...")
            
            # Images klasörünü tara
            images_dir = "app/static/images"
            
            if not os.path.exists(images_dir):
                print(f"❌ Images directory not found: {images_dir}")
                return
            
            added_count = 0
            skipped_count = 0
            
            # Ana images klasöründeki fotoğrafları 3 odaya da ekle
            main_images_dir = os.path.join(images_dir)
            if os.path.exists(main_images_dir):
                for filename in os.listdir(main_images_dir):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        # Her oda tipine ekle
                        room_types = ['Standart', 'Deluxe', 'Suit']
                        for room_type in room_types:
                            existing_image = Image.query.filter_by(
                                filename=filename, 
                                category='room', 
                                room_type=room_type
                            ).first()
                            
                            if not existing_image:
                                image = Image(
                                    filename=filename,
                                    category='room',
                                    room_type=room_type,
                                    display_order=added_count + 1,
                                    is_active=True
                                )
                                db.session.add(image)
                                added_count += 1
                                print(f"✅ Added room ({room_type}): {filename}")
                            else:
                                skipped_count += 1
                                print(f"⏭️  Skipped (already exists): {filename} for {room_type}")
            
            # Oda klasörlerini tara (odaya özgü fotoğraflar)
            room_types = ['standart', 'deluxe', 'suit']
            for room_type in room_types:
                room_dir = os.path.join(images_dir, room_type)
                if os.path.exists(room_dir):
                    for filename in os.listdir(room_dir):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                            # Oda fotoğrafı olarak ekle
                            existing_image = Image.query.filter_by(
                                filename=filename, 
                                category='room', 
                                room_type=room_type.capitalize()
                            ).first()
                            
                            if not existing_image:
                                image = Image(
                                    filename=filename,
                                    category='room',
                                    room_type=room_type.capitalize(),
                                    display_order=added_count + 1,
                                    is_active=True
                                )
                                db.session.add(image)
                                added_count += 1
                                print(f"✅ Added room-specific ({room_type}): {filename}")
                            else:
                                skipped_count += 1
                                print(f"⏭️  Skipped (already exists): {filename}")
            
            db.session.commit()
            print(f"\n🎉 Image scanning completed!")
            print(f"✅ Added: {added_count} images")
            print(f"⏭️  Skipped: {skipped_count} images")
            
            # İstatistikler
            total_images = Image.query.count()
            room_images = Image.query.filter_by(category='room').count()
            
            # Oda tipine göre istatistikler
            standart_count = Image.query.filter_by(category='room', room_type='Standart').count()
            deluxe_count = Image.query.filter_by(category='room', room_type='Deluxe').count()
            suit_count = Image.query.filter_by(category='room', room_type='Suit').count()
            
            print(f"\n📊 Database Statistics:")
            print(f"   Total images: {total_images}")
            print(f"   Room images: {room_images}")
            print(f"     - Standart: {standart_count}")
            print(f"     - Deluxe: {deluxe_count}")
            print(f"     - Suit: {suit_count}")
            
        except Exception as e:
            print(f"❌ Error scanning images: {e}")
            db.session.rollback()

if __name__ == "__main__":
    scan_and_add_images() 