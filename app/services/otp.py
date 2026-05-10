import random
import string
from datetime import datetime, timedelta
from typing import Dict

# Simple in-memory OTP storage (for production, use Redis or database)
otp_storage: Dict[str, Dict] = {}


def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def store_otp(phone: str, otp: str, expiry_minutes: int = 5):
    """Store OTP with expiry time"""
    expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)
    otp_storage[phone] = {
        "otp": otp,
        "expiry": expiry_time,
        "attempts": 0
    }
    print(f"OTP for {phone}: {otp}")  # For testing purposes


def verify_otp(phone: str, otp: str) -> bool:
    """Verify OTP"""
    if phone not in otp_storage:
        return False
    
    stored_data = otp_storage[phone]
    
    # Check expiry
    if datetime.now() > stored_data["expiry"]:
        del otp_storage[phone]
        return False
    
    # Check attempts (max 3 attempts)
    if stored_data["attempts"] >= 3:
        del otp_storage[phone]
        return False
    
    # Verify OTP
    if stored_data["otp"] == otp:
        del otp_storage[phone]
        return True
    else:
        stored_data["attempts"] += 1
        return False


def cleanup_expired_otps():
    """Clean up expired OTPs"""
    current_time = datetime.now()
    expired_phones = [
        phone for phone, data in otp_storage.items()
        if current_time > data["expiry"]
    ]
    for phone in expired_phones:
        del otp_storage[phone]
