# 📧 SendGrid E-posta Kurulum Rehberi

Bu rehber, HotelFlask projenizde SendGrid ile e-posta gönderimi kurmanızı sağlar.

## 🎯 Adım 1: SendGrid Hesabı Oluşturma

### 1.1 SendGrid'e Kayıt Olun
1. [SendGrid.com](https://sendgrid.com) adresine gidin
2. **"Start for Free"** butonuna tıklayın
3. E-posta adresinizi girin ve hesap oluşturun
4. E-posta adresinizi doğrulayın

### 1.2 SendGrid Dashboard'a Giriş
- Oluşturduğunuz hesap bilgileriyle giriş yapın
- Dashboard'da **"Settings"** → **"Sender Authentication"** bölümüne gidin

## 🔑 Adım 2: API Key Oluşturma

### 2.1 API Key Oluşturun
1. SendGrid Dashboard'da **"Settings"** → **"API Keys"** bölümüne gidin
2. **"Create API Key"** butonuna tıklayın
3. API Key adı: `HotelFlask Email`
4. **"Full Access"** seçeneğini seçin
5. **"Create & View"** butonuna tıklayın
6. **API Key'i kopyalayın** (bu sadece bir kez gösterilir!)

### 2.2 API Key'i Güvenli Saklayın
- Kopyaladığınız API Key'i güvenli bir yere kaydedin
- Bu key'i kimseyle paylaşmayın

## 📧 Adım 3: Gönderen E-posta Doğrulama

### 3.1 Single Sender Verification
1. **"Settings"** → **"Sender Authentication"** bölümüne gidin
2. **"Single Sender Verification"** sekmesine tıklayın
3. **"Add New Sender"** butonuna tıklayın
4. Formu doldurun:
   - **From Name:** `Otelimiz`
   - **From Email Address:** `info@yourdomain.com` (kendi e-posta adresiniz)
   - **Company Name:** `Otelimiz`
   - **Address:** Otel adresiniz
   - **City:** Şehir
   - **Country:** Ülke
5. **"Create"** butonuna tıklayın
6. E-posta adresinize gelen doğrulama e-postasını açın
7. **"Verify Single Sender"** linkine tıklayın

## ⚙️ Adım 4: Proje Ayarları

### 4.1 .env Dosyası Oluşturun
Proje klasörünüzde `.env` dosyası oluşturun:

```bash
# Windows PowerShell'de:
New-Item -Path ".env" -ItemType File
```

### 4.2 .env Dosyasını Düzenleyin
`.env` dosyasını notepad veya başka bir editörle açın ve şu içeriği ekleyin:

```env
# Flask Uygulama Ayarları
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Veritabanı Ayarları
DATABASE_URL=sqlite:///site.db

# SendGrid E-posta Ayarları
SENDGRID_API_KEY=your-sendgrid-api-key-here
SENDGRID_FROM_EMAIL=your-verified-email@yourdomain.com
OWNER_EMAIL=otel.sahibi@yourdomain.com
```

### 4.3 Değerleri Değiştirin
- `your-sendgrid-api-key-here` → Adım 2'de aldığınız API Key
- `your-verified-email@yourdomain.com` → Adım 3'te doğruladığınız e-posta
- `otel.sahibi@yourdomain.com` → Otel sahibinin e-posta adresi

## 🐍 Adım 5: Python Kurulumu

### 5.1 Python'u Yükleyin
1. [python.org/downloads](https://www.python.org/downloads/) adresine gidin
2. **"Download Python 3.11.x"** butonuna tıklayın
3. İndirilen dosyayı çalıştırın
4. **"Add Python to PATH"** seçeneğini işaretleyin
5. **"Install Now"** butonuna tıklayın

### 5.2 Kurulumu Kontrol Edin
PowerShell'i yeniden başlatın ve şu komutu çalıştırın:
```powershell
python --version
```

## 📦 Adım 6: Proje Bağımlılıklarını Yükleyin

### 6.1 Bağımlılıkları Yükleyin
Proje klasörünüzde şu komutu çalıştırın:
```powershell
pip install -r requirements.txt
```

## 🗄️ Adım 7: Veritabanını Başlatın

### 7.1 Veritabanını Oluşturun
```powershell
flask db init
flask db migrate
flask db upgrade
```

## 🚀 Adım 8: Uygulamayı Çalıştırın

### 8.1 Uygulamayı Başlatın
```powershell
python run.py
```

### 8.2 Test Edin
1. Tarayıcınızda `http://localhost:5000` adresine gidin
2. **"Rezervasyon"** sayfasına gidin
3. Bir rezervasyon yapın
4. E-posta adresinizi kontrol edin

## ✅ Test Sonuçları

Başarılı kurulum sonrasında şunları göreceksiniz:

### Müşteriye Gönderilen E-posta:
- ✅ Güzel HTML formatında onay e-postası
- 🏨 Otel logosu ve bilgileri
- 📅 Rezervasyon detayları
- 📞 İletişim bilgileri

### Otel Sahibine Gönderilen E-posta:
- 🔔 Yeni rezervasyon bildirimi
- 👤 Müşteri bilgileri
- 📋 Rezervasyon detayları
- ⏰ Rezervasyon tarihi

## 🐛 Sorun Giderme

### E-posta Gönderilmiyor
1. **API Key kontrolü:**
   - SendGrid Dashboard'da API Key'in aktif olduğunu kontrol edin
   - `.env` dosyasındaki API Key'in doğru olduğunu kontrol edin

2. **Gönderen e-posta kontrolü:**
   - SendGrid'de e-posta adresinizin doğrulandığını kontrol edin
   - `.env` dosyasındaki `SENDGRID_FROM_EMAIL` değerinin doğru olduğunu kontrol edin

3. **Log kontrolü:**
   - Uygulama çalışırken konsol çıktısını kontrol edin
   - Hata mesajlarını okuyun

### SendGrid Dashboard'da E-posta Görünmüyor
1. **Activity** bölümüne gidin
2. **"Email Activity"** sekmesini kontrol edin
3. E-postaların gönderilip gönderilmediğini görün

## 📞 Destek

Sorun yaşarsanız:
1. SendGrid Dashboard'da **"Support"** bölümünü kontrol edin
2. API Key'inizin doğru olduğunu tekrar kontrol edin
3. E-posta adresinizin doğrulandığını kontrol edin

## 🎉 Tebrikler!

SendGrid kurulumunuz tamamlandı! Artık rezervasyon yapıldığında güzel HTML formatında e-postalar gönderilecek. 