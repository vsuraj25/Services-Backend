from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import SendOTPRequest, VerifyOTPRequest, OTPResponse, TokenResponse, UserResponse, RegistrationResponse, CustomerRegistrationRequest, WorkerRegistrationRequest
from app.services.auth import AuthService
from app.services.user import UserService
from app.utils.security import get_current_active_user, allow_pending_users
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/send-otp", response_model=OTPResponse)
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP to phone number"""
    try:
        auth_service = AuthService(db)
        otp = auth_service.send_otp(request.phone)
        
        return OTPResponse(
            success=True,
            message="OTP sent successfully",
            otp=otp  # For testing purposes
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP and get access token"""
    try:
        auth_service = AuthService(db)
        result, message = auth_service.verify_otp_and_login(
            phone=request.phone,
            otp=request.otp
        )
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return TokenResponse(
            success=True,
            message=message,
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    """Get current user information"""
    try:
        # Debug: Log current user info
        print(f"Current user: {current_user.id}, role: {current_user.role}")
        
        user_service = UserService(db)
        profile_data = user_service.get_user_profile(current_user)
        
        # Debug: Check if profile_data is None
        if profile_data is None:
            print("Profile data is None!")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        print(f"Profile data: {profile_data}")
        
        return UserResponse(
            success=True,
            message="User profile retrieved successfully",
            data=profile_data
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_current_user_info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/register-customer", response_model=RegistrationResponse)
async def register_customer(
    profile_data: CustomerRegistrationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(allow_pending_users()),
    db: Session = Depends(get_db)
):
    """Complete customer registration"""
    try:
        auth_service = AuthService(db)
        user, message = auth_service.register_customer(current_user, profile_data)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return RegistrationResponse(
            success=True,
            message=message,
            data={
                "id": str(user.id),
                "phone": user.phone,
                "role": user.role,
                "status": user.status
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/register-worker", response_model=RegistrationResponse)
async def register_worker(
    profile_data: WorkerRegistrationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(allow_pending_users()),
    db: Session = Depends(get_db)
):
    """Complete worker registration"""
    try:
        auth_service = AuthService(db)
        user, message = auth_service.register_worker(current_user, profile_data)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        return RegistrationResponse(
            success=True,
            message=message,
            data={
                "id": str(user.id),
                "phone": user.phone,
                "role": user.role,
                "status": user.status
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
