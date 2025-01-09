import pytest
from unittest.mock import Mock, patch
from app.schemas.order import Order, OrderCreate, OrderItemBase, OrderStatus
from app.lib.exceptions import ErrorCode, AppException

TEST_TOKEN = "test-order-token"

@pytest.fixture(autouse=True)
def mock_settings():
    """Mock the settings with our test token. Using autouse=True to ensure it's always applied"""
    with patch("app.dependencies.settings", autospec=True) as mock_settings:
        mock_settings.ORDER_TOKEN = TEST_TOKEN
        yield mock_settings

@pytest.fixture
def headers():
    """Headers with the test token"""
    return {"x-token": TEST_TOKEN}

@pytest.fixture
def mock_order_service(db_session):
    """Create a mock order management service and patch the instance creation"""
    with patch("app.routers.api.v1.routes.orders.OrderManagementService") as mock_service:
        service_instance = Mock()
        mock_service.return_value = service_instance
        yield service_instance

def test_create_order_success(client, mock_order_service, headers):
    # Prepare test data
    request_data = {
        "products": [
            {
                "product_id": 1,
                "quantity": 2
            },
            {
                "product_id": 2,
                "quantity": 1
            }
        ]
    }
    
    expected_response = Order(
        id=1,
        products=[
            OrderItemBase(product_id=1, quantity=2),
            OrderItemBase(product_id=2, quantity=1)
        ],
        total_price=299.99,
        status=OrderStatus.PENDING
    )
    
    # Configure mock
    mock_order_service.process_order.return_value = expected_response
    
    # Make request
    response = client.post("/api/v1/orders/", json=request_data, headers=headers)
    
    # Print debug information if the test fails
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
    
    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert len(data["products"]) == 2
    assert data["total_price"] == 299.99
    assert data["status"] == OrderStatus.PENDING.value
    
    # Verify service called correctly
    mock_order_service.process_order.assert_called_once()
    order_data = mock_order_service.process_order.call_args[0][0]
    assert isinstance(order_data, OrderCreate)
    assert len(order_data.products) == 2

def test_create_order_invalid_data(client, mock_order_service, headers):
    # Test with invalid request data
    invalid_data = {
        "products": [
            {
                "product_id": 1,
                "quantity": 0  # Invalid quantity (must be > 0)
            }
        ]
    }
    
    response = client.post(
        "/api/v1/orders/",
        json=invalid_data,
        headers=headers
    )
    assert response.status_code == 422

def test_create_order_empty_products(client, mock_order_service, headers):
    """Test creating an order with empty products list should fail validation"""
    # Configure mock to raise exception for empty products
    mock_order_service.process_order.side_effect = AppException(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Order must contain at least one product"
    )
    
    # Test with empty products list
    invalid_data = {
        "products": []
    }
    
    response = client.post(
        "/api/v1/orders/",
        json=invalid_data,
        headers=headers
    )
    
    assert response.status_code == 400
    assert "Order must contain at least one product" == response.json()["message"]
def test_missing_token(client, mock_order_service):
    """Test that requests without token fail"""
    request_data = {
        "products": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }
    response = client.post("/api/v1/orders/", json=request_data)
    assert response.status_code == 422  # FastAPI returns 422 for missing required headers

def test_invalid_token(client, mock_order_service):
    """Test that requests with wrong token fail"""
    headers = {"x-token": "wrong-token"}
    request_data = {
        "products": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }
    response = client.post("/api/v1/orders/", json=request_data, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "X-Token header invalid"