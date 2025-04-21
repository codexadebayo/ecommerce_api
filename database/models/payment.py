from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, func, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base
from datetime import datetime
import enum
from typing import Optional

class PaymentStatus(enum.Enum):
    """
    Enum for payment status values.
    """
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    """
    SQLAlchemy model for the payments table.
    """
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Credit Card", "PayPal"
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING
    )
    transaction_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # Provider's transaction ID
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    order = relationship("Order", back_populates="payment")  #  Backref to Order

    def __repr__(self):
        return f"<Payment(order_id={self.order_id}, amount={self.amount}, status='{self.status}')>"
