from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models.order import Order, OrderItem
from database.models.product import Product
from database.schemas.order import OrderCreate, OrderRead, OrderItemCreate, OrderItemRead
from fastapi import HTTPException, status
from decimal import Decimal


def create_order(db: Session, order_create: OrderCreate, user_id: int) -> OrderRead:
    """
    Creates a new order for a user.

    Args:
        db: The database session.
        order_create: The order creation schema.
        user_id: The ID of the user placing the order.

    Returns:
        The created order.

    Raises:
        HTTPException: If any error occurs during order creation.
    """
    try:
        # Validate that the user_id exists.  We'll do this in the route, but
        # we could also do it here.
        # Create order items and calculate total price
        order_items: List[OrderItem] = []
        total_price: Decimal = 0
        for item_create in order_create.items:
            product = db.query(Product).filter(Product.id == item_create.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {item_create.product_id} not found",
                )
            if product.stock_quantity < item_create.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough stock for product {product.name}",
                )

            # Use the price from the database, not the price from the client.
            order_item = OrderItem(
                product_id=item_create.product_id,
                quantity=item_create.quantity,
                price=product.price,  # Use price from database
            )
            order_items.append(order_item)
            total_price += order_item.price * order_item.quantity

            # Reduce stock.  Do this in a transaction.
            product.stock_quantity -= item_create.quantity
            db.add(product)

        # Create the order
        order = Order(
            user_id=user_id,
            shipping_address_id=order_create.shipping_address_id,
            payment_method=order_create.payment_method,
            total_price=total_price,
            items=order_items,
        )
        db.add(order)
        db.commit()  # Commit the entire transaction
        db.refresh(order)

        return order
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}",
        )
    except HTTPException as e:
        db.rollback()  # Rollback for any HTTP exceptions as well
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )



def get_order(db: Session, order_id: int) -> OrderRead:
    """
    Retrieves an order by its ID.

    Args:
        db: The database session.
        order_id: The ID of the order to retrieve.

    Returns:
        The order.

    Raises:
        HTTPException: If the order is not found.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order



def get_orders_by_user(db: Session, user_id: int) -> List[OrderRead]:
    """
    Retrieves all orders for a specific user.

    Args:
        db: The database session.
        user_id: The ID of the user.

    Returns:
        A list of orders for the user.
    """
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders



def update_order_status(db: Session, order_id: int, status: str) -> OrderRead:
    """
    Updates the status of an order.

    Args:
        db: The database session.
        order_id: The ID of the order to update.
        status: The new status of the order.

    Returns:
        The updated order.

    Raises:
        HTTPException: If the order is not found or if an invalid status is provided.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    #  Validate the status.  The enum class handles this,
    #  but we can provide a more helpful error message.
    try:
        OrderStatus(status)  # Check if the status is a valid enum value.
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order status: {status}",
        )

    order.status = status
    db.commit()
    db.refresh(order)
    return order
