import pytest
from unittest.mock import Mock, patch
from app.schemas.product import Product, ProductCreate, FilterProductParams, AllProducts
from app.services.product_service import ProductService
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TEST_TOKEN = "test-product-token"

@pytest.fixture(autouse=True)
def mock_settings():
    """Mock the settings with our test token"""
    with patch("app.dependencies.settings") as mock_settings:
        mock_settings.PRODUCT_TOKEN = TEST_TOKEN
        yield mock_settings

@pytest.fixture
def headers():
    return {"x-token": TEST_TOKEN}

@pytest.fixture
def mock_product_service(db_session):
    """Create a mock product service and patch the instance creation"""
    with patch("app.routers.api.v1.routes.products.ProductService") as mock_service:
        # Configure the mock to return an instance
        service_instance = Mock(spec=ProductService)
        mock_service.return_value = service_instance
        yield service_instance

def test_read_products_success(client, mock_product_service, headers):
    # Prepare test data
    mock_products = AllProducts(
        products=[
            Product(id=1, name="Test Product 1", description="Test description 1", price=99.99, stock=10),
            Product(id=2, name="Test Product 2", description="Test description 2", price=149.99, stock=5)
        ]
    )
    
    # Configure mock to return the test data
    mock_product_service.get_all_products.return_value = mock_products

    # Make request
    response = client.get("/api/v1/products/?skip=0&limit=10", headers=headers)
    
    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) == 2
    assert data["products"][0]["name"] == "Test Product 1"
    assert data["products"][1]["name"] == "Test Product 2"
    
    # Verify service called correctly
    mock_product_service.get_all_products.assert_called_once()
    filter_params = mock_product_service.get_all_products.call_args[0][0]
    assert isinstance(filter_params, FilterProductParams)
    assert filter_params.skip == 0
    assert filter_params.limit == 10

def test_create_product_success(client, mock_product_service, headers):
    # Prepare test data
    request_data = {
        "name": "New Product",
        "description": "Test product description",
        "price": 199.99,
        "stock": 15
    }
    
    created_product = Product(
        id=1,
        name="New Product",
        description="Test product description",
        price=199.99,
        stock=15
    )
    
    # Configure mock
    mock_product_service.create_product.return_value = created_product
    
    # Make request
    response = client.post("/api/v1/products/", json=request_data, headers=headers)
    
    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == request_data["name"]
    assert data["price"] == request_data["price"]
    assert data["stock"] == request_data["stock"]
    assert data["description"] == request_data["description"]
    
    # Verify service called correctly
    mock_product_service.create_product.assert_called_once()
    created_product_data = mock_product_service.create_product.call_args[0][0]
    assert isinstance(created_product_data, ProductCreate)
    assert created_product_data.name == request_data["name"]
    assert created_product_data.price == request_data["price"]
    assert created_product_data.stock == request_data["stock"]
    assert created_product_data.description == request_data["description"]

def test_read_products_invalid_params(client, mock_product_service, headers):
    # Test with invalid query parameters
    response = client.get("/api/v1/products/?skip=-1&limit=0", headers=headers)
    assert response.status_code == 422

def test_create_product_invalid_data(client, mock_product_service, headers):
    # Test with missing required fields
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "",  # Empty name
            "description": "Test",
            # Missing price and stock
        },
        headers=headers
    )
    assert response.status_code == 422

def test_missing_token(client, mock_product_service):
    """Test that requests without token fail"""
    response = client.get("/api/v1/products/?skip=0&limit=10")
    assert response.status_code == 422  # FastAPI returns 422 for missing required headers

def test_invalid_token(client, mock_product_service):
    """Test that requests with wrong token fail"""
    headers = {"x-token": "wrong-token"}
    response = client.get("/api/v1/products/?skip=0&limit=10", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "X-Token header invalid"