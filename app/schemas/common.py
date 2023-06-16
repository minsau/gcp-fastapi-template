from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = None
