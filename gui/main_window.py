import tkinter as tk
from tkinter import ttk
import sys
import time
from datetime import datetime

try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    from pythonping import ping
    PYTHONPING_AVAILABLE = True
except ImportError:
    PYTHONPING_AVAILABLE = False

from .widgets import ControlPanel, ResultsPanel, DebugPanel, ReportPanel
from utils.logger import PrintToLog
from core.scanner import start_network_scan, start_port_scan
from utils.helpers import get_system_info, ping_cihaz

class AgTarayiciGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VMI Scanner Tool v3.0")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f0f0')
        
        # Değişkenler
        self.tarama_devam_ediyor = False
        self.bulunan_cihazlar = []
        self.tarama_baslangic_zamani = None
        self.port_liste_modu = False
        self.SCAPY_AVAILABLE = SCAPY_AVAILABLE
        self.PYTHONPING_AVAILABLE = PYTHONPING_AVAILABLE
        
        self.arayuz_olustur()
        self.sistem_bilgisi()
    
    def arayuz_olustur(self):
        # Notebook (Sekmeler) oluştur
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Ana sekme
        self.ana_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ana_frame, text="▶ Ana Tarama")
        
        # Debug sekmesi
        self.debug_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.debug_frame, text="⚙ Debug Çıktısı")
        
        # Rapor sekmesi
        self.rapor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rapor_frame, text="≡ Detaylı Rapor")
        
        # Bileşenleri oluştur
        self.control_panel = ControlPanel(self, self.ana_frame)
        self.results_panel = ResultsPanel(self, self.ana_frame)
        self.debug_panel = DebugPanel(self, self.debug_frame)
        self.report_panel = ReportPanel(self, self.rapor_frame)
        
        # Print çıktısını yönlendir
        self.print_ciktisini_yonlendir()
    
    def print_ciktisini_yonlendir(self):
        sys.stdout = PrintToLog(self, self.debug_panel.debug_text)
        print("✓ Print çıktısı debug sekmesine yönlendirildi")
        print("▸ Sistem hazır - Tarama başlatmak için kontrol panelini kullanın")
    
    def sistem_bilgisi(self):
        info = get_system_info(self.SCAPY_AVAILABLE, self.PYTHONPING_AVAILABLE)
        for line in info:
            self.results_panel.log_ekle(line)
    
    # GUI State Management
    def update_ui_state(self, scanning=False):
        state = tk.DISABLED if scanning else tk.NORMAL
        self.control_panel.scan_button.config(state=state)
        self.control_panel.port_scan_button.config(state=state)
        self.control_panel.test_button.config(state=state)
        self.control_panel.stop_button.config(state=tk.NORMAL if scanning else tk.DISABLED)
        
        if scanning:
            self.control_panel.progress.start()
        else:
            self.control_panel.progress.stop()
    
    # Tarama Metodları
    def tarama_baslat(self):
        start_network_scan(self)
    
    def port_tarama_baslat(self):
        start_port_scan(self)
    
    def test_tarama(self):
        from core.scanner import test_tarama
        test_tarama(self)
    
    def tarama_durdur(self):
        self.tarama_devam_ediyor = False
        self.results_panel.log_ekle("⏹️ Tarama durduruluyor...")
        self.control_panel.status_var.set("Tarama durduruluyor...")
        time.sleep(0.5)
        self.control_panel.status_var.set("Tarama durduruldu")
    
    def otomatik_ag_tespit(self):
        from utils.helpers import otomatik_ag_tespit
        otomatik_ag_tespit(self)
    
    # Port Setleri
    def hizli_portlar(self):
        self.control_panel.set_port_range("1", "1000", False, "[Aralık]")
        self.results_panel.log_ekle("🚀 Hızlı port aralığı ayarlandı: 1-1000")
    
    def standart_portlar(self):
        self.control_panel.set_port_range("1", "1024", False, "[Aralık]")
        self.results_panel.log_ekle("🎯 Standart port aralığı ayarlandı: 1-1024")
    
    def tum_portlar(self):
        self.control_panel.set_port_range("1", "65535", False, "[Aralık]")
        self.results_panel.log_ekle("🔍 Tüm port aralığı ayarlandı: 1-65535")
    
    def guvenlik_portlari(self):
        guvenlik_portlari = "21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,5900,8080"
        self.control_panel.set_port_range(guvenlik_portlari, "liste", True, "[Liste]")
        self.results_panel.log_ekle("🛡️ Güvenlik portları ayarlandı (liste modu)")
    
    # Rapor Metodları
    def rapor_olustur(self):
        from core.report_generator import generate_report
        report = generate_report(self)
        self.report_panel.show_report(report)
        self.notebook.select(2)  # Rapor sekmesine geç
    
    def rapor_temizle(self):
        self.report_panel.clear_report()
    
    def rapor_kaydet(self):
        from core.report_generator import save_report
        save_report(self.report_panel.rapor_text)
    
    def debug_temizle(self):
        self.debug_panel.clear_debug()