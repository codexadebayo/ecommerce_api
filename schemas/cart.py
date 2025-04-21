from pydantic import BaseModel, conint, validator, ConfigDict
from typing import List, Optional
from database.models.product import Product  # Import Product model


class CartItemCreate(BaseModel):
    """
    Schema for creating a cart item.  This schema is used when adding a product
    to the cart.
    """
    product_id: int
    quantity: conint(gt=0)  # Ensure quantity is greater than zero

    #  No need for a validator here, Pydantic's conint already handles this
    # @validator("quantity")
    # def validate_quantity(cls, value):
    #     if value <= 0:
    #         raise ValueError("Quantity must be greater than zero")
    #     return value



class CartItemRead(BaseModel):
    """
    Schema for reading a cart item.  This schema includes the product details.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    product_id: int
    quantity: int
    product: Optional[Product] = None  # Include product details, make it optional


class CartRead(BaseModel):
    """
    Schema for reading the entire cart.
    """
    id: Optional[int] = None
    user_id: int
    items: List[CartItemRead] = []  # Use CartItemRead
    total_price: Optional[float] = 0.0

    @validator("total_price", always=True)
    def calculate_total_price(cls, v, values):
        """
        Calculates the total price of the cart based on the items.
        """
        total = 0.0
        if values.get("items"):  # Check if items list exists
            for item in values["items"]:
                if item.product:  # Make sure product is loaded
                    total += item.product.price * item.quantity
        return total



class CartUpdate(BaseModel):
    """
    Schema for updating the entire cart.  This schema is used when replacing
    all items in the cart.
    """
    items: List[CartItemCreate]
