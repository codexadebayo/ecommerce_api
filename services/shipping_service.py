from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models.shipping_method import ShippingMethod
from database.schemas.shipping import (
    ShippingMethodCreate,
    ShippingMethodRead,
    ShippingMethodUpdate,
)
from fastapi import HTTPException, status


def get_shipping_method(db: Session, shipping_method_id: int) -> ShippingMethodRead:
    """
    Retrieves a shipping method by its ID.

    Args:
        db: The database session.
        shipping_method_id: The ID of the shipping method to retrieve.

    Returns:
        The shipping method.

    Raises:
        HTTPException: If the shipping method is not found.
    """
    shipping_method = (
        db.query(ShippingMethod)
        .filter(ShippingMethod.id == shipping_method_id)
        .first()
    )
    if not shipping_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipping method not found"
        )
    return shipping_method



def get_shipping_methods(
    db: Session, skip: int = 0, limit: int = 10
) -> List[ShippingMethodRead]:
    """
    Retrieves a list of shipping methods.

    Args:
        db: The database session.
        skip: The number of shipping methods to skip.
        limit: The maximum number of shipping methods to retrieve.

    Returns:
        A list of shipping methods.
    """
    shipping_methods = db.query(ShippingMethod).offset(skip).limit(limit).all()
    return shipping_methods



def create_shipping_method(
    db: Session, shipping_method_create: ShippingMethodCreate
) -> ShippingMethodRead:
    """
    Creates a new shipping method.

    Args:
        db: The database session.
        shipping_method_create: The shipping method creation schema.

    Returns:
        The created shipping method.

    Raises:
        HTTPException: If any error occurs during shipping method creation.
    """
    try:
        db_shipping_method = ShippingMethod(**shipping_method_create.dict())
        db.add(db_shipping_method)
        db.commit()
        db.refresh(db_shipping_method)
        return db_shipping_method
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )



def update_shipping_method(
    db: Session, shipping_method_id: int, shipping_method_update: ShippingMethodUpdate
) -> ShippingMethodRead:
    """
    Updates an existing shipping method.

    Args:
        db: The database session.
        shipping_method_id: The ID of the shipping method to update.
        shipping_method_update: The shipping method update schema.

    Returns:
        The updated shipping method.

    Raises:
        HTTPException: If the shipping method is not found or if any error
        occurs during the update.
    """
    try:
        shipping_method = (
            db.query(ShippingMethod)
            .filter(ShippingMethod.id == shipping_method_id)
            .first()
        )
        if not shipping_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipping method not found",
            )

        for key, value in shipping_method_update.dict(exclude_unset=True).items():
            setattr(shipping_method, key, value)
        db.commit()
        db.refresh(shipping_method)
        return shipping_method
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )



def delete_shipping_method(db: Session, shipping_method_id: int) -> bool:
    """
    Deletes a shipping method by its ID.

    Args:
        db: The database session.
        shipping_method_id: The ID of the shipping method to delete.

    Returns:
        True if the shipping method was deleted, False otherwise.

    Raises:
        HTTPException: If the shipping method is not found or if any error
        occurs during deletion.
    """
    try:
        shipping_method = (
            db.query(ShippingMethod)
            .filter(ShippingMethod.id == shipping_method_id)
            .first()
        )
        if not shipping_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipping method not found",
            )
        db.delete(shipping_method)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
