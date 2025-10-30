# 🔄 Actualización del Backend - QuickTask

## Cambios realizados según el diseño de BD original

Se ha actualizado completamente el backend para que coincida **exactamente** con el diseño de base de datos proporcionado en `Diseño_base_de_datos.md`.

---

## 📊 Principales cambios

### 1. ✅ Sistema de IDs actualizado

**Antes:** UUIDs (String)  
**Ahora:** INTEGER AUTOINCREMENT (como SQLite estándar)

```python
# Antes
id = Column(String, primary_key=True, default=generate_uuid)

# Ahora
id = Column(Integer, primary_key=True, autoincrement=True)
```

**Impacto:**
- ✅ Más eficiente en SQLite
- ✅ Compatible con el diseño original
- ✅ Índices más pequeños y rápidos
- ✅ Migración más fácil a otros DBMS

---

### 2. ✅ Eliminado campo `priority` de Task

**Razón:** El diseño de BD original **no incluye** el campo `priority` en la tabla `tasks`.

**Cambios:**
- ❌ Eliminado de `models.Task`
- ❌ Eliminado de `schemas.TaskCreate` y `TaskUpdate`
- ❌ Eliminado ordenamiento por prioridad en `get_tasks()`
- ✅ Solo se mantienen los campos del diseño: `title`, `description`, `status`, `due_date`

---

### 3. ✅ Añadida tabla `Notification`

**Nuevo modelo completo:**

```python
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)  # email | push
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con User
    user = relationship("User", back_populates="notifications")
```

**Funcionalidades añadidas:**
- ✅ CRUD completo de notificaciones
- ✅ Endpoints `/api/notifications` (GET, POST)
- ✅ Relación User → Notification (1:N)
- ✅ Constraint: `type IN ('email', 'push')`

---

### 4. ✅ Constraints de integridad añadidos

Según el diseño de BD, se añadieron:

```python
# En Task
__table_args__ = (
    CheckConstraint("status IN ('pending', 'completed')", name='check_status'),
)

# En Notification
__table_args__ = (
    CheckConstraint("type IN ('email', 'push')", name='check_notification_type'),
)
```

---

### 5. ✅ Relación Task → Reminder actualizada

**Constraint añadido:**
```python
task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), 
                 unique=True, nullable=False)
```

**Razón:** Según diseño, la relación es 1:1 (una tarea puede tener **un solo** recordatorio).

---

## 📁 Archivos modificados

### Código principal
1. ✅ `app/models.py` - Modelos actualizados (Integer IDs, Notification, constraints)
2. ✅ `app/schemas.py` - Schemas actualizados (sin priority, NotificationCreate/Response)
3. ✅ `app/crud.py` - CRUD actualizado (sin priority, funciones de notifications)
4. ✅ `app/main.py` - Endpoints actualizados (sin order_by=priority, endpoints de notifications)
5. ✅ `init_dev_data.py` - Datos de prueba actualizados (sin priority, con notifications)

---

## 🆕 Nuevos endpoints

### Notificaciones

```http
POST /api/notifications
GET  /api/notifications?limit=50
```

**Ejemplo de uso:**

```powershell
# Crear notificación
curl -X POST "http://localhost:8000/api/notifications" `
  -H "Authorization: Bearer $TOKEN" `
  -H "Content-Type: application/json" `
  -d '{
    "user_id": 1,
    "message": "Recordatorio: Tarea próxima a vencer",
    "type": "push"
  }'

# Listar notificaciones
curl -X GET "http://localhost:8000/api/notifications" `
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "message": "¡Bienvenido a QuickTask!",
    "type": "email",
    "sent_at": "2025-10-29T10:00:00"
  }
]
```

---

## 🗄️ Esquema de BD actualizado

```sql
-- Tabla users (sin cambios estructurales, solo IDs)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla tasks (sin priority)
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('pending', 'completed')) DEFAULT 'pending',
    due_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla reminders (task_id UNIQUE para 1:1)
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL UNIQUE,
    remind_at DATETIME NOT NULL,
    is_sent BOOLEAN DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Tabla notifications (NUEVA)
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    type TEXT CHECK(type IN ('email', 'push')),
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 🔗 Relaciones actualizadas

```
User (1) ──────────────< (N) Task
  │                           │
  │                           │ (1)
  │                           ▼
  │                       (0..1) Reminder
  │
  └──────────────────< (N) Notification
```

**Relaciones:**
- User → Task (1:N)
- Task → Reminder (1:0..1) con UNIQUE constraint
- User → Notification (1:N) **[NUEVO]**

---

## 📝 Esquemas Pydantic actualizados

### TaskCreate (sin priority)
```python
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    # priority eliminado ❌
```

### NotificationCreate (nuevo)
```python
class NotificationCreate(BaseModel):
    user_id: int
    message: str
    type: str  # "email" | "push"
```

### NotificationResponse (nuevo)
```python
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    type: str
    sent_at: datetime
```

---

## 🎯 Funcionalidades afectadas

### ❌ Eliminadas
- Ordenamiento por prioridad: `GET /api/tasks?order_by=priority`
- Campo `priority` en crear/actualizar tareas

### ✅ Mantenidas
- Ordenamiento por fecha: `order_by=created_at` o `order_by=due_date`
- Filtrado por estado: `status=pending` o `status=completed`
- Búsqueda por keywords: `search=keyword`

### ✅ Añadidas
- CRUD completo de notificaciones
- Endpoints `/api/notifications`
- Relación User → Notification
- Notificaciones de prueba en `init_dev_data.py`

---

## 🚀 Migración de datos existentes

Si ya tenías una base de datos con el esquema anterior:

```powershell
# 1. Eliminar BD antigua
Remove-Item quicktask.db

# 2. Recrear con nuevo esquema
python init_dev_data.py

# 3. Reiniciar servidor
uvicorn app.main:app --reload
```

---

## ✅ Verificación

Para verificar que los cambios están correctos:

```powershell
# 1. Inicializar BD
python init_dev_data.py

# Debe mostrar:
# ✅ Usuario creado
# ✅ 8 tareas creadas (sin priority)
# ✅ Recordatorio creado
# ✅ 3 notificaciones creadas ← NUEVO

# 2. Iniciar servidor
uvicorn app.main:app --reload

# 3. Login
curl -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{"email": "dev@quicktask.com", "password": "dev1234"}'

# 4. Listar tareas (sin priority)
curl -X GET "http://localhost:8000/api/tasks" `
  -H "Authorization: Bearer $TOKEN"

# 5. Listar notificaciones (NUEVO)
curl -X GET "http://localhost:8000/api/notifications" `
  -H "Authorization: Bearer $TOKEN"
```

---

## 📚 Documentación actualizada

La documentación Swagger se actualiza automáticamente:

**http://localhost:8000/docs**

Endpoints visibles:
- ✅ `/api/auth/*` - Autenticación
- ✅ `/api/tasks` - Tareas (sin priority)
- ✅ `/api/reminders` - Recordatorios
- ✅ `/api/notifications` - Notificaciones **[NUEVO]**

---

## 🔄 Comparación de esquemas

| Campo/Entidad      | Versión anterior | Versión actual    |
|--------------------|------------------|-------------------|
| **IDs**            | UUID (String)    | INTEGER           |
| **Task.priority**  | ✅ Existía       | ❌ Eliminado      |
| **Notification**   | ❌ No existía    | ✅ Añadido        |
| **Reminder.task_id** | No único       | ✅ UNIQUE (1:1)   |
| **Constraints**    | Parciales        | ✅ Completos      |

---

## 💡 Notas importantes

### IDs en las respuestas
Los IDs ahora son **enteros** en lugar de strings UUID:

```json
// Antes
{
  "id": "abc-123-def-456",
  "title": "Mi tarea"
}

// Ahora
{
  "id": 1,
  "title": "Mi tarea"
}
```

### Eliminación de priority
Si necesitas prioridades en el futuro, deberás:
1. Actualizar el diseño de BD
2. Agregar columna `priority` a tabla `tasks`
3. Actualizar modelos y schemas
4. Crear migración de datos

---

## ✨ Resumen de mejoras

✅ **100% compatible** con el diseño de BD original  
✅ **Notificaciones** completas (email/push)  
✅ **IDs eficientes** (INTEGER AUTOINCREMENT)  
✅ **Constraints** de integridad completos  
✅ **Relaciones** correctamente definidas  
✅ **Cascadas** de eliminación configuradas  
✅ **Índices** optimizados para queries frecuentes  

---

**Backend actualizado y listo para usar** 🎉  
**Versión:** 1.1 (actualizado según diseño de BD original)  
**Fecha:** Octubre 29, 2025
