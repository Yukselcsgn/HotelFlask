# 🏨 HotelFlask - Otel Rezervasyon Sistemi

Modern Flask tabanlı otel rezervasyon sistemi. SendGrid ile profesyonel e-posta gönderimi.

## 🚀 Özellikler

- ✅ Rezervasyon formu
- ✅ SendGrid ile HTML e-posta gönderimi
- ✅ Güzel tasarımlı e-postalar
- ✅ Admin paneli
- ✅ Responsive tasarım
- ✅ SQLite veritabanı

## 📧 SendGrid E-posta Kurulumu

### Adım 1: SendGrid Hesabı Oluşturma
1. [SendGrid.com](https://sendgrid.com) adresine gidin
2. **"Start for Free"** butonuna tıklayın
3. E-posta adresinizi girin ve hesap oluşturun
4. E-posta adresinizi doğrulayın

### Adım 2: API Key Oluşturma
1. SendGrid Dashboard'da **"Settings"** → **"API Keys"** bölümüne gidin
2. **"Create API Key"** butonuna tıklayın
3. API Key adı: `HotelFlask Email`
4. **"Full Access"** seçeneğini seçin
5. **"Create & View"** butonuna tıklayın
6. **API Key'i kopyalayın** (bu sadece bir kez gösterilir!)

### Adım 3: Gönderen E-posta Doğrulama
1. **"Settings"** → **"Sender Authentication"** bölümüne gidin
2. **"Single Sender Verification"** sekmesine tıklayın
3. **"Add New Sender"** butonuna tıklayın
4. Formu doldurun ve e-posta adresinizi doğrulayın

### Adım 4: Proje Ayarları
1. `.env` dosyası oluşturun:
   ```bash
   cp env_example.txt .env
   ```

2. `.env` dosyasını düzenleyin:
   ```env
   SENDGRID_API_KEY=your-sendgrid-api-key-here
   SENDGRID_FROM_EMAIL=your-verified-email@yourdomain.com
   OWNER_EMAIL=otel.sahibi@yourdomain.com
   ```

## 🛠️ Kurulum

### 1. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 2. Veritabanını Başlatın
```bash
flask db init
flask db migrate
flask db upgrade
```

### 3. E-posta Ayarlarını Yapın
- Yukarıdaki SendGrid kurulum talimatlarını takip edin
- `.env` dosyasını oluşturun ve ayarları yapın

### 4. Uygulamayı Çalıştırın
```bash
python run.py
```

## 🌐 Kullanım

Uygulama çalıştığında şu adreslerde erişebilirsiniz:

- **Anasayfa:** http://localhost:5000
- **Rezervasyon:** http://localhost:5000/reserve
- **Admin Panel:** http://localhost:5000/admin
- **Odalar:** http://localhost:5000/rooms

## 📧 E-posta Örnekleri

### Müşteriye Gönderilen E-posta
- ✅ Rezervasyon onayı
- 🏨 Otel bilgileri
- 📅 Tarih detayları
- 📞 İletişim bilgileri

### Otel Sahibine Gönderilen E-posta
- 🔔 Yeni rezervasyon bildirimi
- 👤 Müşteri bilgileri
- 📋 Rezervasyon detayları
- ⏰ Rezervasyon tarihi

## 📁 Proje Yapısı

```
HotelFlask/
├── app/
│   ├── models/          # Veritabanı modelleri
│   ├── routes/          # Route'lar
│   ├── services/        # E-posta servisleri
│   ├── static/          # CSS, JS dosyaları
│   └── templates/       # HTML şablonları
├── migrations/          # Veritabanı migrasyonları
├── config.py           # Konfigürasyon
├── run.py             # Uygulama başlatıcı
└── requirements.txt   # Python bağımlılıkları
```

## 🐛 Sorun Giderme

### E-posta Gönderilmiyor
1. SendGrid API Key'in doğru olduğunu kontrol edin
2. Gönderen e-posta adresinin doğrulandığını kontrol edin
3. `.env` dosyasındaki ayarları kontrol edin

### Detaylı Kurulum Rehberi
Tam adım adım kurulum için `SENDGRID_KURULUM.md` dosyasını inceleyin.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
