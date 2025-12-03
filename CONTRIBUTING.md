# Katkıda Bulunma Rehberi

VMI Scanner Tool projesine katkıda bulunmak istediğiniz için teşekkür ederiz! 🎉

## 🚀 Nasıl Katkıda Bulunurum?

### 1. Repoyu Fork Edin
GitHub'da sağ üstteki "Fork" butonuna tıklayın.

### 2. Yerel Kopyanızı Oluşturun
```bash
git clone https://github.com/KULLANICI_ADINIZ/vmi-scanner-tool.git
cd vmi-scanner-tool
```

### 3. Yeni Bir Branch Oluşturun
```bash
git checkout -b feature/yeni-ozellik
# veya
git checkout -b fix/hata-duzeltmesi
```

### 4. Değişikliklerinizi Yapın
- Kod yazarken Python PEP 8 standartlarına uyun
- Anlamlı commit mesajları yazın
- Kodunuzu test edin

### 5. Commit Edin
```bash
git add .
git commit -m "feat: yeni özellik eklendi"
```

### 6. Push Edin
```bash
git push origin feature/yeni-ozellik
```

### 7. Pull Request Oluşturun
GitHub'da reponuza gidin ve "New Pull Request" butonuna tıklayın.

## 📝 Commit Mesaj Formatı

```
<tip>: <kısa açıklama>

<detaylı açıklama (opsiyonel)>
```

**Tipler:**
- `feat`: Yeni özellik
- `fix`: Hata düzeltmesi
- `docs`: Dokümantasyon değişikliği
- `style`: Kod formatı (işlevselliği etkilemeyen)
- `refactor`: Kod yeniden yapılandırma
- `test`: Test ekleme/düzeltme
- `chore`: Bakım işleri

**Örnekler:**
```
feat: ARP tarama hızlandırıldı
fix: MAC adresi parse hatası düzeltildi
docs: README kurulum bölümü güncellendi
```

## 🐛 Bug Bildirimi

Bug bulduğunuzda lütfen şunları ekleyin:
- İşletim sistemi ve Python versiyonu
- Hatanın nasıl oluştuğu (adım adım)
- Beklenen davranış
- Gerçekleşen davranış
- Hata mesajları (varsa)

## 💡 Özellik İsteği

Yeni özellik önerirken:
- Özelliğin ne işe yarayacağını açıklayın
- Kullanım senaryosu verin
- Mümkünse örnek kod/tasarım ekleyin

## ✅ Kod Standartları

- Python 3.7+ uyumlu kod yazın
- Fonksiyonlara docstring ekleyin
- Değişken isimleri açıklayıcı olsun
- Karmaşık kısımlara yorum ekleyin
- Türkçe veya İngilizce yorum kullanabilirsiniz

## 🧪 Test

Değişikliklerinizi test edin:
```bash
python main.py
```

## 📜 Lisans

Katkıda bulunarak, kodunuzun MIT Lisansı altında yayınlanmasını kabul etmiş olursunuz.

## 🙏 Teşekkürler!

Her türlü katkı değerlidir - kod, dokümantasyon, bug raporu, özellik önerisi...

Hepinize teşekkürler! ❤️
