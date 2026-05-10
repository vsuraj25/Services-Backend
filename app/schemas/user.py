import uuid
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    phone: str
    role: str


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: uuid.UUID
    phone: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
