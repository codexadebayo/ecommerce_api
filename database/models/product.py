from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base from database.py
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from .category import Category  # Import the Category model

class Product(Base):
    """
    SQLAlchemy model for the products table.

    Represents a product in the e-commerce system.
    """
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)  # Use Numeric for currency
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Define the relationship to Category
    category: Mapped[Category] = relationship("Category", back_populates="products")

    #  Define the relationship to CartItem
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="product")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"
