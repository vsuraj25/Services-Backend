from pydantic import BaseModel
from typing import Optional


class SendOTPRequest(BaseModel):
    phone: str


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str
    # role removed - will be set during registration


class OTPResponse(BaseModel):
    success: bool
    message: str
    otp: Optional[str] = None  # For testing purposes


class TokenResponse(BaseModel):
    success: bool
    message: str
    data: dict


class UserResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class CustomerRegistrationRequest(BaseModel):
    name: str
    email: Optional[str] = None
    default_address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class WorkerRegistrationRequest(BaseModel):
    name: str
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None


class RegistrationResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
