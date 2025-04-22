from typing import TypeVar, List, Optional
from pydantic import BaseModel, Field
from fastapi import Query, HTTPException, status
from math import ceil
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query as SQLAlchemyQuery


# Define a generic type for the data items
T = TypeVar("T")


class Page(BaseModel):
    """
    Generic class for representing a paginated response.

    Attributes:
        items: List of data items of type T.
        page: The current page number.
        size: The number of items per page.
        total: The total number of items.
        pages: The total number of pages.
        has_next: Whether there is a next page.
        has_prev: Whether there is a previous page.
        next_page: The next page number, or None if there is no next page.
        prev_page: The previous page number, or None if there is no previous page.
    """

    items: List[T]
    page: int = Field(..., description="Page number")
    size: int = Field(..., description="Number of items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")
    next_page: Optional[int] = Field(None, description="Next page number")
    prev_page: Optional[int] = Field(None, description="Previous page number")

    @classmethod
    def create(
        cls,
        items: List[T],
        page: int,
        size: int,
        total: int,
    ) -> "Page[T]":
        """
        Class method to create a Page instance.

        Calculates pagination metadata based on the provided items, page, size, and total.

        Args:
            items: List of data items.
            page: The current page number.
            size: The number of items per page.
            total: The total number of items.

        Returns:
            A Page instance with the calculated pagination metadata.
        """
        if size <= 0:
            raise ValueError("Page size must be greater than zero")
        pages = ceil(total / size) if size else 0
        has_next = page < pages
        has_prev = page > 1
        next_page = page + 1 if has_next else None
        prev_page = page - 1 if has_prev else None
        return cls(
            items=items,
            page=page,
            size=size,
            total=total,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev,
            next_page=next_page,
            prev_page=prev_page,
        )


def paginate(
    items: List[T],
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    total: Optional[int] = None,
) -> Page[T]:
    """
    Paginates a list of items.

    Args:
        items: The list of items to paginate.
        page: The page number (default: 1).  Must be >= 1.
        size: The number of items per page (default: 10). Must be >= 1 and <= 100.
        total: The total number of items (optional). If provided, used for calculating
               total pages; otherwise, calculated from the length of the `items` list.

    Returns:
        A Page object containing the paginated items and pagination metadata.

    Raises:
        ValueError: If size is not greater than zero.
    """
    if size <= 0:
        raise ValueError("Page size must be greater than zero")

    if total is None:
        total = len(items)  # Calculate total from items if not provided
    pages = ceil(total / size) if size else 0
    if page > pages and pages > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page {page} is out of range (1-{pages})",
        )

    start = (page - 1) * size
    end = start + size
    paged_items = items[start:end]

    return Page.create(
        items=paged_items,
        page=page,
        size=size,
        total=total,
    )



def paginate_query(
    query: SQLAlchemyQuery[T],
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Optional[Session] = None,  # Add an optional db parameter
) -> Page[T]:
    """
    Paginates a SQLAlchemy query.

    This function efficiently paginates a SQLAlchemy query, fetching only the items
    for the specified page.  It calculates the total number of items using `count()`
    on the query, which is more efficient than fetching all items and then calculating
    the length.

    Args:
        query: The SQLAlchemy query to paginate.
        page: The page number (default: 1).
        size: The number of items per page (default: 10).
        db: Optional database session.  If provided, it will be used to execute the count.
            If not provided, the count will be executed on the query itself.

    Returns:
        A Page object containing the paginated items and pagination metadata.

    Raises:
        ValueError: If size is not greater than zero.
        HTTPException: If the requested page is out of range.
    """
    if size <= 0:
        raise ValueError("Page size must be greater than zero")

    # Use the provided db session if available, otherwise, execute the count on the query.
    if db:
        total = db.execute(query.statement.with_only_columns([func.count()]).order_by(None)).scalar()
    else:
        total = query.count()

    pages = ceil(total / size) if size else 0

    if page > pages and pages > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page {page} is out of range (1-{pages})",
        )
    paged_items = query.offset((page - 1) * size).limit(size).all()

    return Page.create(
        items=paged_items,
        page=page,
        size=size,
        total=total,
    )
