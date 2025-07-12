#!/usr/bin/env python3
"""
Script to run database migration
"""

from app import create_app, db
from alembic import command
from alembic.config import Config
import os

def run_migration():
    try:
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            # Initialize Alembic config
            alembic_cfg = Config("migrations/alembic.ini")
            
            print("🔄 Running database migration...")
            
            # Run migration
            command.upgrade(alembic_cfg, "head")
            
            print("✅ Migration completed successfully!")
            
            # Verify tables
            from app.models.reservation import Image, Reservation, RoomPrice
            
            # Check if tables exist
            try:
                image_count = Image.query.count()
                reservation_count = Reservation.query.count()
                room_price_count = RoomPrice.query.count()
                
                print(f"\n📊 Database status after migration:")
                print(f"  Images: {image_count}")
                print(f"  Reservations: {reservation_count}")
                print(f"  Room Prices: {room_price_count}")
                
            except Exception as e:
                print(f"⚠️ Warning: Could not verify tables: {e}")
                
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    run_migration() 