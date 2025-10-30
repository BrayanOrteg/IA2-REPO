# 🚀 Inicio Rápido - QuickTask Backend

Guía rápida para levantar el backend en **menos de 5 minutos**.

---

## ⚡ Pasos rápidos

### 1️⃣ Crear entorno virtual e instalar dependencias

```powershell
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

---

### 2️⃣ Inicializar base de datos con datos de prueba

```powershell
# Ejecutar script de inicialización (crea BD + usuario + tareas de ejemplo)
python init_dev_data.py
```

**Salida esperada:**
```
====================================================================
🔧 INICIALIZADOR DE DATOS DE DESARROLLO - QuickTask
====================================================================

👤 Creando usuario de desarrollo...
✅ Usuario creado: dev@quicktask.com

📝 Creando tareas de ejemplo...
✅ 8 tareas creadas

⏰ Creando recordatorio de ejemplo...
✅ Recordatorio creado para: 'Implementar filtros y búsqueda'

====================================================================
🎉 DATOS DE DESARROLLO INICIALIZADOS
====================================================================

👤 Usuario de prueba:
   Email: dev@quicktask.com
   Password: dev1234

📊 Estadísticas:
   Total de tareas: 8
   Completadas: 3
   Pendientes: 5
```

---

### 3️⃣ Iniciar servidor

```powershell
uvicorn app.main:app --reload
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### 4️⃣ Abrir documentación interactiva

Abrir en el navegador:

**📘 Swagger UI:** http://localhost:8000/docs

Desde ahí puedes:
- Ver todos los endpoints
- Probar la API sin escribir curl
- Autenticarte con el botón **Authorize**

---

## 🧪 Probar la API rápidamente

### Opción A: Usar Swagger UI (más fácil)

1. Ir a http://localhost:8000/docs
2. Expandir `/api/auth/login`
3. Click en **Try it out**
4. Usar credenciales:
   ```json
   {
     "email": "dev@quicktask.com",
     "password": "dev1234"
   }
   ```
5. Click **Execute**
6. Copiar el `access_token` de la respuesta
7. Click en **Authorize** (candado verde arriba)
8. Pegar token en formato: `<token>` (sin "Bearer")
9. Ahora puedes probar todos los endpoints autenticados

---

### Opción B: Usar curl en PowerShell

```powershell
# 1. Login
$response = curl.exe -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/json" -d '{\"email\": \"dev@quicktask.com\", \"password\": \"dev1234\"}' | ConvertFrom-Json

# 2. Guardar el token automáticamente
$TOKEN = $response.access_token

# 3. Listar tareas
curl.exe -X GET "http://localhost:8000/api/tasks" -H "Authorization: Bearer $TOKEN"

# 4. Ver solo pendientes
curl.exe -X GET "http://localhost:8000/api/tasks?status=pending" -H "Authorization: Bearer $TOKEN"

# 5. Crear nueva tarea
curl.exe -X POST "http://localhost:8000/api/tasks" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{\"title\": \"Mi tarea nueva\"}'
```

**Nota importante:** En PowerShell, usa `curl.exe` en lugar de `curl` para evitar conflictos con el alias de `Invoke-WebRequest`.

---

## 🗂️ Estructura de archivos creados

```
backend/
├── app/
│   ├── __init__.py         # Package marker
│   ├── main.py             # ⭐ FastAPI app + endpoints
│   ├── database.py         # Configuración SQLAlchemy
│   ├── models.py           # Modelos ORM (User, Task, Reminder)
│   ├── schemas.py          # Validación Pydantic
│   ├── crud.py             # Operaciones de base de datos
│   └── auth.py             # JWT y autenticación
│
├── venv/                   # Entorno virtual (gitignored)
├── quicktask.db            # Base de datos SQLite (gitignored)
│
├── requirements.txt        # Dependencias
├── init_dev_data.py        # Script para inicializar datos
├── README.md               # Documentación completa
├── test_api.md             # Guía de pruebas con curl
├── QUICKSTART.md           # Este archivo
└── .gitignore              # Archivos ignorados por git
```

---

## 📚 Próximos pasos

1. **Leer documentación completa:** `README.md`
2. **Probar todos los endpoints:** `test_api.md`
3. **Explorar el código:** empezar por `app/main.py`
4. **Modificar y experimentar:** el servidor se recarga automáticamente

---

## 🐛 Problemas comunes

### Error: "python no se reconoce como comando"

Asegúrate de tener Python instalado: https://www.python.org/downloads/

```powershell
python --version  # Debe mostrar Python 3.8+
```

---

### Error: "scripts de ejecución están deshabilitados"

Ejecutar PowerShell como Administrador y ejecutar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Error: "Import 'fastapi' could not be resolved"

Asegúrate de:
1. Tener el entorno virtual activado (debe aparecer `(venv)` en el prompt)
2. Haber instalado las dependencias: `pip install -r requirements.txt`

---

### Error: "Address already in use"

El puerto 8000 ya está ocupado. Usar otro puerto:

```powershell
uvicorn app.main:app --reload --port 8001
```

---

## ✅ Verificación

Si todo funciona correctamente:

- ✅ El servidor está corriendo en http://localhost:8000
- ✅ Puedes acceder a http://localhost:8000/docs
- ✅ Puedes hacer login con `dev@quicktask.com` / `dev1234`
- ✅ Puedes ver las 8 tareas de ejemplo

---

## 💡 Tips

- **Recargar datos de prueba:** volver a ejecutar `python init_dev_data.py`
- **Ver logs del servidor:** aparecen en la terminal donde ejecutaste `uvicorn`
- **Detener servidor:** `Ctrl + C` en la terminal
- **Eliminar BD:** borrar archivo `quicktask.db` y volver a ejecutar `init_dev_data.py`

---

## 🎯 Objetivo logrado

Ya tienes un **backend REST completo** para QuickTask funcionando con:

- ✅ Autenticación JWT
- ✅ CRUD de tareas
- ✅ Filtros y búsqueda
- ✅ Recordatorios
- ✅ Documentación automática
- ✅ Base de datos SQLite
- ✅ Datos de prueba

**¡Listo para desarrollar el frontend!** 🚀
