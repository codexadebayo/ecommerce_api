from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models.product import Product
from database.schemas.product import ProductCreate, ProductRead, ProductUpdate
from fastapi import HTTPException, status



def get_product(db: Session, product_id: int) -> ProductRead:
    """
    Retrieves a product by its ID.

    Args:
        db: The database session.
        product_id: The ID of the product to retrieve.

    Returns:
        The product.

    Raises:
        HTTPException: If the product is not found.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product



def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[ProductRead]:
    """
    Retrieves a list of products.

    Args:
        db: The database session.
        skip: The number of products to skip.
        limit: The maximum number of products to retrieve.

    Returns:
        A list of products.
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return products



def create_product(db: Session, product_create: ProductCreate) -> ProductRead:
    """
    Creates a new product.

    Args:
        db: The database session.
        product_create: The product creation schema.

    Returns:
        The created product.

    Raises:
        HTTPException: If any error occurs during product creation.
    """
    try:
        db_product = Product(**product_create.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
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



def update_product(
    db: Session, product_id: int, product_update: ProductUpdate
) -> ProductRead:
    """
    Updates an existing product.

    Args:
        db: The database session.
        product_id: The ID of the product to update.
        product_update: The product update schema.

    Returns:
        The updated product.

    Raises:
        HTTPException: If the product is not found or if any error occurs during the update.
    """
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        # Update the product attributes
        for key, value in product_update.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
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



def delete_product(db: Session, product_id: int) -> bool:
    """
    Deletes a product by its ID.

    Args:
        db: The database session.
        product_id: The ID of the product to delete.

    Returns:
        True if the product was deleted, False otherwise.

    Raises:
        HTTPException: If the product is not found or if any error occurs during deletion.
    """
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        db.delete(product)
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
