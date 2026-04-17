# CryptoGuard v1.1 - Secure Cipher Engine

## Descripcion Tecnica 
CryptoGuard es un motor de cifrado de archivos desarrollado bajo estandares de criptografia moderna. El objetivo del proyecto es garantizar la Triada de la seguridad (Confidencialidad, Integridad y Disponibilidad) mediante algoritmos de grado militar.

## Especificaciones de Seguridad
* **Cifrado Simetrico:** AES-256 en modo CBC (Cipher Block Chaining).
* **Derivacion de Llaves:** PBKDF2 (Password-Based Key Derivation Function 2) utilizando SHA-256 con **100,000 interacciones** y Salt aleatorio de 16 bytes.
* **Integridad y Autenticidad:** Implementacion de **HMAC-SHA256** (Hash-based Message Authentication Code). El sistema verifica el sello antes de intentar el descifrado para mitigar ataques de manipulacion de bits.
* **Borrado Forense:** Funcion de "Shredding" que sobrescribe fisicamente los sectores del archivo con datos aleatorios (`os.urandom`) antes de la eliminacion de; sistema de archivos.

## Caracteristicas 
- Generador de contraseñas de alta entropia integrado.
- Modo Camuflaje (Extensiones personalizables).
- Bitacora de eventos (Logging) para auditoria.
- Interfaz grafica minimalista en modo oscuro con acentos pasteles.

## Creador
Carlos Sandoval Rodriguez --- Abril 2026. 