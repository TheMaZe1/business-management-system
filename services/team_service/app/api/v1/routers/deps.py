from fastapi import Depends, HTTPException, status
import jwt

from app.config import settings
from app.utils.jwt import oauth2_scheme
from app.services.membership import MembershipService


async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError as e:
        print("test", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = user_id
    return user_id

# Функция проверки роли пользователя в команде
async def get_membership(team_id: int, user_id: int, membership_service: MembershipService):
    membership = await membership_service.get_member_by_team_and_user(team_id, user_id)
    
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this team")

    return membership