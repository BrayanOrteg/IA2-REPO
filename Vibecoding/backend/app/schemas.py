"""
schemas.py
----------
Esquemas Pydantic para validación de datos de entrada/salida.
Define los contratos de la API REST.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ========== USER SCHEMAS ==========

class UserCreate(BaseModel):
    """Schema para crear un nuevo usuario (RF1: Registro)"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Contraseña mínimo 8 caracteres")


class UserLogin(BaseModel):
    """Schema para inicio de sesión (RF2: Login)"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema de respuesta con datos de usuario (sin password)"""
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # Permite convertir desde ORM models


class Token(BaseModel):
    """Schema para respuesta de autenticación"""
    access_token: str
    token_type: str = "bearer"


# ========== TASK SCHEMAS ==========

class TaskBase(BaseModel):
    """Schema base compartido para Task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema para crear tarea (RF4: Crear tarea)"""
    pass


class TaskUpdate(BaseModel):
    """Schema para actualizar tarea (RF5: Editar tarea)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(pending|completed)$")


class TaskResponse(TaskBase):
    """Schema de respuesta con datos completos de tarea"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema para listado paginado de tareas"""
    tasks: list[TaskResponse]
    total: int
    pending: int
    completed: int


# ========== REMINDER SCHEMAS ==========

class ReminderCreate(BaseModel):
    """Schema para crear recordatorio (RF11: Configurar recordatorios)"""
    task_id: int
    remind_at: datetime


class ReminderResponse(BaseModel):
    """Schema de respuesta de recordatorio"""
    id: int
    task_id: int
    remind_at: datetime
    is_sent: bool

    class Config:
        from_attributes = True


# ========== NOTIFICATION SCHEMAS ==========

class NotificationCreate(BaseModel):
    """Schema para crear notificación"""
    user_id: int
    message: str
    type: str = Field(..., pattern="^(email|push)$")


class NotificationResponse(BaseModel):
    """Schema de respuesta de notificación"""
    id: int
    user_id: int
    message: str
    type: str
    sent_at: datetime

    class Config:
        from_attributes = True


# ========== GENERAL SCHEMAS ==========

class MessageResponse(BaseModel):
    """Schema genérico para mensajes de respuesta"""
    message: str
    detail: Optional[str] = None
