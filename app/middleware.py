from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.lib.exceptions import AppException, ErrorCode
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except AppException as e:
        logger.error(
            "Application error",
            extra={
                "error_code": e.error_code.code,
                "error_message": e.message,
                "details": e.details,
                "path": request.url.path
            }
        )
        return JSONResponse(
            status_code=e.error_code.status,
            content=e.to_dict()
        )
    except ValidationError as e:
        logger.error(
            "Validation error",
            extra={
                "errors": e.errors(),
                "path": request.url.path
            }
        )
        app_error = AppException(
            error_code=ErrorCode.VALIDATION_ERROR,
            details={"validation_errors": e.errors()}
        )
        return JSONResponse(
            status_code=app_error.error_code.status,
            content=app_error.to_dict()
        )
    except SQLAlchemyError as e:
        logger.error(
            "Database error",
            exc_info=True,
            extra={"path": request.url.path}
        )
        app_error = AppException(
            error_code=ErrorCode.DATABASE_ERROR,
            message="A database error occurred"
        )
        return JSONResponse(
            status_code=app_error.error_code.status,
            content=app_error.to_dict()
        )
    except Exception as e:
        logger.error(
            "Unhandled exception",
            exc_info=True,
            extra={"path": request.url.path}
        )
        app_error = AppException(
            error_code=ErrorCode.UNKNOWN_ERROR,
            message="An unexpected error occurred"
        )
        return JSONResponse(
            status_code=app_error.error_code.status,
            content=app_error.to_dict()
        )