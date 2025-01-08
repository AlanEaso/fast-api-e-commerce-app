from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # This class will not be mapped to a table in the DB
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<{self.__class__.__name__} Id: {self.id}>'