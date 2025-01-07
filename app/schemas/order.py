from pydantic import BaseModel
from enum import Enum

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderStatus(str, Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'

class OrderBase(BaseModel):
    products: list[OrderItemBase]
    total_price: float
    status: OrderStatus

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True