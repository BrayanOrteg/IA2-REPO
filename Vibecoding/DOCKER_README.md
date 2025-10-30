# 🐳 QuickTask - Despliegue con Docker

## 📦 Archivos Docker creados

Se han generado todos los archivos necesarios para desplegar QuickTask con Docker:

```
backend/
├── Dockerfile                   ⭐ Imagen Docker (Python 3.11 + FastAPI)
├── docker-compose.yaml          ⭐ Orquestación de servicios
├── .dockerignore                🚫 Archivos excluidos de la imagen
├── .env.docker                  🔧 Variables de entorno (ejemplo)
├── docker-entrypoint.sh         🚀 Script de inicialización
├── deploy.ps1                   ⚡ Script automatizado (PowerShell)
│
└── 📚 Documentación:
    ├── DOCKER_STEPS.md          📋 Instrucciones paso a paso
    ├── DOCKER_QUICKSTART.md     ⚡ Guía rápida (5 min)
    ├── DOCKER_DEPLOY.md         📖 Guía completa (troubleshooting)
    └── DOCKER_SUMMARY.md        📊 Resumen ejecutivo
```

---

## 🚀 Inicio rápido (Quick Start)

### Opción 1: Script automatizado (Recomendado)

```powershell
cd backend
.\deploy.ps1
```

Este script hace TODO por ti:
- ✅ Verifica Docker
- ✅ Construye la imagen
- ✅ Inicia el contenedor
- ✅ Verifica que funciona
- ✅ Te muestra las URLs

### Opción 2: Manual

```powershell
cd backend
docker-compose up --build
```

**¡Listo!** La API estará en: http://localhost:8000

---

## 📖 Documentación

| Archivo                    | Para quién                           | Contenido                                |
|----------------------------|--------------------------------------|------------------------------------------|
| `DOCKER_STEPS.md`          | 👨‍💻 Principiantes                     | Instrucciones paso a paso con ejemplos   |
| `DOCKER_QUICKSTART.md`     | ⚡ Quienes quieren empezar rápido    | Guía de 5 minutos con verificaciones     |
| `DOCKER_DEPLOY.md`         | 🔧 Usuarios avanzados                | Configuración completa + troubleshooting |
| `DOCKER_SUMMARY.md`        | 📊 Todos                             | Resumen ejecutivo con checklist          |

**Recomendación:** 
- Si es tu primera vez con Docker → `DOCKER_STEPS.md`
- Si ya conoces Docker → `DOCKER_QUICKSTART.md`

---

## ✅ Verificación rápida

Después de ejecutar `docker-compose up`, verifica:

```powershell
# 1. ¿El contenedor está corriendo?
docker ps

# 2. ¿La API responde?
curl.exe http://localhost:8000/api/health

# 3. ¿Puedo ver la documentación?
# Abrir en navegador: http://localhost:8000/docs
```

---

## 🎯 Características implementadas

- ✅ **Imagen optimizada** con Python 3.11 slim
- ✅ **Hot-reload** habilitado para desarrollo ágil
- ✅ **Volumen persistente** para SQLite (los datos no se pierden)
- ✅ **Health check** automático cada 30 segundos
- ✅ **Variables de entorno** configurables
- ✅ **Script automatizado** de despliegue
- ✅ **Documentación completa** con troubleshooting

---

## 📊 Arquitectura

```
Host Windows (Port 8000)
        │
        ▼
Docker Container: quicktask-api
        │
        ├─ FastAPI (uvicorn)
        ├─ SQLAlchemy ORM
        └─ SQLite Database ◄── Volumen persistente
```

**Ventajas:**
- 🚀 Despliegue en 1 comando
- 🔒 Aislamiento del sistema host
- 💾 Datos persistentes automáticos
- 🔄 Hot-reload para desarrollo
- 📦 Portabilidad total

---

## 🛠️ Comandos esenciales

```powershell
# Iniciar
docker-compose up

# Iniciar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener (mantiene datos)
docker-compose down

# Reiniciar
docker-compose restart

# Reconstruir (después de cambiar dependencias)
docker-compose up --build
```

---

## 🆘 ¿Problemas?

### Puerto 8000 ocupado
```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8000

# O cambiar puerto en docker-compose.yaml
```

### Docker daemon no responde
- Abrir Docker Desktop
- Esperar al ícono verde
- Intentar de nuevo

### Cambios no se reflejan
```powershell
docker-compose restart
```

**Más troubleshooting:** Ver `DOCKER_DEPLOY.md`

---

## 🎓 Lo que aprenderás

Con esta implementación dominarás:

1. **Containerización** con Docker
2. **Orquestación** con Docker Compose
3. **Persistencia** con volúmenes
4. **Hot-reload** en desarrollo
5. **Health checks** y monitoring
6. **Variables de entorno** para configuración
7. **Troubleshooting** de contenedores

---

## 📚 Recursos adicionales

- **Docker oficial:** https://docs.docker.com/
- **FastAPI + Docker:** https://fastapi.tiangolo.com/deployment/docker/
- **Docker Compose:** https://docs.docker.com/compose/

---

## 🎉 Siguiente paso

Una vez que el backend esté corriendo:

1. **Desarrollar frontend web**
   ```powershell
   cd frontend-web
   npm install
   npm start
   ```

2. **Desarrollar frontend móvil**
   ```powershell
   cd frontend-mobile
   npm install
   npx react-native run-android
   ```

3. **Agregar más servicios**
   - Redis (cache + WebSockets)
   - PostgreSQL (producción)
   - Nginx (reverse proxy)

Ver ejemplos en `DOCKER_DEPLOY.md`

---

**✅ Todo listo para desarrollar con Docker! 🐳**
