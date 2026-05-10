from sqlalchemy.orm import Session
from app.models.user import User, Customer, Worker
from app.models.skill import WorkerSkill
from app.schemas.customer import CustomerUpdate
from app.schemas.worker import WorkerUpdate, WorkerStatusUpdate
from app.schemas.skill import WorkerSkillCreate
from datetime import datetime


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_profile(self, user: User):
        """Get user profile based on role"""
        if user.role == "customer":
            customer = self.db.query(Customer).filter(Customer.id == user.id).first()
            if not customer:
                # Create customer profile if it doesn't exist
                customer = Customer(id=user.id)
                self.db.add(customer)
                self.db.commit()
                self.db.refresh(customer)
            
            return {
                "user": {
                    "id": str(user.id),
                    "phone": user.phone,
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                },
                "profile": {
                    "id": str(customer.id),
                    "name": customer.name,
                    "email": customer.email,
                    "default_address": customer.default_address,
                    "lat": customer.lat,
                    "lng": customer.lng
                }
            }
        elif user.role == "worker":
            worker = self.db.query(Worker).filter(Worker.id == user.id).first()
            if not worker:
                # Create worker profile if it doesn't exist
                worker = Worker(id=user.id)
                self.db.add(worker)
                self.db.commit()
                self.db.refresh(worker)
                
            skills = self.db.query(WorkerSkill).filter(WorkerSkill.worker_id == user.id).all()
            skills_data = []
            for skill in skills:
                skills_data.append({
                    "id": str(skill.id),
                    "skill_id": skill.skill_id,
                    "worker_id": str(skill.worker_id)
                })
            
            return {
                "user": {
                    "id": str(user.id),
                    "phone": user.phone,
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                },
                "profile": {
                    "id": str(worker.id),
                    "name": worker.name,
                    "bio": worker.bio,
                    "experience_years": worker.experience_years,
                    "is_verified": worker.is_verified,
                    "rating": worker.rating,
                    "total_jobs": worker.total_jobs,
                    "is_online": worker.is_online,
                    "current_lat": worker.current_lat,
                    "current_lng": worker.current_lng,
                    "last_active": worker.last_active
                },
                "skills": skills_data
            }
        # Default fallback for unknown roles
        return {
            "user": {
                "id": str(user.id),
                "phone": user.phone,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            },
            "profile": None,
            "skills": []
        }

    def update_customer_profile(self, user: User, profile_data: CustomerUpdate):
        """Update customer profile"""
        customer = self.db.query(Customer).filter(Customer.id == user.id).first()
        if not customer:
            return None
        
        update_data = profile_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update_worker_profile(self, user: User, profile_data: WorkerUpdate):
        """Update worker profile"""
        worker = self.db.query(Worker).filter(Worker.id == user.id).first()
        if not worker:
            return None
        
        update_data = profile_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(worker, field, value)
        
        self.db.commit()
        self.db.refresh(worker)
        return worker

    def update_worker_status(self, user: User, status_data: WorkerStatusUpdate):
        """Update worker online status and location"""
        worker = self.db.query(Worker).filter(Worker.id == user.id).first()
        if not worker:
            return None
        
        worker.is_online = status_data.is_online
        if status_data.current_lat is not None:
            worker.current_lat = status_data.current_lat
        if status_data.current_lng is not None:
            worker.current_lng = status_data.current_lng
        
        if status_data.is_online:
            worker.last_active = datetime.now()
        
        self.db.commit()
        self.db.refresh(worker)
        return worker

    def add_worker_skill(self, user: User, skill_data: WorkerSkillCreate):
        """Add skill to worker profile"""
        worker = self.db.query(Worker).filter(Worker.id == user.id).first()
        if not worker:
            return None
        
        skill = WorkerSkill(
            worker_id=user.id,
            skill_name=skill_data.skill_name,
            experience_level=skill_data.experience_level
        )
        
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def get_worker_skills(self, user: User):
        """Get all skills for a worker"""
        return self.db.query(WorkerSkill).filter(WorkerSkill.worker_id == user.id).all()
