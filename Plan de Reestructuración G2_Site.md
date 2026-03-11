# Directiva Técnica: Reestructuración y Optimización G2_Site

## 1. Objetivo y Alcance
[cite_start]Transformar la estructura de archivos planos a una arquitectura de **URLs Limpias**, eliminar dependencias de imágenes externas (Unsplash) y estandarizar la navegación con dominios absolutos para mejorar el SEO y la velocidad de carga.

## 2. Configuración de Variables
- **Dominio Destino:** `https://[INSERTAR_DOMINIO_AQUÍ]/`
- [cite_start]**Carpeta Raíz:** `G2_Site_Template` o `G2_Site_Templatex` 

## 3. Matriz de Reestructuración de Directorios
[cite_start]Se debe crear una carpeta por cada página secundaria y renombrar el archivo fuente a `index.html` dentro de dicha carpeta:

| Archivo Fuente (Raíz) | Directorio Destino | Archivo Final |
| :--- | :--- | :--- |
| `about.html` | `/about-us/` | [cite_start]`index.html`  |
| `contact.html` | `/contact-us/` | [cite_start]`index.html`  |
| `privacy.html` | `/privacy-policy/` | [cite_start]`index.html`  |
| `terms.html` | `/terms-and-conditions/` | [cite_start]`index.html`  |
| `cookies.html` | `/cookie-policy/` | [cite_start]`index.html`  |

## 4. Reglas de Transformación de Contenido

### 4.1 Actualización de Rutas de Assets
- [cite_start]**Archivos en Raíz (`/index.html`):** Mantener rutas como `assets/css/...` o `assets/js/...`.
- [cite_start]**Archivos en Subcarpetas (`/*/index.html`):** Cambiar todas las referencias de assets a `../assets/` para mantener la vinculación correcta.

### 4.2 Estandarización de Navegación (URLs Absolutas)
[cite_start]Sustituir todos los enlaces de navegación en Header y Footer por el dominio completo:
- [cite_start]**Home:** `https://[DOMINIO]/` 
- [cite_start]**About:** `https://[DOMINIO]/about-us/` 
- [cite_start]**Contact:** `https://[DOMINIO]/contact-us/` 
- [cite_start]**Privacy:** `https://[DOMINIO]/privacy-policy/` 
- [cite_start]**Terms:** `https://[DOMINIO]/terms-and-conditions/` 
- [cite_start]**Cookies:** `https://[DOMINIO]/cookie-policy/` 

## 5. Optimización de Diseño y Limpieza Visual

### 5.1 Eliminación de Imágenes Externas
- [cite_start]**Acción:** Localizar y eliminar etiquetas `<img>` o estilos `background-image` que apunten a `unsplash.com` u otros dominios externos.
- [cite_start]**Sustitución en Hero Section:** Reemplazar la imagen de fondo con un gradiente moderno usando Tailwind CSS: `bg-gradient-to-br from-gray-900 via-blue-900 to-black`.

### 5.2 Ajustes de Layout (Compensación de Espacios)
- [cite_start]**Centrado:** Si una sección pierde una imagen lateral, cambiar el ancho del contenedor de texto de `w-1/2` a `w-full` o `max-w-4xl mx-auto`.
- [cite_start]**Espaciado:** Incrementar el padding vertical (`py-20` a `py-32`) en secciones que hayan quedado sin soporte visual para mantener la estética profesional.

## 6. Protocolo de Limpieza de Servidor (SFTP)
[cite_start]Una vez verificada la correcta creación de las nuevas carpetas e índices:
1. [cite_start]**Listar** archivos en la raíz del servidor.
2. [cite_start]**Eliminar** archivos HTML originales: `about.html`, `contact.html`, `privacy.html`, `terms.html` y `cookies.html`.
3. [cite_start]**Restricción:** No eliminar bajo ninguna circunstancia el archivo `readme.html`.

## 7. Verificación Final
1. [cite_start][ ] ¿Todas las subcarpetas contienen un `index.html` funcional? 
2. [cite_start][ ] ¿Los assets (CSS/JS) cargan correctamente desde las subcarpetas (`../`)? 
3. [cite_start][ ] ¿Todos los enlaces de navegación incluyen el protocolo `https://` y el dominio? 
4. [cite_start][ ] ¿Se eliminaron las imágenes externas y se ajustó el layout con Tailwind?