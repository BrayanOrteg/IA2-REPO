#!/usr/bin/env python3
"""
Script de inicialización rápida para desarrollo.
Crea un usuario de prueba y algunas tareas de ejemplo.
"""

import sys
import os

# Agregar el directorio app al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal, engine
from app import models
from app.auth import hash_password
from datetime import datetime, timedelta

# Crear todas las tablas
models.Base.metadata.create_all(bind=engine)

def init_dev_data():
    """Inicializa datos de desarrollo en la base de datos"""
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existe el usuario de prueba
        existing_user = db.query(models.User).filter(
            models.User.email == "dev@quicktask.com"
        ).first()
        
        if existing_user:
            print("⚠️  Usuario de desarrollo ya existe. Limpiando datos anteriores...")
            # Eliminar tareas antiguas
            db.query(models.Task).filter(models.Task.user_id == existing_user.id).delete()
            user = existing_user
        else:
            # Crear usuario de desarrollo
            print("👤 Creando usuario de desarrollo...")
            user = models.User(
                email="dev@quicktask.com",
                password_hash=hash_password("dev1234")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ Usuario creado: {user.email}")
        
        # Crear tareas de ejemplo
        print("\n📝 Creando tareas de ejemplo...")
        
        tasks_data = [
            {
                "title": "Implementar autenticación JWT",
                "description": "Configurar sistema de login con tokens Bearer",
                "status": "completed"
            },
            {
                "title": "Diseñar base de datos",
                "description": "Crear modelos ORM para User, Task, Reminder y Notification",
                "status": "completed"
            },
            {
                "title": "Documentar API con Swagger",
                "description": "FastAPI genera documentación automática",
                "status": "completed"
            },
            {
                "title": "Implementar filtros y búsqueda",
                "description": "Permitir filtrar tareas por estado y buscar por keywords",
                "status": "pending",
                "due_date": datetime.utcnow() + timedelta(days=2)
            },
            {
                "title": "Integrar notificaciones push",
                "description": "Configurar FCM para enviar recordatorios",
                "status": "pending",
                "due_date": datetime.utcnow() + timedelta(days=5)
            },
            {
                "title": "Escribir tests unitarios",
                "description": "Cobertura mínima del 80%",
                "status": "pending",
                "due_date": datetime.utcnow() + timedelta(days=7)
            },
            {
                "title": "Optimizar queries de BD",
                "description": "Agregar índices y cachear resultados frecuentes",
                "status": "pending"
            },
            {
                "title": "Configurar CI/CD",
                "description": "Pipeline automático con GitHub Actions",
                "status": "pending",
                "due_date": datetime.utcnow() + timedelta(days=14)
            }
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            task = models.Task(
                user_id=user.id,
                **task_data
            )
            db.add(task)
            created_tasks.append(task)
        
        db.commit()
        
        print(f"✅ {len(created_tasks)} tareas creadas")
        
        # Crear recordatorio de ejemplo
        print("\n⏰ Creando recordatorio de ejemplo...")
        
        # Buscar una tarea pendiente con fecha
        task_with_date = next(
            (t for t in created_tasks if t.due_date and t.status == "pending"),
            None
        )
        
        if task_with_date:
            db.refresh(task_with_date)  # Asegurar que tenga ID
            reminder = models.Reminder(
                task_id=task_with_date.id,
                remind_at=task_with_date.due_date - timedelta(hours=1)
            )
            db.add(reminder)
            db.commit()
            print(f"✅ Recordatorio creado para: '{task_with_date.title}'")
        
        # Crear notificaciones de ejemplo
        print("\n📧 Creando notificaciones de ejemplo...")
        
        notifications_data = [
            {
                "message": "¡Bienvenido a QuickTask! Tu cuenta ha sido creada exitosamente.",
                "type": "email"
            },
            {
                "message": "Tienes 5 tareas pendientes para esta semana.",
                "type": "push"
            },
            {
                "message": "Recordatorio: La tarea 'Integrar notificaciones push' vence en 5 días.",
                "type": "push"
            }
        ]
        
        for notif_data in notifications_data:
            notification = models.Notification(
                user_id=user.id,
                **notif_data
            )
            db.add(notification)
        
        db.commit()
        print(f"✅ {len(notifications_data)} notificaciones creadas")
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("🎉 DATOS DE DESARROLLO INICIALIZADOS")
        print("="*60)
        print(f"\n👤 Usuario de prueba:")
        print(f"   Email: dev@quicktask.com")
        print(f"   Password: dev1234")
        print(f"\n📊 Estadísticas:")
        
        total = len(created_tasks)
        completed = sum(1 for t in created_tasks if t.status == "completed")
        pending = total - completed
        
        print(f"   Total de tareas: {total}")
        print(f"   Completadas: {completed}")
        print(f"   Pendientes: {pending}")
        print(f"   Notificaciones: {len(notifications_data)}")
        
        print(f"\n🚀 Siguiente paso:")
        print(f"   1. Inicia sesión con las credenciales de arriba")
        print(f"   2. Usa el token para explorar los endpoints")
        print(f"\n💡 Ejemplo de login:")
        print(f'   curl -X POST "http://localhost:8000/api/auth/login" \\')
        print(f'     -H "Content-Type: application/json" \\')
        print(f'     -d \'{{"email": "dev@quicktask.com", "password": "dev1234"}}\'')
        print("\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔧 INICIALIZADOR DE DATOS DE DESARROLLO - QuickTask")
    print("="*60 + "\n")
    
    init_dev_data()
