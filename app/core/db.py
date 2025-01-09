from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI),
                       echo=settings.ENVIRONMENT == "development")

Base = declarative_base()

def get_session():
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
