import customtkinter as ctk
from ui.app_gui import CryptoGuardApp

if __name__ == "__main__":
    # Estética Dark
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue") 
    
    app = CryptoGuardApp()
    app.mainloop()