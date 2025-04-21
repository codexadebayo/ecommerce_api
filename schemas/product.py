from typing import Optional, List
from pydantic import BaseModel,  Field
from pydantic import conint,  Decimal
from datetime import datetime


class ProductBase(BaseModel):
    """
    Base Pydantic schema with common product attributes.
    """
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    price: Decimal = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime]



class ProductCreate(ProductBase):
    """
    Schema for creating a new product.
    """
    #  The id is not required for creating a new product
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    price: Decimal = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)
    is_active: bool = True



class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductRead(ProductBase):
    """
    Schema for reading product information.
    """
    pass

    class Config:
        orm_mode = True
