# Script de despliegue automático para QuickTask con Docker
# Uso: .\deploy.ps1

Write-Host "🚀 QuickTask - Despliegue con Docker" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Docker está instalado
Write-Host "🔍 Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker encontrado: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "   Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Verificar si Docker Compose está disponible
Write-Host "🔍 Verificando Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose encontrado: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker Compose no está disponible" -ForegroundColor Red
    exit 1
}

# Verificar si Docker daemon está corriendo
Write-Host "🔍 Verificando Docker daemon..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✅ Docker daemon está corriendo" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker daemon no está corriendo" -ForegroundColor Red
    Write-Host "   Inicia Docker Desktop desde el menú de Windows" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📦 Construyendo imagen Docker..." -ForegroundColor Yellow
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al construir la imagen" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Imagen construida exitosamente" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Iniciando contenedor..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al iniciar el contenedor" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Contenedor iniciado exitosamente" -ForegroundColor Green
Write-Host ""

# Esperar a que el servidor esté listo
Write-Host "⏳ Esperando a que el servidor esté listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar health check
Write-Host "🏥 Verificando health check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -Method GET -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API está respondiendo correctamente" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Advertencia: No se pudo verificar el health check" -ForegroundColor Yellow
    Write-Host "   La API puede estar iniciando todavía" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅ ¡Despliegue completado!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 URLs disponibles:" -ForegroundColor Cyan
Write-Host "   • API:         http://localhost:8000" -ForegroundColor White
Write-Host "   • API Docs:    http://localhost:8000/docs" -ForegroundColor White
Write-Host "   • Health:      http://localhost:8000/api/health" -ForegroundColor White
Write-Host ""
Write-Host "📋 Comandos útiles:" -ForegroundColor Cyan
Write-Host "   • Ver logs:    docker-compose logs -f" -ForegroundColor White
Write-Host "   • Detener:     docker-compose down" -ForegroundColor White
Write-Host "   • Reiniciar:   docker-compose restart" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentación:" -ForegroundColor Cyan
Write-Host "   • DOCKER_QUICKSTART.md  - Guía rápida" -ForegroundColor White
Write-Host "   • DOCKER_DEPLOY.md      - Guía completa" -ForegroundColor White
Write-Host ""
