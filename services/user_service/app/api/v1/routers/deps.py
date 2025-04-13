from fastapi import Depends, HTTPException, status
import jwt

from app.services.user import UserService
from app.config import settings
from app.utils.jwt import oauth2_scheme


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(UserService)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError as e:
        print("test", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user