from datetime import datetime
from tkinter import filedialog, messagebox
from utils.helpers import nmap_detay_ekle, tarama_suresi_hesapla

def generate_report(gui_instance):
    if not gui_instance.bulunan_cihazlar:
        return "Henüz tarama yapılmamış veya cihaz bulunamamış."
    
    # Port sonuçlarını topla
    port_sonuclari = {}
    for cihaz in gui_instance.bulunan_cihazlar:
        if cihaz['acik_portlar']:
            port_sonuclari[cihaz['ip']] = cihaz['acik_portlar']
    
    rapor = "⚡ VMI SCANNER TOOL - DETAYLI TARAMA RAPORU\n"
    rapor += "="*70 + "\n"
    rapor += f"Tarama Tarihi : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    rapor += f"Hedef Ağ      : {gui_instance.control_panel.network_entry.get()}\n"
    rapor += f"Tarama Yöntemi: {gui_instance.control_panel.scan_method.get().upper()}\n"
    rapor += f"Bulunan Cihaz : {len(gui_instance.bulunan_cihazlar)}\n"
    rapor += f"Tarama Süresi : {tarama_suresi_hesapla(gui_instance)}\n"
    rapor += "="*70 + "\n\n"
    
    # Her cihaz için detaylı rapor
    for cihaz in gui_instance.bulunan_cihazlar:
        rapor += nmap_detay_ekle(cihaz, port_sonuclari)
    
    # İstatistikler
    rapor += "\n≡ İSTATİSTİKLER:\n"
    rapor += "-"*50 + "\n"
    toplam_acik_port = sum(len(cihaz['acik_portlar']) for cihaz in gui_instance.bulunan_cihazlar)
    rapor += f"Toplam Cihaz      : {len(gui_instance.bulunan_cihazlar)}\n"
    rapor += f"Toplam Açık Port  : {toplam_acik_port}\n"
    
    # En çok açık port olan cihaz
    if gui_instance.bulunan_cihazlar:
        en_cok_portlu = max(gui_instance.bulunan_cihazlar, key=lambda x: len(x['acik_portlar']))
        rapor += f"En Çok Portlu     : {en_cok_portlu['ip']} ({len(en_cok_portlu['acik_portlar'])} port)\n"
    
    # OS Dağılımı
    from utils.helpers import os_tahmini_yap
    os_dagilim = {}
    for cihaz in gui_instance.bulunan_cihazlar:
        os_tahmin = os_tahmini_yap(cihaz, port_sonuclari)
        os_dagilim[os_tahmin] = os_dagilim.get(os_tahmin, 0) + 1
    
    if os_dagilim:
        rapor += f"OS Dağılımı       : " + ", ".join([f"{k}({v})" for k, v in os_dagilim.items()]) + "\n"
    
    rapor += "\n" + "="*70 + "\n"
    rapor += "✓ Tarama tamamlandı!\n"
    
    return rapor

def save_report(rapor_text_widget):
    try:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Raporu Kaydet"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(rapor_text_widget.get(1.0, "end"))
            messagebox.showinfo("Başarılı", f"Rapor '{filename}' dosyasına kaydedildi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Rapor kaydedilemedi: {e}")