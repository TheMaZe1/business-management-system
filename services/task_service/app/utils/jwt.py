import jwt
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.schemas.jwt import TokenData

# Путь, по которому пользователи будут отправлять свои учетные данные для получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)

def verify_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenData(**payload)
    except jwt.PyJWTError:
        return None
