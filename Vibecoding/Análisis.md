# Análisis funcional y técnico — **QuickTask**
---

## 1. Resumen funcional (qué hace la app y cómo interactúan los componentes)

QuickTask es una **app de gestión de tareas personales** que permite a los usuarios registrarse, crear/editar/eliminar tareas, marcarlas como completadas, sincronizarlas entre dispositivos y recibir recordatorios.
Flujo simplificado:

* El **usuario** interactúa con la UI (web / móvil) para CRUD de tareas y configuración de recordatorios.
* La **UI** llama a la **API** REST/GraphQL para persistir datos en la **base de datos**.
* Para **sincronización en tiempo real** y notificaciones push, hay un canal de mensajería (WebSockets / servicio push).
* Un componente de **notificaciones** (email + push) envía recordatorios programados.
* Un **servicio de autenticación** proporciona login/registro y emisión de tokens.
* Servicios infra (CDN, almacenamiento de archivos, monitoring, backups) soportan disponibilidad y escalado.

---

## 2. Análisis de módulos / componentes principales

### 2.1 Frontend (Web)

* **Responsabilidades:** UI, interacción, validaciones cliente, cache local, sincronización offline básica.
* **Subcomponentes:** Dashboard (lista/filtrado/orden), detalle de tarea (create/edit), búsqueda, perfil/ajustes (recordatorios, notificaciones).
* **Características clave:** PWA-ready (opcional), offline cache, accessibilidad básica.

### 2.2 Frontend (Móvil)

* **Responsabilidades:** misma funcionalidad que web; notificaciones push nativas; sincronización inmediata.
* **Plataforma inicial:** Android (visto requisito previo), diseñar para soportar iOS en roadmap.

### 2.3 Backend (API)

* **Responsabilidades:** lógica de negocio, validación, autorizaciones, gestión de tareas, planificación de recordatorios, webhooks.
* **Interfaz:** REST (principal) y/o GraphQL (opcional) + WebSocket endpoint para eventos en tiempo real.
* **Escalado:** stateless app servers detrás de load balancer.

### 2.4 Persistencia

* **Base relacional (primaria):** Postgres para transacciones, consultas estructuradas, y relaciones (usuario — tareas).
* **Cache / pubsub:** Redis para cache, rate limiting, sesiones efímeras y pub/sub WebSocket broadcast.
* **Almacenamiento de ficheros:** Object storage (S3-compatible) para anexos, si aplica.

### 2.5 Sincronización / Tiempo real

* **WebSockets** + Redis Pub/Sub para sincronizar cambios entre instancias y dispositivos.
* Estrategia offline: cambios locales + sincronización con control de conflictos (optimistic concurrency / timestamps / version numbers).

### 2.6 Notificaciones y recordatorios

* **Push (Android):** FCM (Firebase Cloud Messaging) o proveedor equivalente.
* **Email:** SendGrid, Mailgun o SMTP gestionado.
* **Scheduler:** Job queue (Celery / RQ / Sidekiq / Hangfire) para ejecutar recordatorios.

### 2.7 Autenticación y Autorización

* **Auth:** OAuth2 + JWT (token corto + refresh token) o uso de un Identity Provider gestionado (Firebase Auth, Auth0).
* **Roles:** usuario estándar (no hay roles complejos inicialmente).

### 2.8 Observabilidad y operación

* **Logging centralizado**, metrics (Prometheus), traces (OpenTelemetry) y alerting.
* **CI/CD:** pipeline automatizado (tests, lint, build, deploy).
* **Backups:** backups periódicos de DB y storage.

---

## 3. Tecnologías recomendadas (por módulo) y stack propuesto

> **Recomendación balanceada** para rapidez de entrega, comunidad y escalabilidad:

### Frontend Web

* **Framework:** React + TypeScript
  *Justificación:* amplio ecosistema, buena interoperabilidad, PWA y librerías maduras para componentes y testing.

### Frontend Móvil

* **Framework:** React Native (TypeScript) **o** Flutter si prioridad es mobile-first.
  *Justificación:* React Native comparte ideas/parte del stack con React web (reaprovechamiento de lógica). Flutter es excelente si se desea UI nativa consistente y mejor performance gráfico, pero implica otra base de código.

### Backend API

* **Framework:** FastAPI (Python) + Uvicorn / Gunicorn
  *Justificación breve:* alto rendimiento, rutas declarativas con tipos (Type Hints), documentación automática (OpenAPI) y desarrollo rápido.

### Persistencia

* **DB:** PostgreSQL (gestión en RDS / Cloud SQL o managed provider)
* **Cache / PubSub:** Redis (managed)
* **Object Storage:** S3 (o compatible)

### Queue / Scheduler

* **Worker:** Celery (Python) con broker Redis / RabbitMQ, o RQ para menor complejidad.

### Autenticación

* **Opción rápida:** Firebase Auth (si quieres acelerar MVP).
* **Opción controlada:** OAuth2/JWTS con provider propio o Auth0 (managed).

### Infraestructura / DevOps

* **Cloud:** AWS / GCP / Azure (cualquiera, elegir por coste/alianzas).
* **CI/CD:** GitHub Actions / GitLab CI.
* **Containerización:** Docker + Kubernetes (o ECS/Fargate si se prefiere serverless containers).
* **Monitoring:** Prometheus + Grafana, logs en ELK/Cloud provider logs.

---

## 4. Riesgos técnicos y mitigaciones

1. **Riesgo: Conflictos de sincronización entre dispositivos (ediciones concurrentes).**
   **Mitigación:** usar versionado de recursos (ETag / version number), estrategia LWW (last write wins) + mostrar historial o advertencia de conflicto en UI.

2. **Riesgo: Costo y complejidad de mantener servicios en tiempo real a escala.**
   **Mitigación:** empezar con polling optimizado o usar un servicio gestionado (Firebase Realtime / Firestore) para MVP; migrar a WebSockets + Redis Pub/Sub cuando la demanda crezca.

3. **Riesgo: Implementación de notificaciones push para múltiples plataformas.**
   **Mitigación:** centralizar en un gateway (FCM para Android; en futuro APNs para iOS) y abstraer en un servicio de notificaciones.

4. **Riesgo: Seguridad de datos (exposición de tareas).**
   **Mitigación:** TLS obligatorio, JWT con expiración corta, claims mínimos, roles y validaciones en backend, revisión de dependencias.

5. **Riesgo: Rendimiento ante picos de usuarios.**
   **Mitigación:** cache a nivel app (Redis), consultas optimizadas, índices DB y escalado horizontal por microservicio.

6. **Riesgo: Complejidad operativa (múltiples stacks y servicios).**
   **Mitigación:** iniciar con arquitectura simple (monolito modular) y evolucionar a microservicios si es necesario.

---

## 5. Mapa general de dependencias (visión de alto nivel)

```
[User Devices] <--HTTPS/WebSocket--> [Load Balancer]
                                       |
                            +----------+----------+
                            |                     |
                      [API Servers] <--> [Redis (cache/pubsub)]
                            |
               +------------+------------+
               |                         |
         [PostgreSQL]             [Object Storage S3]
               |
         (Backups / Replica)
               
[Authentication Provider] <-used by-> [API Servers]
[Job Queue / Workers] <--> [Redis] (runs scheduled reminders)
[Notification Provider (FCM / Email)] <- used by -> [Workers/API]
[CI/CD Pipeline] -> deploys -> [API Servers / Frontend Hosts]
[Monitoring / Logging] <- collects metrics/logs from -> [API Servers / Workers / DB]
```

---

## 6. Justificación técnica de elecciones (comparaciones clave)

### Por qué **FastAPI** sobre **Flask**

* **Rendimiento:** FastAPI (ASGI) maneja concurrencia mejor que Flask (WSGI) sin añadir mucho overhead.
* **Tipado y documentación automática:** FastAPI usa type hints para validación y genera OpenAPI/Swagger automáticamente, acelerando integraciones front-back.
* **Ecosistema Python:** si se desea usar Celery, SQLAlchemy, etc., FastAPI se integra bien.
* **Cuando elegir Flask:** si el equipo ya tiene mucha experiencia legacy en Flask y no se necesita alto throughput, Flask sigue siendo válido.

### Por qué **PostgreSQL** sobre **MongoDB**

* **Modelo de datos relacional:** tareas y usuarios encajan bien en una DB relacional; las consultas (filtrado, orden) y la consistencia son más fáciles.
* **Integridad y ACID:** importante para evitar pérdida / duplicación de tareas.
* **Cuando elegir MongoDB:** si necesitas almacenamiento flexible de documentos (muchos schemas cambiantes) o sincronización offline tipo CouchDB.

### Por qué **React + React Native** sobre otras opciones

* **Reutilización de lógica y equipo:** compartir TypeScript y librerías; velocidad de desarrollo.
* **Ecosistema maduro:** librerías para forms, testing y componentes.
* **Cuando elegir Flutter:** si UI nativa consistente y rendimiento gráfico son prioritarios, o si se prefiere un único equipo para mobile con excelente soporte para animaciones.

### WebSockets vs. polling vs. managed realtime (Firebase)

* **WebSockets:** mejor experiencia en tiempo real y consumo de datos eficiente para cambios frecuentes.
* **Polling:** simple, pero ineficiente; útil para MVP si desea simplicidad.
* **Firebase:** ideal para MVP si se prioriza rapidez de lanzamiento y sincronización automática sin operar infraestructura real-time.

---

## 7. Diseño de API (ejemplos de endpoints principales)

*(REST, usar JSON; autenticar con Bearer JWT)*

* `POST /api/auth/register` — registrar usuario
* `POST /api/auth/login` — obtener JWT + refresh token
* `POST /api/tasks` — crear tarea `{ title, description?, due_date?, priority? }`
* `GET /api/tasks` — obtener lista (filtros: status, q, order)
* `GET /api/tasks/{id}` — detalle tarea
* `PUT /api/tasks/{id}` — actualizar tarea (con version/etag)
* `DELETE /api/tasks/{id}` — eliminar tarea
* `POST /api/tasks/{id}/complete` — marcar completada
* `POST /api/tasks/{id}/reminder` — configurar recordatorio
* `WS /api/ws` — canal WebSocket para eventos `task_created/updated/deleted`

---

## 8. Consideraciones operativas y roadmap técnico (sugerido)

**Fase 0 — MVP (Riesgo bajo, entrega rápida)**

* Monolito FastAPI + Postgres, React web, mobile Android nativo o React Native mínimo.
* Polling cada X segundos para sincronización o simple WebSocket single-instance.
* Firebase Auth (opcional) + FCM para push.
* Deploy en 1-2 instancias gestionadas (Heroku / Cloud Run / ECS Fargate).

**Fase 1 — Escalado y mejora (cuando usuarios activos aumenten)**

* Introducir Redis como cache + pub/sub.
* Workers para recordatorios y enviar notificaciones.
* Horizontal autoscaling, backups, métricas y alertas.

**Fase 2 — Resiliencia / features avanzadas**

* Multi-region DB replicas, CQRS si las consultas superan carga de writes, GraphQL si clientes requieren queries más flexibles.

---

## 9. Resumen ejecutivo — recomendaciones prioritarias

1. **Stack propuesto para MVP:** React (web) + React Native (Android) + FastAPI + PostgreSQL + Redis + Celery + FCM + S3.
2. **Estrategia de sincronización:** empezar con WebSockets + Redis pub/sub para un modelo escalable; si se necesita rapidez de MVP considerar Firebase para realtime gestionado.
3. **Autenticación:** Firebase Auth para tiempo de desarrollo corto; migrar a OAuth2/JWT propio si se requiere control o integraciones complejas.
4. **Observabilidad y Ops:** configurar logging y métricas desde el inicio para poder detectar problemas temprano.
5. **Comenzar simple, diseñar para evolucionar:** monolito modular bien organizado -> microservicios si la carga/organización lo exige.

---

## 10. Lista corta de decisiones que el equipo debe tomar (pendientes)

* ¿Prioridad MVP: velocidad de entrega (usar Firebase) o control total (auth propia + infra)?
* ¿Deseas una sola base de código para móvil y web (React / React Native) o prefieres Flutter?
* ¿Nivel de consistencia y políticas de conflicto en sincronización (LWW vs. merging)?
* ¿Presupuesto para infra gestionada (Auth0, SendGrid, Firebase) vs. infra autogestionada?