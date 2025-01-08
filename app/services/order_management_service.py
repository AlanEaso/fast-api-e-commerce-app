from sqlalchemy.orm import Session
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.lib.exceptions import AppException, ErrorCode
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OrderManagementService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_request: OrderCreate):
        total_price = 0
        products_to_update = []
        try:
            # Starting a transaction to ensure that all operations are atomic
            with self.db.begin():
                # Making sure all products in the request are available
                for item in order_request.products:
                    # Locking the product row to prevent
                    # concurrent updates and getting the wrong stock value
                    product = self.__lock_product(item.product_id)
                    self.__check_stock_integrity(product, item.quantity)

                    # product.stock -= item.quantity
                    total_price += product.price * item.quantity
                    products_to_update.append((product, item.quantity))

                
                
                # Creating the order
                order = self.__create_new_order(products= order_request.products,
                                                total_price=total_price,
                                                status= OrderStatus.PENDING)
                
                # Flush to ensure the order gets an ID
                self.db.flush()
              
                # Refresh to get the latest state including the ID
                self.db.refresh(order)

            # Some payment or other functionalities here which updates the order status

            with self.db.begin():
                
                order.status = OrderStatus.COMPLETED

                if order.status == OrderStatus.COMPLETED:

                  self.__update_stock(products_to_update)

                  # Flush to ensure the order gets an ID
                  self.db.flush()
              
                  # Refresh to get the latest state including the ID
                  self.db.refresh(order)

                return order    

        except SQLAlchemyError as e:
            logger.error('Error creating product: %s', {str(e)})
            raise AppException(
                error_code=ErrorCode.DATABASE_ERROR,
                message="An error occurred while creating the product",
                details={'error_details': str(e)},
                original_error=e
          ) from e
        except IntegrityError as e:
            logger.error('Error creating product: %s', {str(e)})
            raise AppException(
                error_code=ErrorCode.DATABASE_ERROR,
                message="An error occurred while creating the product",
                details={'error_details': str(e)},
                original_error=e
            ) from e
        except AppException as e:
            logger.error('Error creating product: %s', {str(e)})
            self.db.rollback()
            raise e


    def __lock_product(self, product_id) -> Product:
        # Lock the row for update
        query = select(Product).where(Product.id == product_id).with_for_update()
        result = self.db.execute(query).scalars().first()

        if not result:
            raise AppException(
                error_code=ErrorCode.PRODUCT_NOT_FOUND,
                message="Product not found",
                details={'product_id': product_id}
            )
        
        return result

    def __check_stock_integrity(self, product, quantity) -> None:
        if product.stock < quantity:
            raise AppException(
                error_code=ErrorCode.INSUFFICIENT_INVENTORY,
                message="Insufficient stock for order",
                details={'product id:': product.id,
                         'Product Name': product.name,
                         'Available Stock': product.stock,
                         'Requested Stock': quantity}
            )
    def __create_new_order(self, products, total_price, status):
        new_order = Order(products= [item.dict() for item in products],
                          total_price= total_price,
                          status= status)
        self.db.add(new_order)
        return new_order
    
    def __update_stock(self, products) -> None:
        for product, quanity in products:
            product.stock -= quanity
            logger.info('Updating stock for product: %s', {product.id})
            self.db.add(product)


