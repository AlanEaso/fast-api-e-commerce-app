from enum import Enum
from app.models.base_model import BaseModel
from sqlalchemy import Column, Integer, JSON, Float, Enum as SQLAlchemyEnum


class OrderStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'

class Order(BaseModel):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    products = Column(JSON, nullable=False)

    total_price = Column(Float, nullable=False, default=0.0)
    status = Column(SQLAlchemyEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)

    def __repr__(self):
        return f'<Order Id: {self.id}, Product Id: {self.product_id}, Quantity: {self.quantity}, Status: {self.status}>'