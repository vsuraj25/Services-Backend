import uuid
from typing import Optional
from pydantic import BaseModel


class WorkerSkillBase(BaseModel):
    skill_name: str
    experience_level: Optional[str] = None


class WorkerSkillCreate(WorkerSkillBase):
    pass


class WorkerSkillResponse(BaseModel):
    id: uuid.UUID
    skill_name: str
    experience_level: Optional[str]

    class Config:
        from_attributes = True


class SkillListResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[list[WorkerSkillResponse]] = None
