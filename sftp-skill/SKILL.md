# SKILL.md - SFTP Operations Skill

## Skill Purpose
Este archivo describe una habilidad para realizar operaciones básicas mediante SFTP (Protocolo de Transferencia de Archivos SSH), incluyendo:

1. **Subir Archivos:**
   Transferir archivos desde el sistema local al servidor remoto usando el comando `put`.

2. **Descargar Archivos:**
   Copiar archivos desde el servidor remoto al sistema local con el comando `get`.

3. **Editar Archivos:**
   Permitir modificar archivos en el servidor remoto, combinando una descarga, edición local y subida.

4. **Eliminar Archivos:**
   Borrar archivos específicos en el servidor remoto utilizando el comando `rm`.

---

## Prácticas de Seguridad

- **Implementar Claves SSH:** Prioriza la autenticación mediante claves SSH en lugar de contraseñas para mayor seguridad.
- **Validación de Rutas:** Asegúrate de validar correctamente los archivos y rutas antes de ejecutar comandos.
- **Gestión de Permisos:** Limita permisos innecesarios en el servidor remoto.

---

## Requisitos

- **SFTP Client:** Una herramienta, como OpenSSH cliente o cualquier librería en tu configuración de OpenCode, para ejecutar estos comandos de forma automática.
- **Gestión de Errores:** Incluir comprobaciones para errores comunes como credenciales inválidas, archivos inexistentes o fallos de conexión.

---

## Cómo Procesará OpenCode

1. **Automatización:** Este archivo es interpretado por OpenCode como una guía práctica para los comandos.
2. **Ejemplos:** Cada operación puede ser desencadenada como un comando directo: por ejemplo, subir nuevos archivos a rutas fijas específicas en su servidor (p. ej., /var/www/).

    - **Subir:**
      ```plaintext
      sftp usuario@host
      sftp> put local_file
      ```
    
    - **Descargar:**
      ```plaintext
      sftp> get remote_file target_path_local/
      ```