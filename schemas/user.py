from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """Base user schema with common attributes"""
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    """Schema for reading user data"""
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for updating user data"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None