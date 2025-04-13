from pydantic import BaseModel


class UserSummary(BaseModel):
    user_id: int