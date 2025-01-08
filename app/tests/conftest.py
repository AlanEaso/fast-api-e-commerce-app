import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base_model import Base
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import get_session
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def db_engine():
    """Create a SQLite in-memory database engine for testing"""
    logger.info("Creating SQLite database engine...")
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    logger.info("Database engine cleaned up")

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a new database session for a test"""
    logger.info("Creating new database session...")
    SessionLocal = sessionmaker(
        bind=db_engine,
        autocommit=False,
        autoflush=False
    )
    
    # Create a new session
    session = SessionLocal()
    
    try:
        yield session
    finally:
        logger.info("Cleaning up database session...")
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create a FastAPI test client"""
    def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def setup_app():
    # Register all routers
    from app.routers.api.v1.routes import products, orders
    app.include_router(products.router)
    app.include_router(orders.router)
    yield