import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class WorkerSkill(Base):
    __tablename__ = "worker_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_id = Column(UUID(as_uuid=True), ForeignKey("workers.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    experience_level = Column(String(50))  # beginner, intermediate, expert

    # Relationships
    worker = relationship("Worker", back_populates="skills")
