from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database.database import Base  # Import Base
from typing import List

# Assuming you have a Product model in a separate file, e.g., product.py
# If not, you'll need to define it here as well.
# from .product import Product  # Import the Product model

class Cart(Base):
    """
    SQLAlchemy model for the Cart table.

    Represents the shopping cart for a user.
    """
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    # items: List["CartItem"] = relationship("CartItem", back_populates="cart")  # Use the string name
    items = relationship("CartItem", back_populates="cart")

    def __repr__(self):
        return f"<Cart(user_id={self.user_id}, items={len(self.items)})>"



class CartItem(Base):
    """
    SQLAlchemy model for the cart_items table.

    Represents an item in a shopping cart.  This is an association table
    between Cart and Product.
    """
    __tablename__ = "cart_items"

    cart_id = Column(Integer, ForeignKey("cart.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")  #  Relationship with the Product model

    def __repr__(self):
        return f"<CartItem(cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})>"
