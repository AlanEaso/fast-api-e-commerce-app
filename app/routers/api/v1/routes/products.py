from fastapi import APIRouter, Query, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.schemas.product import Product, ProductCreate, FilterProductParams, AllProducts
from app.dependencies import get_product_header
from app.core.db import get_session
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_product_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=AllProducts)
async def read_products(filter_query: Annotated[FilterProductParams, Query()], db: Session = Depends(get_session)):
    return ProductService(db).get_all_products(filter_query)

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_session)):
    return ProductService(db).create_product(product)