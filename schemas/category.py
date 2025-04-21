from typing import Optional
from pydantic import BaseModel,  Field
from datetime import datetime


class CategoryBase(BaseModel):
    """
    Base Pydantic schema for categories.
    """
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime]


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category.
    """
    # id is not needed for creating
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: bool = True



class CategoryUpdate(BaseModel):
    """
    Schema for updating an existing category.  All fields are optional for partial updates.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class CategoryRead(CategoryBase):
    """
    Schema for reading category information.
    """
    id: int

    class Config:
        orm_mode = True
