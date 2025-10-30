"""
conftest.py
-----------
Fixtures compartidas para todas las pruebas.
Define base de datos en memoria, cliente de pruebas y datos de ejemplo.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User, Task, Reminder
from app import auth

# ========== CONFIGURACIÓN DE BASE DE DATOS DE PRUEBA ==========

# Base de datos en memoria (se destruye después de cada prueba)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dependencia get_db para usar la BD de prueba"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override de dependencia en la app
app.dependency_overrides[get_db] = override_get_db


# ========== FIXTURES ==========

@pytest.fixture(scope="function")
def db_session():
    """
    Crea una sesión de base de datos de prueba.
    Se destruye después de cada test.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente HTTP de prueba para hacer requests a la API.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user_data():
    """Datos de usuario de ejemplo"""
    return {
        "email": "test@quicktask.com",
        "password": "TestPassword123!"
    }


@pytest.fixture
def sample_task_data():
    """Datos de tarea de ejemplo"""
    return {
        "title": "Tarea de prueba",
        "description": "Esta es una tarea de prueba",
        "due_date": "2025-12-31T23:59:59"
    }


@pytest.fixture
def sample_reminder_data():
    """Datos de recordatorio de ejemplo"""
    return {
        "remind_at": "2025-12-30T09:00:00"
    }


@pytest.fixture
def created_user(db_session, sample_user_data):
    """
    Crea un usuario en la base de datos de prueba.
    Retorna el objeto User.
    """
    password_hash = auth.hash_password(sample_user_data["password"])
    user = User(
        email=sample_user_data["email"],
        password_hash=password_hash
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(client, sample_user_data, created_user):
    """
    Autentica al usuario y retorna el token JWT.
    """
    response = client.post(
        "/api/auth/login",
        json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """
    Retorna los headers con el token de autenticación.
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def created_task(db_session, created_user, sample_task_data):
    """
    Crea una tarea en la base de datos de prueba.
    Retorna el objeto Task.
    """
    task = Task(
        user_id=created_user.id,
        title=sample_task_data["title"],
        description=sample_task_data["description"],
        status="pending"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task
