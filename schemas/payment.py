from typing import Optional
from pydantic import BaseModel,  Field
from datetime import datetime
from enum import Enum
from decimal import Decimal

class PaymentStatus(str, Enum):
    """
    Enum for payment status values.
    """
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentBase(BaseModel):
    """
    Base schema for payments.
    """
    order_id: int
    amount: Decimal
    payment_method: str
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]



class PaymentCreate(BaseModel):
    """
    Schema for creating a new payment.
    """
    order_id: int
    amount: Decimal
    payment_method: str
    #status: PaymentStatus = PaymentStatus.PENDING # Removed, default value in PaymentBase is sufficient



class PaymentRead(PaymentBase):
    """
    Schema for reading payment information.
    """
    id: int

    class Config:
        orm_mode = True



class PaymentUpdate(BaseModel):
    """
    Schema for updating payment information.  All fields are optional.
    """
    order_id: Optional[int] = None
    amount: Optional[Decimal] = None
    payment_method: Optional[str] = None
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
