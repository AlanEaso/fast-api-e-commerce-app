from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    description: str = None
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class AllProducts(BaseModel):
    products: list[Product]

class FilterProductParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1)
    