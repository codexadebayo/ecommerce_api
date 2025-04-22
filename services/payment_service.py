from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models.payment import Payment, PaymentStatus
from database.models.order import Order
from database.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdate
from fastapi import HTTPException, status
from decimal import Decimal
from typing import Optional


def create_payment(db: Session, payment_create: PaymentCreate) -> PaymentRead:
    """
    Creates a new payment for an order.

    Args:
        db: The database session.
        payment_create: The payment creation schema.

    Returns:
        The created payment.

    Raises:
        HTTPException: If the order is not found, the total price doesn't match,
                       or if any other error occurs during payment creation.
    """
    try:
        order = db.query(Order).filter(Order.id == payment_create.order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        #  Check if the order's total price matches the payment amount.
        if order.total_price != payment_create.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment amount ({payment_create.amount}) does not match order total ({order.total_price})",
            )

        # Create the payment
        payment = Payment(
            order_id=payment_create.order_id,
            amount=payment_create.amount,
            payment_method=payment_create.payment_method,
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except HTTPException as e:
        db.rollback()  # Rollback for any HTTP exceptions as well.
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )



def get_payment(db: Session, payment_id: int) -> PaymentRead:
    """
    Retrieves a payment by its ID.

    Args:
        db: The database session.
        payment_id: The ID of the payment to retrieve.

    Returns:
        The payment.

    Raises:
        HTTPException: If the payment is not found.
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )
    return payment



def update_payment_status(
    db: Session, payment_id: int, status: str, transaction_id: Optional[str] = None
) -> PaymentRead:
    """
    Updates the status of a payment.

    Args:
        db: The database session.
        payment_id: The ID of the payment to update.
        status: The new status of the payment.
        transaction_id: Optional transaction ID from the payment provider.

    Returns:
        The updated payment.

    Raises:
        HTTPException: If the payment is not found or if an invalid status is provided.
    """
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )

    #  Validate the status
    try:
        PaymentStatus(status)  # Check if it's a valid enum value
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid payment status: {status}",
        )

    payment.status = status
    if transaction_id:
        payment.transaction_id = transaction_id
    db.commit()
    db.refresh(payment)
    return payment
