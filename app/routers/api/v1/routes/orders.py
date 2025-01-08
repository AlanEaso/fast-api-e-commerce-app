from fastapi import APIRouter, Depends
from app.schemas.order import OrderCreate
from sqlalchemy.orm import Session
from app.dependencies import get_order_header
from app.core.db import get_session
from app.schemas.order import Order
from app.services.order_management_service import OrderManagementService

router = APIRouter()

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_order_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Order)
async def create_order(order: OrderCreate, db: Session = Depends(get_session)):
    return OrderManagementService(db).create_order(order)