"""
test_tasks.py
-------------
Pruebas CRUD de tareas: crear, leer, actualizar, eliminar y filtrar.
"""

import pytest


# ========== PRUEBAS DE CREACIÓN ==========

@pytest.mark.integration
def test_create_task_success(client, auth_headers, sample_task_data):
    """RF4: Crear una tarea exitosamente"""
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json=sample_task_data
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert "id" in data
    assert data["title"] == sample_task_data["title"]
    assert data["description"] == sample_task_data["description"]
    assert data["status"] == "pending"
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.integration
def test_create_task_without_auth(client, sample_task_data):
    """Verifica que crear tarea requiera autenticación"""
    response = client.post(
        "/api/tasks",
        json=sample_task_data
    )
    
    assert response.status_code == 403


@pytest.mark.integration
def test_create_task_without_title(client, auth_headers):
    """Verifica que el título sea obligatorio"""
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={
            "description": "Tarea sin título"
        }
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.integration
def test_create_task_minimal_data(client, auth_headers):
    """Verifica creación de tarea solo con título (campos opcionales)"""
    response = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Tarea mínima"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["title"] == "Tarea mínima"
    assert data["description"] is None
    assert data["due_date"] is None


# ========== PRUEBAS DE LECTURA ==========

@pytest.mark.integration
def test_list_tasks_empty(client, auth_headers):
    """Verifica que listar tareas sin tareas retorne lista vacía"""
    response = client.get(
        "/api/tasks",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "tasks" in data
    assert "total" in data
    assert "pending" in data
    assert "completed" in data
    assert data["tasks"] == []
    assert data["total"] == 0


@pytest.mark.integration
def test_list_tasks_with_data(client, auth_headers, created_task):
    """RF12: Listar tareas existentes"""
    response = client.get(
        "/api/tasks",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["tasks"]) == 1
    assert data["total"] == 1
    assert data["pending"] == 1
    assert data["completed"] == 0
    
    task = data["tasks"][0]
    assert task["id"] == created_task.id
    assert task["title"] == created_task.title


@pytest.mark.integration
def test_get_task_by_id(client, auth_headers, created_task):
    """Verifica obtención de tarea por ID"""
    response = client.get(
        f"/api/tasks/{created_task.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == created_task.id
    assert data["title"] == created_task.title


@pytest.mark.integration
def test_get_nonexistent_task(client, auth_headers):
    """Verifica que obtener tarea inexistente retorne 404"""
    response = client.get(
        "/api/tasks/99999",
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.integration
def test_list_tasks_without_auth(client, created_task):
    """Verifica que listar tareas requiera autenticación"""
    response = client.get("/api/tasks")
    
    assert response.status_code == 403


# ========== PRUEBAS DE FILTRADO Y BÚSQUEDA ==========

@pytest.mark.integration
def test_filter_tasks_by_status_pending(client, auth_headers, db_session, created_user):
    """RF8: Filtrar tareas por estado (pending)"""
    from app.models import Task
    
    # Crear 2 tareas pendientes y 1 completada
    task1 = Task(user_id=created_user.id, title="Pendiente 1", status="pending")
    task2 = Task(user_id=created_user.id, title="Pendiente 2", status="pending")
    task3 = Task(user_id=created_user.id, title="Completada", status="completed")
    db_session.add_all([task1, task2, task3])
    db_session.commit()
    
    response = client.get(
        "/api/tasks?status=pending",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["tasks"]) == 2
    assert all(task["status"] == "pending" for task in data["tasks"])


@pytest.mark.integration
def test_filter_tasks_by_status_completed(client, auth_headers, db_session, created_user):
    """RF8: Filtrar tareas por estado (completed)"""
    from app.models import Task
    
    task1 = Task(user_id=created_user.id, title="Pendiente", status="pending")
    task2 = Task(user_id=created_user.id, title="Completada", status="completed")
    db_session.add_all([task1, task2])
    db_session.commit()
    
    response = client.get(
        "/api/tasks?status=completed",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["status"] == "completed"


@pytest.mark.integration
def test_search_tasks_by_keyword(client, auth_headers, db_session, created_user):
    """RF13: Buscar tareas por palabra clave"""
    from app.models import Task
    
    task1 = Task(user_id=created_user.id, title="Comprar leche", description="En el supermercado")
    task2 = Task(user_id=created_user.id, title="Estudiar Python", description="FastAPI")
    task3 = Task(user_id=created_user.id, title="Llamar al doctor", description="Revisión médica")
    db_session.add_all([task1, task2, task3])
    db_session.commit()
    
    # Buscar por "Python"
    response = client.get(
        "/api/tasks?search=Python",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["tasks"]) == 1
    assert "Python" in data["tasks"][0]["title"]


@pytest.mark.integration
def test_order_tasks_by_created_at(client, auth_headers, db_session, created_user):
    """RF9: Ordenar tareas por fecha de creación"""
    from app.models import Task
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    task1 = Task(user_id=created_user.id, title="Primera", created_at=now - timedelta(days=2))
    task2 = Task(user_id=created_user.id, title="Segunda", created_at=now - timedelta(days=1))
    task3 = Task(user_id=created_user.id, title="Tercera", created_at=now)
    db_session.add_all([task1, task2, task3])
    db_session.commit()
    
    response = client.get(
        "/api/tasks?order_by=created_at",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["tasks"]) == 3
    # Debe estar ordenado de más reciente a más antiguo
    assert data["tasks"][0]["title"] == "Tercera"
    assert data["tasks"][2]["title"] == "Primera"


# ========== PRUEBAS DE ACTUALIZACIÓN ==========

@pytest.mark.integration
def test_update_task_success(client, auth_headers, created_task):
    """RF5: Actualizar una tarea exitosamente"""
    update_data = {
        "title": "Título actualizado",
        "description": "Descripción actualizada"
    }
    
    response = client.put(
        f"/api/tasks/{created_task.id}",
        headers=auth_headers,
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == created_task.id
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


@pytest.mark.integration
def test_update_task_partial(client, auth_headers, created_task):
    """Verifica actualización parcial (solo un campo)"""
    response = client.put(
        f"/api/tasks/{created_task.id}",
        headers=auth_headers,
        json={"title": "Solo título actualizado"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == "Solo título actualizado"
    # La descripción debe mantenerse
    assert data["description"] == created_task.description


@pytest.mark.integration
def test_update_nonexistent_task(client, auth_headers):
    """Verifica que actualizar tarea inexistente retorne 404"""
    response = client.put(
        "/api/tasks/99999",
        headers=auth_headers,
        json={"title": "No existe"}
    )
    
    assert response.status_code == 404


@pytest.mark.integration
def test_mark_task_completed(client, auth_headers, created_task):
    """RF6: Marcar tarea como completada"""
    response = client.post(
        f"/api/tasks/{created_task.id}/complete",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == created_task.id
    assert data["status"] == "completed"


@pytest.mark.integration
def test_mark_task_pending(client, auth_headers, db_session, created_user):
    """RF6: Revertir tarea a pendiente"""
    from app.models import Task
    
    # Crear tarea completada
    task = Task(user_id=created_user.id, title="Completada", status="completed")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    response = client.post(
        f"/api/tasks/{task.id}/pending",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "pending"


# ========== PRUEBAS DE ELIMINACIÓN ==========

@pytest.mark.integration
def test_delete_task_success(client, auth_headers, created_task):
    """RF7: Eliminar una tarea exitosamente"""
    task_id = created_task.id
    
    response = client.delete(
        f"/api/tasks/{task_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert "eliminada" in response.json()["message"]
    
    # Verificar que ya no existe
    get_response = client.get(
        f"/api/tasks/{task_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404


@pytest.mark.integration
def test_delete_nonexistent_task(client, auth_headers):
    """Verifica que eliminar tarea inexistente retorne 404"""
    response = client.delete(
        "/api/tasks/99999",
        headers=auth_headers
    )
    
    assert response.status_code == 404


# ========== PRUEBAS DE ESTADÍSTICAS ==========

@pytest.mark.integration
def test_task_statistics(client, auth_headers, db_session, created_user):
    """RF14: Vista de progreso con estadísticas"""
    from app.models import Task
    
    # Crear 3 pendientes y 2 completadas
    tasks = [
        Task(user_id=created_user.id, title="P1", status="pending"),
        Task(user_id=created_user.id, title="P2", status="pending"),
        Task(user_id=created_user.id, title="P3", status="pending"),
        Task(user_id=created_user.id, title="C1", status="completed"),
        Task(user_id=created_user.id, title="C2", status="completed"),
    ]
    db_session.add_all(tasks)
    db_session.commit()
    
    response = client.get(
        "/api/tasks",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total"] == 5
    assert data["pending"] == 3
    assert data["completed"] == 2


# ========== PRUEBAS DE AISLAMIENTO DE USUARIOS ==========

@pytest.mark.integration
def test_user_cannot_see_other_users_tasks(client, db_session, sample_user_data):
    """Verifica que usuarios solo vean sus propias tareas (privacidad)"""
    from app.models import User, Task
    from app import auth
    
    # Crear usuario 1 con tarea
    user1_data = {"email": "user1@test.com", "password": "Pass1234!"}
    user1 = User(email=user1_data["email"], password_hash=auth.hash_password(user1_data["password"]))
    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)
    
    task1 = Task(user_id=user1.id, title="Tarea de usuario 1")
    db_session.add(task1)
    db_session.commit()
    
    # Crear usuario 2 con tarea
    user2_data = {"email": "user2@test.com", "password": "Pass1234!"}
    user2 = User(email=user2_data["email"], password_hash=auth.hash_password(user2_data["password"]))
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)
    
    task2 = Task(user_id=user2.id, title="Tarea de usuario 2")
    db_session.add(task2)
    db_session.commit()
    
    # Login como usuario 1
    login_response = client.post("/api/auth/login", json=user1_data)
    token1 = login_response.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    
    # Usuario 1 solo debe ver su tarea
    response = client.get("/api/tasks", headers=headers1)
    data = response.json()
    
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Tarea de usuario 1"
