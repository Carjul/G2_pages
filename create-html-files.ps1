# Script para crear una carpeta y copiar archivos desde la plantilla '1'

# Nombre de la carpeta
$folderName = "G2_Site_Template29"
$templatePath = "1\1"

# Crear la carpeta si no existe
if (-not (Test-Path $folderName)) {
    New-Item -ItemType Directory -Path $folderName -Force | Out-Null
    Write-Host "Carpeta '$folderName' creada exitosamente" -ForegroundColor Green
}
else {
    Write-Host "La carpeta '$folderName' ya existe" -ForegroundColor Yellow
}

# Copiar archivos desde la plantilla en lugar de crearlos vacíos
if (Test-Path $templatePath) {
    Copy-Item -Path "$templatePath\*" -Destination $folderName -Recurse -Force
    Write-Host "Archivos copiados desde '$templatePath' a '$folderName'" -ForegroundColor Cyan
}
else {
    Write-Host "Error: No se encontró la carpeta de plantilla '$templatePath'" -ForegroundColor Red
}

Write-Host "`nTodos los archivos han sido copiados en la carpeta '$folderName'" -ForegroundColor Green
