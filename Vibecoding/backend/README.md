# QuickTask Backend API

Backend REST API para la aplicación de gestión de tareas QuickTask, desarrollado con **FastAPI**, **SQLAlchemy** y **SQLite**.

---

## 📋 Características implementadas

### Autenticación (RF1-RF3)
- ✅ **RF1:** Registro de usuarios con email y contraseña
- ✅ **RF2:** Inicio de sesión con JWT tokens
- ✅ **RF3:** Estructura para recuperación de contraseña (pendiente implementar envío email)

### Gestión de Tareas (RF4-RF9, RF13-RF14)
- ✅ **RF4:** Crear tareas con título, descripción, fecha límite y prioridad
- ✅ **RF5:** Editar tareas existentes
- ✅ **RF6:** Marcar tareas como completadas o pendientes
- ✅ **RF7:** Eliminar tareas permanentemente
- ✅ **RF8:** Filtrar tareas por estado (pending/completed)
- ✅ **RF9:** Ordenar tareas por fecha de creación o fecha límite
- ✅ **RF13:** Buscar tareas por palabras clave
- ✅ **RF14:** Vista de progreso con estadísticas (total, completadas, pendientes)

### Recordatorios y Notificaciones (RF11)
- ✅ **RF11:** Configurar recordatorios para tareas
- ✅ Sistema de notificaciones (email/push)
- ⚠️ Envío real de notificaciones pendiente (requiere integración con FCM/Email)

### Seguridad (RNF5)
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Autenticación con JWT Bearer tokens
- ✅ Validación de datos con Pydantic

---

## 🛠️ Stack tecnológico

| Componente        | Tecnología                  |
|-------------------|-----------------------------|
| Framework         | FastAPI 0.104.1             |
| ORM               | SQLAlchemy 2.0.23           |
| Base de datos     | SQLite (archivo local)      |
| Validación        | Pydantic 2.5.0              |
| Autenticación     | JWT (python-jose)           |
| Hashing passwords | bcrypt (passlib)            |
| Servidor ASGI     | Uvicorn                     |

---

## 📁 Estructura del proyecto

```
backend/
│
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # Aplicación FastAPI y endpoints
│   ├── database.py          # Configuración de SQLAlchemy
│   ├── models.py            # Modelos ORM (User, Task, Reminder)
│   ├── schemas.py           # Schemas Pydantic para validación
│   ├── crud.py              # Operaciones CRUD
│   └── auth.py              # Lógica de autenticación y JWT
│
├── requirements.txt         # Dependencias Python
├── .env.example             # Ejemplo de variables de entorno
└── README.md                # Este archivo
```

---

## 🚀 Instalación y ejecución

### Opción A: Con Docker (Recomendado) 🐳

**Requisitos:** Docker Desktop instalado

```powershell
# 1. Navegar al directorio backend
cd backend

# 2. Levantar el contenedor
docker-compose up --build
```

El servidor estará corriendo en: **http://localhost:8000**

**Ver guía completa de Docker:** `DOCKER_DEPLOY.md`

### Opción B: Instalación local

#### 1. Crear entorno virtual

```powershell
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

#### 3. Ejecutar el servidor

```powershell
# Desde la carpeta backend/
uvicorn app.main:app --reload
```

El servidor estará corriendo en: **http://localhost:8000**

- **Documentación interactiva (Swagger):** http://localhost:8000/docs
- **Documentación alternativa (ReDoc):** http://localhost:8000/redoc

### 4. Ejecutar pruebas (opcional)

```powershell
# Instalar dependencias de testing
pip install -r requirements-dev.txt

# Ejecutar todas las pruebas
pytest

# Con reporte de cobertura
pytest --cov=app --cov-report=html
```

**Ver guía completa:** `TESTING.md`

---

## 📡 Endpoints de la API

### Autenticación

| Método | Endpoint              | Descripción                    | Auth |
|--------|-----------------------|--------------------------------|------|
| POST   | `/api/auth/register`  | Registrar nuevo usuario        | No   |
| POST   | `/api/auth/login`     | Iniciar sesión (obtener token) | No   |
| GET    | `/api/auth/me`        | Obtener usuario autenticado    | Sí   |

### Tareas

| Método | Endpoint                       | Descripción                      | Auth |
|--------|--------------------------------|----------------------------------|------|
| POST   | `/api/tasks`                   | Crear tarea                      | Sí   |
| GET    | `/api/tasks`                   | Listar tareas (con filtros)      | Sí   |
| GET    | `/api/tasks/{task_id}`         | Obtener detalle de tarea         | Sí   |
| PUT    | `/api/tasks/{task_id}`         | Actualizar tarea                 | Sí   |
| DELETE | `/api/tasks/{task_id}`         | Eliminar tarea                   | Sí   |
| POST   | `/api/tasks/{task_id}/complete`| Marcar como completada           | Sí   |
| POST   | `/api/tasks/{task_id}/pending` | Revertir a pendiente             | Sí   |

### Recordatorios

| Método | Endpoint          | Descripción                        | Auth |
|--------|-------------------|------------------------------------|------|
| POST   | `/api/reminders`  | Crear recordatorio para una tarea  | Sí   |
| GET    | `/api/reminders`  | Listar recordatorios del usuario   | Sí   |

### Notificaciones

| Método | Endpoint            | Descripción                           | Auth |
|--------|---------------------|---------------------------------------|------|
| POST   | `/api/notifications`| Crear notificación (email o push)     | Sí   |
| GET    | `/api/notifications`| Listar notificaciones del usuario     | Sí   |

### Utilidades

| Método | Endpoint      | Descripción        | Auth |
|--------|---------------|--------------------|------|
| GET    | `/`           | Info de la API     | No   |
| GET    | `/api/health` | Health check       | No   |

---

## 🧪 Ejemplos de uso con `curl`

### 1. Registrar usuario

```powershell
curl -X POST "http://localhost:8000/api/auth/register" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"usuario@example.com\", \"password\": \"password123\"}'
```

**Respuesta:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "usuario@example.com",
  "created_at": "2025-10-29T10:00:00"
}
```

### 2. Iniciar sesión

```powershell
curl -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"email\": \"usuario@example.com\", \"password\": \"password123\"}'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**⚠️ Guardar el `access_token` para usarlo en las siguientes peticiones.**

### 3. Crear tarea

```powershell
curl -X POST "http://localhost:8000/api/tasks" `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer TU_TOKEN_AQUI" `
  -d '{\"title\": \"Estudiar FastAPI\", \"description\": \"Completar tutorial oficial\"}'
```

**Respuesta:**
```json
{
  "id": 1,
  "title": "Estudiar FastAPI",
  "description": "Completar tutorial oficial",
  "status": "pending",
  "due_date": null,
  "created_at": "2025-10-29T10:05:00",
  "updated_at": "2025-10-29T10:05:00",
  "user_id": 1
}
```

### 4. Listar tareas (con filtros)

```powershell
# Todas las tareas
curl -X GET "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# Solo pendientes
curl -X GET "http://localhost:8000/api/tasks?status=pending" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# Ordenadas por fecha límite
curl -X GET "http://localhost:8000/api/tasks?order_by=due_date" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# Búsqueda por palabra clave
curl -X GET "http://localhost:8000/api/tasks?search=FastAPI" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Estudiar FastAPI",
      "description": "Completar tutorial oficial",
      "status": "pending",
      "due_date": null,
      "created_at": "2025-10-29T10:05:00",
      "updated_at": "2025-10-29T10:05:00",
      "user_id": 1
    }
  ],
  "total": 1,
  "pending": 1,
  "completed": 0
}
```

### 5. Obtener detalle de tarea

```powershell
curl -X GET "http://localhost:8000/api/tasks/1" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### 6. Actualizar tarea

```powershell
curl -X PUT "http://localhost:8000/api/tasks/1" `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer TU_TOKEN_AQUI" `
  -d '{\"description\": \"Completar tutorial oficial y hacer ejercicios prácticos\"}'
```

### 7. Marcar como completada

```powershell
curl -X POST "http://localhost:8000/api/tasks/1/complete" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### 8. Eliminar tarea

```powershell
curl -X DELETE "http://localhost:8000/api/tasks/1" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### 9. Crear recordatorio

```powershell
curl -X POST "http://localhost:8000/api/reminders" `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer TU_TOKEN_AQUI" `
  -d '{\"task_id\": 1, \"remind_at\": \"2025-10-30T09:00:00\"}'
```

### 10. Crear notificación

```powershell
curl -X POST "http://localhost:8000/api/notifications" `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer TU_TOKEN_AQUI" `
  -d '{\"user_id\": 1, \"message\": \"Recordatorio de tarea\", \"type\": \"push\"}'
```

### 11. Listar notificaciones

```powershell
curl -X GET "http://localhost:8000/api/notifications" `
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## 🔐 Autenticación

Todos los endpoints de tareas y recordatorios requieren autenticación mediante **JWT Bearer token**.

### Flujo de autenticación:

1. **Registrarse:** `POST /api/auth/register`
2. **Iniciar sesión:** `POST /api/auth/login` → obtienes `access_token`
3. **Usar el token:** incluir header `Authorization: Bearer {access_token}` en cada request

**Ejemplo de header:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📊 Modelo de datos

### User
- `id` (INTEGER, autoincrement)
- `email` (String, único)
- `password_hash` (String)
- `created_at` (DateTime)

### Task
- `id` (INTEGER, autoincrement)
- `title` (String)
- `description` (String, opcional)
- `status` (String: pending|completed)
- `due_date` (DateTime, opcional)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- `user_id` (FK → User)

### Reminder
- `id` (INTEGER, autoincrement)
- `task_id` (FK → Task, UNIQUE para 1:1)
- `remind_at` (DateTime)
- `is_sent` (Boolean)

### Notification
- `id` (INTEGER, autoincrement)
- `user_id` (FK → User)
- `message` (String)
- `type` (String: email|push)
- `sent_at` (DateTime)

---

## 🎯 Próximos pasos (Roadmap)

- [ ] Implementar envío de notificaciones email (RF11)
- [ ] Implementar recuperación de contraseña completa (RF3)
- [ ] WebSockets para sincronización en tiempo real (RF10)
- [ ] Paginación en listado de tareas
- [ ] Tests unitarios y de integración
- [ ] Migración a PostgreSQL para producción
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

Asegúrate de ejecutar uvicorn desde la carpeta `backend/`:

```powershell
cd backend
uvicorn app.main:app --reload
```

### Error: "Could not validate credentials"

Tu token JWT expiró (duración: 30 minutos). Inicia sesión nuevamente:

```powershell
curl -X POST "http://localhost:8000/api/auth/login" ...
```

---

## 📝 Notas adicionales

- **Base de datos:** SQLite crea automáticamente el archivo `quicktask.db` en la raíz del proyecto
- **SECRET_KEY:** En producción, cambiar `SECRET_KEY` en `auth.py` por una variable de entorno segura
- **CORS:** Actualmente permite todos los orígenes (`*`). En producción, especificar dominios permitidos

---

## 👨‍💻 Autor

Desarrollado para el proyecto QuickTask - IA2, SEMESTRE_9.

**Tecnologías:** Python, FastAPI, SQLAlchemy, JWT, Pydantic
