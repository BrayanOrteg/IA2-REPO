# 🚀 QuickTask Docker - Instrucciones Paso a Paso

## 📋 Pasos para ejecutar QuickTask con Docker

### ✅ Paso 1: Verificar Docker Desktop

```powershell
docker --version
```

**✔️ Resultado esperado:**
```
Docker version 24.0.x, build xxxxx
```

**❌ Si falla:**
- Instalar Docker Desktop desde: https://www.docker.com/products/docker-desktop
- Reiniciar Windows después de la instalación
- Abrir Docker Desktop y esperar a que el ícono esté verde

---

### ✅ Paso 2: Navegar al directorio backend

```powershell
cd c:\Users\Brayan\Documents\Trabajos_U\SEMESTRE_9\IA2\Vibecoding\backend
```

**✔️ Verificar que estás en el directorio correcto:**
```powershell
ls
```

Deberías ver:
- `Dockerfile`
- `docker-compose.yaml`
- `requirements.txt`
- carpeta `app/`

---

### ✅ Paso 3: Levantar el contenedor

```powershell
docker-compose up --build
```

**⏳ Esto tomará 1-2 minutos la primera vez.**

**✔️ Verás mensajes como:**
```
[+] Building 45.2s (10/10) FINISHED
[+] Running 2/2
 ✔ Volume "backend_quicktask-data"    Created
 ✔ Container quicktask-api            Started
quicktask-api  | INFO:     Uvicorn running on http://0.0.0.0:8000
quicktask-api  | INFO:     Application startup complete.
```

**✅ ¡Listo!** La API está corriendo.

---

### ✅ Paso 4: Verificar que funciona

#### Opción A: Navegador web
Abrir en el navegador: http://localhost:8000/docs

Deberías ver la documentación interactiva de Swagger.

#### Opción B: Comando curl
```powershell
curl.exe http://localhost:8000/api/health
```

**✔️ Respuesta esperada:**
```json
{"status":"ok"}
```

---

### ✅ Paso 5: Probar la API

#### 5.1 Registrar un usuario

```powershell
curl.exe -X POST "http://localhost:8000/api/auth/register" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"mi@email.com\", \"password\": \"password123\"}'
```

**✔️ Respuesta esperada (201 Created):**
```json
{
  "id": 1,
  "email": "mi@email.com",
  "created_at": "2025-10-29T..."
}
```

#### 5.2 Iniciar sesión

```powershell
curl.exe -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"mi@email.com\", \"password\": \"password123\"}'
```

**✔️ Respuesta esperada (200 OK):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**💾 GUARDA EL TOKEN** (lo necesitarás para los siguientes pasos)

#### 5.3 Crear una tarea

```powershell
# Reemplaza TU_TOKEN_AQUI con el token del paso anterior
curl.exe -X POST "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer TU_TOKEN_AQUI" `
  -H "Content-Type: application/json" `
  -d '{\"title\": \"Mi primera tarea\", \"description\": \"Aprender Docker\"}'
```

**✔️ Respuesta esperada (201 Created):**
```json
{
  "id": 1,
  "title": "Mi primera tarea",
  "description": "Aprender Docker",
  "status": "pending",
  "user_id": 1,
  ...
}
```

#### 5.4 Listar tareas

```powershell
curl.exe -X GET "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**✔️ Deberías ver tu tarea creada en el paso anterior**

---

### ✅ Paso 6: Verificar persistencia de datos

#### 6.1 Detener el contenedor

```powershell
# Presiona Ctrl+C en la terminal donde está corriendo docker-compose
# O en una nueva terminal:
docker-compose down
```

**✔️ Verás:**
```
[+] Running 1/1
 ✔ Container quicktask-api  Removed
```

#### 6.2 Reiniciar el contenedor

```powershell
docker-compose up
```

#### 6.3 Verificar que los datos siguen ahí

```powershell
# Iniciar sesión otra vez (mismo usuario)
curl.exe -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"mi@email.com\", \"password\": \"password123\"}'

# Listar tareas (deberías ver las tareas anteriores)
curl.exe -X GET "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer NUEVO_TOKEN"
```

**✅ ¡Los datos persisten!** Gracias al volumen Docker.

---

## 🎯 Comandos útiles del día a día

### Iniciar el servidor

```powershell
# En primer plano (ver logs)
docker-compose up

# En segundo plano
docker-compose up -d
```

### Ver logs

```powershell
# Ver logs en tiempo real
docker-compose logs -f

# Ver últimas 50 líneas
docker-compose logs --tail=50
```

### Detener el servidor

```powershell
# Detener (mantiene datos)
docker-compose down

# Detener y eliminar TODOS los datos (⚠️ cuidado)
docker-compose down -v
```

### Reiniciar después de cambios

```powershell
# Si cambiaste código Python (hot-reload automático, no hace falta reiniciar)
# Solo guarda el archivo y espera 1-2 segundos

# Si cambiaste requirements.txt
docker-compose up --build

# Si cambiaste Dockerfile o docker-compose.yaml
docker-compose down
docker-compose up --build
```

### Ejecutar comandos dentro del contenedor

```powershell
# Abrir bash
docker-compose exec quicktask-backend bash

# Ejecutar pytest
docker-compose exec quicktask-backend pytest

# Crear datos de prueba
docker-compose exec quicktask-backend python init_dev_data.py
```

---

## 🔍 Verificación de estado

### ¿El contenedor está corriendo?

```powershell
docker ps
```

**✔️ Deberías ver:**
```
CONTAINER ID   IMAGE              STATUS         PORTS                    NAMES
abc123...      backend-quicktask  Up 5 minutes   0.0.0.0:8000->8000/tcp   quicktask-api
```

### ¿Cuánto recursos usa?

```powershell
docker stats quicktask-api
```

**✔️ Verás CPU, memoria, red y disco en tiempo real**

### ¿Dónde están mis datos?

```powershell
docker volume ls
```

**✔️ Deberías ver:**
```
DRIVER    VOLUME NAME
local     backend_quicktask-data
```

---

## ⚠️ Problemas comunes

### Problema 1: "Puerto 8000 ya está en uso"

**Causa:** Otro proceso está usando el puerto 8000

**Solución A - Detener el otro proceso:**
```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :8000

# Detener el proceso (reemplaza <PID> con el número que aparece)
taskkill /PID <PID> /F
```

**Solución B - Cambiar el puerto:**
Editar `docker-compose.yaml`:
```yaml
ports:
  - "3000:8000"  # Cambia 3000 por el puerto que quieras
```

Ahora la API estará en: http://localhost:3000

---

### Problema 2: "Cannot connect to the Docker daemon"

**Causa:** Docker Desktop no está corriendo

**Solución:**
1. Abrir Docker Desktop desde el menú de Windows
2. Esperar a que el ícono de la bandeja esté verde
3. Intentar de nuevo

---

### Problema 3: "Error building image"

**Causa:** Error en Dockerfile o dependencias

**Solución:**
```powershell
# Ver logs detallados
docker-compose build --no-cache

# Si hay error en requirements.txt, revisa las versiones
```

---

### Problema 4: Los cambios no se reflejan

**Causa:** Hot-reload no está funcionando

**Solución:**
```powershell
# Verificar que el volumen está montado
docker-compose exec quicktask-backend ls -la /app/app

# Reiniciar contenedor
docker-compose restart
```

---

### Problema 5: "ModuleNotFoundError"

**Causa:** Dependencias no instaladas correctamente

**Solución:**
```powershell
# Reconstruir imagen desde cero
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## 📊 Diagrama del flujo

```
┌─────────────────────────────────────────────────────────┐
│                    TU COMPUTADORA                        │
│                                                          │
│  1. Terminal                                             │
│     docker-compose up                                    │
│           │                                              │
│           ▼                                              │
│  2. Docker construye imagen                              │
│     - Descarga Python 3.11                               │
│     - Instala requirements.txt                           │
│     - Copia código de app/                               │
│           │                                              │
│           ▼                                              │
│  3. Docker crea contenedor                               │
│     - Nombre: quicktask-api                              │
│     - Puerto: 8000                                       │
│     - Volumen: quicktask-data                            │
│           │                                              │
│           ▼                                              │
│  4. FastAPI inicia servidor                              │
│     uvicorn app.main:app                                 │
│           │                                              │
│           ▼                                              │
│  5. API lista en http://localhost:8000                   │
│                                                          │
│  6. Navegador / curl                                     │
│     http://localhost:8000/docs ◄─── ¡Funciona!           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Checklist completo

Marca cada paso completado:

- [ ] Docker Desktop instalado
- [ ] Docker Desktop corriendo (ícono verde)
- [ ] Navegado a directorio `backend/`
- [ ] `docker-compose up --build` ejecutado sin errores
- [ ] Servidor corriendo (mensaje "Application startup complete")
- [ ] http://localhost:8000/docs accesible en navegador
- [ ] Health check funciona: `curl http://localhost:8000/api/health`
- [ ] Registro de usuario exitoso
- [ ] Login exitoso (token recibido)
- [ ] Creación de tarea exitosa
- [ ] Listado de tareas funciona
- [ ] Datos persisten después de `docker-compose down` y `up`

---

## 🎉 ¡Felicidades!

Si completaste todos los pasos del checklist, tu backend QuickTask está:

✅ Corriendo en Docker
✅ Accesible en http://localhost:8000
✅ Con datos persistentes
✅ Listo para desarrollo
✅ Listo para conectar frontend

**Siguiente paso:** Desarrollar el frontend web o móvil

---

## 📚 Más información

- **Guía completa:** `DOCKER_DEPLOY.md`
- **Resumen ejecutivo:** `DOCKER_SUMMARY.md`
- **Documentación API:** `README.md`
- **Pruebas:** `TESTING.md`

---

**¿Necesitas ayuda?** Revisa la sección de troubleshooting arriba o consulta los logs:
```powershell
docker-compose logs -f
```
