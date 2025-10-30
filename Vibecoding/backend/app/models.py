"""
models.py
---------
Modelos ORM de SQLAlchemy que representan las entidades del sistema.
Basado en el diseño de base de datos de QuickTask.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    """
    Modelo de Usuario.
    Representa a un usuario registrado en QuickTask.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación: un usuario tiene múltiples tareas
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    
    # Relación: un usuario tiene múltiples notificaciones
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Task(Base):
    """
    Modelo de Tarea.
    Representa una tarea creada por un usuario.
    """
    __tablename__ = "tasks"
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'completed')", name='check_status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending | completed
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con User
    owner = relationship("User", back_populates="tasks")

    # Relación con Reminder (1:1 opcional)
    reminder = relationship("Reminder", back_populates="task", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"


class Reminder(Base):
    """
    Modelo de Recordatorio.
    Representa un recordatorio asociado a una tarea.
    """
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), unique=True, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    is_sent = Column(Boolean, default=False)

    # Relación con Task
    task = relationship("Task", back_populates="reminder")

    def __repr__(self):
        return f"<Reminder(id={self.id}, task_id={self.task_id}, remind_at={self.remind_at})>"


class Notification(Base):
    """
    Modelo de Notificación.
    Registra notificaciones enviadas al usuario (email o push).
    """
    __tablename__ = "notifications"
    
    __table_args__ = (
        CheckConstraint("type IN ('email', 'push')", name='check_notification_type'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)  # email | push
    sent_at = Column(DateTime, default=datetime.utcnow)

    # Relación con User
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, user_id={self.user_id})>"
