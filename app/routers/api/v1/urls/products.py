from fastapi import APIRouter, Query
from typing import Annotated
from app.schemas.product import Product, ProductCreate, FilterProductParams

router = APIRouter()

@router.get("/")
async def read_products(filter_query: Annotated[FilterProductParams, Query()]):
    return filter_query

@router.post("/")
async def create_product(product: ProductCreate):
    return product