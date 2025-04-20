from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from sqlalchemy.orm import Session
from database.database import Base  # Import Base from database.py

class User(Base):
    """
    SQLAlchemy model for the User table.

    This class defines the structure of the User table in the database.
    It includes columns for user ID, email, hashed password, first name,
    last name, is_active status, and timestamps for creation and last update.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        """
        Returns a string representation of the User object.
        """
        return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"
