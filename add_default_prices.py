#!/usr/bin/env python3
"""
Script to add default room prices to the database
"""

from app import create_app, db
from app.models.reservation import RoomPrice
from datetime import datetime

def add_default_prices():
    app = create_app()
    
    with app.app_context():
        # Check if prices already exist
        existing_prices = RoomPrice.query.all()
        if existing_prices:
            print("Room prices already exist in the database:")
            for price in existing_prices:
                print(f"- {price.room_type}: {price.price_per_night}₺")
            return
        
        # Add default prices
        default_prices = [
            {
                'room_type': 'Standart',
                'price_per_night': 250.0,
                'original_price': 250.0,
                'discount_percentage': 0.0,
                'is_discounted': False,
                'description': 'Konforlu yatak, modern banyo, klima ve ücretsiz Wi-Fi içeren standart oda.'
            },
            {
                'room_type': 'Deluxe',
                'price_per_night': 350.0,
                'original_price': 350.0,
                'discount_percentage': 0.0,
                'is_discounted': False,
                'description': 'Daha geniş alan, lüks dekorasyon ve ekstra oturma bölümü sunan deluxe oda.'
            },
            {
                'room_type': 'Suit',
                'price_per_night': 500.0,
                'original_price': 500.0,
                'discount_percentage': 0.0,
                'is_discounted': False,
                'description': 'Özel salon, ayrı yatak odası ve jakuzi içeren en lüks oda seçeneği.'
            }
        ]
        
        for price_data in default_prices:
            room_price = RoomPrice(**price_data)
            db.session.add(room_price)
        
        try:
            db.session.commit()
            print("Default room prices added successfully:")
            for price_data in default_prices:
                print(f"- {price_data['room_type']}: {price_data['price_per_night']}₺")
        except Exception as e:
            print(f"Error adding default prices: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_default_prices() 