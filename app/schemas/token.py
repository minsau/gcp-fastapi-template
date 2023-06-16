from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserBase


class Token(BaseModel):
    access_token: str
    user: UserBase


class TokenPayload(BaseModel):
    sub: Optional[int] = None
