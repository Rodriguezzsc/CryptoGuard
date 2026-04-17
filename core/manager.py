import os
from core.encryptor import cifrar_archivo, descifrar_archivo

def procesar_carpeta(ruta_carpeta, password, modo="cifrar"):
    resultados = {"exitos": 0, "errores": 0}
    
    # El "Barrido": revisamos cada cosa dentro de la carpeta
    for nombre in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, nombre)
        
        if os.path.isfile(ruta_completa):
            if modo == "cifrar" and not nombre.endswith(".crypt"):
                cifrar_archivo(ruta_completa, password)
                resultados["exitos"] += 1
            elif modo == "descifrar" and nombre.endswith(".crypt"):
                res = descifrar_archivo(ruta_completa, password)
                if res == "ERROR_PASSWORD":
                    resultados["errores"] += 1
                else:
                    resultados["exitos"] += 1
    return resultados