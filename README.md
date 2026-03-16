# <span style="color: #2E86AB; font-family: Arial, sans-serif;">README - Boceto de Páginas de Educación Financiera</span>

## <span style="color: #A23B72; font-weight: bold;">Introducción</span>
<p style="font-size: 16px; line-height: 1.6; color: #333;">
  Este proyecto utiliza el directorio <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">1/1/</code> como Boceto base para crear nuevas páginas de educación financiera. Estas páginas se generan copiando la estructura y aplicando estilos personalizados mediante las reglas definidas en <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">.agents/rules/pages.md</code>. El enfoque es crear sitios genéricos, sin referencias específicas a brokers, y optimizados para SEO, velocidad y seguridad. No se utilizan imágenes externas; en su lugar, se emplean gradientes de Tailwind CSS. Los dominios se manejan con carpetas para ocultar extensiones .html y mejorar la navegación.
</p>

## <span style="color: #A23B72; font-weight: bold;">Estructura del Boceto</span>
<div style="background-color: #F7F7F7; padding: 15px; border-left: 5px solid #2E86AB; margin: 10px 0;">
  <p style="font-size: 16px; line-height: 1.6; color: #333;">El Boceto base se encuentra en <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">1/1/</code> y consta de:</p>
  <ul style="font-size: 16px; line-height: 1.6; color: #333;">
    <li><strong>index.html:</strong> Página principal con secciones como Hero, Características, Audiencia y Transparencia.</li>
    <li><strong>Subdirectorios con index.html para URLs limpias (sin .html visible):</strong>
      <ul>
        <li><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">about-us/</code>: Página "Acerca de" con información genérica sobre el sitio.</li>
        <li><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">contact-us/</code>: Página de contacto simple.</li>
        <li><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">cookie-policy/</code>, <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">privacy-policy/</code>, <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">terms-and-conditions/</code>: Políticas básicas (contenido minimalista).</li>
      </ul>
    </li>
  </ul>
  <p style="font-size: 16px; line-height: 1.6; color: #333;">La navegación utiliza URLs absolutas (ej. <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">/about-us/</code>) para consistencia. Los assets (CSS/JS) se ubican en <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">assets/</code> en la raíz; en subpáginas, se accede con <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">../assets/</code>.</p>
</div>

## <span style="color: #A23B72; font-weight: bold;">Desglose del Contenido</span>
<p style="font-size: 16px; line-height: 1.6; color: #333;">
  Cada archivo HTML sigue una estructura repetitiva para educación financiera:
</p>
<ul style="font-size: 16px; line-height: 1.6; color: #333;">
  <li><strong>Disclaimers:</strong> Dos al principio y al final de cada página, con texto genérico sobre riesgos e información general (no específico de inversiones).</li>
  <li><strong>Contenido Genérico:</strong> Secciones como ELS (Educación en Línea Segura) sin menciones a brokers. El contenido es repetitivo para reforzar conceptos educativos, pero adaptable.</li>
  <li><strong>Elementos Comunes:</strong> Header con navegación, footer estándar, y diseño responsivo con Tailwind CSS.</li>
</ul>
<p style="font-size: 16px; line-height: 1.6; color: #333;">
  <em>Ejemplo en index.html:</em> Hero con gradiente de fondo, listas de características, y llamadas a acción genéricas.
</p>

## <span style="color: #A23B72; font-weight: bold;">Proceso de Personalización</span>
<ol style="font-size: 16px; line-height: 1.6; color: #333;">
  <li><strong>Copiar el Boceto:</strong> Usa scripts como <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">create-html-files.ps1</code> para duplicar <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">1/1/</code> a un nuevo directorio (ej. <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">G2_Site_TemplateX</code>).</li>
  <li><strong>Aplicar Estilos:</strong> Modifica solo las clases de Tailwind CSS en <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">class=""</code> o <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">className=""</code> según las reglas en <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">pages.md</code> (elige conceptos como Glassmorphism o Minimalismo, asegura contraste WCAG y espaciado coherente). No cambies etiquetas HTML, texto ni lógica.</li>
  <li><strong>Cambios Post-Copia:</strong> Actualiza nombres de dominios a absolutos (ej. <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">https://[dominio]/about-us/</code>), elimina imágenes (reemplaza con gradientes), y ajusta rutas de assets.</li>
  <li><strong>Seguridad:</strong> Integra reglas de <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">.htaccess</code> desde <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">segurity.txt</code> (HSTS, CSP, X-Frame-Options, etc.) usando scripts como <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">add_csp_hash.py</code>.</li>
  <li><strong>Verificación:</strong> Ejecuta checks con <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">site_check_report.csv</code> para validar enlaces y assets.</li>
</ol>

## <span style="color: #A23B72; font-weight: bold;">Registro de Mejoras</span>
<div style="background-color: #E8F4F8; padding: 15px; border-radius: 8px; margin: 10px 0;">
  <ul style="font-size: 16px; line-height: 1.6; color: #333;">
    <li><strong>Despliegue Directo:</strong> Sin WordPress; se hace directamente en el dominio principal vía SFTP (scripts como <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">sftp_deploy_template.py</code>).</li>
    <li><strong>Revisión de Headers:</strong> Se agregan códigos personalizados al header y footer para navegación consistente.</li>
    <li><strong>Estructura de Contenido:</strong> Contenido genérico (no broker-like), con políticas minimalistas en Contact y About.</li>
    <li><strong>Reestructuración de Directorios:</strong> Conversión de archivos planos a carpetas para URLs limpias (plan en <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">Plan de Reestructuración G2_Site.md</code>).</li>
    <li><strong>Optimizaciones Visuales:</strong> Eliminación de imágenes externas, expansión de layouts, y gradientes para fondos.</li>
    <li><strong>Automatización:</strong> Scripts Python para reemplazos masivos (<code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">bulk_replace.py</code>) y uploads remotos.</li>
    <li><strong>Seguridad Mejorada:</strong> Headers de seguridad integrados, sin dependencias externas innecesarias.</li>
    <li><strong>Últimas Mejoras:</strong> Integración de CSP hashes, validación post-despliegue, y organización de carpetas por dominio (manejo por Mauricio).</li>
  </ul>
</div>

## <span style="color: #A23B72; font-weight: bold;">Flujos Internos</span>
<ul style="font-size: 16px; line-height: 1.6; color: #333;">
  <li><strong>Organización de Carpetas:</strong> Dominios en subcarpetas nombradas genéricamente (ej. <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">site1/</code>, <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">site2/</code>); assets compartidos.</li>
  <li><strong>Revisores Utilizados:</strong> Validación manual y automática con scripts; checks para accesibilidad y carga.</li>
  <li><strong>Prácticas de Código:</strong> Mantén consistencia en clases Tailwind, usa absolutas para enlaces, y evita lógica JS adicional.</li>
  <li><strong>Despliegue:</strong> Sube vía SFTP, elimina archivos originales post-verificación.</li>
</ul>

<p style="font-size: 16px; line-height: 1.6; color: #333; font-style: italic;">
  Este Boceto permite crear variantes rápidas y seguras para educación financiera. Para dudas, consulta los scripts en <code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px;">scripts/</code> o el plan de reestructuración.
</p>