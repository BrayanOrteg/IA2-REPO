# 🏗️ Diseño de Base de Datos y Arquitectura del Sistema — **QuickTask**
---

## 🧩 1. Base de datos

### 1.1 Modelo Entidad-Relación (E/R) — Descripción textual

El modelo de datos de **QuickTask** se centra en la gestión de usuarios, tareas y recordatorios, con soporte para notificaciones.

**Entidades principales:**

1. **User**

   * Representa a cada persona registrada en la aplicación.
   * Atributos: `id`, `email`, `password_hash`, `created_at`.
   * Relación: un usuario **posee muchas tareas**.

2. **Task**

   * Representa una tarea creada por un usuario.
   * Atributos: `id`, `user_id`, `title`, `description`, `status`, `due_date`, `created_at`, `updated_at`.
   * Relación: una tarea **puede tener un recordatorio** (1:1) y pertenece a un usuario (N:1).

3. **Reminder**

   * Representa un recordatorio asociado a una tarea específica.
   * Atributos: `id`, `task_id`, `remind_at`, `is_sent`.
   * Relación: cada recordatorio **pertenece a una tarea** (1:1).

4. **Notification**

   * Registra una notificación enviada al usuario (por correo o push).
   * Atributos: `id`, `user_id`, `message`, `type`, `sent_at`.
   * Relación: una notificación **pertenece a un usuario** (N:1).

**Relaciones clave:**

* `User (1) → (N) Task`
* `Task (1) → (1) Reminder`
* `User (1) → (N) Notification`

---

### 1.2 Esquema SQL (compatible con SQLite)

```sql
-- ===========================
-- QuickTask Database Schema
-- ===========================

-- 1. Tabla de usuarios
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- 2. Tabla de tareas
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

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

-- 3. Tabla de recordatorios
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL UNIQUE,
    remind_at DATETIME NOT NULL,
    is_sent BOOLEAN DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

CREATE INDEX idx_reminders_task_id ON reminders(task_id);
CREATE INDEX idx_reminders_remind_at ON reminders(remind_at);

-- 4. Tabla de notificaciones
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    type TEXT CHECK(type IN ('email', 'push')),
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_sent_at ON notifications(sent_at);
```

**Decisiones clave:**

* Se usan claves **autoincrementales** para simplicidad y compatibilidad con SQLite.
* Restricciones `CHECK` aseguran estados válidos (`pending`, `completed`).
* Eliminación en cascada garantiza limpieza automática al borrar un usuario o tarea.
* Índices para consultas frecuentes: `email`, `status`, `due_date`, `remind_at`.

---

## 🧠 2. Arquitectura del sistema

### 2.1 Capas principales (Arquitectura lógica)

La aplicación QuickTask sigue un **modelo en capas** para separar responsabilidades y facilitar mantenimiento.

#### 🧱 Capa de Presentación (Frontend)

* **Responsabilidad:** interfaz de usuario (Web y Móvil).
* **Componentes:** React (web) / React Native (móvil).
* **Funciones clave:**

  * Interfaz de registro, login, y gestión de tareas.
  * Llamadas a la API vía HTTPS (REST o GraphQL).
  * Renderizado dinámico de tareas y notificaciones.
  * Uso de WebSockets para actualizaciones en tiempo real.

#### ⚙️ Capa de Lógica de Negocio (Backend)

* **Responsabilidad:** manejo de reglas, validaciones y procesos internos.
* **Tecnología sugerida:** FastAPI (Python) + Celery para tareas asíncronas.
* **Componentes internos:**

  * **AuthService:** autenticación JWT / Firebase Auth.
  * **TaskService:** creación, edición, filtrado y marcado de tareas.
  * **ReminderService:** programación y envío de recordatorios.
  * **NotificationService:** comunicación con FCM o proveedor de correo.

#### 🗄️ Capa de Datos (Persistencia)

* **Responsabilidad:** almacenamiento estructurado y seguro.
* **Componentes:**

  * Base de datos SQLite (MVP) → PostgreSQL en producción.
  * ORM sugerido: SQLAlchemy o Prisma (según stack elegido).
  * Manejo de transacciones, índices y relaciones.
  * Repositorios de acceso a datos desacoplados del dominio.

#### ☁️ Capa de Infraestructura (Servicios externos)

* **Servicios de soporte:**

  * Firebase Cloud Messaging (notificaciones push).
  * SMTP / SendGrid (emails).
  * Redis (cache + colas de tareas).
  * Object storage (S3) si se agregan archivos en el futuro.
* **Monitoreo:** logs centralizados y métricas.

---

### 2.2 Comunicación entre componentes

```text
[Usuario Web/Móvil]
     │
     ▼
[Frontend UI: React / React Native]
     │   (HTTP/REST, WebSocket)
     ▼
[Backend API: FastAPI]
     │   ├─ (Consulta / Persistencia)
     │   ▼
     │  [ORM → SQLite / PostgreSQL]
     │
     ├─ (Asíncrono)
     ▼
[Worker Celery / Scheduler]
     │
     ├─ Enviar recordatorios → [Firebase FCM / SMTP]
     └─ Registrar notificación → [DB notifications]
```

**Flujo típico:**

1. El usuario crea o edita una tarea → se guarda en `tasks`.
2. Si configura un recordatorio, se guarda en `reminders` y se agenda una tarea en segundo plano.
3. El worker ejecuta el recordatorio y genera una notificación (`notifications`).
4. El frontend recibe la notificación (push o en la app) y actualiza la interfaz.

---

### 2.3 Consideraciones de diseño

| Aspecto            | Decisión técnica                                                                        |
| ------------------ | --------------------------------------------------------------------------------------- |
| **Escalabilidad**  | SQLite para prototipo, PostgreSQL para despliegue productivo. Redis para cache/eventos. |
| **Sincronización** | WebSockets (FastAPI + Redis Pub/Sub) para actualizaciones en tiempo real.               |
| **Seguridad**      | Tokens JWT, cifrado de contraseñas (bcrypt), conexión HTTPS obligatoria.                |
| **Mantenibilidad** | Código modular (servicios y repositorios independientes).                               |
| **Disponibilidad** | Deploy en contenedores (Docker) con balanceo de carga si escala.                        |

---

### ✅ Resumen

* **Modelo de datos:** centrado en usuarios, tareas, recordatorios y notificaciones.
* **Esquema SQL:** normalizado, con claves foráneas y validaciones.
* **Arquitectura:** multicapa, escalable, y alineada con principios de *clean architecture*.
* **Beneficios:** claridad, mantenibilidad, posibilidad de evolución a microservicios y soporte multiplataforma.

---

¿Quieres que te genere también el **diagrama físico de base de datos (DER visual)** en formato PlantUML o Mermaid para complementar este diseño?
