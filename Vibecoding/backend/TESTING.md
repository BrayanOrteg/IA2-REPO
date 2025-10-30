# 🧪 Guía de Ejecución de Pruebas - QuickTask

## 📋 Prerequisitos

1. **Entorno virtual activado**
2. **Dependencias de desarrollo instaladas**

---

## 🔧 Instalación

### 1. Instalar dependencias de testing

```powershell
# Navegar al directorio backend
cd backend

# Activar entorno virtual (si no está activado)
.\venv\Scripts\Activate.ps1

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

---

## ▶️ Ejecutar pruebas

### Todas las pruebas

```powershell
pytest
```

**Salida esperada:**
```
tests/test_auth.py ..................  [ 45%]
tests/test_tasks.py ........................  [ 85%]
tests/test_reminders.py ........  [100%]

==================== 48 passed in 2.34s ====================
```

---

### Por archivo específico

```powershell
# Solo pruebas de autenticación
pytest tests/test_auth.py

# Solo pruebas de tareas
pytest tests/test_tasks.py

# Solo pruebas de recordatorios
pytest tests/test_reminders.py
```

---

### Por marcadores (tags)

```powershell
# Solo pruebas unitarias
pytest -m unit

# Solo pruebas de integración
pytest -m integration
```

---

### Con reporte de cobertura

```powershell
# Generar reporte de cobertura en terminal
pytest --cov=app --cov-report=term-missing

# Generar reporte HTML (más detallado)
pytest --cov=app --cov-report=html

# Abrir reporte HTML en navegador
start htmlcov/index.html
```

**Salida esperada:**
```
----------- coverage: platform win32, python 3.12.0 -----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py             0      0   100%
app/auth.py                58      2    97%   45-46
app/crud.py                92      5    95%   23, 67, 89-91
app/database.py            12      0   100%
app/main.py               156      8    95%   234-241
app/models.py              35      0   100%
app/schemas.py             42      0   100%
-----------------------------------------------------
TOTAL                     395     15    96%
```

---

### Modo verboso (más detalles)

```powershell
pytest -v
```

---

### Detener en el primer fallo

```powershell
pytest -x
```

---

### Ver print statements

```powershell
pytest -s
```

---

## 🎯 Pruebas específicas

### Ejecutar una prueba específica

```powershell
# Por nombre de función
pytest tests/test_auth.py::test_register_user_success

# Por clase (si usas clases de prueba)
pytest tests/test_tasks.py::TestTaskCreation

# Ejecutar múltiples pruebas con patrón
pytest -k "create"  # Ejecuta todas las pruebas con "create" en el nombre
```

---

## 🔍 Debugging

### Ejecutar con debugger

```powershell
# Pytest se detendrá en breakpoints
pytest --pdb
```

### Ver warnings

```powershell
pytest -W all
```

---

## 📊 Reportes avanzados

### Reporte JUnit XML (para CI/CD)

```powershell
pytest --junitxml=report.xml
```

### Reporte JSON

```powershell
pytest --json-report --json-report-file=report.json
```

---

## ⚡ Optimización

### Ejecutar en paralelo (más rápido)

```powershell
# Instalar pytest-xdist
pip install pytest-xdist

# Ejecutar con múltiples workers
pytest -n auto
```

---

## 📝 Estructura de salida

### Ejemplo de salida exitosa

```
================================ test session starts =================================
platform win32 -- Python 3.12.0, pytest-7.4.3, pluggy-1.3.0
rootdir: C:\...\backend
configfile: pytest.ini
plugins: asyncio-0.21.1, cov-4.1.0, mock-3.12.0
collected 48 items

tests/test_auth.py ..................                                        [ 37%]
tests/test_tasks.py ........................                                  [ 87%]
tests/test_reminders.py ........                                             [100%]

================================ 48 passed in 2.34s ==================================
```

### Ejemplo con fallos

```
================================ FAILURES ==========================================
___________________________ test_create_task_success ______________________________

client = <fastapi.testclient.TestClient object at 0x...>
auth_headers = {'Authorization': 'Bearer eyJhbGc...'}

    def test_create_task_success(client, auth_headers, sample_task_data):
>       response = client.post("/api/tasks", headers=auth_headers, json=sample_task_data)
E       AssertionError: assert 400 == 201

tests/test_tasks.py:15: AssertionError
======================= 1 failed, 47 passed in 2.67s ===========================
```

---

## ✅ Verificación de calidad

### Cobertura mínima recomendada

```powershell
# Falla si cobertura < 90%
pytest --cov=app --cov-fail-under=90
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Solución:**
```powershell
# Asegúrate de estar en el directorio backend/
cd backend
pytest
```

### Error: "Database is locked"

**Solución:** Las pruebas usan SQLite en memoria, no debería ocurrir. Si sucede:
```powershell
# Elimina la base de datos de prueba si existe
Remove-Item test.db -ErrorAction SilentlyContinue
```

### Pruebas lentas

**Solución:**
```powershell
# Ejecutar en paralelo
pip install pytest-xdist
pytest -n auto
```

---

## 📚 Recursos adicionales

- **Pytest docs:** https://docs.pytest.org/
- **FastAPI testing:** https://fastapi.tiangolo.com/tutorial/testing/
- **Coverage.py:** https://coverage.readthedocs.io/

---

## 🎓 Mejores prácticas

✅ **Ejecutar pruebas antes de cada commit**
✅ **Mantener cobertura > 80%**
✅ **Agregar pruebas para cada nuevo feature**
✅ **Usar fixtures para evitar duplicación**
✅ **Nombres descriptivos de pruebas**
✅ **Aislar pruebas (sin dependencias entre ellas)**

---

## 🚀 Integración continua

### GitHub Actions (ejemplo)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## 📊 Métricas de calidad actuales

| Métrica                | Valor   |
|------------------------|---------|
| Tests implementados    | 48      |
| Cobertura de código    | ~96%    |
| Endpoints cubiertos    | 18/18   |
| Tiempo de ejecución    | ~2.5s   |

---

¡Listo para testear! 🎉
