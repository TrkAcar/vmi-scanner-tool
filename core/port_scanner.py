import threading
import socket
from tkinter import messagebox
from utils.helpers import port_listesi_olustur

def start_port_scan(gui_instance):
    if not gui_instance.bulunan_cihazlar:
        messagebox.showwarning("Uyarı", "Önce ağ taraması yapmalısınız!")
        return
    
    if gui_instance.tarama_devam_ediyor:
        return
    
    try:
        port_input = gui_instance.control_panel.port_start.get().strip()
        port_end_input = gui_instance.control_panel.port_end.get().strip()
        
        # Port listesi modu kontrolü
        if port_end_input == "liste" or ',' in port_input:
            gui_instance.port_liste_modu = True
            port_araligi = port_listesi_olustur(port_input)
            if not port_araligi:
                messagebox.showerror("Hata", "Geçersiz port listesi formatı!")
                return
        else:
            gui_instance.port_liste_modu = False
            # Normal aralık
            port_baslangic = int(port_input)
            port_bitis = int(port_end_input)
            if port_baslangic > port_bitis:
                messagebox.showerror("Hata", "Başlangıç portu bitiş portundan büyük olamaz!")
                return
            port_araligi = range(port_baslangic, port_bitis + 1)
            
    except ValueError as e:
        messagebox.showerror("Hata", f"Geçersiz port formatı: {e}")
        return
    
    gui_instance.tarama_devam_ediyor = True
    gui_instance.update_ui_state(scanning=True)
    
    from utils.helpers import nmap_stili_baslik
    gui_instance.results_panel.log_ekle(nmap_stili_baslik("PORT TARAMASI BAŞLATILDI"))
    if gui_instance.port_liste_modu:
        gui_instance.results_panel.log_ekle(f"Port Listesi: {len(port_araligi)} port")
    else:
        gui_instance.results_panel.log_ekle(f"Port Aralığı: {port_araligi[0]}-{port_araligi[-1]}")
    gui_instance.results_panel.log_ekle(f"Hedef Cihaz: {len(gui_instance.bulunan_cihazlar)} cihaz")
    gui_instance.control_panel.status_var.set(f"Port taraması yapılıyor...")
    
    # Thread'de port tarama başlat
    thread = threading.Thread(target=port_taramasi_islemi, args=(gui_instance, port_araligi))
    thread.daemon = True
    thread.start()

def port_taramasi_islemi(gui_instance, port_araligi):
    try:
        if gui_instance.port_liste_modu:
            print(f"Port tarama başlatıldı (liste): {len(port_araligi)} port")
        else:
            print(f"Port tarama başlatıldı: {port_araligi[0]}-{port_araligi[-1]}")
        
        for cihaz in gui_instance.bulunan_cihazlar:
            if not gui_instance.tarama_devam_ediyor:
                break
                
            print(f"Cihaz port taraması: {cihaz['ip']}")
            gui_instance.root.after(0, gui_instance.results_panel.log_ekle, f"\n🔍 {cihaz['ip']} port taraması başlatılıyor...")
            
            acik_portlar = []
            for port in port_araligi:
                if not gui_instance.tarama_devam_ediyor:
                    break
                
                print(f"Port kontrol: {cihaz['ip']}:{port}")
                
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(0.3)
                        if sock.connect_ex((cihaz['ip'], port)) == 0:
                            try:
                                servis = socket.getservbyport(port, 'tcp')
                            except:
                                servis = "bilinmeyen"
                            
                            acik_portlar.append((port, servis))
                            print(f"Açık port bulundu: {cihaz['ip']}:{port} ({servis})")
                            
                            # Nmap tarzı port bilgisi
                            port_info = f"    {port}/tcp   open   {servis}"
                            gui_instance.root.after(0, gui_instance.results_panel.log_ekle, port_info)
                except Exception as e:
                    print(f"Port kontrol hatası: {cihaz['ip']}:{port} - {e}")
            
            cihaz['acik_portlar'] = acik_portlar
            print(f"Cihaz tarama tamamlandı: {cihaz['ip']} - {len(acik_portlar)} açık port")
            
            # Cihaz özeti
            if acik_portlar:
                gui_instance.root.after(0, gui_instance.results_panel.log_ekle, f"\n📍 {cihaz['ip']} - {len(acik_portlar)} açık port bulundu")
            
            port_listesi = ", ".join([f"{p[0]}" for p in acik_portlar[:5]])
            if len(acik_portlar) > 5:
                port_listesi += f" ...(+{len(acik_portlar)-5})"
            
            from utils.helpers import os_tahmini_yap
            os_tahmin = os_tahmini_yap(cihaz, {cihaz['ip']: acik_portlar})
            
            # Treeview güncelleme
            gui_instance.root.after(0, gui_instance.results_panel.cihaz_ekle_guncelle, cihaz['ip'], cihaz['mac'], "Portlar Taranmış", port_listesi, os_tahmin)
        
        print("Port tarama tamamlandı")
        from core.scanner import tarama_tamamlandi
        gui_instance.root.after(0, tarama_tamamlandi, gui_instance, gui_instance.bulunan_cihazlar)
        
    except Exception as e:
        print(f"Port tarama hatası: {str(e)}")
        from core.scanner import tarama_hatasi
        gui_instance.root.after(0, tarama_hatasi, gui_instance, str(e))