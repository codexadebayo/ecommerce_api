from typing import Optional
from pydantic import BaseModel,  Field
from datetime import datetime
from decimal import Decimal


class ShippingMethodBase(BaseModel):
    """
    Base schema for shipping methods.
    """
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    cost: Decimal = Field(..., ge=0)
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime]



class ShippingMethodCreate(BaseModel):
    """
    Schema for creating a new shipping method.
    """
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    cost: Decimal = Field(..., ge=0)
    is_active: bool = True



class ShippingMethodRead(ShippingMethodBase):
    """
    Schema for reading shipping method information.
    """
    id: int

    class Config:
        orm_mode = True



class ShippingMethodUpdate(BaseModel):
    """
    Schema for updating shipping method information. All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    cost: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
