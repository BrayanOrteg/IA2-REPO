# 🐳 QuickTask - Despliegue Local con Docker

## ✅ Resumen Ejecutivo

Has creado exitosamente los archivos de Docker para desplegar QuickTask localmente.

---

## 📦 Archivos creados

| Archivo                   | Propósito                                              |
|---------------------------|--------------------------------------------------------|
| `Dockerfile`              | Imagen Docker con Python 3.11 y FastAPI               |
| `docker-compose.yaml`     | Orquestación de servicios con volumen persistente     |
| `.dockerignore`           | Archivos excluidos de la imagen                       |
| `.env.docker`             | Variables de entorno de ejemplo                       |
| `docker-entrypoint.sh`    | Script de inicialización del contenedor               |
| `DOCKER_DEPLOY.md`        | Guía completa de despliegue con Docker                |

---

## 🚀 Pasos para ejecutar QuickTask

### Paso 1: Verificar requisitos previos

```powershell
# Verificar que Docker Desktop está instalado y corriendo
docker --version
docker-compose --version
```

**Resultado esperado:**
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

### Paso 2: Navegar al directorio backend

```powershell
cd c:\Users\Brayan\Documents\Trabajos_U\SEMESTRE_9\IA2\Vibecoding\backend
```

### Paso 3: Levantar el contenedor

```powershell
docker-compose up --build
```

**Esto hará:**
1. ✅ Descarga la imagen de Python 3.11
2. ✅ Instala todas las dependencias desde `requirements.txt`
3. ✅ Copia el código de la aplicación
4. ✅ Crea un volumen persistente para SQLite
5. ✅ Inicia el servidor FastAPI en http://localhost:8000
6. ✅ Habilita hot-reload (los cambios en código se reflejan automáticamente)

**Verás en la consola:**
```
quicktask-api  | INFO:     Uvicorn running on http://0.0.0.0:8000
quicktask-api  | INFO:     Application startup complete.
```

### Paso 4: Verificar que la API está funcionando

Abrir en el navegador:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

---

## 🧪 Pruebas rápidas

### 1. Crear usuario de prueba

```powershell
curl.exe -X POST "http://localhost:8000/api/auth/register" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"docker@quicktask.com\", \"password\": \"docker1234\"}'
```

**Respuesta esperada (201 Created):**
```json
{
  "id": 1,
  "email": "docker@quicktask.com",
  "created_at": "2025-10-29T..."
}
```

### 2. Iniciar sesión

```powershell
curl.exe -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"docker@quicktask.com\", \"password\": \"docker1234\"}'
```

**Respuesta esperada (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**💡 Guarda el token para los siguientes comandos!**

### 3. Crear una tarea

```powershell
$token = "TU_TOKEN_AQUI"
curl.exe -X POST "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{\"title\": \"Aprender Docker\", \"description\": \"Desplegar QuickTask con Docker\"}'
```

**Respuesta esperada (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Aprender Docker",
  "description": "Desplegar QuickTask con Docker",
  "status": "pending",
  "due_date": null,
  "created_at": "2025-10-29T...",
  "updated_at": "2025-10-29T..."
}
```

### 4. Listar tareas

```powershell
curl.exe -X GET "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer $token"
```

---

## 🛠️ Comandos útiles

### Ver logs en tiempo real

```powershell
docker-compose logs -f
```

### Detener el contenedor (mantiene datos)

```powershell
docker-compose down
```

### Reiniciar el contenedor

```powershell
docker-compose restart
```

### Ejecutar comandos dentro del contenedor

```powershell
# Abrir bash en el contenedor
docker-compose exec quicktask-backend bash

# Crear datos de prueba
docker-compose exec quicktask-backend python init_dev_data.py

# Ejecutar tests
docker-compose exec quicktask-backend pytest
```

### Ver estado del contenedor

```powershell
docker ps
```

### Ver uso de recursos

```powershell
docker stats quicktask-api
```

---

## 📊 Verificación de persistencia

### Verificar que los datos persisten después de reiniciar

```powershell
# 1. Crear una tarea (como arriba)
# 2. Detener el contenedor
docker-compose down

# 3. Reiniciar el contenedor
docker-compose up

# 4. Verificar que la tarea sigue ahí
curl.exe -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer $token"
```

✅ **La tarea debe seguir existiendo!**

### Ver dónde está almacenada la base de datos

```powershell
# Listar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect backend_quicktask-data
```

---

## 🔍 Troubleshooting

### Error: "Puerto 8000 ya está en uso"

**Solución 1:** Detener el proceso que usa el puerto
```powershell
netstat -ano | findstr :8000
# Luego: taskkill /PID <numero_proceso> /F
```

**Solución 2:** Cambiar el puerto en `docker-compose.yaml`
```yaml
ports:
  - "3000:8000"  # Usa puerto 3000 en el host
```

### Error: "No se puede conectar al daemon de Docker"

**Solución:** Asegurarte de que Docker Desktop está corriendo
- Abrir Docker Desktop desde el menú de Windows
- Esperar a que aparezca el ícono verde

### Error: "ModuleNotFoundError" o dependencias faltantes

**Solución:** Reconstruir la imagen
```powershell
docker-compose down
docker-compose up --build
```

### Ver logs de error detallados

```powershell
docker-compose logs quicktask-backend --tail=100
```

---

## 📂 Estructura de volúmenes

```
Docker Volume: backend_quicktask-data
  └── quicktask.db          # Base de datos SQLite persistente
  └── quicktask.db-journal  # Journal de transacciones
```

Los datos persisten incluso después de:
- ✅ `docker-compose down`
- ✅ `docker-compose restart`
- ✅ Reiniciar Docker Desktop
- ✅ Reiniciar Windows

**⚠️ Solo se eliminan con:** `docker-compose down -v` (incluye flag `-v`)

---

## 🎯 Checklist de verificación

Marca cada paso completado:

- [ ] Docker Desktop instalado y corriendo
- [ ] Navegado al directorio `backend/`
- [ ] `docker-compose up --build` ejecutado sin errores
- [ ] Servidor corriendo en http://localhost:8000
- [ ] API Docs accesible en http://localhost:8000/docs
- [ ] Registro de usuario exitoso
- [ ] Login exitoso (token recibido)
- [ ] Creación de tarea exitosa
- [ ] Listado de tareas funcional
- [ ] Datos persisten después de `docker-compose down` y `up`

---

## 📚 Documentación adicional

Para más detalles, consulta:
- **`DOCKER_DEPLOY.md`** - Guía completa de Docker (incluye producción)
- **`README.md`** - Documentación general del backend
- **`QUICKSTART.md`** - Guía de inicio rápido sin Docker
- **`test_api.md`** - Ejemplos de pruebas con curl

---

## 🎉 ¡Siguiente paso!

Tu backend ahora está corriendo en Docker. Para desarrollar el frontend:

1. **Frontend Web (React):**
   ```powershell
   cd ../frontend-web
   npm install
   npm start
   ```

2. **Frontend Móvil (React Native):**
   ```powershell
   cd ../frontend-mobile
   npm install
   npx react-native run-android
   ```

**Configurar la URL de la API:**
- Para desarrollo local: `http://localhost:8000`
- Para desarrollo desde móvil: `http://TU_IP_LOCAL:8000` (ej: `http://192.168.1.10:8000`)

---

**🐳 ¡Despliegue completado exitosamente!**
