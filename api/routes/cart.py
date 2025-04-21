from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from database.models.user import User
from database.models.cart import Cart
from database.models.product import Product
from schemas.cart import CartRead, CartItemCreate, CartItemRead, CartUpdate
from api.dependencies import get_current_active_user  # Import the dependency
from typing import Dict

router = APIRouter()


@router.get("/", response_model=CartRead)
def get_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
) -> Cart:
    """
    Retrieves the user's shopping cart.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current active user.
            Defaults to Depends(get_current_active_user).

    Returns:
        Cart: The user's shopping cart.

    Raises:
        HTTPException: 404 Not Found if the cart is not found.
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    return cart



@router.post("/items", response_model=CartRead)
def add_item_to_cart(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Cart:
    """
    Adds an item to the user's shopping cart.  If the item is already in the cart,
    it updates the quantity.

    Args:
        cart_item (CartItemCreate): The item to add to the cart, including product_id and quantity.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current active user.
            Defaults to Depends(get_current_active_user).

    Returns:
        Cart: The updated shopping cart.

    Raises:
        HTTPException: 400 Bad Request if the product does not exist or the quantity is invalid.
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)  # Create cart if it doesn't exist
        db.add(cart)
        db.commit()

    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product does not exist"
        )

    if cart_item.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid quantity"
        )

    # Check if the item is already in the cart
    existing_item = next(
        (item for item in cart.items if item.product_id == cart_item.product_id), None
    )

    if existing_item:
        existing_item.quantity = cart_item.quantity  # Update the quantity
    else:
        #  Create a new CartItem and add it to the cart's items collection.
        new_item = CartItemRead(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
        )
        cart.items.append(new_item)

    db.commit()
    db.refresh(cart)
    return cart



@router.delete("/items/{product_id}", response_model=CartRead)
def remove_item_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Cart:
    """
    Removes an item from the user's shopping cart.

    Args:
        product_id (int): The ID of the product to remove from the cart.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current active user.
            Defaults to Depends(get_current_active_user).

    Returns:
        Cart: The updated shopping cart.

    Raises:
        HTTPException: 404 Not Found if the cart is not found
        HTTPException: 400 Bad Request if the item is not in the cart.
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    # Check if the item is in the cart
    item_to_remove = next(
        (item for item in cart.items if item.product_id == product_id), None
    )
    if not item_to_remove:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Item not in cart"
        )

    cart.items.remove(item_to_remove)  # Remove the item
    db.commit()
    db.refresh(cart)
    return cart



@router.patch("/", response_model=CartRead)
def update_cart(
    cart_update: CartUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Cart:
    """
    Updates the entire cart.  This endpoint expects a list of cart items
    with product IDs and quantities.  It will replace the existing cart items
    with the provided items.

    Args:
        cart_update (CartUpdate):  A CartUpdate object containing a list of CartItemCreate objects.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current active user.
            Defaults to Depends(get_current_active_user).

    Returns:
        Cart: The updated cart.

    Raises:
        HTTPException: 404 Not Found if the cart is not found.
        HTTPException: 400 Bad Request if any of the products in the cart_update are invalid,
                        or if any of the quantities are invalid.
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    # Clear the existing cart items
    cart.items.clear()

    # Add the new items from the cart_update
    for item_update in cart_update.items:
        product = db.query(Product).filter(Product.id == item_update.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with id {item_update.product_id} does not exist",
            )
        if item_update.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid quantity for product {item_update.product_id}",
            )
        new_item = CartItemRead(product_id=item_update.product_id, quantity=item_update.quantity)
        cart.items.append(new_item)

    db.commit()
    db.refresh(cart)
    return cart
