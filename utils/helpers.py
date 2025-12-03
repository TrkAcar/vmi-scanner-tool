import platform
import socket
import subprocess
import os
import time
import json
from datetime import datetime
from pathlib import Path

# MAC Veritabanı Cache
_MAC_VENDORS_CACHE = None

def load_mac_vendors():
    """MAC üretici veritabanını JSON'dan yükle (cache ile)"""
    global _MAC_VENDORS_CACHE
    
    if _MAC_VENDORS_CACHE is not None:
        return _MAC_VENDORS_CACHE
    
    try:
        # JSON dosyasının yolu
        data_dir = Path(__file__).parent.parent / 'data'
        json_file = data_dir / 'mac_vendors.json'
        
        # JSON'dan yükle
        with open(json_file, 'r', encoding='utf-8') as f:
            _MAC_VENDORS_CACHE = json.load(f)
        
        print(f"✓ MAC veritabanı yüklendi: {len(_MAC_VENDORS_CACHE)} prefix")
        return _MAC_VENDORS_CACHE
        
    except Exception as e:
        print(f"⚠ MAC veritabanı yüklenemedi: {e}")
        # Fallback: Boş dictionary
        _MAC_VENDORS_CACHE = {}
        return _MAC_VENDORS_CACHE

# Sistem Bilgisi
def get_system_info(scapy_available=False, pythonping_available=False):
    info = []
    info.append("🔧 Sistem Bilgisi:")
    info.append(f"   - İşletim Sistemi: {platform.system()} {platform.release()}")
    info.append(f"   - Python: {platform.python_version()}")
    info.append(f"   - Scapy Durumu: {'Kurulu' if scapy_available else 'Kurulu Değil'}")
    info.append(f"   - PythonPing: {'Kurulu' if pythonping_available else 'Kurulu Değil - ICMP ping için kurulum önerilir'}")
    
    if not pythonping_available:
        info.append("   💡 ICMP ping için: pip install pythonping")
    
    # Yetki kontrolü
    try:
        if os.name == 'posix' and os.geteuid() != 0:
            info.append("   - ⚠️  UYARI: Root yetkisi gerekebilir (ARP/Scapy için)")
        elif os.name == 'nt':
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                info.append("   - ⚠️  UYARI: Yönetici yetkisi gerekebilir")
            else:
                info.append("   - ✅ Yönetici yetkisi: Var")
    except:
        pass
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        info.append(f"   - Yerel IP: {local_ip}")
        info.append(f"   - Hostname: {hostname}")
    except:
        info.append(f"   - Ağ bilgileri alınamadı")
    
    return info

# Ping Fonksiyonları
def ping_cihaz(ip):
    """Gerçek ICMP ping - pythonping kullanarak"""
    try:
        from pythonping import ping
        # 1 paket, 2 saniye timeout
        result = ping(ip, count=1, timeout=2, verbose=False)
        return result.success()
    except ImportError:
        # pythonping kurulu değilse fallback
        return ping_cihaz_fallback(ip)
    except Exception as e:
        print(f"PythonPing hatası {ip}: {e}")
        # Hata durumunda fallback
        return ping_cihaz_fallback(ip)

def ping_cihaz_fallback(ip):
    """Geliştirilmiş subprocess ping (fallback)"""
    try:
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "1", "-w", "3000", ip]
        else:
            command = ["ping", "-c", "1", "-W", "3", ip]
            
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=4
        )
        
        # Gelişmiş başarı kontrolü
        output = (result.stdout + result.stderr).lower()
        
        success_indicators = [
            "ttl=", "time=", "bytes from", "reply from", "1 received"
        ]
        
        failure_indicators = [
            "request timed out", "destination host unreachable", 
            "100% packet loss", "0 received"
        ]
        
        # Returncode 0 ise ve hata göstergesi yoksa başarılı
        if result.returncode == 0:
            return not any(fail in output for fail in failure_indicators)
        
        # Returncode 0 değilse ama başarı göstergesi varsa
        return any(success in output for success in success_indicators)
        
    except subprocess.TimeoutExpired:
        return False
    except FileNotFoundError:
        print(f"Ping komutu bulunamadı")
        return False
    except Exception as e:
        print(f"Fallback ping hatası {ip}: {e}")
        return False

# Ağ Tespiti
def otomatik_ag_tespit(gui_instance):
    gui_instance.results_panel.log_ekle("🔄 Yerel ağ tespit ediliyor...")
    
    try:
        # Yerel IP'yi al
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # Ağ adresini hesapla (örnek: 192.168.1.100 -> 192.168.1.0/24)
        ip_parts = local_ip.split('.')
        network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        
        gui_instance.control_panel.network_entry.delete(0, "end")
        gui_instance.control_panel.network_entry.insert(0, network)
        
        gui_instance.results_panel.log_ekle(f"✅ Ağ tespit edildi: {network}")
        gui_instance.results_panel.log_ekle(f"📍 Yerel IP'niz: {local_ip}")
        gui_instance.control_panel.status_var.set(f"Tespit edilen ağ: {network}")
        
    except Exception as e:
        gui_instance.results_panel.log_ekle(f"❌ Ağ tespit edilemedi: {e}")
        # Varsayılan ağ
        gui_instance.control_panel.network_entry.delete(0, "end")
        gui_instance.control_panel.network_entry.insert(0, "192.168.1.0/24")
        gui_instance.results_panel.log_ekle("⚠️ Varsayılan ağ kullanılıyor: 192.168.1.0/24")

# MAC Adresi
def mac_adresi_al(ip):
    """Cross-platform MAC adresi alma - Geliştirilmiş"""
    try:
        # Önce ping atarak ARP tablosunu güncelle
        try:
            if platform.system().lower() == "windows":
                subprocess.run(["ping", "-n", "1", "-w", "500", ip], 
                             capture_output=True, timeout=2)
            else:
                subprocess.run(["ping", "-c", "1", "-W", "1", ip], 
                             capture_output=True, timeout=2)
        except:
            pass  # Ping başarısız olsa bile devam et
        
        # Kısa bir bekleme (ARP tablosunun güncellenmesi için)
        time.sleep(0.1)
        
        if platform.system().lower() == "windows":
            # Windows için - Daha detaylı parsing
            command = f"arp -a {ip}"
            output = subprocess.check_output(command, shell=True, encoding='latin-1', errors='ignore', timeout=3)
            
            # Windows ARP tablo formatını parse et
            for line in output.split('\n'):
                if ip in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if ip in part and i + 1 < len(parts):
                            mac = parts[i + 1]
                            # MAC adresi formatı kontrolü (XX-XX-XX-XX-XX-XX veya XX:XX:XX:XX:XX:XX)
                            if '-' in mac or ':' in mac:
                                if len(mac.replace('-', '').replace(':', '')) == 12:
                                    return mac.replace('-', ':').upper()
                        
        else:
            # Linux/macOS için - Daha detaylı parsing
            command = f"arp -n {ip}"
            output = subprocess.check_output(command, shell=True, encoding='utf-8', errors='ignore', timeout=3)
            
            for line in output.split('\n'):
                if ip in line:
                    parts = line.split()
                    for part in parts:
                        # MAC adresi formatı kontrolü (XX:XX:XX:XX:XX:XX)
                        if ':' in part and len(part.replace(':', '')) == 12:
                            return part.upper()
                        
    except subprocess.TimeoutExpired:
        print(f"MAC adresi alma timeout {ip}")
    except Exception as e:
        print(f"MAC adresi alınamadı {ip}: {e}")
    
    return "Bilinmiyor"

def mac_ureticisi_bul(mac):
    """MAC adresinden üreticiyi tahmin et"""
    vendors = load_mac_vendors()
    
    if not vendors:
        return "Bilinmiyor"
    
    # MAC adresini normalize et
    mac_clean = mac.upper().replace("-", ":").replace(".", ":")
    
    # İlk 8 karakteri al (XX:XX:XX formatı)
    if len(mac_clean) >= 8:
        prefix = mac_clean[:8]
        return vendors.get(prefix, "Bilinmiyor")
    
    return "Bilinmiyor"


# OS Tahmini - Gelişmiş
def os_tahmini_yap(cihaz, port_sonuclari):
    """Gelişmiş işletim sistemi tahmini - Port, MAC ve TTL bazlı"""
    
    # 1. ÖNCE PORT BAZLI TAHMİN (En güvenilir)
    if port_sonuclari and cihaz['ip'] in port_sonuclari and port_sonuclari[cihaz['ip']]:
        acik_portlar = [port for port, servis in port_sonuclari[cihaz['ip']]]
        
        # Windows imzaları (Öncelikli)
        if 3389 in acik_portlar:  # RDP
            if 445 in acik_portlar or 135 in acik_portlar:
                return "Windows Server"
            return "Windows (RDP)"
        
        if 445 in acik_portlar:  # SMB
            if 135 in acik_portlar and 139 in acik_portlar:
                return "Windows (Active Directory)"
            if 3389 in acik_portlar:
                return "Windows Server"
            return "Windows (SMB)"
        
        if 135 in acik_portlar and 139 in acik_portlar:
            return "Windows"
        
        if 1433 in acik_portlar:  # MSSQL
            return "Windows (SQL Server)"
        
        if 5985 in acik_portlar or 5986 in acik_portlar:  # WinRM
            return "Windows Server"
        
        # Linux/Unix imzaları
        if 22 in acik_portlar:  # SSH
            if 3306 in acik_portlar:  # MySQL
                return "Linux (MySQL Server)"
            if 5432 in acik_portlar:  # PostgreSQL
                return "Linux (PostgreSQL Server)"
            if 27017 in acik_portlar:  # MongoDB
                return "Linux (MongoDB Server)"
            if 6379 in acik_portlar:  # Redis
                return "Linux (Redis Server)"
            if 9200 in acik_portlar:  # Elasticsearch
                return "Linux (Elasticsearch)"
            if 111 in acik_portlar:  # RPC
                return "Linux/Unix (NFS)"
            if 2049 in acik_portlar:  # NFS
                return "Linux (NFS Server)"
            return "Linux/Unix (SSH)"
        
        # Web sunucu tespiti
        if 80 in acik_portlar or 443 in acik_portlar:
            if 8080 in acik_portlar or 8443 in acik_portlar:
                return "Web/App Server"
            if 3000 in acik_portlar:  # Node.js
                return "Linux (Node.js)"
            if 8000 in acik_portlar or 8888 in acik_portlar:
                return "Development Server"
            return "Web Server"
        
        # Veritabanı sunucuları
        if 3306 in acik_portlar:
            return "MySQL Server"
        if 5432 in acik_portlar:
            return "PostgreSQL Server"
        if 1521 in acik_portlar:
            return "Oracle Database"
        if 27017 in acik_portlar:
            return "MongoDB Server"
        
        # Diğer servisler
        if 21 in acik_portlar:
            return "FTP Server"
        if 23 in acik_portlar:
            return "Telnet Server (Eski)"
        if 25 in acik_portlar:
            return "Mail Server (SMTP)"
        if 53 in acik_portlar:
            return "DNS Server"
        if 110 in acik_portlar or 143 in acik_portlar:
            return "Mail Server"
        if 161 in acik_portlar or 162 in acik_portlar:
            return "Network Device (SNMP)"
        if 389 in acik_portlar or 636 in acik_portlar:
            return "LDAP Server"
        if 1723 in acik_portlar:
            return "VPN Server (PPTP)"
        if 5900 in acik_portlar:
            return "VNC Server"
        if 8080 in acik_portlar:
            return "Proxy/Web Server"
        if 9090 in acik_portlar:
            return "Management Interface"
    
    # 2. MAC BAZLI TAHMİN (Port bilgisi yoksa)
    if 'mac' in cihaz and cihaz['mac'] and cihaz['mac'] != "Bilinmiyor":
        mac_vendor = mac_ureticisi_bul(cihaz['mac'])
        
        # Mobil cihazlar
        if mac_vendor == "Apple":
            return "macOS/iOS"
        if mac_vendor in ["Samsung", "Xiaomi", "Huawei", "OnePlus", "Oppo", "Vivo"]:
            return "Android"
        
        # Bilgisayarlar
        if mac_vendor in ["Dell", "HP", "Lenovo", "Acer", "Toshiba"]:
            return "Windows/Linux PC"
        if mac_vendor == "ASUS":
            return "PC/Laptop"
        if mac_vendor == "Intel":
            return "Intel NUC/PC"
        
        # Ağ cihazları
        if mac_vendor in ["Cisco", "Juniper", "Arista"]:
            return "Network Switch/Router"
        if mac_vendor in ["Netgear", "TP-Link", "D-Link", "Linksys", "Asus"]:
            return "Router/Access Point"
        if mac_vendor in ["Ubiquiti", "MikroTik"]:
            return "Enterprise Network"
        
        # Sanallaştırma
        if mac_vendor == "VMware":
            return "VMware VM"
        if mac_vendor == "VirtualBox":
            return "VirtualBox VM"
        if mac_vendor == "Hyper-V":
            return "Hyper-V VM"
        if mac_vendor == "QEMU":
            return "QEMU/KVM VM"
        
        # IoT ve diğer cihazlar
        if mac_vendor in ["Raspberry", "Arduino"]:
            return "IoT Device (Linux)"
        if mac_vendor in ["Sony", "LG", "Panasonic"]:
            return "Smart TV/Console"
        if mac_vendor in ["Canon", "Epson", "HP"]:
            return "Printer/Scanner"
        
        # Bilinmeyen üretici ama MAC var
        if mac_vendor != "Bilinmeyen":
            return f"{mac_vendor}"
    
    # 3. TTL BAZLI TAHMİN (Gelecekte eklenebilir)
    # TTL 128 = Windows
    # TTL 64 = Linux/Unix
    # TTL 255 = Cisco/Network
    
    return "Bilinmeyen"

# Port İşlemleri
def port_listesi_olustur(port_input):
    """Port listesi oluştur - virgülle ayrılmış ve aralıkları destekler"""
    try:
        port_listesi = []
        for port_str in port_input.split(','):
            port_str = port_str.strip()
            if not port_str:
                continue
                
            if '-' in port_str:
                # Aralık formatı: 1-100
                start_end = port_str.split('-')
                if len(start_end) == 2:
                    start, end = map(int, start_end)
                    port_listesi.extend(range(start, end + 1))
            else:
                # Tek port
                port_listesi.append(int(port_str))
        
        # Tekilleştir ve sırala
        port_listesi = sorted(set(port_listesi))
        return port_listesi
        
    except ValueError as e:
        print(f"Port listesi oluşturma hatası: {e}")
        return []

# Raporlama
def nmap_stili_baslik(mesaj):
    """Nmap tarzı başlık oluştur"""
    return f"\n[{datetime.now().strftime('%H:%M:%S')}] >>> {mesaj}\n" + "="*60

def nmap_detay_ekle(cihaz, port_sonuclari=None):
    """Nmap benzeri detaylı cihaz bilgisi ekle"""
    detay = f"\n▶ CIHAZ DETAYI: {cihaz['ip']}\n"
    detay += "="*50 + "\n"
    detay += f"IP Adresi    : {cihaz['ip']}\n"
    detay += f"MAC Adresi   : {cihaz.get('mac', 'Bilinmiyor')}\n"
    
    # MAC üretici
    mac = cihaz.get('mac', 'Bilinmiyor')
    if mac and mac != 'Bilinmiyor':
        mac_uretici = mac_ureticisi_bul(mac)
        detay += f"MAC Üretici  : {mac_uretici}\n"
    else:
        detay += f"MAC Üretici  : -\n"
    
    detay += f"Durum        : {cihaz.get('durum', 'Bilinmiyor')}\n"
    
    # OS tahmini - port_sonuclari veya cihaz içindeki acik_portlar kullan
    if port_sonuclari is None:
        port_sonuclari = {}
    
    # Eğer cihazın kendi acik_portlar'ı varsa onu kullan
    if 'acik_portlar' in cihaz and cihaz['acik_portlar']:
        if cihaz['ip'] not in port_sonuclari:
            port_sonuclari[cihaz['ip']] = cihaz['acik_portlar']
    
    os_tahmin = os_tahmini_yap(cihaz, port_sonuclari)
    detay += f"OS Tahmini   : {os_tahmin}\n"
    
    # Açık portlar
    acik_portlar = None
    if port_sonuclari and cihaz['ip'] in port_sonuclari:
        acik_portlar = port_sonuclari[cihaz['ip']]
    elif 'acik_portlar' in cihaz:
        acik_portlar = cihaz['acik_portlar']
    
    if acik_portlar:
        detay += f"\nAÇIK PORTLAR ({len(acik_portlar)} tane):\n"
        detay += "PORT    STATE   SERVICE\n"
        detay += "----    -----   -------\n"
        for port, servis in acik_portlar:
            detay += f"{port:<8}open    {servis}\n"
    else:
        detay += "\nAÇIK PORTLAR: Port taraması yapılmadı\n"
    
    detay += "\n" + "="*50 + "\n"
    return detay

def tarama_suresi_hesapla(gui_instance):
    """Tarama süresini hesapla"""
    if not gui_instance.tarama_baslangic_zamani:
        return "Bilinmiyor"
    
    sure = time.time() - gui_instance.tarama_baslangic_zamani
    return f"{sure:.2f} saniye"