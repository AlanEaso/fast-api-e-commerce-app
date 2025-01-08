from pydantic import BaseModel, Field
from enum import Enum

class OrderItemBase(BaseModel):
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., gt=0, description="Quantity of the product, must be greater than 0")

class OrderStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'

class OrderBase(BaseModel):
    products: list[OrderItemBase]
    total_price: float
    status: OrderStatus

class OrderCreate(BaseModel):
    products: list[OrderItemBase]

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True