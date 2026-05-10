from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.jwt import verify_token

# Simple JWT Bearer authentication
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_active_user)):
        print(f"User role: '{current_user.role}', status: '{current_user.status}', Allowed roles: {allowed_roles}")
        # Check user status first
        if current_user.status not in allowed_roles:
            print(f"Role check failed: '{current_user.status}' not in {allowed_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        print(f"Role check passed: '{current_user.status}' in {allowed_roles}")
        return current_user
    return role_checker


def allow_pending_users():
    """Allow users with pending status"""
    def pending_checker(current_user: User = Depends(get_current_active_user)):
        print(f"User status: '{current_user.status}'")
        if current_user.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not pending registration"
            )
        print(f"Pending user check passed")
        return current_user
    return pending_checker
