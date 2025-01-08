from sqlalchemy import Column, Integer, String
from app.models.base_model import BaseModel

class Product(BaseModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    stock = Column(Integer, default=0)

    def __repr__(self):
        return f'<Product Id: {self.id}, Name: {self.name}>'