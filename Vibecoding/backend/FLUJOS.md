# 🔄 Diagramas de Flujo - Backend QuickTask

Diagramas de secuencia y flujo de los procesos principales implementados.

---

## 📋 1. Flujo de Registro de Usuario (RF1)

```
┌────────┐          ┌──────────┐         ┌──────────┐        ┌──────────┐
│ Client │          │ FastAPI  │         │   auth   │        │ Database │
└───┬────┘          └────┬─────┘         └────┬─────┘        └────┬─────┘
    │                    │                    │                   │
    │ POST /auth/register│                    │                   │
    │  email, password   │                    │                   │
    ├───────────────────>│                    │                   │
    │                    │                    │                   │
    │                    │ Validate schema    │                   │
    │                    │ (Pydantic)         │                   │
    │                    │────────────┐       │                   │
    │                    │            │       │                   │
    │                    │<───────────┘       │                   │
    │                    │                    │                   │
    │                    │ Check if email     │                   │
    │                    │ exists             │                   │
    │                    ├────────────────────┼──────────────────>│
    │                    │                    │     Query User    │
    │                    │<───────────────────┼───────────────────┤
    │                    │  User exists?      │                   │
    │                    │                    │                   │
    │  ❌ 400 Error      │                    │                   │
    │<───────────────────┤ if email exists    │                   │
    │  "Email already    │                    │                   │
    │   registered"      │                    │                   │
    │                    │                    │                   │
    │                    │ hash_password()    │                   │
    │                    ├───────────────────>│                   │
    │                    │                    │                   │
    │                    │<───────────────────┤                   │
    │                    │  password_hash     │                   │
    │                    │                    │                   │
    │                    │ create_user()      │                   │
    │                    ├────────────────────┼──────────────────>│
    │                    │                    │   INSERT User     │
    │                    │<───────────────────┼───────────────────┤
    │                    │  new_user          │                   │
    │                    │                    │                   │
    │  ✅ 201 Created    │                    │                   │
    │  {id, email,       │                    │                   │
    │   created_at}      │                    │                   │
    │<───────────────────┤                    │                   │
    │                    │                    │                   │
```

---

## 🔐 2. Flujo de Autenticación (Login) (RF2)

```
┌────────┐          ┌──────────┐         ┌──────────┐        ┌──────────┐
│ Client │          │ FastAPI  │         │   auth   │        │ Database │
└───┬────┘          └────┬─────┘         └────┬─────┘        └────┬─────┘
    │                    │                    │                   │
    │ POST /auth/login   │                    │                   │
    │  email, password   │                    │                   │
    ├───────────────────>│                    │                   │
    │                    │                    │                   │
    │                    │ authenticate_user()│                   │
    │                    ├───────────────────>│                   │
    │                    │                    │                   │
    │                    │                    │ Get user by email │
    │                    │                    ├──────────────────>│
    │                    │                    │                   │
    │                    │                    │<──────────────────┤
    │                    │                    │  User object      │
    │                    │                    │                   │
    │                    │                    │ verify_password() │
    │                    │                    │  (bcrypt)         │
    │                    │                    │────────┐          │
    │                    │                    │        │          │
    │                    │                    │<───────┘          │
    │                    │                    │  match?           │
    │                    │                    │                   │
    │  ❌ 401 Unauthorized│                   │                   │
    │<───────────────────┼────────────────────┤                   │
    │  if password wrong │                    │  No match         │
    │                    │                    │                   │
    │                    │<───────────────────┤                   │
    │                    │  User object       │  Match ✅         │
    │                    │                    │                   │
    │                    │ create_access_token│                   │
    │                    ├───────────────────>│                   │
    │                    │  {"sub": user_id}  │                   │
    │                    │                    │                   │
    │                    │<───────────────────┤                   │
    │                    │  JWT token         │                   │
    │                    │                    │                   │
    │  ✅ 200 OK         │                    │                   │
    │  {access_token,    │                    │                   │
    │   token_type}      │                    │                   │
    │<───────────────────┤                    │                   │
    │                    │                    │                   │
```

---

## 📝 3. Flujo de Crear Tarea (RF4)

```
┌────────┐          ┌──────────┐    ┌──────────┐   ┌──────┐    ┌──────────┐
│ Client │          │ FastAPI  │    │   auth   │   │ crud │    │ Database │
└───┬────┘          └────┬─────┘    └────┬─────┘   └───┬──┘    └────┬─────┘
    │                    │               │             │             │
    │ POST /api/tasks    │               │             │             │
    │ Bearer: <token>    │               │             │             │
    │ {title, priority}  │               │             │             │
    ├───────────────────>│               │             │             │
    │                    │               │             │             │
    │                    │ get_current_user()          │             │
    │                    │ (Dependency)  │             │             │
    │                    ├──────────────>│             │             │
    │                    │               │             │             │
    │                    │               │ Decode JWT  │             │
    │                    │               │────────┐    │             │
    │                    │               │        │    │             │
    │                    │               │<───────┘    │             │
    │                    │               │             │             │
    │                    │               │ Get user    │             │
    │                    │               ├─────────────┼────────────>│
    │                    │               │             │   Query     │
    │                    │               │<────────────┼─────────────┤
    │                    │               │  User       │             │
    │                    │               │             │             │
    │  ❌ 401 Error      │               │             │             │
    │<───────────────────┼───────────────┤             │             │
    │  if token invalid  │               │  None       │             │
    │                    │               │             │             │
    │                    │<──────────────┤             │             │
    │                    │  current_user │             │             │
    │                    │               │             │             │
    │                    │ Validate TaskCreate         │             │
    │                    │ (Pydantic)    │             │             │
    │                    │────────────┐  │             │             │
    │                    │            │  │             │             │
    │                    │<───────────┘  │             │             │
    │                    │               │             │             │
    │                    │ create_task() │             │             │
    │                    ├───────────────┼────────────>│             │
    │                    │               │             │             │
    │                    │               │             │ INSERT Task │
    │                    │               │             ├────────────>│
    │                    │               │             │             │
    │                    │               │             │<────────────┤
    │                    │               │             │  new_task   │
    │                    │               │             │             │
    │                    │<──────────────┼─────────────┤             │
    │                    │  Task object  │             │             │
    │                    │               │             │             │
    │  ✅ 201 Created    │               │             │             │
    │  {id, title,       │               │             │             │
    │   status, ...}     │               │             │             │
    │<───────────────────┤               │             │             │
    │                    │               │             │             │
```

---

## 📊 4. Flujo de Listar Tareas con Filtros (RF8, RF9, RF13)

```
┌────────┐          ┌──────────┐         ┌──────┐         ┌──────────┐
│ Client │          │ FastAPI  │         │ crud │         │ Database │
└───┬────┘          └────┬─────┘         └───┬──┘         └────┬─────┘
    │                    │                   │                  │
    │ GET /api/tasks?    │                   │                  │
    │  status=pending&   │                   │                  │
    │  order_by=priority │                   │                  │
    │ Bearer: <token>    │                   │                  │
    ├───────────────────>│                   │                  │
    │                    │                   │                  │
    │                    │ [Authenticate]    │                  │
    │                    │ get_current_user()│                  │
    │                    │───────────┐       │                  │
    │                    │           │       │                  │
    │                    │<──────────┘       │                  │
    │                    │  current_user     │                  │
    │                    │                   │                  │
    │                    │ Validate params   │                  │
    │                    │ (status, order_by)│                  │
    │                    │───────────┐       │                  │
    │                    │           │       │                  │
    │                    │<──────────┘       │                  │
    │                    │                   │                  │
    │                    │ get_tasks()       │                  │
    │                    ├──────────────────>│                  │
    │                    │  user_id,         │                  │
    │                    │  status="pending",│                  │
    │                    │  order_by="priority"                 │
    │                    │                   │                  │
    │                    │                   │ SELECT * FROM    │
    │                    │                   │  tasks           │
    │                    │                   │ WHERE user_id=?  │
    │                    │                   │  AND status='pending'
    │                    │                   │ ORDER BY priority│
    │                    │                   ├─────────────────>│
    │                    │                   │                  │
    │                    │                   │<─────────────────┤
    │                    │                   │  [Task1, Task2]  │
    │                    │                   │                  │
    │                    │                   │ get_task_statistics()
    │                    │                   ├─────────────────>│
    │                    │                   │  COUNT queries   │
    │                    │                   │<─────────────────┤
    │                    │                   │  {total, pending,│
    │                    │                   │   completed}     │
    │                    │                   │                  │
    │                    │<──────────────────┤                  │
    │                    │  tasks + stats    │                  │
    │                    │                   │                  │
    │  ✅ 200 OK         │                   │                  │
    │  {tasks: [...],    │                   │                  │
    │   total: 10,       │                   │                  │
    │   pending: 6,      │                   │                  │
    │   completed: 4}    │                   │                  │
    │<───────────────────┤                   │                  │
    │                    │                   │                  │
```

---

## ✅ 5. Flujo de Marcar Tarea como Completada (RF6)

```
┌────────┐          ┌──────────┐         ┌──────┐         ┌──────────┐
│ Client │          │ FastAPI  │         │ crud │         │ Database │
└───┬────┘          └────┬─────┘         └───┬──┘         └────┬─────┘
    │                    │                   │                  │
    │ POST /api/tasks/   │                   │                  │
    │   {id}/complete    │                   │                  │
    │ Bearer: <token>    │                   │                  │
    ├───────────────────>│                   │                  │
    │                    │                   │                  │
    │                    │ [Authenticate]    │                  │
    │                    │ get_current_user()│                  │
    │                    │                   │                  │
    │                    │ mark_task_completed()                │
    │                    ├──────────────────>│                  │
    │                    │  task_id, user_id │                  │
    │                    │                   │                  │
    │                    │                   │ SELECT task      │
    │                    │                   │ WHERE id=? AND   │
    │                    │                   │  user_id=?       │
    │                    │                   ├─────────────────>│
    │                    │                   │                  │
    │  ❌ 404 Not Found  │                   │                  │
    │<───────────────────┼───────────────────┤                  │
    │  if not found      │                   │  None            │
    │                    │                   │                  │
    │                    │                   │<─────────────────┤
    │                    │                   │  Task object     │
    │                    │                   │                  │
    │                    │                   │ UPDATE tasks     │
    │                    │                   │ SET status=      │
    │                    │                   │  'completed',    │
    │                    │                   │  updated_at=NOW  │
    │                    │                   │ WHERE id=?       │
    │                    │                   ├─────────────────>│
    │                    │                   │                  │
    │                    │                   │<─────────────────┤
    │                    │                   │  Success         │
    │                    │                   │                  │
    │                    │<──────────────────┤                  │
    │                    │  updated_task     │                  │
    │                    │                   │                  │
    │  ✅ 200 OK         │                   │                  │
    │  {id, status:      │                   │                  │
    │   "completed", ...}│                   │                  │
    │<───────────────────┤                   │                  │
    │                    │                   │                  │
```

---

## ⏰ 6. Flujo de Crear Recordatorio (RF11)

```
┌────────┐          ┌──────────┐         ┌──────┐         ┌──────────┐
│ Client │          │ FastAPI  │         │ crud │         │ Database │
└───┬────┘          └────┬─────┘         └───┬──┘         └────┬─────┘
    │                    │                   │                  │
    │ POST /api/reminders│                   │                  │
    │ {task_id,          │                   │                  │
    │  remind_at}        │                   │                  │
    │ Bearer: <token>    │                   │                  │
    ├───────────────────>│                   │                  │
    │                    │                   │                  │
    │                    │ [Authenticate]    │                  │
    │                    │                   │                  │
    │                    │ Validate schema   │                  │
    │                    │ (ReminderCreate)  │                  │
    │                    │                   │                  │
    │                    │ create_reminder() │                  │
    │                    ├──────────────────>│                  │
    │                    │  reminder, user_id│                  │
    │                    │                   │                  │
    │                    │                   │ Verify task      │
    │                    │                   │ exists & belongs │
    │                    │                   │ to user          │
    │                    │                   ├─────────────────>│
    │                    │                   │  SELECT task     │
    │                    │                   │<─────────────────┤
    │                    │                   │  Task or None    │
    │                    │                   │                  │
    │  ❌ 404 Error      │                   │                  │
    │<───────────────────┼───────────────────┤                  │
    │  if task not found │                   │  None            │
    │  or not owned      │                   │                  │
    │                    │                   │                  │
    │                    │                   │ INSERT Reminder  │
    │                    │                   ├─────────────────>│
    │                    │                   │                  │
    │                    │                   │<─────────────────┤
    │                    │                   │  new_reminder    │
    │                    │                   │                  │
    │                    │<──────────────────┤                  │
    │                    │  Reminder object  │                  │
    │                    │                   │                  │
    │  ✅ 201 Created    │                   │                  │
    │  {id, task_id,     │                   │                  │
    │   remind_at,       │                   │                  │
    │   is_sent: false}  │                   │                  │
    │<───────────────────┤                   │                  │
    │                    │                   │                  │
```

---

## 🔍 7. Flujo de Búsqueda por Palabras Clave (RF13)

```
Cliente envía: GET /api/tasks?search=FastAPI

1. Autenticación (get_current_user)
   ↓
2. get_tasks(db, user_id, search="FastAPI")
   ↓
3. Query SQL:
   SELECT * FROM tasks
   WHERE user_id = ?
     AND (title LIKE '%FastAPI%' 
          OR description LIKE '%FastAPI%')
   ORDER BY created_at DESC
   ↓
4. Retornar tareas que contienen "FastAPI"
```

---

## 📈 8. Flujo de Estadísticas (RF14)

```
Cliente envía: GET /api/tasks

1. Autenticación
   ↓
2. get_tasks() → retorna lista de tareas
   ↓
3. get_task_statistics(db, user_id)
   ↓
   SELECT COUNT(*) FROM tasks WHERE user_id = ?
   → total
   
   SELECT COUNT(*) FROM tasks 
   WHERE user_id = ? AND status = 'completed'
   → completed
   
   pending = total - completed
   ↓
4. Retornar JSON:
   {
     "tasks": [...],
     "total": 10,
     "completed": 3,
     "pending": 7
   }
```

---

## 🔄 9. Ciclo de vida de una petición autenticada

```
1. Client Request
   ↓
   Headers: Authorization: Bearer <JWT>
   
2. FastAPI Router
   ↓
   Dependency: get_current_user()
   
3. HTTPBearer extracts token
   ↓
   Token validation (decode JWT)
   
4. Query database for user
   ↓
   User exists?
   
   ❌ No → 401 Unauthorized
   ✅ Yes → Continue
   
5. Execute endpoint logic
   ↓
   CRUD operations
   
6. Return response
   ↓
   JSON serialization (Pydantic)
   
7. Client receives response
```

---

## 🛡️ 10. Validación de Ownership (Seguridad)

```
Ejemplo: Actualizar tarea

1. Cliente envía:
   PUT /api/tasks/task-123
   Bearer: token_de_usuario_A

2. get_current_user()
   → User A (id: user-A)

3. update_task(db, task_id="task-123", user_id="user-A")
   ↓
4. get_task_by_id(db, "task-123", "user-A")
   ↓
   Query:
   SELECT * FROM tasks
   WHERE id = 'task-123'
     AND user_id = 'user-A'  ← Validación de ownership
   
   Si la tarea pertenece a otro usuario:
   → None → 404 Not Found
   
   Si la tarea pertenece al usuario:
   → Task object → Permitir actualización
```

**Esto previene que usuarios accedan a tareas de otros usuarios.**

---

## 🔐 11. Generación y validación de JWT

```
=== LOGIN (Generación de JWT) ===

1. Usuario envía email + password
   ↓
2. Verificar credenciales
   ↓
3. create_access_token({"sub": user_id})
   ↓
4. JWT Structure:
   
   Header:
   {
     "alg": "HS256",
     "typ": "JWT"
   }
   
   Payload:
   {
     "sub": "user-abc-123",  ← user_id
     "exp": 1730000000       ← expiration timestamp
   }
   
   Signature:
   HMACSHA256(
     base64UrlEncode(header) + "." +
     base64UrlEncode(payload),
     SECRET_KEY
   )
   ↓
5. Return token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWI..."

=== REQUEST AUTENTICADO (Validación) ===

1. Cliente envía:
   Authorization: Bearer eyJhbGc...
   ↓
2. decode_access_token(token)
   ↓
   • Verificar firma (HMAC con SECRET_KEY)
   • Verificar expiración (exp claim)
   • Extraer user_id (sub claim)
   ↓
   Valid? → user_id
   Invalid? → None → 401 Unauthorized
```

---

**Diagramas de flujo del backend QuickTask v1.0**  
**Todos los flujos implementados y funcionando ✅**
