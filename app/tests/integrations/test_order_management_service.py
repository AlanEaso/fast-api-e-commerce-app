import pytest
from app.services.order_management_service import OrderManagementService
from app.services.product_service import ProductService
from app.schemas.order import OrderCreate
from app.schemas.product import ProductCreate
from app.models.order import OrderStatus
from app.models.product import Product
from app.lib.exceptions import AppException, ErrorCode

class TestOrderManagementService:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.service = OrderManagementService(db_session)
        self.product_service = ProductService(db_session)
        self.db_session = db_session
        
        # Create test product
        product_data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 100,
            "stock": 10
        }
        self.test_product = self.product_service.create_product(
            ProductCreate(**product_data)
        )


    def test_process_order_insufficient_stock(self):
        order_data = {
            "products": [
                {
                    "product_id": self.test_product.id,
                    "quantity": 20  # More than available stock
                }
            ]
        }
        
        with pytest.raises(AppException) as exc:
            self.service.process_order(OrderCreate(**order_data))
        assert exc.value.error_code.INSUFFICIENT_INVENTORY

    def test_process_order_product_not_found(self):
        order_data = {
            "products": [
                {
                    "product_id": 99999,  # Non-existent product
                    "quantity": 1
                }
            ]
        }
        
        with pytest.raises(AppException) as exc:
            self.service.process_order(OrderCreate(**order_data))
        assert exc.value.error_code.PRODUCT_NOT_FOUND

    def test_process_order_success(self):
        """
        Test successful order processing with stock update verification.
        """
        self.db_session.rollback()
        self.db_session.expire_all()
        
        # Prepare order data
        order_data = {
            "products": [
                {
                    "product_id": self.test_product.id,
                    "quantity": 2
                }
            ]
        }
        
        # Process the order
        order = self.service.process_order(OrderCreate(**order_data))
        
        # Verify order status and price
        assert order.status == OrderStatus.COMPLETED
        assert order.total_price == 200  # 2 * 100
        
        # Refresh test_product to get the latest state
        self.db_session.refresh(self.test_product)
        assert self.test_product.stock == 8  # 10 - 2

    def test_invalid_order_status_update_stock(self):
        order_data = {
            "products": [
                {
                    "product_id": self.test_product.id,
                    "quantity": 2
                }
            ]
        }
        
        # Process the order
        order, products_to_update = self.service._OrderManagementService__create_order(order_request=OrderCreate(**order_data))
        self.db_session.rollback()
        self.db_session.expire_all()
        
        # Try to process the same order again
        with pytest.raises(AppException) as exc:
            self.service._OrderManagementService__verify_and_update_product_stock(order, products_to_update)
        assert exc.value.error_code == ErrorCode.CANNOT_UPDATE_STOCK