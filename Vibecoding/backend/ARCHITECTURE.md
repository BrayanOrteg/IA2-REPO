# 📐 Arquitectura del Backend QuickTask

Este documento describe la arquitectura implementada del backend de QuickTask.

---

## 🏗️ Diagrama de capas

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE (Frontend)                       │
│                    Web / Mobile / curl / Postman                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS (JSON)
                             │ Authorization: Bearer <JWT>
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE API (FastAPI)                     │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │   Auth Routes  │  │  Task Routes   │  │ Reminder Routes  │  │
│  │  /api/auth/*   │  │  /api/tasks/*  │  │ /api/reminders/* │  │
│  └────────┬───────┘  └────────┬───────┘  └─────────┬────────┘  │
│           │                   │                     │           │
│           └───────────────────┼─────────────────────┘           │
│                               │                                 │
│                     ┌─────────▼──────────┐                      │
│                     │  Middleware CORS   │                      │
│                     │  (allow origins)   │                      │
│                     └─────────┬──────────┘                      │
│                               │                                 │
│                     ┌─────────▼──────────┐                      │
│                     │  Dependency        │                      │
│                     │  Injection         │                      │
│                     │  - get_db()        │                      │
│                     │  - get_current_    │                      │
│                     │    user()          │                      │
│                     └─────────┬──────────┘                      │
└───────────────────────────────┼─────────────────────────────────┘
                                │
                                │ Inyección de dependencias
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE LÓGICA DE NEGOCIO                   │
│                                                                  │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │   auth.py       │  │   crud.py    │  │   schemas.py      │  │
│  │                 │  │              │  │                   │  │
│  │ • hash_password │  │ • create_    │  │ • TaskCreate      │  │
│  │ • verify_       │  │   task()     │  │ • TaskResponse    │  │
│  │   password      │  │ • get_tasks()│  │ • UserCreate      │  │
│  │ • create_token  │  │ • update_    │  │ • Validación      │  │
│  │ • authenticate  │  │   task()     │  │   Pydantic        │  │
│  │ • get_current_  │  │ • delete_    │  │                   │  │
│  │   user()        │  │   task()     │  │                   │  │
│  │                 │  │ • create_    │  │                   │  │
│  │ JWT + bcrypt    │  │   reminder() │  │                   │  │
│  └─────────────────┘  └──────┬───────┘  └───────────────────┘  │
│                               │                                 │
└───────────────────────────────┼─────────────────────────────────┘
                                │
                                │ SQLAlchemy ORM
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE PERSISTENCIA                        │
│                                                                  │
│                         ┌─────────────┐                          │
│                         │  models.py  │                          │
│                         │             │                          │
│                         │  User       │                          │
│                         │  Task       │                          │
│                         │  Reminder   │                          │
│                         │             │                          │
│                         │  ORM Models │                          │
│                         └──────┬──────┘                          │
│                                │                                 │
│                      ┌─────────▼───────────┐                     │
│                      │   database.py       │                     │
│                      │                     │                     │
│                      │  • Engine           │                     │
│                      │  • SessionLocal     │                     │
│                      │  • Base             │                     │
│                      │  • get_db()         │                     │
│                      └─────────┬───────────┘                     │
└────────────────────────────────┼─────────────────────────────────┘
                                 │
                                 │ SQLAlchemy Engine
                                 ▼
                    ┌────────────────────────┐
                    │   SQLite Database      │
                    │   (quicktask.db)       │
                    │                        │
                    │  • users               │
                    │  • tasks               │
                    │  • reminders           │
                    └────────────────────────┘
```

---

## 🔄 Flujo de una petición (Ejemplo: Crear tarea)

```
1. Cliente (Frontend)
   │
   │  POST /api/tasks
   │  Authorization: Bearer eyJhbGc...
   │  Body: {"title": "Nueva tarea", "priority": "high"}
   │
   ▼
2. FastAPI Router (main.py)
   │  @app.post("/api/tasks")
   │  def create_task(...)
   │
   ▼
3. Dependency: get_current_user() (auth.py)
   │  • Extrae token JWT del header
   │  • Valida y decodifica token
   │  • Busca usuario en BD
   │  • Retorna User object
   │
   ▼
4. Dependency: get_db() (database.py)
   │  • Crea sesión SQLAlchemy
   │  • Yield sesión
   │  • Auto-close al finalizar
   │
   ▼
5. Validación Pydantic (schemas.py)
   │  • Valida TaskCreate schema
   │  • title no vacío
   │  • priority en [low, medium, high]
   │
   ▼
6. CRUD Operation (crud.py)
   │  • crud.create_task(db, task, user_id)
   │  • Crea objeto Task ORM
   │  • db.add(task)
   │  • db.commit()
   │  • db.refresh(task)
   │
   ▼
7. ORM → SQL (models.py + SQLAlchemy)
   │  • Task model → INSERT SQL
   │  INSERT INTO tasks (id, title, priority, user_id, ...)
   │  VALUES (uuid, 'Nueva tarea', 'high', user_id, ...)
   │
   ▼
8. SQLite Database
   │  • Persiste registro
   │  • Retorna fila insertada
   │
   ▼
9. Respuesta (schemas.py)
   │  • Convierte Task ORM → TaskResponse Pydantic
   │  • Serializa a JSON
   │
   ▼
10. Cliente
    {
      "id": "abc-123...",
      "title": "Nueva tarea",
      "priority": "high",
      "status": "pending",
      ...
    }
```

---

## 📦 Módulos y responsabilidades

### `main.py` (Capa de presentación)
**Responsabilidad:** Definir endpoints y orquestar el flujo de requests.

- Define rutas HTTP (GET, POST, PUT, DELETE)
- Configura CORS
- Maneja errores HTTP (404, 401, 400)
- Inyecta dependencias (DB session, current user)
- Retorna respuestas HTTP

---

### `database.py` (Configuración de BD)
**Responsabilidad:** Gestión de conexiones a base de datos.

- Configura SQLAlchemy engine (SQLite)
- Define SessionLocal factory
- Provee dependency `get_db()` para inyección

---

### `models.py` (Modelos ORM)
**Responsabilidad:** Representar entidades como clases Python.

- `User`: usuario registrado
- `Task`: tarea del usuario
- `Reminder`: recordatorio de tarea
- Define relaciones (User → Tasks, Task → Reminder)
- Mapea a tablas SQL

---

### `schemas.py` (Validación y serialización)
**Responsabilidad:** Contratos de entrada/salida de la API.

- Validación de datos con Pydantic
- Conversión JSON ↔ Python objects
- Separación de schemas (Create, Update, Response)
- Type safety

---

### `crud.py` (Lógica de negocio)
**Responsabilidad:** Operaciones sobre la base de datos.

- Create, Read, Update, Delete (CRUD)
- Implementa TaskService del diagrama de clases
- Filtrado, ordenamiento, búsqueda
- Lógica de negocio (ej: estadísticas)

---

### `auth.py` (Autenticación y seguridad)
**Responsabilidad:** Gestión de identidad y autorización.

- Hash de contraseñas (bcrypt)
- Creación y validación de JWT tokens
- Autenticación de usuarios
- Dependency `get_current_user()` para proteger endpoints
- Implementa AuthService del diagrama de clases

---

## 🔐 Seguridad implementada

### 1. Contraseñas hasheadas (RNF5)
```python
# auth.py
pwd_context = CryptContext(schemes=["bcrypt"])
password_hash = pwd_context.hash("password123")
```

### 2. JWT Bearer tokens
```python
# Header de requests autenticados
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Validación de ownership
```python
# crud.py - Asegura que usuario solo vea sus tareas
def get_task_by_id(db, task_id, user_id):
    return db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id  # ← Validación
    ).first()
```

### 4. Validación de datos (Pydantic)
```python
# schemas.py
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
```

---

## 🗃️ Esquema de base de datos

```sql
-- Tabla users
CREATE TABLE users (
    id TEXT PRIMARY KEY,           -- UUID
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME
);

-- Tabla tasks
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,           -- UUID
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending', -- pending | completed
    due_date DATETIME,
    priority TEXT DEFAULT 'medium', -- low | medium | high
    created_at DATETIME,
    updated_at DATETIME,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabla reminders
CREATE TABLE reminders (
    id TEXT PRIMARY KEY,           -- UUID
    task_id TEXT NOT NULL,
    remind_at DATETIME NOT NULL,
    is_sent BOOLEAN DEFAULT 0,
    created_at DATETIME,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

---

## 🔗 Relaciones entre entidades

```
User (1) ──────────────< (N) Task
                              │
                              │ (1)
                              │
                              ▼
                           (0..1) Reminder
```

- **User → Task:** Un usuario tiene muchas tareas (1:N)
- **Task → Reminder:** Una tarea puede tener un recordatorio opcional (1:0..1)
- **Cascade delete:** Al eliminar User, se eliminan sus Tasks. Al eliminar Task, se elimina su Reminder.

---

## 📊 Endpoints agrupados por funcionalidad

### Autenticación (RF1, RF2, RF3)
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Login (obtener JWT)
- `GET /api/auth/me` - Info usuario autenticado

### Gestión de tareas (RF4-RF9, RF13, RF14)
- `POST /api/tasks` - Crear tarea
- `GET /api/tasks` - Listar con filtros/búsqueda/orden
- `GET /api/tasks/{id}` - Detalle de tarea
- `PUT /api/tasks/{id}` - Actualizar tarea
- `DELETE /api/tasks/{id}` - Eliminar tarea
- `POST /api/tasks/{id}/complete` - Marcar completada
- `POST /api/tasks/{id}/pending` - Revertir a pendiente

### Recordatorios (RF11)
- `POST /api/reminders` - Crear recordatorio
- `GET /api/reminders` - Listar recordatorios

### Utilidades
- `GET /` - Info de la API
- `GET /api/health` - Health check

---

## 🎯 Patrones de diseño utilizados

### 1. **Dependency Injection** (FastAPI Depends)
```python
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),  # ← Inyección
    db: Session = Depends(get_db)                    # ← Inyección
):
    ...
```

### 2. **Repository Pattern** (crud.py)
Centraliza lógica de acceso a datos:
```python
# En lugar de escribir queries en cada endpoint:
crud.create_task(db, task, user_id)
crud.get_tasks(db, user_id, filters)
```

### 3. **Service Layer** (auth.py, crud.py)
Separa lógica de negocio de presentación.

### 4. **DTO Pattern** (schemas.py)
Data Transfer Objects con Pydantic para transferir datos entre capas.

### 5. **Factory Pattern** (database.py)
```python
SessionLocal = sessionmaker(bind=engine)  # Factory de sesiones
```

---

## 🚀 Ventajas de esta arquitectura

✅ **Separación de responsabilidades** (Single Responsibility Principle)
✅ **Fácil de testear** (cada capa se puede probar independientemente)
✅ **Escalable** (agregar nuevas features sin modificar core)
✅ **Type-safe** (Pydantic + Python type hints)
✅ **Documentación automática** (FastAPI genera OpenAPI/Swagger)
✅ **DRY** (Don't Repeat Yourself - reutilización de código)

---

## 🔮 Evolución futura

### Fase 1 - MVP (Actual) ✅
- Monolito FastAPI
- SQLite local
- JWT autenticación
- CRUD básico

### Fase 2 - Producción
- Migrar a PostgreSQL
- Redis para cache y sessions
- Workers (Celery) para recordatorios
- Deploy en cloud (AWS/GCP)

### Fase 3 - Escala
- Separar en microservicios
- WebSockets para tiempo real
- Message queue (RabbitMQ)
- Kubernetes orchestration

---

## 📚 Referencias

- **FastAPI:** https://fastapi.tiangolo.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Pydantic:** https://docs.pydantic.dev/
- **JWT:** https://jwt.io/

---

**Documentación del backend QuickTask - Versión 1.0**
