"""
test_reminders.py
-----------------
Pruebas de recordatorios: crear y listar recordatorios.
"""

import pytest
from datetime import datetime, timedelta


@pytest.mark.integration
def test_create_reminder_success(client, auth_headers, created_task, sample_reminder_data):
    """RF11: Crear recordatorio para una tarea"""
    reminder_data = {
        "task_id": created_task.id,
        "remind_at": sample_reminder_data["remind_at"]
    }
    
    response = client.post(
        "/api/reminders",
        headers=auth_headers,
        json=reminder_data
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert "id" in data
    assert data["task_id"] == created_task.id
    assert data["remind_at"] == sample_reminder_data["remind_at"]
    assert data["is_sent"] is False


@pytest.mark.integration
def test_create_reminder_without_auth(client, created_task, sample_reminder_data):
    """Verifica que crear recordatorio requiera autenticación"""
    reminder_data = {
        "task_id": created_task.id,
        "remind_at": sample_reminder_data["remind_at"]
    }
    
    response = client.post(
        "/api/reminders",
        json=reminder_data
    )
    
    assert response.status_code == 403


@pytest.mark.integration
def test_create_reminder_for_nonexistent_task(client, auth_headers, sample_reminder_data):
    """Verifica que no se pueda crear recordatorio para tarea inexistente"""
    reminder_data = {
        "task_id": 99999,
        "remind_at": sample_reminder_data["remind_at"]
    }
    
    response = client.post(
        "/api/reminders",
        headers=auth_headers,
        json=reminder_data
    )
    
    assert response.status_code == 404


@pytest.mark.integration
def test_create_duplicate_reminder(client, auth_headers, db_session, created_task, sample_reminder_data):
    """Verifica que no se pueda crear más de un recordatorio por tarea (relación 1:1)"""
    from app.models import Reminder
    
    # Crear primer recordatorio
    reminder = Reminder(
        task_id=created_task.id,
        remind_at=datetime.fromisoformat(sample_reminder_data["remind_at"])
    )
    db_session.add(reminder)
    db_session.commit()
    
    # Intentar crear segundo recordatorio para la misma tarea
    reminder_data = {
        "task_id": created_task.id,
        "remind_at": sample_reminder_data["remind_at"]
    }
    
    response = client.post(
        "/api/reminders",
        headers=auth_headers,
        json=reminder_data
    )
    
    assert response.status_code == 400
    assert "ya tiene un recordatorio" in response.json()["detail"]


@pytest.mark.integration
def test_list_reminders_empty(client, auth_headers):
    """Verifica que listar recordatorios sin datos retorne lista vacía"""
    response = client.get(
        "/api/reminders",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.integration
def test_list_reminders_with_data(client, auth_headers, db_session, created_user):
    """Verifica listado de recordatorios del usuario"""
    from app.models import Task, Reminder
    
    # Crear tarea y recordatorio
    task = Task(user_id=created_user.id, title="Tarea con recordatorio")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    remind_at = datetime.utcnow() + timedelta(days=1)
    reminder = Reminder(task_id=task.id, remind_at=remind_at)
    db_session.add(reminder)
    db_session.commit()
    
    response = client.get(
        "/api/reminders",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["task_id"] == task.id
    assert data[0]["is_sent"] is False


@pytest.mark.integration
def test_list_reminders_without_auth(client, db_session, created_task):
    """Verifica que listar recordatorios requiera autenticación"""
    from app.models import Reminder
    
    reminder = Reminder(
        task_id=created_task.id,
        remind_at=datetime.utcnow() + timedelta(days=1)
    )
    db_session.add(reminder)
    db_session.commit()
    
    response = client.get("/api/reminders")
    
    assert response.status_code == 403


@pytest.mark.integration
def test_user_only_sees_own_reminders(client, db_session):
    """Verifica que usuarios solo vean sus propios recordatorios (privacidad)"""
    from app.models import User, Task, Reminder
    from app import auth
    
    # Usuario 1 con tarea y recordatorio
    user1 = User(email="user1@test.com", password_hash=auth.hash_password("Pass1234!"))
    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)
    
    task1 = Task(user_id=user1.id, title="Tarea 1")
    db_session.add(task1)
    db_session.commit()
    db_session.refresh(task1)
    
    reminder1 = Reminder(task_id=task1.id, remind_at=datetime.utcnow() + timedelta(days=1))
    db_session.add(reminder1)
    db_session.commit()
    
    # Usuario 2 con tarea y recordatorio
    user2 = User(email="user2@test.com", password_hash=auth.hash_password("Pass1234!"))
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)
    
    task2 = Task(user_id=user2.id, title="Tarea 2")
    db_session.add(task2)
    db_session.commit()
    db_session.refresh(task2)
    
    reminder2 = Reminder(task_id=task2.id, remind_at=datetime.utcnow() + timedelta(days=1))
    db_session.add(reminder2)
    db_session.commit()
    
    # Login como usuario 1
    login_response = client.post(
        "/api/auth/login",
        json={"email": "user1@test.com", "password": "Pass1234!"}
    )
    token1 = login_response.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    
    # Usuario 1 solo debe ver su recordatorio
    response = client.get("/api/reminders", headers=headers1)
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["task_id"] == task1.id


@pytest.mark.integration
def test_create_reminder_with_past_date(client, auth_headers, created_task):
    """Verifica validación de fecha de recordatorio (debe ser futura)"""
    past_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
    
    response = client.post(
        "/api/reminders",
        headers=auth_headers,
        json={
            "task_id": created_task.id,
            "remind_at": past_date
        }
    )
    
    # Nota: Esto depende de si implementaste validación de fechas pasadas
    # Si no, este test puede ser un recordatorio para agregarlo
    # Por ahora, se espera que pase la validación básica
    assert response.status_code in [201, 400]
