from fastapi import Depends, HTTPException, Request, status
import httpx
import jwt

from app.config import settings
from app.utils.jwt import oauth2_scheme
from app.schemas.membership import MembershipResponse


MEMBERSHIP_SERVICE_URL = "http://127.0.0.1:8002/teams"

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
async def get_membership(team_id: int, user_id: int, request: Request) -> MembershipResponse:
    token = request.headers.get("Authorization")
    
    headers = {"Authorization": token} if token else {}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEMBERSHIP_SERVICE_URL}/{team_id}/members/{user_id}", headers=headers)
    
    if response.status_code == 200:
        return MembershipResponse(**response.json())
    elif response.status_code == 404:
        raise HTTPException(status_code=403, detail="User is not a team member")
    else:
        raise HTTPException(status_code=500, detail="Failed to contact membership service")