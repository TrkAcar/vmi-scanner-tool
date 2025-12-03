import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

class ControlPanel:
    def __init__(self, controller, parent):
        self.controller = controller
        self.parent = parent
        self.olustur()
    
    def olustur(self):
        # Başlık
        title_frame = tk.Frame(self.parent, bg='#2c3e50', height=70)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="⚡ VMI Scanner Tool v3.0", 
            font=('Arial', 18, 'bold'), 
            fg='white', 
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Kontrol Paneli
        control_frame = tk.LabelFrame(self.parent, text=" Tarama Kontrolleri ", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.olustur_ag_girisi(control_frame)
        self.olustur_tarama_yontemleri(control_frame)
        self.olustur_port_ayarlari(control_frame)
        self.olustur_port_setleri(control_frame)
        self.olustur_butonlar(control_frame)
        self.olustur_ilerleme(control_frame)
    
    def olustur_ag_girisi(self, parent):
        network_frame = tk.Frame(parent, bg='#f0f0f0')
        network_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(network_frame, text="Hedef Ağ:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        self.network_entry = tk.Entry(network_frame, width=20, font=('Arial', 10))
        self.network_entry.pack(side=tk.LEFT, padx=5)
        
        self.auto_detect_button = tk.Button(
            network_frame,
            text="↻ Ağı Otomatik Tespit Et",
            command=self.controller.otomatik_ag_tespit,
            font=('Arial', 9),
            bg='#f39c12',
            fg='white'
        )
        self.auto_detect_button.pack(side=tk.LEFT, padx=5)
    
    def olustur_tarama_yontemleri(self, parent):
        method_frame = tk.Frame(parent, bg='#f0f0f0')
        method_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(method_frame, text="Tarama Yöntemi:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.scan_method = tk.StringVar(value="ping")
        
        tk.Radiobutton(method_frame, text="Ping Tarama (Hızlı)", variable=self.scan_method, 
                      value="ping", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(method_frame, text="ARP Tarama (Scapy)", variable=self.scan_method, 
                      value="arp", bg='#f0f0f0', 
                      state=tk.NORMAL if self.controller.SCAPY_AVAILABLE else tk.DISABLED).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(method_frame, text="TCP SYN Tarama", variable=self.scan_method, 
                      value="tcp", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
    
    def olustur_port_ayarlari(self, parent):
        port_frame = tk.Frame(parent, bg='#f0f0f0')
        port_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(port_frame, text="Port Aralığı:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        self.port_start = tk.Entry(port_frame, width=15, font=('Arial', 10))
        self.port_start.pack(side=tk.LEFT, padx=2)
        self.port_start.insert(0, "1")
        
        tk.Label(port_frame, text="-", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        self.port_end = tk.Entry(port_frame, width=8, font=('Arial', 10))
        self.port_end.pack(side=tk.LEFT, padx=2)
        self.port_end.insert(0, "100")
        
        self.port_mod_label = tk.Label(port_frame, text="[Aralık]", font=('Arial', 8), bg='#f0f0f0', fg='#666')
        self.port_mod_label.pack(side=tk.LEFT, padx=5)
    
    def olustur_port_setleri(self, parent):
        port_sets_frame = tk.Frame(parent, bg='#f0f0f0')
        port_sets_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(port_sets_frame, text="Hızlı Port Setleri:", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        
        tk.Button(port_sets_frame, text="⚡ Hızlı (1-1000)", command=self.controller.hizli_portlar, 
                 font=('Arial', 8), bg='#27ae60', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(port_sets_frame, text="◉ Standart (1-1024)", command=self.controller.standart_portlar, 
                 font=('Arial', 8), bg='#2980b9', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(port_sets_frame, text="◎ Tam (1-65535)", command=self.controller.tum_portlar, 
                 font=('Arial', 8), bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(port_sets_frame, text="⚠ Güvenlik", command=self.controller.guvenlik_portlari, 
                 font=('Arial', 8), bg='#f39c12', fg='white').pack(side=tk.LEFT, padx=2)
    
    def olustur_butonlar(self, parent):
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.scan_button = tk.Button(
            button_frame, 
            text="▶ Ağ Taraması", 
            command=self.controller.tarama_baslat,
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            width=18,
            height=2
        )
        self.scan_button.pack(side=tk.LEFT, padx=5)
        
        self.port_scan_button = tk.Button(
            button_frame, 
            text="◉ Port Taraması", 
            command=self.controller.port_tarama_baslat,
            font=('Arial', 10, 'bold'),
            bg='#2980b9',
            fg='white',
            width=18,
            height=2
        )
        self.port_scan_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame, 
            text="■ Durdur", 
            command=self.controller.tarama_durdur,
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=12,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.test_button = tk.Button(
            button_frame, 
            text="⚙ Test", 
            command=self.controller.test_tarama,
            font=('Arial', 10),
            bg='#f39c12',
            fg='white',
            width=12,
            height=2
        )
        self.test_button.pack(side=tk.LEFT, padx=5)
    
    def olustur_ilerleme(self, parent):
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır - Ağ otomatik tespit için butona tıklayın")
        status_bar = tk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, 
                            anchor=tk.W, bg='#34495e', fg='white')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_port_range(self, start, end, liste_modu, mod_text):
        self.port_start.delete(0, tk.END)
        self.port_start.insert(0, start)
        self.port_end.delete(0, tk.END)
        self.port_end.insert(0, end)
        self.controller.port_liste_modu = liste_modu
        self.port_mod_label.config(text=mod_text)

class ResultsPanel:
    def __init__(self, controller, parent):
        self.controller = controller
        self.parent = parent
        self.olustur()
    
    def olustur(self):
        results_frame = tk.LabelFrame(self.parent, text=" Tarama Sonuçları ", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for devices
        tree_frame = tk.Frame(results_frame, bg='#f0f0f0')
        tree_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('IP', 'MAC', 'Durum', 'Açık Portlar', 'İşletim Sistemi'), show='headings', height=8)
        self.tree.heading('IP', text='IP Adresi')
        self.tree.heading('MAC', text='MAC Adresi')
        self.tree.heading('Durum', text='Durum')
        self.tree.heading('Açık Portlar', text='Açık Portlar')
        self.tree.heading('İşletim Sistemi', text='OS Tahmini')
        self.tree.column('IP', width=150)
        self.tree.column('MAC', width=180)
        self.tree.column('Durum', width=100)
        self.tree.column('Açık Portlar', width=200)
        self.tree.column('İşletim Sistemi', width=150)
        self.tree.pack(fill=tk.X)
        
        # Scrollable log area
        log_frame = tk.Frame(results_frame, bg='#f0f0f0')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(log_frame, text="Nmap Tarzı Detaylı Log:", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor=tk.W)
        self.log_area = scrolledtext.ScrolledText(
            log_frame, 
            wrap=tk.WORD, 
            width=100, 
            height=15,
            font=('Consolas', 9),
            state="disabled"
        )
        self.log_area.pack(fill=tk.BOTH, expand=True)
    
    def log_ekle(self, mesaj):
        timestamp = self.controller.results_panel.get_timestamp()
        log_message = f"[{timestamp}] {mesaj}\n"
        
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, log_message)
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")
        self.controller.root.update()
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def cihaz_ekle_guncelle(self, ip, mac, durum, portlar, os_tahmin=""):
        for item in self.tree.get_children():
            if self.tree.item(item, 'values')[0] == ip:
                self.tree.item(item, values=(ip, mac, durum, portlar, os_tahmin))
                return
        
        self.tree.insert('', tk.END, values=(ip, mac, durum, portlar, os_tahmin))
    
    def temizle(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.log_area.config(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state="disabled")

class DebugPanel:
    def __init__(self, controller, parent):
        self.controller = controller
        self.parent = parent
        self.olustur()
    
    def olustur(self):
        # Debug başlık
        debug_title_frame = tk.Frame(self.parent, bg='#34495e', height=50)
        debug_title_frame.pack(fill=tk.X, padx=10, pady=5)
        debug_title_frame.pack_propagate(False)
        
        debug_title = tk.Label(
            debug_title_frame,
            text="⚙ Python Debug Çıktısı - Tüm print() ve sistem mesajları burada görünecek",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#34495e'
        )
        debug_title.pack(expand=True)
        
        # Debug kontrolleri
        debug_control_frame = tk.Frame(self.parent, bg='#f0f0f0')
        debug_control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        clear_debug_btn = tk.Button(
            debug_control_frame,
            text="✖ Debug Çıktısını Temizle",
            command=self.controller.debug_temizle,
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white'
        )
        clear_debug_btn.pack(side=tk.LEFT, padx=5)
        
        # Debug text alanı
        self.debug_text = scrolledtext.ScrolledText(
            self.parent,
            wrap=tk.WORD,
            width=100,
            height=35,
            font=('Consolas', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        self.debug_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Başlangıç mesajı
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.debug_text.config(state="normal")
        self.debug_text.insert(tk.END, "="*80 + "\n")
        self.debug_text.insert(tk.END, f"[{timestamp}] ⚙ Python Debug Konsolu Başlatıldı\n")
        self.debug_text.insert(tk.END, f"[{timestamp}] ▸ Tüm print() çıktıları ve sistem mesajları burada görünecek\n")
        self.debug_text.insert(tk.END, "="*80 + "\n\n")
        self.debug_text.config(state="disabled")
    
    def clear_debug(self):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.debug_text.config(state="normal")
        self.debug_text.delete(1.0, tk.END)
        self.debug_text.insert(tk.END, "="*80 + "\n")
        self.debug_text.insert(tk.END, f"[{timestamp}] ✖ Debug Çıktısı Temizlendi\n")
        self.debug_text.insert(tk.END, "="*80 + "\n\n")
        self.debug_text.config(state="disabled")
        print("Debug ekranı temizlendi")

class ReportPanel:
    def __init__(self, controller, parent):
        self.controller = controller
        self.parent = parent
        self.olustur()
    
    def olustur(self):
        # Rapor başlık
        rapor_title_frame = tk.Frame(self.parent, bg='#27ae60', height=50)
        rapor_title_frame.pack(fill=tk.X, padx=10, pady=5)
        rapor_title_frame.pack_propagate(False)
        
        rapor_title = tk.Label(
            rapor_title_frame,
            text="≡ Detaylı Tarama Raporu - Nmap Formatında",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#27ae60'
        )
        rapor_title.pack(expand=True)
        
        # Rapor kontrolleri
        rapor_control_frame = tk.Frame(self.parent, bg='#f0f0f0')
        rapor_control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        rapor_olustur_btn = tk.Button(
            rapor_control_frame,
            text="+ Rapor Oluştur",
            command=self.controller.rapor_olustur,
            font=('Arial', 10),
            bg='#2980b9',
            fg='white'
        )
        rapor_olustur_btn.pack(side=tk.LEFT, padx=5)
        
        rapor_temizle_btn = tk.Button(
            rapor_control_frame,
            text="✖ Raporu Temizle",
            command=self.controller.rapor_temizle,
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white'
        )
        rapor_temizle_btn.pack(side=tk.LEFT, padx=5)
        
        rapor_kaydet_btn = tk.Button(
            rapor_control_frame,
            text="↓ Raporu Kaydet",
            command=self.controller.rapor_kaydet,
            font=('Arial', 10),
            bg='#f39c12',
            fg='white'
        )
        rapor_kaydet_btn.pack(side=tk.LEFT, padx=5)
        
        # Rapor text alanı
        self.rapor_text = scrolledtext.ScrolledText(
            self.parent,
            wrap=tk.WORD,
            width=100,
            height=35,
            font=('Consolas', 9),
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='white'
        )
        self.rapor_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Başlangıç mesajı
        self.rapor_text.config(state="normal")
        self.rapor_text.insert(tk.END, "≡ DETAYLI TARAMA RAPORU\n")
        self.rapor_text.insert(tk.END, "="*50 + "\n")
        self.rapor_text.insert(tk.END, "Tarama yapıldıktan sonra rapor burada görünecek...\n")
        self.rapor_text.config(state="disabled")
    
    def show_report(self, report):
        self.rapor_text.config(state="normal")
        self.rapor_text.delete(1.0, tk.END)
        self.rapor_text.insert(tk.END, report)
        self.rapor_text.see(tk.END)
        self.rapor_text.config(state="disabled")
    
    def clear_report(self):
        self.rapor_text.config(state="normal")
        self.rapor_text.delete(1.0, tk.END)
        self.rapor_text.insert(tk.END, "✖ Rapor temizlendi\n")
        self.rapor_text.config(state="disabled")