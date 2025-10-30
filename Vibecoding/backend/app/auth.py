"""
auth.py
-------
Servicio de autenticación y autorización.
Implementa AuthService del diagrama de clases.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

# Configuración de seguridad
SECRET_KEY = "quicktask-secret-key-change-in-production-2025"  # En producción usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Context para hashear contraseñas (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme para Bearer token
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt (RNF5: Seguridad)"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token con los datos proporcionados.
    Implementa AuthService.generateToken() del diagrama.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica y valida un JWT token"""
    try:
        print(f"🔑 DEBUG decode: Intentando decodificar token de {len(token)} caracteres")
        print(f"🔑 DEBUG decode: SECRET_KEY = {SECRET_KEY[:20]}...")
        print(f"🔑 DEBUG decode: ALGORITHM = {ALGORITHM}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ DEBUG decode: Token decodificado exitosamente: {payload}")
        return payload
    except JWTError as e:
        print(f"❌ DEBUG decode: Error JWTError: {type(e).__name__}: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ DEBUG decode: Error inesperado: {type(e).__name__}: {str(e)}")
        return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Autentica un usuario verificando email y password.
    Implementa AuthService.login() del diagrama.
    """
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency para obtener el usuario autenticado desde el token JWT.
    Se usa en endpoints protegidos.
    
    Valida el token JWT y retorna el usuario correspondiente.
    Lanza HTTPException 401 si el token es inválido o el usuario no existe.
    """
    token = credentials.credentials
    print(f"🔍 DEBUG: Token recibido: {token[:50]}...")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificar token
    payload = decode_access_token(token)
    print(f"🔍 DEBUG: Payload decodificado: {payload}")
    
    if payload is None:
        print("❌ DEBUG: Payload es None - Token inválido o expirado")
        raise credentials_exception
    
    # Extraer user_id del payload
    user_id = payload.get("sub")
    print(f"🔍 DEBUG: user_id extraído: {user_id} (tipo: {type(user_id).__name__})")
    
    if user_id is None:
        print("❌ DEBUG: user_id es None en el payload")
        raise credentials_exception
    
    # Asegurar que user_id sea int (por si viene como string del JWT)
    try:
        user_id = int(user_id)
        print(f"✅ DEBUG: user_id convertido a int: {user_id}")
    except (ValueError, TypeError) as e:
        print(f"❌ DEBUG: Error al convertir user_id a int: {e}")
        raise credentials_exception
    
    # Buscar usuario en la base de datos
    user = db.query(User).filter(User.id == user_id).first()
    print(f"🔍 DEBUG: Usuario encontrado en BD: {user.email if user else 'None'}")
    
    if user is None:
        print(f"❌ DEBUG: Usuario con id={user_id} no existe en la base de datos")
        raise credentials_exception
    
    print(f"✅ DEBUG: Autenticación exitosa para {user.email}")
    return user
