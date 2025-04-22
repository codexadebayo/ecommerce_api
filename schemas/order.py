from typing import List, Optional
from pydantic import BaseModel,  Field
from datetime import datetime
from enum import Enum
from decimal import Decimal
from schemas.address import AddressRead  # Import AddressRead
#from schemas.order_item import OrderItemRead # circular import
from schemas.user import UserRead # Import UserRead


class OrderStatus(str, Enum):
    """
    Enum for order status values.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"



class OrderItemRead(BaseModel):
    """
    Schema for reading order items.  Includes product details.
    """
    product_id: int
    quantity: int
    price: Decimal  # Price at the time of order
    # product: ProductRead  #  Avoid circular dependencies.


class OrderItemCreate(BaseModel):
    """
    Schema for creating order items.
    """
    product_id: int
    quantity: int
    price: Decimal



class OrderBase(BaseModel):
    """
    Base schema for orders.
    """
    user_id: int
    shipping_address_id: Optional[int]
    order_date: datetime
    total_price: Decimal
    status: OrderStatus = OrderStatus.PENDING
    payment_method: str
    items: List[OrderItemRead]



class OrderCreate(BaseModel):
    """
    Schema for creating a new order.
    """
    user_id: int
    shipping_address_id: Optional[int]
    payment_method: str
    items: List[OrderItemCreate] # Use OrderItemCreate for creating


class OrderRead(OrderBase):
    """
    Schema for reading order information.
    """
    id: int
    user: UserRead
    shipping_address: Optional[AddressRead]
    #items: List[OrderItemRead]  # Avoid the circular import.

    class Config:
        orm_mode = True

