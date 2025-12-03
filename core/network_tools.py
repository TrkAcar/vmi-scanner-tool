import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
from utils.helpers import ping_cihaz, mac_adresi_al, os_tahmini_yap, mac_ureticisi_bul

def ping_tarama(gui_instance, hedef_ag):
    print("Ping tarama başlatılıyor...")
    
    try:
        ag = ipaddress.IPv4Network(hedef_ag, strict=False)
        canli_cihazlar = []
        ip_listesi = list(ag.hosts())[:254]  # Sadece ilk 254 IP
        
        print(f"Taranacak IP sayısı: {len(ip_listesi)}")
        
        # Thread sayısını sınırla (daha az thread = daha az donma)
        max_workers = min(20, len(ip_listesi))  # 20 thread'den fazla olmasın
        
        def ip_kontrol(ip):
            if not gui_instance.tarama_devam_ediyor:
                return None
                
            ip_str = str(ip)
            
            if ping_cihaz(ip_str):
                mac = mac_adresi_al(ip_str)
                return {
                    "ip": ip_str, 
                    "mac": mac, 
                    "acik_portlar": [],
                    "durum": "Canlı"
                }
            return None
        
        # ThreadPool ile paralel tarama - DAHA OPTIMIZE
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {executor.submit(ip_kontrol, ip): ip for ip in ip_listesi}
            
            completed = 0
            for future in as_completed(future_to_ip):
                if not gui_instance.tarama_devam_ediyor:
                    executor.shutdown(wait=False)  # Hemen durdur
                    break
                    
                completed += 1
                ip = future_to_ip[future]
                
                # İlerleme durumunu güncelle - ana thread'e gönder
                if completed % 5 == 0:  # Her 5 IP'de bir güncelle
                    gui_instance.root.after(0, lambda c=completed, t=len(ip_listesi): 
                        gui_instance.control_panel.status_var.set(f"Taranıyor: {c}/{t} IP"))
                
                try:
                    cihaz = future.result(timeout=10)  # Timeout ekle
                    if cihaz:
                        canli_cihazlar.append(cihaz)
                        print(f"Canlı cihaz bulundu: {cihaz['ip']}")
                        
                        # GUI güncellemesi - ana thread'e gönder
                        gui_instance.root.after(0, lambda c=cihaz: gui_update_callback(gui_instance, c))
                        
                except Exception as e:
                    print(f"IP kontrol hatası {ip}: {e}")
        
        print(f"Ping tarama tamamlandı: {len(canli_cihazlar)} cihaz bulundu")
        return canli_cihazlar
        
    except Exception as e:
        print(f"Ping tarama hatası: {e}")
        gui_instance.root.after(0, lambda: gui_instance.results_panel.log_ekle(f"❌ Ping tarama hatası: {e}"))
        return []

def gui_update_callback(gui_instance, cihaz):
    """GUI güncellemeleri için callback fonksiyonu - ANA thread'de çalışır"""
    gui_instance.results_panel.log_ekle(f"✅ Canlı cihaz: {cihaz['ip']} - {cihaz['mac']}")
    
    # Nmap tarzı detaylı log
    detay = f"\n[+] {cihaz['ip']} - MAC: {cihaz['mac']}\n"
    detay += f"    Durum: Canlı\n"
    detay += f"    TTL: ~64 (tahmini)\n"
    gui_instance.results_panel.log_ekle(detay)
    
    os_tahmin = os_tahmini_yap(cihaz, {})
    gui_instance.results_panel.cihaz_ekle_guncelle(cihaz['ip'], cihaz['mac'], "Canlı", "", os_tahmin)

# ARP ve TCP tarama fonksiyonları AYNI KALACAK
def arp_tarama(gui_instance, hedef_ag):
    if not gui_instance.SCAPY_AVAILABLE:
        gui_instance.results_panel.log_ekle("❌ Scapy kurulu değil! Ping taramasına geçiliyor...")
        return ping_tarama(gui_instance, hedef_ag)
    
    try:
        import scapy.all as scapy
        import os
        
        # Yetki kontrolü
        if os.name == 'posix' and os.geteuid() != 0:
            gui_instance.root.after(0, gui_instance.results_panel.log_ekle, "⚠️  ARP tarama için root yetkisi gerekli! Ping taramasına geçiliyor...")
            return ping_tarama(gui_instance, hedef_ag)
            
        gui_instance.root.after(0, gui_instance.results_panel.log_ekle, "🔍 ARP tarama başlatılıyor...")
        
        arp_request = scapy.ARP(pdst=hedef_ag)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False, retry=2)[0]
        
        cihazlar = []
        for element in answered_list:
            cihaz = {
                "ip": element[1].psrc, 
                "mac": element[1].hwsrc, 
                "acik_portlar": [],
                "durum": "Canlı"
            }
            cihazlar.append(cihaz)
            print(f"ARP yanıtı: {cihaz['ip']} - {cihaz['mac']}")
            
            # Nmap tarzı detaylı log
            detay = f"\n[+] {cihaz['ip']} - MAC: {cihaz['mac']}\n"
            detay += f"    Durum: Canlı (ARP yanıtı)\n"
            detay += f"    MAC Üretici: {mac_ureticisi_bul(cihaz['mac'])}\n"
            gui_instance.root.after(0, gui_instance.results_panel.log_ekle, detay)
            
            gui_instance.root.after(0, gui_instance.results_panel.cihaz_ekle_guncelle, cihaz['ip'], cihaz['mac'], "Canlı", "", "ARP")
        
        return cihazlar
        
    except Exception as e:
        gui_instance.root.after(0, gui_instance.results_panel.log_ekle, f"❌ ARP tarama hatası: {e}")
        return ping_tarama(gui_instance, hedef_ag)

def tcp_tarama(gui_instance, hedef_ag):
    print("TCP tabanlı tarama başlatılıyor...")
    
    try:
        ag = ipaddress.IPv4Network(hedef_ag, strict=False)
        canli_cihazlar = []
        
        # Sık kullanılan portlar
        test_ports = [22, 23, 80, 443, 3389, 8080]
        
        def ip_kontrol(ip):
            if not gui_instance.tarama_devam_ediyor:
                return
            
            ip_str = str(ip)
            for port in test_ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(0.3)
                        if sock.connect_ex((ip_str, port)) == 0:
                            mac = mac_adresi_al(ip_str)
                            cihaz = {
                                "ip": ip_str, 
                                "mac": mac, 
                                "acik_portlar": [(port, "test")],
                                "durum": "Canlı"
                            }
                            canli_cihazlar.append(cihaz)
                            print(f"TCP bağlantı: {ip_str}:{port}")
                            
                            # Nmap tarzı detaylı log
                            detay = f"\n[+] {ip_str} - MAC: {mac}\n"
                            detay += f"    Durum: Canlı (TCP/{port})\n"
                            try:
                                servis = socket.getservbyport(port, 'tcp')
                            except:
                                servis = "bilinmeyen"
                            detay += f"    Servis: {servis}\n"
                            gui_instance.root.after(0, gui_instance.results_panel.log_ekle, detay)
                            
                            os_tahmin = os_tahmini_yap(cihaz, {ip_str: [(port, "test")]})
                            gui_instance.root.after(0, gui_instance.results_panel.cihaz_ekle_guncelle, ip_str, mac, "Canlı", f"{port}", os_tahmin)
                            break
                except:
                    pass
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(ip_kontrol, list(ag.hosts())[:100])
        
        return canli_cihazlar
        
    except Exception as e:
        print(f"TCP tarama hatası: {e}")
        gui_instance.root.after(0, gui_instance.results_panel.log_ekle, f"❌ TCP tarama hatası: {e}")
        return []