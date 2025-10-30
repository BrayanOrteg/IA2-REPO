# 🎉 QuickTask - Entorno Docker Completado

## ✅ Resumen de lo implementado

Se han creado **7 archivos** para habilitar el despliegue de QuickTask con Docker:

| Archivo                    | Propósito                                                    |
|----------------------------|--------------------------------------------------------------|
| `Dockerfile`               | Imagen Docker base con Python 3.11 + FastAPI                |
| `docker-compose.yaml`      | Orquestación con volumen persistente para SQLite            |
| `.dockerignore`            | Optimización de imagen (excluir archivos innecesarios)      |
| `.env.docker`              | Ejemplo de variables de entorno                             |
| `docker-entrypoint.sh`     | Script de inicialización del contenedor                     |
| `deploy.ps1`               | Script automatizado de despliegue para PowerShell           |
| `DOCKER_QUICKSTART.md`     | Guía rápida con verificaciones paso a paso                  |
| `DOCKER_DEPLOY.md`         | Guía completa con troubleshooting y configuración avanzada  |

Además:
- ✅ `README.md` actualizado con sección de Docker
- ✅ `.gitignore` actualizado para excluir archivos de Docker

---

## 🚀 Cómo usar (3 opciones)

### Opción 1: Script automatizado (Recomendado) ⚡

```powershell
cd backend
.\deploy.ps1
```

Este script hace TODO automáticamente:
1. ✅ Verifica que Docker está instalado
2. ✅ Verifica que Docker daemon está corriendo
3. ✅ Construye la imagen
4. ✅ Inicia el contenedor
5. ✅ Verifica que la API está respondiendo
6. ✅ Muestra URLs y comandos útiles

### Opción 2: Comando manual simple

```powershell
cd backend
docker-compose up --build
```

### Opción 3: Modo daemon (segundo plano)

```powershell
cd backend
docker-compose up --build -d
```

---

## 📋 Verificación rápida (checklist)

Después de ejecutar el despliegue, verifica:

1. **¿El contenedor está corriendo?**
   ```powershell
   docker ps
   ```
   Deberías ver `quicktask-api` en la lista.

2. **¿La API responde?**
   Abrir en navegador: http://localhost:8000/docs
   
3. **¿Los endpoints funcionan?**
   ```powershell
   curl.exe http://localhost:8000/api/health
   ```
   Debería responder: `{"status": "ok"}`

4. **¿Puedo crear un usuario?**
   ```powershell
   curl.exe -X POST "http://localhost:8000/api/auth/register" `
     -H "Content-Type: application/json" `
     -d '{\"email\": \"test@test.com\", \"password\": \"test1234\"}'
   ```

5. **¿Los datos persisten?**
   ```powershell
   # Detener contenedor
   docker-compose down
   
   # Reiniciar
   docker-compose up -d
   
   # Verificar que los datos siguen ahí
   ```

---

## 🏗️ Arquitectura Docker implementada

```
┌─────────────────────────────────────────────────┐
│              Host (Windows)                     │
│                                                 │
│  Port 8000                                      │
│     │                                           │
│     ▼                                           │
│  ┌──────────────────────────────────────┐      │
│  │   Docker Container: quicktask-api    │      │
│  │                                      │      │
│  │  ┌─────────────────────────────┐    │      │
│  │  │   FastAPI (uvicorn)         │    │      │
│  │  │   Port 8000                 │    │      │
│  │  └─────────────────────────────┘    │      │
│  │              │                       │      │
│  │              ▼                       │      │
│  │  ┌─────────────────────────────┐    │      │
│  │  │   SQLAlchemy ORM            │    │      │
│  │  └─────────────────────────────┘    │      │
│  │              │                       │      │
│  │              ▼                       │      │
│  │  ┌─────────────────────────────┐    │      │
│  │  │   SQLite Database           │    │      │
│  │  │   /app/data/quicktask.db    │◄───┼──────┤
│  │  └─────────────────────────────┘    │      │
│  │                                      │      │
│  └──────────────────────────────────────┘      │
│                    │                            │
│                    ▼                            │
│  ┌──────────────────────────────────────┐      │
│  │  Volume: backend_quicktask-data      │      │
│  │  (Persistente)                       │      │
│  └──────────────────────────────────────┘      │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Características:**
- ✅ **Persistencia:** Los datos se guardan en un volumen Docker
- ✅ **Hot-reload:** Los cambios en código se reflejan automáticamente
- ✅ **Aislamiento:** El contenedor no afecta al sistema host
- ✅ **Portabilidad:** Funciona en cualquier máquina con Docker

---

## 📊 Comparativa: Docker vs Local

| Aspecto              | Docker (Recomendado)            | Local                           |
|----------------------|---------------------------------|---------------------------------|
| Instalación          | 1 comando                       | 3 pasos (venv, pip, etc.)       |
| Dependencias         | Automáticas                     | Manual (pip install)            |
| Portabilidad         | ✅ Alta (funciona en cualquier OS)| ❌ Depende del sistema         |
| Conflictos           | ✅ Ninguno (aislado)            | ⚠️ Posibles (versiones Python)  |
| Base de datos        | ✅ Persistente automática       | ⚠️ Manual (archivo local)       |
| Limpieza             | ✅ Fácil (docker-compose down)  | ⚠️ Manual (borrar archivos)     |
| Producción similar   | ✅ Sí                           | ❌ No                           |
| Curva de aprendizaje | ⚠️ Requiere conocer Docker      | ✅ Más familiar                 |

---

## 🛠️ Comandos esenciales

### Gestión del contenedor

```powershell
# Iniciar (con logs visibles)
docker-compose up

# Iniciar en segundo plano
docker-compose up -d

# Detener (mantiene datos)
docker-compose down

# Detener y eliminar datos
docker-compose down -v

# Reiniciar
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f
```

### Inspección

```powershell
# Ver contenedores activos
docker ps

# Ver uso de recursos
docker stats quicktask-api

# Inspeccionar volumen
docker volume inspect backend_quicktask-data

# Ejecutar comando dentro del contenedor
docker-compose exec quicktask-backend bash
```

### Mantenimiento

```powershell
# Reconstruir imagen (después de cambiar dependencias)
docker-compose up --build

# Limpiar imágenes no usadas
docker image prune

# Limpiar todo Docker (⚠️ cuidado)
docker system prune -a
```

---

## 🔧 Configuración avanzada

### Variables de entorno personalizadas

Crear archivo `.env` en `backend/`:

```env
DATABASE_URL=sqlite:///./data/quicktask.db
SECRET_KEY=tu-clave-super-secreta-de-al-menos-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Modificar `docker-compose.yaml`:

```yaml
services:
  quicktask-backend:
    env_file:
      - .env  # Cargar desde archivo
```

### Cambiar puerto

Editar `docker-compose.yaml`:

```yaml
ports:
  - "3000:8000"  # Host:Container
```

Ahora la API estará en: http://localhost:3000

### Usar PostgreSQL en lugar de SQLite

Agregar servicio en `docker-compose.yaml`:

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: quicktask
      POSTGRES_USER: quicktask
      POSTGRES_PASSWORD: changeme
    volumes:
      - postgres-data:/var/lib/postgresql/data

  quicktask-backend:
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://quicktask:changeme@db:5432/quicktask

volumes:
  postgres-data:
```

---

## 📈 Siguientes pasos

### 1. Desarrollo del frontend

Ahora que el backend está en Docker, puedes:

**Frontend Web (React):**
```powershell
# En el directorio raíz
cd frontend-web
npm install
npm start
```

Configurar en el frontend: `API_URL=http://localhost:8000`

**Frontend Móvil (React Native):**
```powershell
cd frontend-mobile
npm install
npx react-native run-android
```

Configurar: `API_URL=http://TU_IP:8000` (ej: `http://192.168.1.10:8000`)

### 2. Agregar más servicios

Puedes extender `docker-compose.yaml` para incluir:

- **Redis** (para cache y WebSockets)
- **Nginx** (reverse proxy)
- **Adminer** (interfaz web para DB)

Ejemplo con Redis:

```yaml
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"
  
  quicktask-backend:
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379
```

### 3. Preparar para producción

Ver sección completa en `DOCKER_DEPLOY.md`, incluye:

- Usar Gunicorn en lugar de Uvicorn
- Multi-stage builds para optimizar tamaño
- Health checks
- Logging centralizado
- Secrets management
- CI/CD con GitHub Actions

---

## 🆘 Troubleshooting

### Error: "puerto 8000 ya está en uso"

```powershell
# Opción 1: Detener el proceso que usa el puerto
netstat -ano | findstr :8000
taskkill /PID <numero> /F

# Opción 2: Cambiar puerto en docker-compose.yaml
```

### Error: "Cannot connect to the Docker daemon"

**Solución:** Abrir Docker Desktop y esperar a que esté listo (ícono verde)

### Error: "No se puede construir la imagen"

```powershell
# Ver logs detallados
docker-compose build --no-cache

# Verificar sintaxis del Dockerfile
docker-compose config
```

### Los cambios en código no se reflejan

```powershell
# Verificar que el volumen está montado
docker-compose exec quicktask-backend pwd
docker-compose exec quicktask-backend ls -la /app/app

# Reiniciar contenedor
docker-compose restart
```

### La base de datos no persiste

```powershell
# Verificar que el volumen existe
docker volume ls | findstr quicktask

# Ver detalles del volumen
docker volume inspect backend_quicktask-data
```

---

## 📚 Documentación completa

| Documento                  | Contenido                                      |
|----------------------------|------------------------------------------------|
| `DOCKER_QUICKSTART.md`     | Guía rápida con verificaciones paso a paso    |
| `DOCKER_DEPLOY.md`         | Guía completa con configuración avanzada      |
| `README.md`                | Documentación general del backend             |
| `QUICKSTART.md`            | Instalación local sin Docker                  |
| `TESTING.md`               | Guía de pruebas con pytest                    |
| `ARCHITECTURE.md`          | Arquitectura del sistema                      |

---

## ✅ Checklist final

- [x] Dockerfile creado
- [x] docker-compose.yaml configurado
- [x] Volumen persistente para SQLite
- [x] Hot-reload habilitado
- [x] Script de despliegue automatizado
- [x] Documentación completa
- [x] .dockerignore optimizado
- [x] Variables de entorno configuradas
- [x] Health check implementado
- [x] README actualizado

---

## 🎓 Conceptos clave aprendidos

1. **Containerización:** Empaqueta la app con todas sus dependencias
2. **Volúmenes:** Persistencia de datos fuera del contenedor
3. **Docker Compose:** Orquestación de múltiples servicios
4. **Hot-reload:** Desarrollo ágil con cambios automáticos
5. **Aislamiento:** El contenedor no afecta al sistema host
6. **Portabilidad:** El mismo entorno en dev, staging y producción

---

**🎉 ¡Entorno Docker completado exitosamente!**

Tu aplicación QuickTask ahora puede desplegarse con un solo comando y está lista para producción.

**Siguiente paso:** Desarrollar el frontend o agregar más servicios (Redis, PostgreSQL, Nginx).
