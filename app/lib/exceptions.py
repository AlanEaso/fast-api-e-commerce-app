from enum import Enum
from typing import Any, Dict, Optional
from http import HTTPStatus

class ErrorCode(Enum):
    # Generic Errors (1000-1999)
    UNKNOWN_ERROR = (1000, HTTPStatus.INTERNAL_SERVER_ERROR, "An unknown error occurred")
    VALIDATION_ERROR = (1001, HTTPStatus.BAD_REQUEST, "Validation error")
    NOT_FOUND = (1002, HTTPStatus.NOT_FOUND, "Resource not found")
    
    # Authentication/Authorization Errors (2000-2999)
    UNAUTHORIZED = (2000, HTTPStatus.UNAUTHORIZED, "Unauthorized access")
    FORBIDDEN = (2001, HTTPStatus.FORBIDDEN, "Access forbidden")
    
    # Database Errors (3000-3999)
    DATABASE_ERROR = (3000, HTTPStatus.INTERNAL_SERVER_ERROR, "Database error")
    DUPLICATE_ENTRY = (3001, HTTPStatus.CONFLICT, "Resource already exists")
    
    # Product Errors (4000-4999)
    PRODUCT_NOT_FOUND = (4000, HTTPStatus.NOT_FOUND, "Product not found")
    PRODUCT_CREATE_ERROR = (4001, HTTPStatus.BAD_REQUEST, "Failed to create product")
    PRODUCT_UPDATE_ERROR = (4002, HTTPStatus.BAD_REQUEST, "Failed to update product")
    
    # Order Errors (5000-5999)
    ORDER_NOT_FOUND = (5000, HTTPStatus.NOT_FOUND, "Order not found")
    ORDER_CREATE_ERROR = (5001, HTTPStatus.BAD_REQUEST, "Failed to create order")
    INSUFFICIENT_INVENTORY = (5002, HTTPStatus.CONFLICT, "Insufficient inventory")

    def __init__(self, code: int, status: HTTPStatus, message: str):
        self.code = code
        self.status = status
        self.message = message

class AppException(Exception):
    def __init__(
        self,
        error_code: ErrorCode,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        self.error_code = error_code
        self.message = message or error_code.message
        self.details = details or {}
        self.original_error = original_error
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.error_code.code,
            "message": self.message,
            "details": self.details
        }