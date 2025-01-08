import pytest
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, FilterProductParams
from app.lib.exceptions import AppException, ErrorCode
import logging


class TestProductService:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.service = ProductService(db_session)
        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.valid_product_data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 100,
            "stock": 10
        }

    def test_create_product_success(self):
        product_create = ProductCreate(**self.valid_product_data)
        product = self.service.create_product(product_create)
        
        assert product.name == self.valid_product_data["name"]
        assert product.price == self.valid_product_data["price"]
        assert product.stock == self.valid_product_data["stock"]

    def test_create_product_invalid_data(self):
        self.logger.debug("Testing product creation with invalid data")
        invalid_data = self.valid_product_data.copy()
        invalid_data["price"] = -100
        
        with pytest.raises(AppException) as exc_info:
            self.service.create_product(ProductCreate(**invalid_data))
        
        self.logger.debug(f"Raised exception: {exc_info.value}")
        assert exc_info.value.error_code == ErrorCode.VALIDATION_ERROR

    def test_get_all_products(self):
        # Create some test products
        product_create = ProductCreate(**self.valid_product_data)
        self.service.create_product(product_create)
        
        filter_params = FilterProductParams(skip=0, limit=10)
        result = self.service.get_all_products(filter_params)
        
        assert len(result.products) > 0
        assert result.products[0].name == self.valid_product_data["name"]