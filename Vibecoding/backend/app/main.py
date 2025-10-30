"""
main.py
-------
Aplicación principal de FastAPI.
Define los endpoints de la API REST de QuickTask.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta

from . import models, schemas, crud, auth
from .database import engine, get_db

# Crear tablas en la BD
models.Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="QuickTask API",
    description="API REST para gestión de tareas personales",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS (permitir requests desde frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== ENDPOINTS DE AUTENTICACIÓN ==========

@app.post("/api/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    RF1: Registrar un nuevo usuario.
    
    Crea una cuenta con email y contraseña hasheada (RNF5).
    """
    # Verificar si el email ya existe
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Hashear contraseña y crear usuario
    password_hash = auth.hash_password(user.password)
    new_user = crud.create_user(db, user, password_hash)
    
    return new_user


@app.post("/api/auth/login", response_model=schemas.Token)
def login_user(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    RF2: Iniciar sesión.
    
    Autentica usuario y retorna JWT token.
    """
    user = auth.authenticate_user(db, user_login.email, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar token JWT (sub debe ser string según el estándar JWT)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """
    Obtiene información del usuario autenticado.
    """
    return current_user


# ========== ENDPOINTS DE TAREAS ==========

@app.post("/api/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    RF4: Crear una nueva tarea.
    
    El usuario autenticado puede crear tareas con título, descripción y fecha límite opcional.
    """
    new_task = crud.create_task(db, task, current_user.id)
    return new_task


@app.get("/api/tasks", response_model=schemas.TaskListResponse)
def list_tasks(
    status: Optional[str] = None,
    order_by: str = "created_at",
    search: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    RF8, RF9, RF13: Listar tareas con filtros y búsqueda.
    
    Requiere autenticación. Lista solo las tareas del usuario autenticado.
    
    Parámetros:
    - status: Filtrar por estado (pending|completed)
    - order_by: Ordenar por (created_at|due_date)
    - search: Buscar por palabras clave
    """
    # Validar status
    if status and status not in ["pending", "completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status debe ser 'pending' o 'completed'"
        )
    
    # Validar order_by
    if order_by not in ["created_at", "due_date"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order_by debe ser 'created_at' o 'due_date'"
        )
    
    # Obtener tareas del usuario autenticado
    tasks = crud.get_tasks(db, current_user.id, status, order_by, search)
    stats = crud.get_task_statistics(db, current_user.id)
    
    return {
        "tasks": tasks,
        "total": stats["total"],
        "pending": stats["pending"],
        "completed": stats["completed"]
    }


@app.get("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener detalle de una tarea específica.
    """
    task = crud.get_task_by_id(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    return task


@app.put("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    RF5: Actualizar datos de una tarea.
    
    Permite modificar título, descripción, fecha límite y estado.
    """
    updated_task = crud.update_task(db, task_id, current_user.id, task_update)
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    return updated_task


@app.post("/api/tasks/{task_id}/complete", response_model=schemas.TaskResponse)
def complete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    RF6: Marcar tarea como completada.
    """
    task = crud.mark_task_completed(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    return task


@app.post("/api/tasks/{task_id}/pending", response_model=schemas.TaskResponse)
def revert_task_to_pending(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    RF6: Revertir tarea a estado pendiente.
    """
    task = crud.mark_task_pending(db, task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    return task


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    RF7: Eliminar permanentemente una tarea.
    """
    success = crud.delete_task(db, task_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    return None


# ========== ENDPOINTS DE RECORDATORIOS ==========

@app.post("/api/reminders", response_model=schemas.ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    reminder: schemas.ReminderCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    RF11: Configurar recordatorio para una tarea.
    
    Programa una notificación para la fecha/hora especificada.
    """
    new_reminder = crud.create_reminder(db, reminder, current_user.id)
    
    if not new_reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada o no pertenece al usuario"
        )
    
    return new_reminder


@app.get("/api/reminders", response_model=list[schemas.ReminderResponse])
def list_reminders(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar todos los recordatorios del usuario.
    """
    reminders = crud.get_reminders_by_user(db, current_user.id)
    return reminders


# ========== ENDPOINTS DE NOTIFICACIONES ==========

@app.post("/api/notifications", response_model=schemas.NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification: schemas.NotificationCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear una notificación (uso interno o para testing).
    
    En producción, las notificaciones se crearían automáticamente
    por el sistema de recordatorios.
    """
    # Verificar que el usuario solo pueda crear notificaciones para sí mismo
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes crear notificaciones para otros usuarios"
        )
    
    new_notification = crud.create_notification(
        db, 
        notification.user_id, 
        notification.message, 
        notification.type
    )
    return new_notification


@app.get("/api/notifications", response_model=list[schemas.NotificationResponse])
def list_notifications(
    limit: int = 50,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar las notificaciones más recientes del usuario.
    """
    notifications = crud.get_notifications_by_user(db, current_user.id, limit)
    return notifications


# ========== ENDPOINT DE ESTADO ==========

@app.get("/")
def root():
    """
    Endpoint raíz para verificar que la API está funcionando.
    """
    return {
        "message": "QuickTask API v1.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/api/health")
def health_check():
    """
    Health check para monitoreo.
    """
    return {"status": "healthy"}
