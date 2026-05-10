from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer import CustomerUpdate, CustomerProfileResponse
from app.services.user import UserService
from app.utils.security import get_current_active_user, require_role
from app.models.user import User

router = APIRouter(prefix="/customer", tags=["customer"])
security = HTTPBearer()


@router.get("/profile", response_model=CustomerProfileResponse)
async def get_customer_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_role(["customer"])),
    db: Session = Depends(get_db)
):
    """Get customer profile"""
    try:
        user_service = UserService(db)
        profile_data = user_service.get_user_profile(current_user)
        
        return CustomerProfileResponse(
            success=True,
            message="Customer profile retrieved successfully",
            data=profile_data["profile"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/profile", response_model=CustomerProfileResponse)
async def update_customer_profile(
    profile_data: CustomerUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_role(["customer"])),
    db: Session = Depends(get_db)
):
    """Update customer profile"""
    try:
        user_service = UserService(db)
        updated_profile = user_service.update_customer_profile(current_user, profile_data)
        
        if updated_profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer profile not found"
            )
        
        return CustomerProfileResponse(
            success=True,
            message="Customer profile updated successfully",
            data=updated_profile
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
