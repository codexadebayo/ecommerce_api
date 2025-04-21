from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, func, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base
from typing import List, Optional
from datetime import datetime
import enum


class OrderStatus(enum.Enum):
    """
    Enum for order status values.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    """
    SQLAlchemy model for the orders table.
    """
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    shipping_address_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("addresses.id"), nullable=True)
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    total_price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    payment_method: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Credit Card", "PayPal"

    user = relationship("User", back_populates="orders")
    shipping_address = relationship("Address")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, order_date='{self.order_date}', status='{self.status}')>"
