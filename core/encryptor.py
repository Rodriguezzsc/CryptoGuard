import os
from cryptography.hazmat.primitives import hashes, padding, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from core.utils import registrar_evento

def generar_llave(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32 + 32, # 32 para AES, 32 para HMAC
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    llaves = kdf.derive(password.encode())
    return llaves[:32], llaves[32:] # Retornamos (llave_aes, llave_hmac)

def cifrar_archivo(ruta_origen, password, extension=".crypt"):
    try:
        salt = os.urandom(16)
        iv = os.urandom(16)
        llave_aes, llave_hmac = generar_llave(password, salt)
        
        with open(ruta_origen, "rb") as f:
            datos = f.read()
            
        padder = padding.PKCS7(128).padder()
        datos_con_padding = padder.update(datos) + padder.finalize()
        
        cipher = Cipher(algorithms.AES(llave_aes), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        cuerpo_cifrado = encryptor.update(datos_con_padding) + encryptor.finalize()
        
        # --- GENERAR SELLO HMAC ---
        h = hmac.HMAC(llave_hmac, hashes.SHA256(), backend=default_backend())
        h.update(salt + iv + cuerpo_cifrado)
        sello = h.finalize()
        
        # Asegurar que la extensión tenga el punto
        if not extension.startswith("."):
            extension = "." + extension
            
        ruta_destino = ruta_origen + extension
        with open(ruta_destino, "wb") as f:
            f.write(salt + iv + cuerpo_cifrado + sello)
            
        registrar_evento(f"🔒 CIFRADO (Modo Camuflaje {extension}): {ruta_origen}")
        return ruta_destino
    except Exception as e:
        registrar_evento(f"❌ ERROR AL CIFRAR: {str(e)}", "error")
        return "ERROR_SISTEMA"

def descifrar_archivo(ruta_cifrada, password):
    try:
        with open(ruta_cifrada, "rb") as f:
            datos_totales = f.read()
        
        salt = datos_totales[:16]
        iv = datos_totales[16:32]
        sello_leido = datos_totales[-32:]
        cuerpo_cifrado = datos_totales[32:-32]
        
        llave_aes, llave_hmac = generar_llave(password, salt)
        
        h = hmac.HMAC(llave_hmac, hashes.SHA256(), backend=default_backend())
        h.update(salt + iv + cuerpo_cifrado)
        try:
            h.verify(sello_leido)
        except Exception:
            registrar_evento(f"⚠️ INTEGRIDAD FALLIDA O CLAVE ERRÓNEA: {ruta_cifrada}", "warning")
            return "ERROR_PASSWORD"

        cipher = Cipher(algorithms.AES(llave_aes), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        datos_con_padding = decryptor.update(cuerpo_cifrado) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        datos_originales = unpadder.update(datos_con_padding) + unpadder.finalize()
        
        # Limpiar cualquier extensión de camuflaje
        nombre_archivo = os.path.basename(ruta_cifrada)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        
        directorio = os.path.dirname(ruta_cifrada)
        ruta_final = os.path.join(directorio, f"RECUPERADO_{nombre_sin_ext}")
        
        with open(ruta_final, "wb") as f:
            f.write(datos_originales)
            
        registrar_evento(f"🔓 DESCIFRADO EXITOSO: {ruta_cifrada}")
        return ruta_final
    except Exception as e:
        registrar_evento(f"❌ ERROR CRÍTICO: {str(e)}", "error")
        return "ERROR_SISTEMA"