from datetime import datetime

from pydantic import BaseModel


class InviteCodeResponse(BaseModel):
    code: str
    expires_at: datetime | None

    class Config:
        from_attributes = True