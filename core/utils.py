import os
import logging
import string
import secrets
import pyperclip
from datetime import datetime

# Configurar el formato de la bitácora
logging.basicConfig(
    filename='cryptoguard.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def registrar_evento(mensaje, nivel="info"):
    """Registra una acción en el archivo cryptoguard.log"""
    if nivel == "info":
        logging.info(mensaje)
    elif nivel == "error":
        logging.error(mensaje)
    elif nivel == "warning":
        logging.warning(mensaje)

def verificar_archivo(ruta):
    """Comprueba si el archivo existe y es accesible."""
    existe = os.path.exists(ruta)
    if not existe:
        registrar_evento(f"Archivo no encontrado: {ruta}", "error")
    return existe

def borrado_seguro(ruta):
    """Sobreescribe el archivo con datos aleatorios antes de borrarlo."""
    if os.path.exists(ruta):
        try:
            size = os.path.getsize(ruta)
            with open(ruta, "ba+", buffering=0) as f:
                f.write(os.urandom(size)) # Sobreescribir con basura aleatoria
            os.remove(ruta)
            registrar_evento(f"🗑️ BORRADO SEGURO: {ruta} eliminado permanentemente.")
            return True
        except Exception as e:
            registrar_evento(f"❌ FALLO EN BORRADO SEGURO {ruta}: {str(e)}", "error")
            return False

def generar_password_segura(longitud=16):
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alfabeto) for i in range(longitud))
    
    # Intentar copiar al portapapeles
    pyperclip.copy(password)
    
    # Verificación extra: si no se copió, al menos la tenemos en el entry
    registrar_evento("🔑 Contraseña generada.")
    return password