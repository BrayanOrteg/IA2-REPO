"""
test_auth.py
------------
Pruebas de autenticación: registro, login y obtención de usuario actual.
"""

import pytest
from app import auth


# ========== PRUEBAS UNITARIAS ==========

@pytest.mark.unit
def test_hash_password():
    """Verifica que las contraseñas se hasheen correctamente"""
    password = "MySecurePassword123!"
    hashed = auth.hash_password(password)
    
    # El hash no debe ser igual a la contraseña original
    assert hashed != password
    
    # El hash debe verificarse correctamente
    assert auth.verify_password(password, hashed) is True
    
    # Una contraseña incorrecta no debe verificarse
    assert auth.verify_password("WrongPassword", hashed) is False


@pytest.mark.unit
def test_create_and_decode_token():
    """Verifica creación y decodificación de tokens JWT"""
    user_id = 1
    token = auth.create_access_token(data={"sub": str(user_id)})
    
    # El token debe ser una cadena no vacía
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decodificar el token debe retornar el user_id correcto
    payload = auth.decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == str(user_id)


@pytest.mark.unit
def test_decode_invalid_token():
    """Verifica que tokens inválidos retornen None"""
    invalid_token = "invalid.token.here"
    payload = auth.decode_access_token(invalid_token)
    assert payload is None


# ========== PRUEBAS DE INTEGRACIÓN ==========

@pytest.mark.integration
def test_register_user_success(client, sample_user_data):
    """RF1: Registrar un usuario exitosamente"""
    response = client.post(
        "/api/auth/register",
        json=sample_user_data
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert "id" in data
    assert data["email"] == sample_user_data["email"]
    assert "password" not in data  # No debe exponer la contraseña
    assert "password_hash" not in data
    assert "created_at" in data


@pytest.mark.integration
def test_register_duplicate_email(client, sample_user_data, created_user):
    """Verifica que no se puedan registrar emails duplicados"""
    response = client.post(
        "/api/auth/register",
        json=sample_user_data
    )
    
    assert response.status_code == 400
    assert "ya está registrado" in response.json()["detail"]


@pytest.mark.integration
def test_register_invalid_email(client):
    """Verifica validación de formato de email"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "invalid-email",
            "password": "Password123!"
        }
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.integration
def test_login_success(client, sample_user_data, created_user):
    """RF2: Login exitoso retorna token JWT"""
    response = client.post(
        "/api/auth/login",
        json=sample_user_data
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


@pytest.mark.integration
def test_login_wrong_password(client, sample_user_data, created_user):
    """Verifica que login falle con contraseña incorrecta"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": sample_user_data["email"],
            "password": "WrongPassword123!"
        }
    )
    
    assert response.status_code == 401
    assert "incorrectos" in response.json()["detail"]


@pytest.mark.integration
def test_login_nonexistent_user(client):
    """Verifica que login falle con usuario inexistente"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "Password123!"
        }
    )
    
    assert response.status_code == 401


@pytest.mark.integration
def test_get_current_user(client, auth_headers, created_user, sample_user_data):
    """Verifica obtención de información del usuario autenticado"""
    response = client.get(
        "/api/auth/me",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == created_user.id
    assert data["email"] == sample_user_data["email"]
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.integration
def test_get_current_user_without_token(client):
    """Verifica que endpoints protegidos requieran autenticación"""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 403  # Forbidden (sin Authorization header)


@pytest.mark.integration
def test_get_current_user_invalid_token(client):
    """Verifica que tokens inválidos sean rechazados"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    assert response.status_code == 401
    assert "No se pudo validar las credenciales" in response.json()["detail"]
