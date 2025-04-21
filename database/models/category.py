from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base from database.py
from typing import List, Optional
from datetime import datetime


class Category(Base):
    """
    SQLAlchemy model for the categories table.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Define the relationship to Product
    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"
