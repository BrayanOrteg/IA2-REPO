"""
crud.py
-------
Operaciones CRUD (Create, Read, Update, Delete) para las entidades.
Implementa TaskService del diagrama de clases.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from . import models, schemas


# ========== USER CRUD ==========

def create_user(db: Session, user: schemas.UserCreate, password_hash: str) -> models.User:
    """
    Crea un nuevo usuario en la BD.
    Implementa AuthService.register() del diagrama.
    """
    db_user = models.User(
        email=user.email,
        password_hash=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Obtiene un usuario por email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Obtiene un usuario por ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


# ========== TASK CRUD ==========

def create_task(db: Session, task: schemas.TaskCreate, user_id: int) -> models.Task:
    """
    Crea una nueva tarea para un usuario.
    Implementa TaskService.createTask() del diagrama (RF4).
    """
    db_task = models.Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(
    db: Session,
    user_id: int,
    status: Optional[str] = None,
    order_by: str = "created_at",
    search: Optional[str] = None
) -> List[models.Task]:
    """
    Obtiene lista de tareas de un usuario con filtros opcionales.
    Implementa TaskService.filterTasks() del diagrama (RF8, RF9, RF13).
    
    Args:
        status: Filtrar por estado (pending|completed) - RF8
        order_by: Ordenar por campo (created_at|due_date) - RF9
        search: Búsqueda por palabras clave en título/descripción - RF13
    """
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    
    # Filtro por estado (RF8)
    if status:
        query = query.filter(models.Task.status == status)
    
    # Búsqueda por keywords (RF13)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (models.Task.title.ilike(search_pattern)) |
            (models.Task.description.ilike(search_pattern))
        )
    
    # Ordenamiento (RF9)
    if order_by == "due_date":
        query = query.order_by(models.Task.due_date.desc().nullslast())
    else:  # created_at por defecto
        query = query.order_by(models.Task.created_at.desc())
    
    return query.all()


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Optional[models.Task]:
    """Obtiene una tarea específica verificando que pertenezca al usuario"""
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()


def update_task(
    db: Session,
    task_id: int,
    user_id: int,
    task_update: schemas.TaskUpdate
) -> Optional[models.Task]:
    """
    Actualiza los datos de una tarea.
    Implementa TaskService.updateTask() del diagrama (RF5).
    """
    db_task = get_task_by_id(db, task_id, user_id)
    
    if not db_task:
        return None
    
    # Actualizar solo los campos proporcionados
    update_data = task_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    
    return db_task


def mark_task_completed(db: Session, task_id: int, user_id: int) -> Optional[models.Task]:
    """
    Marca una tarea como completada.
    Implementa TaskService.markCompleted() del diagrama (RF6).
    """
    db_task = get_task_by_id(db, task_id, user_id)
    
    if not db_task:
        return None
    
    db_task.status = "completed"
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    
    return db_task


def mark_task_pending(db: Session, task_id: int, user_id: int) -> Optional[models.Task]:
    """Revierte una tarea a estado pendiente (RF6)"""
    db_task = get_task_by_id(db, task_id, user_id)
    
    if not db_task:
        return None
    
    db_task.status = "pending"
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    
    return db_task


def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    """
    Elimina permanentemente una tarea.
    Implementa TaskService.deleteTask() del diagrama (RF7).
    """
    db_task = get_task_by_id(db, task_id, user_id)
    
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    
    return True


def get_task_statistics(db: Session, user_id: int) -> dict:
    """
    Obtiene estadísticas de tareas del usuario (RF14).
    Retorna total, completadas y pendientes.
    """
    total = db.query(models.Task).filter(models.Task.user_id == user_id).count()
    completed = db.query(models.Task).filter(
        models.Task.user_id == user_id,
        models.Task.status == "completed"
    ).count()
    pending = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }


# ========== REMINDER CRUD ==========

def create_reminder(db: Session, reminder: schemas.ReminderCreate, user_id: int) -> Optional[models.Reminder]:
    """
    Crea un recordatorio para una tarea.
    Implementa ReminderService.scheduleReminder() del diagrama (RF11).
    """
    # Verificar que la tarea existe y pertenece al usuario
    task = get_task_by_id(db, reminder.task_id, user_id)
    
    if not task:
        return None
    
    db_reminder = models.Reminder(
        task_id=reminder.task_id,
        remind_at=reminder.remind_at
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    
    return db_reminder


def get_reminders_by_user(db: Session, user_id: int) -> List[models.Reminder]:
    """Obtiene todos los recordatorios de un usuario"""
    return db.query(models.Reminder).join(models.Task).filter(
        models.Task.user_id == user_id
    ).all()


# ========== NOTIFICATION CRUD ==========

def create_notification(
    db: Session, 
    user_id: int, 
    message: str, 
    notification_type: str
) -> models.Notification:
    """
    Crea una notificación para un usuario.
    Implementa NotificationService del diseño.
    """
    db_notification = models.Notification(
        user_id=user_id,
        message=message,
        type=notification_type
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    return db_notification


def get_notifications_by_user(db: Session, user_id: int, limit: int = 50) -> List[models.Notification]:
    """Obtiene las notificaciones más recientes de un usuario"""
    return db.query(models.Notification).filter(
        models.Notification.user_id == user_id
    ).order_by(models.Notification.sent_at.desc()).limit(limit).all()
