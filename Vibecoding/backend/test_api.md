# 🧪 Guía de Prueba de la API QuickTask

Esta guía proporciona comandos **curl** listos para probar todos los endpoints de la API.

---

## ⚙️ Prerequisitos

1. Tener el servidor corriendo:
   ```powershell
   cd backend
   uvicorn app.main:app --reload
   ```

2. El servidor debe estar en: `http://localhost:8000`

---

## 🔐 1. AUTENTICACIÓN

### 1.1 Registrar usuario

```powershell
curl.exe -X POST "http://localhost:8000/api/auth/register" -H "Content-Type: application/json" -d '{\"email\": \"test@quicktask.com\", \"password\": \"test1234\"}'
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "email": "test@quicktask.com",
  "created_at": "2025-10-29T..."
}
```

### 1.2 Iniciar sesión

```powershell
curl.exe -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/json" -d '{\"email\": \"test@quicktask.com\", \"password\": \"test1234\"}'
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJI...",
  "token_type": "bearer"
}
```

**⚠️ IMPORTANTE: Guardar el token automáticamente en una variable:**

```powershell
# Extraer el token automáticamente
$response = curl.exe -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/json" -d '{\"email\": \"test@quicktask.com\", \"password\": \"test1234\"}' | ConvertFrom-Json
$TOKEN = $response.access_token
Write-Host "Token guardado: $TOKEN"
```

### 1.3 Obtener información del usuario autenticado

```powershell
curl.exe -X GET "http://localhost:8000/api/auth/me" -H "Authorization: Bearer $TOKEN"
```

---

## 📝 2. TAREAS (CRUD)

### 2.1 Crear tarea #1

```powershell
curl.exe -X POST "http://localhost:8000/api/tasks" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{\"title\": \"Completar proyecto IA2\", \"description\": \"Implementar backend de QuickTask con FastAPI\"}'
```

### 2.2 Crear tarea #2 (Con fecha límite)

```powershell
curl.exe -X POST "http://localhost:8000/api/tasks" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{\"title\": \"Estudiar para examen\", \"description\": \"Repasar capítulos 5-8\", \"due_date\": \"2025-11-05T09:00:00\"}'
```

### 2.3 Crear tarea #3

```powershell
curl.exe -X POST "http://localhost:8000/api/tasks" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{\"title\": \"Leer documentación React\"}'
```

**💡 Guardar el `id` de alguna tarea para los siguientes pasos:**

```powershell
$TASK_ID = 1  # Usar el ID de alguna tarea de las respuestas anteriores
```

### 2.4 Listar TODAS las tareas

```powershell
curl.exe -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer $TOKEN"
```

### 2.5 Filtrar solo tareas PENDIENTES

```powershell
curl.exe -X GET "http://localhost:8000/api/tasks?status=pending" -H "Authorization: Bearer $TOKEN"
```

### 2.6 Ordenar por PRIORIDAD (high → medium → low)

```powershell
curl -X GET "http://localhost:8000/api/tasks?order_by=priority" -H "Authorization: Bearer $TOKEN"
```

### 2.7 Ordenar por FECHA LÍMITE

```powershell
curl -X GET "http://localhost:8000/api/tasks?order_by=due_date" -H "Authorization: Bearer $TOKEN"
```

### 2.8 Buscar tareas que contengan "examen"

```powershell
curl -X GET "http://localhost:8000/api/tasks?search=examen" -H "Authorization: Bearer $TOKEN"
```

### 2.9 Combinar filtros (pendientes + ordenadas por prioridad)

```powershell
curl -X GET "http://localhost:8000/api/tasks?status=pending&order_by=priority" -H "Authorization: Bearer $TOKEN"
```

### 2.10 Obtener detalle de UNA tarea específica

```powershell
curl -X GET "http://localhost:8000/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN"
```

### 2.11 Actualizar tarea (cambiar descripción y prioridad)

```powershell
curl -X PUT "http://localhost:8000/api/tasks/$TASK_ID" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "{\"description\": \"Descripción actualizada desde API\", \"priority\": \"high\"}"
```

### 2.12 Marcar tarea como COMPLETADA

```powershell
curl -X POST "http://localhost:8000/api/tasks/$TASK_ID/complete" -H "Authorization: Bearer $TOKEN"
```

### 2.13 Revertir tarea a PENDIENTE

```powershell
curl -X POST "http://localhost:8000/api/tasks/$TASK_ID/pending" -H "Authorization: Bearer $TOKEN"
```

### 2.14 Listar solo tareas COMPLETADAS

```powershell
curl -X GET "http://localhost:8000/api/tasks?status=completed" -H "Authorization: Bearer $TOKEN"
```

### 2.15 Eliminar tarea permanentemente

```powershell
curl -X DELETE "http://localhost:8000/api/tasks/$TASK_ID" -H "Authorization: Bearer $TOKEN"
```

---

## ⏰ 3. RECORDATORIOS

### 3.1 Crear recordatorio para una tarea

```powershell
curl -X POST "http://localhost:8000/api/reminders" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "{\"task_id\": \"$TASK_ID\", \"remind_at\": \"2025-11-01T08:00:00\"}"
```

### 3.2 Listar todos los recordatorios

```powershell
curl -X GET "http://localhost:8000/api/reminders" -H "Authorization: Bearer $TOKEN"
```

---

## 🏥 4. ENDPOINTS DE UTILIDAD

### 4.1 Health check

```powershell
curl -X GET "http://localhost:8000/api/health"
```

### 4.2 Información de la API

```powershell
curl -X GET "http://localhost:8000/"
```

---

## 📊 5. VERIFICAR ESTADÍSTICAS (RF14)

Después de crear varias tareas y marcar algunas como completadas:

```powershell
curl -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer $TOKEN"
```

La respuesta incluirá estadísticas:
```json
{
  "tasks": [...],
  "total": 5,
  "pending": 3,
  "completed": 2
}
```

---

## 🎯 Flujo completo de prueba

```powershell
# 1. Registrarse
curl -X POST "http://localhost:8000/api/auth/register" -H "Content-Type: application/json" -d "{\"email\": \"demo@test.com\", \"password\": \"demo1234\"}"

# 2. Login y guardar token
$response = curl -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/json" -d "{\"email\": \"demo@test.com\", \"password\": \"demo1234\"}" | ConvertFrom-Json
$TOKEN = $response.access_token

# 3. Crear tarea
$taskResponse = curl -X POST "http://localhost:8000/api/tasks" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "{\"title\": \"Mi primera tarea\", \"priority\": \"high\"}" | ConvertFrom-Json
$TASK_ID = $taskResponse.id

# 4. Ver todas las tareas
curl -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer $TOKEN"

# 5. Marcar como completada
curl -X POST "http://localhost:8000/api/tasks/$TASK_ID/complete" -H "Authorization: Bearer $TOKEN"

# 6. Ver tareas completadas
curl -X GET "http://localhost:8000/api/tasks?status=completed" -H "Authorization: Bearer $TOKEN"
```

---

## ❌ Casos de error esperados

### Error 401: Token inválido o expirado

```powershell
curl -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer token_invalido"
```

**Respuesta:**
```json
{
  "detail": "No se pudo validar las credenciales"
}
```

### Error 404: Tarea no encontrada

```powershell
curl -X GET "http://localhost:8000/api/tasks/id-inexistente" -H "Authorization: Bearer $TOKEN"
```

**Respuesta:**
```json
{
  "detail": "Tarea no encontrada"
}
```

### Error 400: Email ya registrado

```powershell
# Intentar registrar el mismo email dos veces
curl -X POST "http://localhost:8000/api/auth/register" -H "Content-Type: application/json" -d "{\"email\": \"test@quicktask.com\", \"password\": \"test1234\"}"
```

**Respuesta:**
```json
{
  "detail": "El email ya está registrado"
}
```

---

## 📌 Tips de PowerShell

### Formatear JSON en la respuesta

```powershell
curl -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Guardar respuesta en variable

```powershell
$tasks = curl -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer $TOKEN" | ConvertFrom-Json
echo $tasks.total
```

---

## 🌐 Documentación interactiva

En lugar de usar curl, puedes probar la API visualmente en:

**Swagger UI:** http://localhost:8000/docs

Ahí podrás:
- Ver todos los endpoints documentados
- Probar requests directamente desde el navegador
- Ver esquemas de datos automáticamente

---

## ✅ Checklist de funcionalidades

Marcar después de probar:

- [ ] Registrar usuario (RF1)
- [ ] Iniciar sesión (RF2)
- [ ] Crear tarea (RF4)
- [ ] Editar tarea (RF5)
- [ ] Marcar como completada (RF6)
- [ ] Eliminar tarea (RF7)
- [ ] Filtrar por estado (RF8)
- [ ] Ordenar tareas (RF9)
- [ ] Buscar por palabras clave (RF13)
- [ ] Ver estadísticas (RF14)
- [ ] Crear recordatorio (RF11)
