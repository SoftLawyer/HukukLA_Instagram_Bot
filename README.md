# HukukLA Instagram & Carousel Otomasyon Sistemi

Bu depo, HukukLA için Instagram içerikleri (Story ve çok sayfalı Carousel gönderileri) üreten yapay zeka destekli profesyonel bir otomasyon sistemidir.

---

## 🚀 Instagram Carousel (Kaydırmalı Gönderi) Üreticisi

Kullanıcı **"Sıradaki"** dediğinde veya `generate_next.py` komutu çalıştırıldığında:
1. `carousel_topics.json` dosyasından bekleyen sıradaki konuyu alır.
2. Instagram 4:5 (1080x1350 px) boyutunda, modern koyu temalı, yüksek kaliteli slaytlar üretir:
   - **Slide 1:** Kapak / Kanca (Hook), Kategori Rozeti, Merak Uyandıran Alt Başlık
   - **Slide 2-5:** 3 Büyük Hata / Stratejik Hamleler / Problem-Çözüm-Taktik Kartları
   - **Slide 6:** Aksiyon / Kaydet-Paylaş ve HukukLA Uygulama Tanıtım Kartı (CTA)
3. Görselleri doğrudan kullanıcının **İndirilenler (`~/Downloads/<Konu_Basligi>/`)** klasörüne otomatik olarak kaydeder.
4. Konunun durumunu `completed` olarak işaretler.

### Hızlı Kullanım Komutları

```bash
# Sıradaki konuyu otomatik üret ve İndirilenler'e kaydet:
./venv/bin/python generate_next.py

# Tüm 20 konunun durumunu listele:
./venv/bin/python generate_next.py --list

# Belirli bir konuyu üret (Örn: Konu 3):
./venv/bin/python generate_next.py --id 3

# Tüm konuları sıfırla (yeniden bekliyor durumuna getir):
./venv/bin/python generate_next.py --reset
```

---

## 📚 Başlangıç 20 Konu Havuzu

1. **Deneme Sınavlarında Netleri Dibe Çeken 3 Büyük Hata** *(HMGS Strateji)*
2. **Hukuk Fakültesinde Kimsenin Bahsetmediği Maden: KVKK ve Veri Hukuku Uzmanlığı** *(2026 Kariyer)*
3. **HMGS'de 155 Dakikan Var Ama Gerçekte Sadece 113 Dakikan Var!** *(Zaman Yönetimi)*
4. **Türk Hukuk Diplomasıyla Yurt Dışında Çalışmanın 4 Küresel Rotası** *(Küresel Kariyer)*
5. **Medeni Hukuk'u 'Kolay Ders' Sananların HMGS'de Düştüğü 4 Eleyici Tuzak** *(Ders Analizi)*
6. **'Yapay Zeka Hukukçuları İşsiz Bırakacak' Diyenlerin Yanıldığı 3 Nokta** *(Hukuk & Teknoloji)*
7. **Fakülte Notlarıyla Sınavı Geçeceğini Sananların Başına Gelecek Acı Gerçek** *(Gerçeklerle Yüzleş)*
8. **HMGS'de Adayların %70'ini Ters Köşe Yapacak O 'Büyük Eleyici' Ders: İYUK** *(Büyük Eleyici Ders)*
9. **'Avukatlık Bitti' Diyenler Türkiye Vergi Rekortmenleri Listesine Baksın** *(Kariyer Gerçekleri)*
10. **Ceza Genel Hükümlerde Her Yıl Binlerce Kişiyi Eleyen 3 Kritik Kavram** *(Puan Avcısı)*
11. **Hukuk Fakültesinin Sana Söylemediği ve 5 Yılını Çöpe Atan O 'Büyük İllüzyon'** *(Gerçeklerle Yüzleş)*
12. **Sınava Sayılı Günler Kala Netleri Zıplatacak 3 Acil Durum Hamlesi** *(Son Düzlük Taktiği)*
13. **Hukuk İngilizcesi Bilenlerin Ayda 3.000$+ Kazandığı Alan: SaaS ve Sözleşmeler** *(Küresel Kariyer)*
14. **Anayasa Hukuku'nda En Çok Puan Kaybettiren 4 'Sayısal Süre' ve Nisap Tuzağı** *(Puan Avcısı)*
15. **HMGS'ye Gerçekten Hazır Mısın? Sınav Kazandıran 4 Maddelik Check-List** *(Kontrol Listesi)*
16. **Stajyer ve Yeni Mezunların İlk Yılında Düştüğü 3 Büyük 'Kariyer İntiharı' Hatası** *(Genç Avukat Rehberi)*
17. **Borçlar Hukuku Genel Hükümler: Sınavda Zaman Çalan 3 Soru Tipi ve Pratik Çözümü** *(HMGS Taktik)*
18. **Günde 10 Saat Çalışıp Neti Artmayanların Ortak Kusuru: Pasif Okuma Tuzağı** *(Çalışma Metodolojisi)*
19. **Hukukçular İçin Finansal Okuryazarlık: Ticaret ve Şirketler Hukukunda Neden Az İsim Zirvede?** *(Kariyer Vizyonu)*
20. **HMGS Sınav Günü Masada Paniklememek İçin 24 Saat Önceden Uygulaman Gereken Protokol** *(Sınav Psikolojisi)*

---

## 🛠️ Teknik Altyapı
- **Dil & Motor:** Python 3 + Playwright (Headless Chromium)
- **Tasarım:** Tailwind CSS + Google Fonts (Playfair Display, Plus Jakarta Sans, Outfit)
- **Çözünürlük:** 1080 x 1350 px (Instagram 4:5 Portrait Standartı)
- **Kayıt Yolu:** `~/Downloads/<Konu_Klasoru>/slide_X.png`
