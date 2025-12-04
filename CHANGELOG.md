# Changelog

Projedeki tüm önemli değişiklikler bu dosyada belgelenir.

Format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardına dayanır.

## [3.0.0] - 2025-01-12

### ✨ Eklenenler
- 🎨 Modern GUI arayüzü (tkinter)
- 🌐 3 farklı tarama yöntemi (Ping, ARP, TCP)
- 🎯 Gelişmiş port tarama (1-65535)
- 🔍 MAC üretici tanıma (1683 prefix veritabanı)
- 🖥️ Akıllı OS tahmini (MAC + Port bazlı)
- 📊 Nmap formatında detaylı raporlama
- 🐍 Debug konsolu ve logger sistemi
- 💾 Rapor kaydetme özelliği
- 🔄 Otomatik ağ tespiti
- ⚡ Çoklu thread desteği (20-50 thread)

### 🔧 İyileştirmeler
- MAC veritabanı JSON formatına taşındı
- Kod yapısı modüler hale getirildi
- Performans optimizasyonları
- Hata yönetimi iyileştirildi
- Cross-platform uyumluluk artırıldı

### 📝 Dokümantasyon
- Kapsamlı README.md
- Kurulum rehberi
- Kullanım örnekleri
- Güvenlik uyarıları

### 🐛 Düzeltmeler
- MAC adresi parse hataları düzeltildi
- Thread güvenliği iyileştirildi
- GUI donma sorunları çözüldü
- Port tarama timeout sorunları giderildi

## [2.0.0] - 2025-04-10

### ✨ Eklenenler
- Temel ağ tarama
- Port tarama
- Basit raporlama

## [1.0.0] - 2025-02-10

### ✨ Eklenenler
- İlk sürüm
- Temel ping tarama
- Konsol arayüzü

---

**Format Açıklaması:**
- `✨ Eklenenler`: Yeni özellikler
- `🔧 İyileştirmeler`: Mevcut özelliklerde iyileştirmeler
- `🐛 Düzeltmeler`: Bug düzeltmeleri
- `📝 Dokümantasyon`: Dokümantasyon değişiklikleri
- `⚠️ Kaldırılanlar`: Kaldırılan özellikler
- `🔒 Güvenlik`: Güvenlik güncellemeleri
