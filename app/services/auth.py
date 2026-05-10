from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User, Customer, Worker
from app.schemas.user import UserCreate
from app.utils.jwt import create_access_token
from app.services.otp import generate_otp, store_otp, verify_otp


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def send_otp(self, phone: str) -> str:
        """Generate and store OTP for phone number"""
        otp = generate_otp()
        store_otp(phone, otp)
        return otp

    def verify_otp_and_login(self, phone: str, otp: str):
        """Verify OTP and create/login user (no role required)"""
        if not verify_otp(phone, otp):
            return None, "Invalid OTP"
        
        # Check if user exists
        user = self.db.query(User).filter(User.phone == phone).first()
        
        if user is None:
            # Create new user with pending status
            user = User(
                phone=phone,
                role=None,  # Will be set during registration
                status="pending"
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            message = "User verified successfully. Please complete registration."
        else:
            # Check if user is already registered
            print(f"Existing user found: phone={user.phone}, status={user.status}, status_type={type(user.status)}")
            
            # Handle existing users with old schema or invalid status
            if not user.status or user.status in ["customer", "worker", "admin"]:
                # User is already registered with a role
                return None, f"User already registered as {user.status}"
            elif user.status != "pending":
                # User has invalid status, reset to pending for re-registration
                user.status = "pending"
                user.role = None
                self.db.commit()
                print(f"Reset user {user.phone} to pending status for re-registration")
            
            message = "User verified successfully. Please complete registration."
        
        # Generate JWT token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "phone": user.phone,
                "role": user.role,
                "status": user.status
            }
        }, message

    def register_customer(self, user: User, profile_data):
        """Complete customer registration"""
        if user.status != "pending":
            return None, "User cannot be registered"
        
        # Update user role and status
        user.role = "customer"
        user.status = "customer"
        
        # Create customer profile with details
        customer = Customer(
            id=user.id,
            name=profile_data.name,
            email=profile_data.email,
            default_address=profile_data.default_address,
            lat=profile_data.lat,
            lng=profile_data.lng
        )
        self.db.add(customer)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user, "Customer registration completed"

    def register_worker(self, user: User, profile_data):
        """Complete worker registration"""
        if user.status != "pending":
            return None, "User cannot be registered"
        
        # Update user role and status
        user.role = "worker"
        user.status = "worker"
        
        # Create worker profile with details
        worker = Worker(
            id=user.id,
            name=profile_data.name,
            bio=profile_data.bio,
            experience_years=profile_data.experience_years,
            current_lat=profile_data.current_lat,
            current_lng=profile_data.current_lng,
            last_active=datetime.utcnow()
        )
        self.db.add(worker)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user, "Worker registration completed"
