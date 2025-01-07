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
        orm_mode = True
        from_attributes = True

class FilterProductParams(BaseModel):
    page_no: int = Field(1, ge=1)
    limit: int = Field(1, ge=1)