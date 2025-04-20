from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api.routes import (
    products,
    categories,
    users,
    orders,
    cart,
    checkout,
    payment,
    shipping,
    wishlist,
)


from core.config import settings
from database.database import engine
from database.database import Base

Base.metadata.create_all(bind=engine)



app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS configuration (adjust as needed for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500/"],  # Replace with your frontend origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test_api():
  return {"Hello":"World"}

# Include API routers
# app.include_router(products.router, prefix=settings.API_V1_STR)
# app.include_router(categories.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR + "/users")
# app.include_router(orders.router, prefix=settings.API_V1_STR)
# app.include_router(cart.router, prefix=settings.API_V1_STR)
# app.include_router(checkout.router, prefix=settings.API_V1_STR)
# app.include_router(payment.router, prefix=settings.API_V1_STR)
# app.include_router(shipping.router, prefix=settings.API_V1_STR)
# app.include_router(wishlist.router, prefix=settings.API_V1_STR)