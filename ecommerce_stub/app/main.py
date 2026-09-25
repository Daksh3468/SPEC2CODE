"""
main.py — FastAPI application entry point for ShopFlow.
"""
from fastapi import FastAPI
from app.api import orders, users, products

app = FastAPI(title="ShopFlow E-Commerce API", version="1.0.0")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
