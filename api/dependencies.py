from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional

from core.config import settings
from core.security import verify_password
from database.database import get_db
from database.models.user import User
from schemas.user import UserRead  # Import UserRead schema

# Define the token URL for obtaining the JWT.  This is used by FastAPI's
# OAuth2PasswordBearer to define the endpoint that clients use to get a token.
# In your main.py, you'll have an endpoint that generates this token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Retrieves the current user based on the JWT token provided in the request.

    This function is a dependency that can be used in FastAPI route handlers
    to get the authenticated user.  It performs the following steps:

    1.  It retrieves the JWT token from the request using the
        `OAuth2PasswordBearer` scheme.
    2.  It decodes the token using the application's secret key and algorithm.
    3.  It extracts the user's email from the decoded token.
    4.  It retrieves the user from the database based on the email.
    5.  If the token is invalid or the user is not found, it raises an
        appropriate HTTPException.
    6.  It returns the user object.

    Args:
        db (Session, optional): The database session.
            Defaults to Depends(get_db).
        token (str, optional): The JWT token.
            Defaults to Depends(oauth2_scheme).

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: 401 Unauthorized if the token is invalid or expired.
        HTTPException: 404 Not Found if the user is not found in the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #  Payload is a dict containing the data from the token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")  # "sub" is the standard key for the subject (user identifier)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user



def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Retrieves the current active user.

    This function is a dependency that can be used in FastAPI route handlers
    to ensure that the authenticated user is active.  It builds upon
    `get_current_user` by checking the user's `is_active` status.

    Args:
        current_user (User, optional): The current user.
            Defaults to Depends(get_current_user).

    Returns:
        User: The current active user object.

    Raises:
        HTTPException: 400 Bad Request if the user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
