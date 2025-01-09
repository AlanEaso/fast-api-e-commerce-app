from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, AllProducts
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.lib.exceptions import AppException, ErrorCode
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate):
        try:
            self.__validate_create_params(product)
            db_product = Product(**product.model_dump())
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            return db_product
        except SQLAlchemyError as e:
            logger.error('Error creating product: %s', {str(e)})
            self.db.rollback()
            raise AppException(
                error_code=ErrorCode.DATABASE_ERROR,
                message="An error occurred while creating the product",
                details={'error_details': str(e)},
                original_error=e
            ) from e
        except ValueError as e:
            logger.error('Error creating product: %s', {str(e)})
            self.db.rollback()
            raise AppException(
                error_code=ErrorCode.VALIDATION_ERROR,
                message="Invalid product data",
                details={'error_details': str(e)},
                original_error=e
            ) from e
        except Exception as e:
            logger.error('Error creating product: %s', {str(e)})
            self.db.rollback()
            raise AppException(
                error_code=ErrorCode.UNKNOWN_ERROR,
                message="An unknown error occurred while creating the product",
                details={'error_details': str(e)},
                original_error=e
            ) from e
    
    def get_all_products(self, filter_query):
        try:
            statement = select(Product).offset(filter_query.skip).limit(filter_query.limit)
            products = self.db.scalars(statement).all()
            return AllProducts(products=products)
        except SQLAlchemyError as e:
            logger.error('Error creating product: %s', {str(e)})
            self.db.rollback()
            raise AppException(
                error_code=ErrorCode.DATABASE_ERROR,
                message="An error occurred while creating the product",
                details={'error_details': str(e)},
                original_error=e
            ) from e
        
    def __validate_create_params(self, params):
        if params.price < 0:
            raise ValueError("Price cannot be negative")
        if params.stock < 0:
            raise ValueError("Stock cannot be negative")
        return True