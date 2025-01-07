from fastapi import APIRouter
from .urls import products, orders

api_v1_router = APIRouter()
api_v1_router.include_router(products.router, prefix='/products', tags=['products'])
api_v1_router.include_router(orders.router, prefix='/orders', tags=['orders'])
