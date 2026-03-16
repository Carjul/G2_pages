# README - Boceto de Páginas de Educación Financiera

## Introducción
Este proyecto utiliza el directorio `1/1/` como Boceto base para crear nuevas páginas de educación financiera. Estas páginas se generan copiando la estructura y aplicando estilos personalizados mediante las reglas definidas en `.agents/rules/pages.md`. El enfoque es crear sitios genéricos, sin referencias específicas a brokers, y optimizados para SEO, velocidad y seguridad. No se utilizan imágenes externas; en su lugar, se emplean gradientes de Tailwind CSS. Los dominios se manejan con carpetas para ocultar extensiones .html y mejorar la navegación.

## Estructura del Boceto
El Boceto base se encuentra en `1/1/` y consta de:
- `index.html`: Página principal con secciones como Hero, Características, Audiencia y Transparencia.
- Subdirectorios con `index.html` para URLs limpias (sin .html visible):
  - `about-us/`: Página "Acerca de" con información genérica sobre el sitio.
  - `contact-us/`: Página de contacto simple.
  - `cookie-policy/`, `privacy-policy/`, `terms-and-conditions/`: Políticas básicas (contenido minimalista).

La navegación utiliza URLs absolutas (ej. `/about-us/`) para consistencia. Los assets (CSS/JS) se ubican en `assets/` en la raíz; en subpáginas, se accede con `../assets/`.

## Desglose del Contenido
Cada archivo HTML sigue una estructura repetitiva para educación financiera:
- **Disclaimers**: Dos al principio y al final de cada página, con texto genérico sobre riesgos e información general (no específico de inversiones).
- **Contenido Genérico**: Secciones como ELS (Educación en Línea Segura) sin menciones a brokers. El contenido es repetitivo para reforzar conceptos educativos, pero adaptable.
- **Elementos Comunes**: Header con navegación, footer estándar, y diseño responsivo con Tailwind CSS.

Ejemplo en `index.html`: Hero con gradiente de fondo, listas de características, y llamadas a acción genéricas.

## Proceso de Personalización
1. **Copiar el Boceto**: Usa scripts como `create-html-files.ps1` para duplicar `1/1/` a un nuevo directorio (ej. `G2_Site_TemplateX`).
2. **Aplicar Estilos**: Modifica solo las clases de Tailwind CSS en `class=""` o `className=""` según las reglas en `pages.md` (elige conceptos como Glassmorphism o Minimalismo, asegura contraste WCAG y espaciado coherente). No cambies etiquetas HTML, texto ni lógica.
3. **Cambios Post-Copia**: Actualiza nombres de dominios a absolutos (ej. `https://[dominio]/about-us/`), elimina imágenes (reemplaza con gradientes), y ajusta rutas de assets.
4. **Seguridad**: Integra reglas de `.htaccess` desde `segurity.txt` (HSTS, CSP, X-Frame-Options, etc.) usando scripts como `add_csp_hash.py`.
5. **Verificación**: Ejecuta checks con `site_check_report.csv` para validar enlaces y assets.

## Registro de Mejoras
- **Despliegue Directo**: Sin WordPress; se hace directamente en el dominio principal vía SFTP (scripts como `sftp_deploy_template.py`).
- **Revisión de Headers**: Se agregan códigos personalizados al header y footer para navegación consistente.
- **Estructura de Contenido**: Contenido genérico (no broker-like), con políticas minimalistas en Contact y About.
- **Reestructuración de Directorios**: Conversión de archivos planos a carpetas para URLs limpias (plan en `Plan de Reestructuración G2_Site.md`).
- **Optimizaciones Visuales**: Eliminación de imágenes externas, expansión de layouts, y gradientes para fondos.
- **Automatización**: Scripts Python para reemplazos masivos (`bulk_replace.py`) y uploads remotos.
- **Seguridad Mejorada**: Headers de seguridad integrados, sin dependencias externas innecesarias.
- **Últimas Mejoras**: Integración de CSP hashes, validación post-despliegue, y organización de carpetas por dominio (manejo por Mauricio).

## Flujos Internos
- **Organización de Carpetas**: Dominios en subcarpetas nombradas genéricamente (ej. `site1/`, `site2/`); assets compartidos.
- **Revisores Utilizados**: Validación manual y automática con scripts; checks para accesibilidad y carga.
- **Prácticas de Código**: Mantén consistencia en clases Tailwind, usa absolutas para enlaces, y evita lógica JS adicional.
- **Despliegue**: Sube vía SFTP, elimina archivos originales post-verificación.

Este Boceto permite crear variantes rápidas y seguras para educación financiera. Para dudas, consulta los scripts en `scripts/` o el plan de reestructuración.