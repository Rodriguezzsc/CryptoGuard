import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.encryptor import cifrar_archivo, descifrar_archivo
from core.manager import procesar_carpeta
from core.utils import borrado_seguro, generar_password_segura

class CryptoGuardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CryptoGuard v1.2 - Secure Cipher Engine")
        self.geometry("600x650") # Un poco más alta para el campo de extensión
        
        self.grid_columnconfigure(0, weight=1)
        
        # --- UI ELEMENTS ---
        self.label_titulo = ctk.CTkLabel(self, text="CRYPTOGUARD", 
                                         font=ctk.CTkFont(size=28, weight="bold", slant="italic"),
                                         text_color="#00FF41")
        self.label_titulo.grid(row=0, column=0, padx=20, pady=25)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Ingresa la contraseña maestra...", 
                                           width=400, show="*")
        self.entry_password.grid(row=1, column=0, padx=20, pady=10)

        self.btn_gen_pass = ctk.CTkButton(self, text="Generar y Copiar Clave Segura", 
                                           command=self.accion_generar_pass, 
                                           fg_color="#5D3FD3", hover_color="#4832a8")
        self.btn_gen_pass.grid(row=2, column=0, padx=20, pady=5)

        self.check_ver = ctk.CTkCheckBox(self, text="Mostrar Contraseña", command=self.toggle_password)
        self.check_ver.grid(row=3, column=0, padx=20, pady=5)

        self.switch_shred = ctk.CTkSwitch(self, text="Borrado Seguro (Triturar original)", 
                                          progress_color="#00FF41")
        self.switch_shred.grid(row=4, column=0, padx=20, pady=10)

        # MODO CAMUFLAJE: Entrada de extensión
        self.label_ext = ctk.CTkLabel(self, text="Extensión de Camuflaje:", font=("Arial", 12))
        self.label_ext.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.entry_ext = ctk.CTkEntry(self, placeholder_text=".crypt, .dll, .sys...", width=150)
        self.entry_ext.insert(0, ".crypt")
        self.entry_ext.grid(row=6, column=0, padx=20, pady=(0, 10))

        self.btn_file = ctk.CTkButton(self, text="Seleccionar Archivo", 
                                       command=self.accion_archivo, 
                                       fg_color="#1f538d", hover_color="#14375e")
        self.btn_file.grid(row=7, column=0, padx=20, pady=10)

        self.btn_folder = ctk.CTkButton(self, text="Procesar Carpeta (Barrido)", 
                                         command=self.accion_carpeta, 
                                         fg_color="#1f538d", hover_color="#14375e")
        self.btn_folder.grid(row=8, column=0, padx=20, pady=10)

        self.status_box = ctk.CTkTextbox(self, width=500, height=120, font=("Courier New", 12))
        self.status_box.grid(row=9, column=0, padx=20, pady=20)
        self.status_box.insert("0.0", ">>> SISTEMA CRYPTOGUARD ONLINE\n>>> Modo Camuflaje Activo...")

    def toggle_password(self):
        if self.check_ver.get() == 1:
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")

    def log(self, mensaje, tipo="info"):
        prefix = "> "
        if tipo == "error": prefix = "[!] ERROR: "
        if tipo == "success": prefix = "[+] SUCCESS: "
        self.status_box.insert("end", f"\n{prefix}{mensaje}")
        self.status_box.see("end")

    def accion_generar_pass(self):
        nueva_pass = generar_password_segura()
        self.entry_password.delete(0, 'end')
        self.entry_password.insert(0, nueva_pass)
        self.log("Clave generada y lista para usar.", "success")

    def accion_archivo(self):
        pwd = self.entry_password.get()
        ext_camuflaje = self.entry_ext.get() or ".crypt"
        if not pwd:
            messagebox.showwarning("Seguridad", "Se requiere contraseña.")
            return

        ruta = filedialog.askopenfilename()
        if ruta:
            # Si el archivo seleccionado ya tiene la extensión de camuflaje, desciframos
            if ruta.endswith(ext_camuflaje):
                res = descifrar_archivo(ruta, pwd)
                if res == "ERROR_PASSWORD":
                    self.log("Integridad fallida o clave errónea.", "error")
                elif res == "ERROR_SISTEMA":
                    self.log("Fallo crítico en el motor.", "error")
                else:
                    self.log(f"Recuperado con éxito: {res}", "success")
            else:
                # Si no, ciframos con la extensión elegida
                res = cifrar_archivo(ruta, pwd, extension=ext_camuflaje)
                if res != "ERROR_SISTEMA":
                    self.log(f"Cifrado como {ext_camuflaje} exitoso.", "success")
                    if self.switch_shred.get():
                        borrado_seguro(ruta)
                        self.log("Original triturado.", "info")
                else:
                    self.log("Error al cifrar.", "error")

    def accion_carpeta(self):
        pwd = self.entry_password.get()
        if not pwd: return
        ruta = filedialog.askdirectory()
        if ruta:
            res = procesar_carpeta(ruta, pwd, modo="cifrar")
            self.log(f"Barrido completo: {res['exitos']} protegidos.", "info")