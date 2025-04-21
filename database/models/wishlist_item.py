from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base
from typing import List

# Define the association table for the many-to-many relationship between Wishlist and Product
wishlist_products = Table(
    "wishlist_products",
    Base.metadata,
    Column("wishlist_id", Integer, ForeignKey("wishlists.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)


class Wishlist(Base):
    """
    SQLAlchemy model for the wishlists table.

    Represents a wishlist for a user, containing a collection of products.
    """
    __tablename__ = "wishlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Define the relationship to Product using the association table
    products: Mapped[List["Product"]] = relationship(
        "Product", secondary=wishlist_products, back_populates="wishlists"
    )

    user = relationship("User", back_populates="wishlist") #relationship to user

    def __repr__(self):
        return f"<Wishlist(user_id={self.user_id}, products={len(self.products)})>"
