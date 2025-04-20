from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database.models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from core.security import get_password_hash, verify_password
from api.dependencies import get_current_active_user  # Import the dependency
from typing import Optional

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Creates a new user.

    Args:
        user (UserCreate): The user data for creation.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The created user object.

    Raises:
        HTTPException: 400 Bad Request if the email is already registered.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Retrieves the current user's information.

    Args:
        current_user (User, optional): The current active user.
            Defaults to Depends(get_current_active_user).

    Returns:
        User: The current user object.
    """
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)) -> User:
    """
    Retrieves a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The user object.

    Raises:
        HTTPException: 404 Not Found if the user is not found.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user



@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Updates a user's information.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The user data for the update.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current active user.
            Defaults to Depends(get_current_active_user).

    Returns:
        User: The updated user object.

    Raises:
        HTTPException: 404 Not Found if the user is not found.
        HTTPException: 403 Forbidden if the user is not allowed to update.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if db_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.first_name is not None:
        db_user.first_name = user_update.first_name
    if user_update.last_name is not None:
        db_user.last_name = user_update.last_name
    if user_update.password is not None:
        db_user.hashed_password = get_password_hash(user_update.password)
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Deletes a user.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current active user.
            Defaults to Depends(get_current_active_user).

    Returns:
        User: The deleted user object.

    Raises:
        HTTPException: 404 Not Found if the user is not found.
        HTTPException: 403 Forbidden if the user is not allowed to delete.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if db_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )
    db.delete(db_user)
    db.commit()
    return db_user
