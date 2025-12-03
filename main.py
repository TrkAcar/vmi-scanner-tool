import tkinter as tk
from gui.main_window import AgTarayiciGUI

def main():
    try:
        root = tk.Tk()
        app = AgTarayiciGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Uygulama hatası: {e}")
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()