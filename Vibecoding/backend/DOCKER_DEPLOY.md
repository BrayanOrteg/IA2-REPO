# 🐳 Guía de Despliegue con Docker - QuickTask

Esta guía explica cómo desplegar QuickTask localmente usando Docker y Docker Compose.

---

## 📋 Requisitos previos

- **Docker Desktop** instalado (versión 20.10 o superior)
- **Docker Compose** (incluido con Docker Desktop)
- **Git** (para clonar el repositorio)

### Verificar instalación:

```powershell
docker --version
docker-compose --version
```

---

## 🚀 Despliegue rápido (Quick Start)

### 1. Navegar al directorio backend

```powershell
cd backend
```

### 2. Construir y levantar el contenedor

```powershell
docker-compose up --build
```

Este comando:
- ✅ Construye la imagen Docker con todas las dependencias
- ✅ Crea un volumen persistente para la base de datos SQLite
- ✅ Inicia el servidor FastAPI en http://localhost:8000
- ✅ Habilita hot-reload para desarrollo

### 3. Verificar que la API está funcionando

Abrir en el navegador:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

---

## 📦 Comandos útiles de Docker

### Iniciar el contenedor (en segundo plano)

```powershell
docker-compose up -d
```

### Ver logs en tiempo real

```powershell
docker-compose logs -f
```

### Detener el contenedor

```powershell
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ elimina la base de datos)

```powershell
docker-compose down -v
```

### Reconstruir la imagen (después de cambiar dependencias)

```powershell
docker-compose up --build
```

### Ejecutar comandos dentro del contenedor

```powershell
# Abrir bash en el contenedor
docker-compose exec quicktask-backend bash

# Inicializar datos de prueba
docker-compose exec quicktask-backend python init_dev_data.py

# Ejecutar tests
docker-compose exec quicktask-backend pytest
```

---

## 🗂️ Estructura de archivos Docker

```
backend/
├── Dockerfile              # Definición de la imagen Docker
├── docker-compose.yaml     # Orquestación de servicios
├── .env.docker            # Variables de entorno (ejemplo)
├── requirements.txt       # Dependencias Python
└── app/                   # Código de la aplicación
    ├── main.py
    ├── database.py
    └── ...
```

---

## ⚙️ Configuración avanzada

### Variables de entorno

Puedes personalizar la configuración creando un archivo `.env` en el directorio `backend`:

```env
DATABASE_URL=sqlite:///./data/quicktask.db
SECRET_KEY=tu-clave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Luego modifica `docker-compose.yaml` para usar el archivo:

```yaml
services:
  quicktask-backend:
    env_file:
      - .env
```

### Cambiar puerto

Si el puerto 8000 está ocupado, edita `docker-compose.yaml`:

```yaml
ports:
  - "3000:8000"  # Mapea puerto 3000 del host al 8000 del contenedor
```

---

## 🧪 Pruebas de la API con Docker

### 1. Crear un usuario de prueba

```powershell
curl -X POST "http://localhost:8000/api/auth/register" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"test@quicktask.com\", \"password\": \"test1234\"}'
```

### 2. Iniciar sesión

```powershell
curl -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"test@quicktask.com\", \"password\": \"test1234\"}'
```

Respuesta:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 3. Crear una tarea (usar el token obtenido)

```powershell
curl -X POST "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer TU_TOKEN_AQUI" `
  -H "Content-Type: application/json" `
  -d '{\"title\": \"Mi primera tarea en Docker\", \"description\": \"Funciona!\"}'
```

---

## 🔍 Troubleshooting

### El contenedor no inicia

**Verificar logs:**
```powershell
docker-compose logs quicktask-backend
```

**Problemas comunes:**
- Puerto 8000 ocupado → Cambiar puerto en `docker-compose.yaml`
- Error en dependencias → Reconstruir imagen: `docker-compose up --build`

### La base de datos no persiste

**Verificar volúmenes:**
```powershell
docker volume ls
```

**Ver dónde está montado:**
```powershell
docker volume inspect backend_quicktask-data
```

### Hot-reload no funciona

Asegúrate de que el código está montado como volumen en `docker-compose.yaml`:

```yaml
volumes:
  - ./app:/app/app
```

### Acceder a la base de datos SQLite

```powershell
# Copiar DB al host
docker cp quicktask-api:/app/data/quicktask.db ./quicktask.db

# O acceder directamente en el contenedor
docker-compose exec quicktask-backend sqlite3 /app/data/quicktask.db
```

---

## 🌐 Despliegue en producción

Para producción, modifica el `Dockerfile` y `docker-compose.yaml`:

### Dockerfile de producción

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

# Usar gunicorn para producción
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Agregar gunicorn a requirements.txt

```txt
gunicorn==21.2.0
```

### Usar PostgreSQL en producción

Modifica `docker-compose.yaml`:

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

## 📊 Monitoreo

### Ver uso de recursos

```powershell
docker stats quicktask-api
```

### Health check manual

```powershell
curl http://localhost:8000/api/health
```

### Logs con filtro

```powershell
# Solo errores
docker-compose logs quicktask-backend | Select-String "ERROR"

# Últimas 50 líneas
docker-compose logs --tail=50 quicktask-backend
```

---

## ✅ Checklist de despliegue

- [ ] Docker Desktop instalado y corriendo
- [ ] Repositorio clonado
- [ ] `docker-compose up --build` ejecutado sin errores
- [ ] API docs accesible en http://localhost:8000/docs
- [ ] Health check respondiendo OK
- [ ] Registro y login funcionando
- [ ] Creación de tareas exitosa
- [ ] Base de datos persiste después de `docker-compose down`

---

## 📚 Recursos adicionales

- **Documentación oficial Docker:** https://docs.docker.com/
- **FastAPI con Docker:** https://fastapi.tiangolo.com/deployment/docker/
- **Docker Compose:** https://docs.docker.com/compose/

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs -f`
2. Verifica la documentación de la API: http://localhost:8000/docs
3. Consulta los archivos de documentación:
   - `README.md`
   - `QUICKSTART.md`
   - `ARCHITECTURE.md`

---

**¡Listo para desarrollar! 🚀**
