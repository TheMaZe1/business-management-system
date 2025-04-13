import jwt
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta

from app.config import settings
from app.schemas.jwt import TokenData

# Путь, по которому пользователи будут отправлять свои учетные данные для получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# Генерация JWT токена
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Верификация токена
def verify_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenData(**payload)
    except jwt.PyJWTError:
        return None
