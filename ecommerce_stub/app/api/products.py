"""
products.py — FastAPI router for product endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.models.product import Product, ProductPage
from app.services.product_service import ProductService

router = APIRouter()
_svc = ProductService()


@router.get("/", response_model=ProductPage)
def list_products(page: int = 1, page_size: int = 20):
    result = _svc.list_products(page, page_size)
    return result or ProductPage(items=[], total=0, page=page, page_size=page_size)


@router.get("/search", response_model=ProductPage)
def search_products(q: str, page: int = 1):
    result = _svc.search_products(q, page)
    return result or ProductPage(items=[], total=0, page=page, page_size=20)


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str):
    result = _svc.get_product(product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result
