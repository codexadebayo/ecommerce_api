from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base from database.py
from typing import Optional


class Address(Base):
    """
    SQLAlchemy model for the addresses table.

    Represents a shipping address for a user.
    """
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    street_address: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    postal_code: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    # Define the relationship to User
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(street_address='{self.street_address}', city='{self.city}', state='{self.state}', postal_code='{self.postal_code}', country='{self.country}')>"
