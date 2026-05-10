from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.worker import WorkerUpdate, WorkerProfileResponse, WorkerStatusUpdate
from app.schemas.skill import WorkerSkillCreate, SkillListResponse
from app.services.user import UserService
from app.utils.security import get_current_active_user, require_role
from app.models.user import User

router = APIRouter(prefix="/worker", tags=["worker"])
security = HTTPBearer()


@router.get("/profile", response_model=WorkerProfileResponse)
async def get_worker_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Get worker profile"""
    try:
        user_service = UserService(db)
        profile_data = user_service.get_user_profile(current_user)
        
        return WorkerProfileResponse(
            success=True,
            message="Worker profile retrieved successfully",
            data=profile_data["profile"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/profile", response_model=WorkerProfileResponse)
async def update_worker_profile(
    profile_data: WorkerUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Update worker profile"""
    try:
        user_service = UserService(db)
        updated_profile = user_service.update_worker_profile(current_user, profile_data)
        
        if updated_profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found"
            )
        
        return WorkerProfileResponse(
            success=True,
            message="Worker profile updated successfully",
            data=updated_profile
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/status", response_model=WorkerProfileResponse)
async def update_worker_status(
    status_data: WorkerStatusUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Update worker online status and location"""
    try:
        user_service = UserService(db)
        updated_worker = user_service.update_worker_status(current_user, status_data)
        
        if updated_worker is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found"
            )
        
        return WorkerProfileResponse(
            success=True,
            message="Worker status updated successfully",
            data=updated_worker
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/skills", response_model=SkillListResponse)
async def add_worker_skill(
    skill_data: WorkerSkillCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Add skill to worker profile"""
    try:
        user_service = UserService(db)
        new_skill = user_service.add_worker_skill(current_user, skill_data)
        
        if new_skill is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker profile not found"
            )
        
        return SkillListResponse(
            success=True,
            message="Skill added successfully",
            data=[new_skill]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/skills", response_model=SkillListResponse)
async def get_worker_skills(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    """Get all worker skills"""
    try:
        user_service = UserService(db)
        skills = user_service.get_worker_skills(current_user)
        
        return SkillListResponse(
            success=True,
            message="Skills retrieved successfully",
            data=skills
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
