import uuid
from typing import Optional
from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    default_address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    default_address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class CustomerResponse(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    email: Optional[str]
    default_address: Optional[str]
    lat: Optional[float]
    lng: Optional[float]

    class Config:
        from_attributes = True


class CustomerProfileResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[CustomerResponse] = None
