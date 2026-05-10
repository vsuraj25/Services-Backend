import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Float, Integer, Double, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=True)  # customer, worker, admin (set during registration)
    status = Column(String(20), nullable=False, default="pending")  # pending, customer, worker, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="user", uselist=False)
    worker = relationship("Worker", back_populates="user", uselist=False)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    default_address = Column(Text)
    lat = Column(Double)
    lng = Column(Double)

    # Relationships
    user = relationship("User", back_populates="customer")


class Worker(Base):
    __tablename__ = "workers"

    id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    name = Column(String(100))
    bio = Column(Text)
    experience_years = Column(Integer)
    is_verified = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    total_jobs = Column(Integer, default=0)
    is_online = Column(Boolean, default=False)
    current_lat = Column(Double)
    current_lng = Column(Double)
    last_active = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="worker")
    skills = relationship("WorkerSkill", back_populates="worker", cascade="all, delete-orphan")
