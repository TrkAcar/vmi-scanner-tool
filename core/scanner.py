import threading
import time
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed
from .network_tools import ping_tarama, arp_tarama, tcp_tarama
from utils.helpers import nmap_stili_baslik, ping_cihaz

def start_network_scan(gui_instance):
    if gui_instance.tarama_devam_ediyor:
        return
    
    hedef_ag = gui_instance.control_panel.network_entry.get().strip()
    if not hedef_ag:
        messagebox.showerror("Hata", "Lütfen hedef ağı giriniz!")
        return
    
    # GUI durumunu güncelle - HEMEN ana thread'de
    gui_instance.tarama_baslangic_zamani = time.time()
    gui_instance.tarama_devam_ediyor = True
    gui_instance.update_ui_state(scanning=True)
    
    # Temizle - HEMEN ana thread'de
    gui_instance.results_panel.temizle()
    
    yontem = gui_instance.control_panel.scan_method.get()
    
    # Nmap stili başlangıç - HEMEN ana thread'de
    gui_instance.results_panel.log_ekle(nmap_stili_baslik(f"TARAMA BAŞLATILDI: {hedef_ag}"))
    gui_instance.results_panel.log_ekle(f"Tarama Yöntemi : {yontem.upper()}")
    gui_instance.results_panel.log_ekle(f"Başlangıç Zamanı: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    gui_instance.results_panel.log_ekle("Tarama devam ediyor...")
    
    gui_instance.control_panel.status_var.set(f"Tarama yapılıyor: {hedef_ag}")
    
    # Thread'de tarama başlat - ASENKRON
    thread = threading.Thread(target=ag_taramasi_islemi, args=(gui_instance, hedef_ag, yontem))
    thread.daemon = True  # BU SATIR ÇOK ÖNEMLİ!
    thread.start()

def ag_taramasi_islemi(gui_instance, hedef_ag, yontem):
    """Bu fonksiyon arka plan thread'inde çalışacak"""
    try:
        print(f"Tarama thread'i başlatıldı: {hedef_ag} - {yontem}")
        
        if yontem == "arp" and gui_instance.SCAPY_AVAILABLE:
            print("ARP tarama yöntemi seçildi")
            cihazlar = arp_tarama(gui_instance, hedef_ag)
        elif yontem == "tcp":
            print("TCP tarama yöntemi seçildi")
            cihazlar = tcp_tarama(gui_instance, hedef_ag)
        else:
            print("Ping tarama yöntemi seçildi")
            cihazlar = ping_tarama(gui_instance, hedef_ag)
        
        gui_instance.bulunan_cihazlar = cihazlar
        print(f"Tarama tamamlandı: {len(cihazlar)} cihaz bulundu")
        
        # GUI güncelleme - ana thread'e geri dön
        gui_instance.root.after(0, tarama_tamamlandi, gui_instance, cihazlar)
        
    except Exception as e:
        print(f"Thread hatası: {str(e)}")
        gui_instance.root.after(0, tarama_hatasi, gui_instance, str(e))

def tarama_tamamlandi(gui_instance, cihazlar):
    """Bu fonksiyon ANA thread'de çalışacak"""
    gui_instance.tarama_devam_ediyor = False
    gui_instance.update_ui_state(scanning=False)
    
    tarama_suresi = tarama_suresi_hesapla(gui_instance)
    
    gui_instance.results_panel.log_ekle(nmap_stili_baslik("TARAMA TAMAMLANDI"))
    gui_instance.results_panel.log_ekle(f"🎉 Tarama tamamlandı! Toplam {len(cihazlar)} cihaz bulundu.")
    gui_instance.results_panel.log_ekle(f"⏱️  Tarama Süresi: {tarama_suresi}")
    gui_instance.control_panel.status_var.set(f"Tarama tamamlandı - {len(cihazlar)} cihaz - {tarama_suresi}")
    
    if len(cihazlar) == 0:
        gui_instance.results_panel.log_ekle("❌ Hiç cihaz bulunamadı. Ağ adresinizi kontrol edin.")
        gui_instance.results_panel.log_ekle("💡 İpucu: 'Test Et' butonu ile önce kendi ağınızı test edin.")
    else:
        # Otomatik rapor oluştur
        gui_instance.root.after(1000, gui_instance.rapor_olustur)

def tarama_hatasi(gui_instance, hata):
    """Bu fonksiyon ANA thread'de çalışacak"""
    gui_instance.tarama_devam_ediyor = False
    gui_instance.update_ui_state(scanning=False)
    
    gui_instance.results_panel.log_ekle(f"\n❌ HATA: {hata}")
    gui_instance.control_panel.status_var.set("Hata oluştu")

def tarama_suresi_hesapla(gui_instance):
    if not gui_instance.tarama_baslangic_zamani:
        return "Bilinmiyor"
    
    sure = time.time() - gui_instance.tarama_baslangic_zamani
    return f"{sure:.2f} saniye"

# Diğer fonksiyonlar aynı kalacak...
def start_port_scan(gui_instance):
    from .port_scanner import start_port_scan as start_port_scan_main
    start_port_scan_main(gui_instance)

def test_tarama(gui_instance):
    """Test taraması - thread'de çalışsın"""
    def test_islemi():
        gui_instance.results_panel.log_ekle("🧪 Test taraması başlatılıyor...")
        
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            ip_parts = local_ip.split('.')
            gateway = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1"
            
            test_ips = [local_ip, gateway, "127.0.0.1"]
            
            gui_instance.root.after(0, lambda: gui_instance.results_panel.log_ekle(f"🧪 Test IP'leri: {', '.join(test_ips)}"))
            
            for test_ip in test_ips:
                gui_instance.root.after(0, lambda ip=test_ip: gui_instance.results_panel.log_ekle(f"🔍 Test: {ip} taranıyor..."))
                
                if ping_cihaz(test_ip):
                    gui_instance.root.after(0, lambda ip=test_ip: gui_instance.results_panel.log_ekle(f"✅ {ip} - ERİŞİLEBİLİR"))
                    gui_instance.root.after(0, lambda ip=test_ip: gui_instance.results_panel.cihaz_ekle_guncelle(ip, "Test Cihazı", "Erişilebilir", "", "Test"))
                else:
                    gui_instance.root.after(0, lambda ip=test_ip: gui_instance.results_panel.log_ekle(f"❌ {ip} - ERİŞİLEMEZ"))
            
            gui_instance.root.after(0, lambda: gui_instance.results_panel.log_ekle("🧪 Test taraması tamamlandı"))
            
        except Exception as e:
            gui_instance.root.after(0, lambda: gui_instance.results_panel.log_ekle(f"❌ Test hatası: {e}"))
    
    # Testi thread'de çalıştır
    thread = threading.Thread(target=test_islemi)
    thread.daemon = True
    thread.start()