## 🧩 1. Diagrama de casos de uso — *PlantUML code*

```
@startuml
left to right direction
actor "Usuario" as User
actor "Sistema QuickTask" as System

rectangle "QuickTask" {
    usecase "Registrarse" as UC_Register
    usecase "Iniciar sesión" as UC_Login
    usecase "Recuperar contraseña" as UC_Recover
    usecase "Crear tarea" as UC_CreateTask
    usecase "Editar tarea" as UC_EditTask
    usecase "Eliminar tarea" as UC_DeleteTask
    usecase "Marcar tarea como completada" as UC_CompleteTask
    usecase "Filtrar/ordenar tareas" as UC_FilterTasks
    usecase "Configurar recordatorios" as UC_SetReminder
    usecase "Recibir notificaciones" as UC_ReceiveNotification
    usecase "Sincronizar tareas entre dispositivos" as UC_SyncTasks
}

User --> UC_Register
User --> UC_Login
User --> UC_Recover
User --> UC_CreateTask
User --> UC_EditTask
User --> UC_DeleteTask
User --> UC_CompleteTask
User --> UC_FilterTasks
User --> UC_SetReminder
UC_SetReminder --> UC_ReceiveNotification : <<include>>
User --> UC_SyncTasks

System --> UC_ReceiveNotification
System --> UC_SyncTasks
@enduml
```

### 🎯 Propósito del diagrama de casos de uso

Este diagrama muestra **cómo interactúan los actores (Usuario y Sistema)** con las funcionalidades principales de QuickTask.
Permite visualizar los **flujos de acción de alto nivel**, como la gestión de tareas, autenticación y recordatorios, sin entrar en detalles técnicos.
Es útil para comunicación con usuarios finales y stakeholders, mostrando **qué hace el sistema** y **quién lo usa**.

---

## 🧱 2. Diagrama de clases — *PlantUML code*

```
@startuml
class User {
    +id: UUID
    +email: String
    +passwordHash: String
    +createdAt: DateTime
    +login(email, password)
    +register(email, password)
    +recoverPassword(email)
}

class Task {
    +id: UUID
    +title: String
    +description: String
    +status: String
    +dueDate: Date
    +createdAt: DateTime
    +updatedAt: DateTime
    +markCompleted()
    +updateDetails(title, description, dueDate)
}

class Reminder {
    +id: UUID
    +taskId: UUID
    +remindAt: DateTime
    +sendNotification()
}

class Notification {
    +id: UUID
    +type: String
    +message: String
    +sentAt: DateTime
}

class AuthService {
    +login(email, password)
    +register(email, password)
    +generateToken(userId)
}

class TaskService {
    +createTask(userId, title, description, dueDate)
    +updateTask(taskId, title, description, dueDate)
    +deleteTask(taskId)
    +markCompleted(taskId)
    +filterTasks(userId, status, order)
}

class ReminderService {
    +scheduleReminder(taskId, remindAt)
    +triggerReminder(reminderId)
}

User "1" -- "0..*" Task : "posee"
Task "1" -- "0..1" Reminder : "tiene"
Reminder --> Notification : "genera"
AuthService ..> User : "gestiona autenticación"
TaskService ..> Task : "opera sobre"
ReminderService ..> Reminder : "programa"

@enduml
```

### 🧠 Propósito del diagrama de clases

El diagrama de clases representa la **estructura lógica del sistema QuickTask**.
Define las **entidades principales** (User, Task, Reminder) junto con sus **atributos, métodos y relaciones**.
También incluye **servicios funcionales** (AuthService, TaskService, ReminderService) que encapsulan la lógica de negocio.

Sirve para:

* Comunicar la **arquitectura orientada a objetos** a desarrolladores.
* Identificar relaciones (1:N, composiciones, dependencias).
* Servir de base para la implementación del modelo de dominio en código.