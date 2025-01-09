from enum import Enum
from typing import Any, Dict, Optional
from http import HTTPStatus

class ErrorCode(Enum):
    # Generic Errors (400-499)
    BAD_REQUEST = (400, HTTPStatus.BAD_REQUEST, "Bad Request")
    UNAUTHORIZED = (401, HTTPStatus.UNAUTHORIZED, "Unauthorized")
    FORBIDDEN = (403, HTTPStatus.FORBIDDEN, "Forbidden")
    NOT_FOUND = (404, HTTPStatus.NOT_FOUND, "Not Found")
    METHOD_NOT_ALLOWED = (405, HTTPStatus.METHOD_NOT_ALLOWED, "Method Not Allowed")
    CONFLICT = (409, HTTPStatus.CONFLICT, "Conflict")
    UNPROCESSABLE_ENTITY = (422, HTTPStatus.UNPROCESSABLE_ENTITY, "Unprocessable Entity")

    # Server Errors (500-599)
    INTERNAL_SERVER_ERROR = (500, HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Server Error")
    NOT_IMPLEMENTED = (501, HTTPStatus.NOT_IMPLEMENTED, "Not Implemented")
    BAD_GATEWAY = (502, HTTPStatus.BAD_GATEWAY, "Bad Gateway")
    SERVICE_UNAVAILABLE = (503, HTTPStatus.SERVICE_UNAVAILABLE, "Service Unavailable")
    GATEWAY_TIMEOUT = (504, HTTPStatus.GATEWAY_TIMEOUT, "Gateway Timeout")

    # Validation Errors
    VALIDATION_ERROR = (400, HTTPStatus.BAD_REQUEST, "Validation Error")
    INVALID_PRODUCT_DATA = (400, HTTPStatus.BAD_REQUEST, "Invalid Product Data")
    INVALID_ORDER_DATA = (400, HTTPStatus.BAD_REQUEST, "Invalid Order Data")

    # Authentication/Authorization Errors
    AUTHENTICATION_FAILED = (401, HTTPStatus.UNAUTHORIZED, "Authentication Failed")
    INVALID_TOKEN = (401, HTTPStatus.UNAUTHORIZED, "Invalid Token")
    INSUFFICIENT_PERMISSIONS = (403, HTTPStatus.FORBIDDEN, "Insufficient Permissions")

    # Resource Errors
    PRODUCT_NOT_FOUND = (404, HTTPStatus.NOT_FOUND, "Product Not Found")
    ORDER_NOT_FOUND = (404, HTTPStatus.NOT_FOUND, "Order Not Found")
    INSUFFICIENT_INVENTORY = (409, HTTPStatus.CONFLICT, "Insufficient Inventory")

    # Database Errors
    DATABASE_ERROR = (500, HTTPStatus.INTERNAL_SERVER_ERROR, "Database Error")
    PRODUCT_CREATE_ERROR = (501, HTTPStatus.INTERNAL_SERVER_ERROR, "Failed to Create Product")
    PRODUCT_UPDATE_ERROR = (501, HTTPStatus.INTERNAL_SERVER_ERROR, "Failed to Update Product")
    ORDER_CREATE_ERROR = (501, HTTPStatus.INTERNAL_SERVER_ERROR, "Failed to Create Order")
    UNKNOWN_ERROR = (500, HTTPStatus.INTERNAL_SERVER_ERROR, "An unknown error occurred")
    CANNOT_UPDATE_STOCK = (40002, HTTPStatus.BAD_REQUEST, "Cannot update stock if order is not completed")

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