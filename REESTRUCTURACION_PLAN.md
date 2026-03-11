# Plan de Reestructuración del Sitio Web

## Objetivo
Reorganizar la estructura del sitio web para usar URLs limpias y eliminar imágenes externas, manteniendo la funcionalidad y diseño profesional.

## Estructura de Carpetas a Crear
```
G2_Site_Templatex /G2_Site_Template/ o G2_Site_Templatex 
├── about-us/
│   └── index.html
├── contact-us/
│   └── index.html
├── privacy-policy/
│   └── index.html
├── terms-and-conditions/
│   └── index.html
└── cookie-policy/
    └── index.html
```

## Archivos Fuente Existentes
- `about.html` → `/about-us/index.html`
- `contact.html` → `/contact-us/index.html`
- `privacy.html` → `/privacy-policy/index.html`
- `terms.html` → `/terms-and-conditions/index.html`
- `cookies.html` → `/cookie-policy/index.html`

## Modificaciones Necesarias

### 1. Actualización de URLs
- Cambiar enlaces relativos a formato `/ruta/` (ej: `about.html` → `/about-us/`)
- Actualizar rutas de navegación en headers y footers
- Ajustar rutas de assets (CSS, JS) para estructura de carpetas
- Actualizar dominio principal en todas las referencias (actual: esperar la ruta a ser asignada)
- **Agregar dominio completo a URLs de navegación**: Convertir rutas `/ruta/` a `ruta esperada por chat`

### 2. Eliminación de Imágenes
- **index.html**: Remover imagen de Unsplash en Hero section
- **about.html**: Verificar y eliminar imágenes externas si existen
- Reemplazar imágenes con elementos de diseño alternativos (iconos SVG, gradientes)
- Ajustar márgenes y layout para mantener diseño sin imágenes

### 3. Mejora de Estilos
- Aumentar espaciado en secciones para compensar falta de imágenes
- Mantener estructura responsive y accesibilidad
- Preservar colores, tipografía y componentes existentes

### 4. Mantenimiento de Funcionalidad
- Preservar scripts de navegación móvil
- Mantener estilos CSS y Tailwind
- Conservar formularios de contacto y popups
- Mantener estructura de compliance notices

## Consideraciones Técnicas

### Rutas de Assets
- Archivos en carpetas: usar `../assets/`
- Archivos en raíz: usar `assets/`
- Verificar que todas las rutas sean correctas

### URLs Absolutas vs Relativas
- **Navegación principal**: usar `https://esperar la ruta a ser asignada/ruta/` (dominio completo)
- **Assets**: usar rutas relativas según ubicación (`../assets/` para carpetas, `assets/` para raíz)
- **Enlaces en footer**: actualizar consistentemente con dominio completo
- **Dominio principal**: actualizar en enlaces y referencias textuales
- **Logo/Home**: actualizar a `https://esperar la ruta a ser asignada/`

### Eliminación de Archivos Originales
- Eliminar archivos HTML originales después de crear versiones en carpetas
- Verificar que no queden referencias a archivos eliminados

## Verificación Final
1. ✅ Todas las carpetas creadas
2. ✅ Todos los archivos transformados
3. ✅ URLs actualizadas correctamente
4. ✅ Rutas de assets funcionando
5. ✅ Imágenes eliminadas/reemplazadas
6. ✅ Márgenes y layout optimizados
7. ✅ Navegación consistente en todas las páginas
8. ✅ Dominios actualizados en URLs de navegación (https://esperar la ruta a ser asignada/)

## Notas de Implementación

### index.html
- Hero section: reemplazar imagen de Unsplash con icono y gradiente
- Aumentar márgenes para compensar falta de imagen
- Actualizar todos los enlaces de navegación con dominio completo

### Actualización de URLs con Dominio
- **Todos los archivos HTML**: Actualizar enlaces de navegación a formato `https://esperar la ruta a ser asignada/ruta/`
- **Tipos de enlaces actualizados**:
  - Logo/Home: `href="https://esperar la ruta a ser asignada/"`
  - About Us: `href="https://esperar la ruta a ser asignada/about-us/"`
  - Contact Us: `href="https://esperar la ruta a ser asignada/contact-us/"`
  - Privacy Policy: `href="https://esperar la ruta a ser asignada/privacy-policy/"`
  - Terms & Conditions: `href="https://esperar la ruta a ser asignada/terms-and-conditions/"`
  - Cookie Policy: `href="https://esperar la ruta a ser asignada/cookie-policy/"`
- **Verificación**: Eliminar todas las URLs relativas `/` restantes

### Archivos en Carpetas
- Mantener contenido textual original
- Actualizar headers y footers con nuevas URLs (dominio completo)
- Ajustar rutas de assets a `../assets/`
- Actualizar enlace del logo a `https://esperar la ruta a ser asignada/`

### Estilos CSS
- No modificar archivos CSS existentes
- Usar clases Tailwind para ajustes de layout
- Mantener consistencia visual

## Proceso de Actualización de Dominios

### Archivos Afectados
1. **index.html** - Navegación principal y footer
2. **about-us/index.html** - Navegación y footer  
3. **contact-us/index.html** - Navegación y footer
4. **privacy-policy/index.html** - Navegación y footer
5. **terms-and-conditions/index.html** - Navegación y footer
6. **cookie-policy/index.html** - Navegación y footer

### Comandos Ejecutados
```bash
# Actualizar enlaces de navegación en todos los archivos
sed -i 's|href="/about-us/"|href="https://esperar la ruta a ser asignada/about-us/"|g' archivo.html
sed -i 's|href="/contact-us/"|href="https://esperar la ruta a ser asignada/contact-us/"|g' archivo.html
sed -i 's|href="/privacy-policy/"|href="https://esperar la ruta a ser asignada/privacy-policy/"|g' archivo.html
sed -i 's|href="/terms-and-conditions/"|href="https://esperar la ruta a ser asignada/terms-and-conditions/"|g' archivo.html
sed -i 's|href="/cookie-policy/"|href="https://esperar la ruta a ser asignada/cookie-policy/"|g' archivo.html
sed -i 's|href="../index.html"|href="https://esperar la ruta a ser asignada/"|g' archivo.html
sed -i 's|href="index.html"|href="https://esperar la ruta a ser asignada/"|g' archivo.html
```

### Verificación Final
- ✅ Todas las URLs relativas `/` eliminadas
- ✅ Navegación consistente en todas las páginas
- ✅ Dominio completo aplicado a todos los enlaces de navegación
- ✅ Rutas de assets preservadas y funcionando

## Resultado Esperado
Sitio web con estructura organizada, URLs limpias con dominio completo, sin dependencias de imágenes externas, manteniendo diseño profesional y funcionalidad completa.