#!/usr/bin/env python3
"""
Script to add default FAQs to the database
"""

from app import create_app, db
from app.models.reservation import FAQ

def add_default_faqs():
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Adding default FAQs...")
            
            # Varsayılan FAQ'lar
            default_faqs = [
                {
                    'question': 'Check-in ve check-out saatleri nedir?',
                    'answer': 'Check-in saati 14:00, check-out saati 11:00\'dır. Erken check-in veya geç check-out için önceden bilgi veriniz.',
                    'display_order': 1
                },
                {
                    'question': 'Kahvaltı dahil mi?',
                    'answer': 'Evet, tüm odalarımızda zengin Türk kahvaltısı dahildir. Kahvaltı saatleri 07:00-10:00 arasındadır.',
                    'display_order': 2
                },
                {
                    'question': 'Otopark hizmeti var mı?',
                    'answer': 'Evet, ücretsiz otopark hizmetimiz mevcuttur. Araç güvenliği için 7/24 kamera sistemi bulunmaktadır.',
                    'display_order': 3
                },
                {
                    'question': 'Rezervasyon iptali nasıl yapılır?',
                    'answer': 'Rezervasyon iptali için en az 24 saat önceden bilgi vermeniz gerekmektedir. İptal işlemi için bizimle iletişime geçiniz.',
                    'display_order': 4
                },
                {
                    'question': 'Wi-Fi hizmeti ücretsiz mi?',
                    'answer': 'Evet, tüm odalarımızda ücretsiz yüksek hızlı Wi-Fi hizmeti sunulmaktadır.',
                    'display_order': 5
                },
                {
                    'question': 'Evcil hayvan kabul ediyor musunuz?',
                    'answer': 'Maalesef evcil hayvan kabul etmiyoruz. Bu konuda anlayışınız için teşekkür ederiz.',
                    'display_order': 6
                }
            ]
            
            # FAQ'ları ekle
            for faq_data in default_faqs:
                # Aynı soru varsa ekleme
                existing_faq = FAQ.query.filter_by(question=faq_data['question']).first()
                if not existing_faq:
                    faq = FAQ(
                        question=faq_data['question'],
                        answer=faq_data['answer'],
                        display_order=faq_data['display_order'],
                        is_active=True
                    )
                    db.session.add(faq)
                    print(f"✅ Added: {faq_data['question'][:50]}...")
                else:
                    print(f"⏭️  Skipped (already exists): {faq_data['question'][:50]}...")
            
            db.session.commit()
            print("\n🎉 Default FAQs added successfully!")
            
            # FAQ sayısını göster
            faq_count = FAQ.query.count()
            print(f"📊 Total FAQs in database: {faq_count}")
            
        except Exception as e:
            print(f"❌ Error adding FAQs: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_default_faqs() 