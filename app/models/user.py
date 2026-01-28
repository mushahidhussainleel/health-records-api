from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

# -------------------------------
# 1. Signup Model
# -------------------------------
class SignupModel(BaseModel):
    """
    Model for user signup data validation.
    """
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=1, le=120)  # Age must be between 1 and 120
    country: str = Field(..., min_length=2)
    password: str = Field(..., min_length=8)
    purpose: Optional[str] = Field(None, max_length=200)  # Optional purpose of signup

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """
        Ensure the password meets the minimum length requirement.
        """
        if len(v) < 8:
            raise ValueError('Password length must be at least 8 characters')
        return v


# -------------------------------
# 2. Login Model
# -------------------------------
class LoginModel(BaseModel):
    """
    Model for user login data validation.
    """
    email: EmailStr
    password: str


# -------------------------------
# 3. User Response Model
# -------------------------------
class UserResponseModel(BaseModel):
    """
    Model to structure the user data returned in responses.
    """
    user_id: int
    name: str
    email: EmailStr
    message: str
