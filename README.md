<div align="center">

# ⚡ VMI Scanner Tool

### Profesyonel Ağ Tarama ve Güvenlik Analiz Aracı

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)](https://github.com)

[Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Ekran Görüntüleri](#-ekran-görüntüleri) • [Katkıda Bulunma](#-katkıda-bulunma)

</div>

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🌐 Ağ Tarama
- ✅ **3 Tarama Yöntemi**: Ping (ICMP), ARP (Scapy), TCP SYN
- ✅ **Otomatik Ağ Tespiti**: Yerel ağınızı otomatik bulur
- ✅ **Çoklu Thread**: Hızlı paralel tarama (20-50 thread)
- ✅ **254 IP Desteği**: /24 ağları tam tarama

### 🎯 Port Tarama
- ✅ **Geniş Aralık**: 1-65535 port desteği
- ✅ **Esnek Girdi**: Aralık (1-1000) veya liste (80,443,8080)
- ✅ **Hızlı Setler**: Standart, güvenlik, tüm portlar
- ✅ **Servis Tespiti**: Açık portların servislerini tanır

</td>
<td width="50%">

### 🔍 Cihaz Tanıma
- ✅ **MAC Üretici**: 1683 üretici veritabanı
- ✅ **OS Tahmini**: MAC ve port bazlı akıllı tahmin
- ✅ **Sanal Makine**: VMware, VirtualBox, Hyper-V tespiti
- ✅ **Mobil Cihaz**: Android, iOS tanıma

### 📊 Raporlama
- ✅ **Nmap Formatı**: Profesyonel detaylı raporlar
- ✅ **İstatistikler**: Cihaz sayısı, port dağılımı, OS analizi
- ✅ **Kaydetme**: TXT formatında rapor kaydetme
- ✅ **Gerçek Zamanlı**: Anlık sonuç görüntüleme

</td>
</tr>
</table>

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.7 veya üzeri
- tkinter (genellikle Python ile gelir)
- Windows / Linux / macOS

### Hızlı Başlangıç

```bash
# 1. Repoyu klonlayın
git clone https://github.com/TrkAcar/vmi-scanner-tool.git
cd vmi-scanner-tool

# 2. Bağımlılıkları kurun
pip install -r requirements.txt

# 3. Programı başlatın
python main.py
```

### Platform Bazlı Kurulum

<details>
<summary><b>🪟 Windows</b></summary>

```bash
# Yönetici olarak PowerShell açın
pip install -r requirements.txt
python main.py
```

**Not**: ARP tarama için yönetici yetkisi gereklidir.

</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Bağımlılıkları kurun
sudo apt-get install python3-tk
pip install -r requirements.txt

# Root yetkisiyle çalıştırın (ARP tarama için)
sudo python3 main.py
```

</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Homebrew ile Python kuruluysa tkinter zaten vardır
pip install -r requirements.txt

# Root yetkisiyle çalıştırın (ARP tarama için)
sudo python3 main.py
```

</details>

---

## 💻 Kullanım

### Hızlı Başlangıç

1. **Programı Başlatın**
   ```bash
   python main.py
   ```

2. **Ağı Tespit Edin**
   - "🔄 Ağı Otomatik Tespit Et" butonuna tıklayın
   - Yerel ağınız otomatik bulunur (örn: 192.168.1.0/24)

3. **Tarama Yapın**
   - Tarama yöntemini seçin (Ping/ARP/TCP)
   - "🔍 Ağ Taraması Başlat" butonuna tıklayın
   - Sonuçları bekleyin

4. **Port Tarayın** (Opsiyonel)
   - Port aralığı seçin veya hızlı set kullanın
   - "🎯 Port Taraması Başlat" butonuna tıklayın

5. **Rapor Görüntüleyin**
   - "📊 Detaylı Rapor" sekmesine geçin
   - Raporu kaydetmek için "💾 Raporu Kaydet" butonuna tıklayın

### Tarama Yöntemleri

#### 🔵 Ping Tarama (Önerilen)
- **Hız**: Orta (5-10 IP/saniye)
- **Yetki**: Gerekli değil
- **Uyumluluk**: Tüm platformlar
- **Kullanım**: Genel ağ keşfi

#### 🟢 ARP Tarama (En Hızlı)
- **Hız**: Çok hızlı (50-100 IP/saniye)
- **Yetki**: Yönetici/root gerekli
- **Uyumluluk**: Yerel ağ (LAN)
- **Kullanım**: Hızlı yerel tarama

#### 🟡 TCP Tarama
- **Hız**: Yavaş (1-2 IP/saniye)
- **Yetki**: Gerekli değil
- **Uyumluluk**: Tüm ağlar
- **Kullanım**: Firewall arkası cihazlar

### Port Setleri

| Set | Portlar | Kullanım |
|-----|---------|----------|
| 🚀 Hızlı | 1-1000 | Genel tarama |
| 🎯 Standart | 1-1024 | Yaygın servisler |
| 🔍 Tam | 1-65535 | Kapsamlı analiz |
| 🛡️ Güvenlik | 21,22,23,25,80,443,3389... | Güvenlik açıkları |

---

## 📁 Proje Yapısı

```
vmi-scanner-tool/
├── 📄 main.py                      # Ana program giriş noktası
├── 📄 requirements.txt             # Python bağımlılıkları
├── 📄 README.md                    # Proje dokümantasyonu
├── 📄 LICENSE                      # MIT Lisansı
├── 📄 .gitignore                   # Git ignore kuralları
│
├── 📁 core/                        # Ana işlevsellik modülleri
│   ├── scanner.py                 # Ağ tarama motoru
│   ├── port_scanner.py            # Port tarama işlemleri
│   ├── network_tools.py           # Ağ araçları (ping, ARP, TCP)
│   └── report_generator.py        # Rapor oluşturma ve formatlama
│
├── 📁 gui/                         # Grafik kullanıcı arayüzü
│   ├── main_window.py             # Ana pencere ve layout
│   └── widgets.py                 # Özel GUI bileşenleri
│
├── 📁 utils/                       # Yardımcı araçlar
│   ├── helpers.py                 # Yardımcı fonksiyonlar
│   └── logger.py                  # Debug logger sistemi
│
└── 📁 data/                        # Veri dosyaları
    └── mac_vendors.json           # MAC üretici veritabanı (1683 prefix)
```

**Toplam**: 1,675 satır kod | 12 Python modülü | 64.1 KB

---

## 🔒 Güvenlik

### ⚠️ Önemli Uyarılar

1. **Yasal Kullanım**
   - Sadece kendi ağınızda kullanın
   - İzinsiz ağ taraması yasadışıdır
   - Kurumsal ağlarda IT departmanından izin alın

2. **Yönetici Yetkisi**
   - ARP tarama için gerekli
   - Dikkatli kullanın
   - Gereksiz yere yönetici olarak çalıştırmayın

3. **Ağ Güvenliği**
   - Port tarama IDS/IPS tetikleyebilir
   - Agresif taramalar ağı yavaşlatabilir
   - Üretim ortamlarında dikkatli olun

### 🛡️ Güvenli Kullanım

```bash
# Test ortamında
python main.py

# Sadece ping tarama kullanın
# Port taramayı dikkatli yapın
# Sonuçları güvenli saklayın
```

---

## 🐛 Sorun Giderme

### Program açılmıyor
```bash
# Python versiyonunu kontrol edin
python --version  # 3.7+ olmalı

# Tkinter kurulu mu?
python -c "import tkinter"
```

### Tarama çalışmıyor
- Ağ bağlantınızı kontrol edin
- Firewall ayarlarını kontrol edin
- Yönetici yetkisiyle çalıştırın (ARP için)

### Cihazlar görünmüyor
- Ping tarama yerine ARP deneyin
- Hedef ağı kontrol edin
- Debug konsolunu inceleyin

---

## 📸 Ekran Görüntüleri

<details>
<summary><b>🖼️ Ekran Görüntülerini Göster</b></summary>

> **Not**: Ekran görüntüleri yakında eklenecek. Projeyi çalıştırarak arayüzü görebilirsiniz.

</details>

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Projeye katkıda bulunmak için:

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

### Geliştirme Fikirleri
- [ ] Web arayüzü desteği
- [ ] Zafiyet tarama modülü
- [ ] Otomatik rapor e-posta gönderimi
- [ ] Çoklu ağ tarama desteği
- [ ] API entegrasyonu

---

## 📝 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

## ⚠️ Yasal Uyarı

Bu araç yalnızca **eğitim ve yasal güvenlik testleri** için tasarlanmıştır. 

- ✅ Kendi ağınızda kullanabilirsiniz
- ✅ İzin aldığınız sistemlerde test edebilirsiniz
- ❌ İzinsiz ağ taraması **yasadışıdır**
- ❌ Kötü amaçlı kullanım **kesinlikle yasaktır**

**Kullanıcı sorumluluğu**: Bu aracın kullanımından kaynaklanan tüm sorumluluk kullanıcıya aittir.

---

## 📞 İletişim & Destek

- 🐛 **Bug Bildirimi**: [Issues](https://github.com/TrkAcar/vmi-scanner-tool/issues) sayfasını kullanın
- 💡 **Özellik İsteği**: [Issues](https://github.com/TrkAcar/vmi-scanner-tool/issues) sayfasından öneride bulunun
- ⭐ **Beğendiyseniz**: Projeye yıldız vermeyi unutmayın!

---

<div align="center">

**⚡ VMI Scanner Tool - Profesyonel Ağ Tarama Aracı**

Made with ❤️ by VMI Team

[![GitHub stars](https://img.shields.io/github/stars/TrkAcar/vmi-scanner-tool?style=social)](https://github.com/TrkAcar/vmi-scanner-tool/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/TrkAcar/vmi-scanner-tool?style=social)](https://github.com/TrkAcar/vmi-scanner-tool/network/members)

</div>
