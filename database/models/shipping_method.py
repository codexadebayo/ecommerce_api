from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base
from datetime import datetime
from typing import Optional


class ShippingMethod(Base):
    """
    SQLAlchemy model for the shipping_methods table.
    """
    __tablename__ = "shipping_methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cost: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)  # Store cost as Numeric
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<ShippingMethod(name='{self.name}', cost={self.cost})>"
