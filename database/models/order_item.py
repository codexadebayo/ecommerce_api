from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.database import Base  # Import Base from database.py


class OrderItem(Base):
    """
    SQLAlchemy model for the order_items table.

    Represents an item within an order.  This is an association table
    between Order and Product.
    """
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)  # Price at the time of order

    order = relationship("Order", back_populates="items")
    product = relationship("Product")  # Relationship with the Product model

    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})>"
