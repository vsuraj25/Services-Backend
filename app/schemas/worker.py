import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class WorkerBase(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None


class WorkerResponse(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    bio: Optional[str]
    experience_years: Optional[int]
    is_verified: bool
    rating: float
    total_jobs: int
    is_online: bool
    current_lat: Optional[float]
    current_lng: Optional[float]
    last_active: Optional[datetime]

    class Config:
        from_attributes = True


class WorkerProfileResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[WorkerResponse] = None


class WorkerStatusUpdate(BaseModel):
    is_online: bool
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
