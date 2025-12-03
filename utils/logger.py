import sys
import tkinter as tk
from datetime import datetime

class PrintToLog:
    def __init__(self, gui_instance, debug_text_widget):
        self.gui = gui_instance
        self.debug_text = debug_text_widget
        self.original_stdout = sys.stdout
        self.buffer = ""  # Satır tamponlama için
    
    def write(self, text):
        # Orijinal stdout'a yaz
        self.original_stdout.write(text)
        
        # Boş metin kontrolü
        if not text:
            return
        
        # Buffer'a ekle
        self.buffer += text
        
        # Satır sonu varsa işle
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            # Son eleman boş olabilir (satır \n ile bitiyorsa)
            self.buffer = lines[-1]
            
            # Tamamlanmış satırları işle
            for line in lines[:-1]:
                if line.strip():  # Boş satırları atla
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    formatted_line = f"[{timestamp}] {line}\n"
                    
                    self.debug_text.config(state="normal")
                    self.debug_text.insert(tk.END, formatted_line)
                    self.debug_text.see(tk.END)
                    self.debug_text.config(state="disabled")
    
    def flush(self):
        # Buffer'da kalan varsa yazdır
        if self.buffer.strip():
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_line = f"[{timestamp}] {self.buffer}\n"
            
            self.debug_text.config(state="normal")
            self.debug_text.insert(tk.END, formatted_line)
            self.debug_text.see(tk.END)
            self.debug_text.config(state="disabled")
            
            self.buffer = ""
        
        self.original_stdout.flush()