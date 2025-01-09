from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self
from typing import Literal, Union
from pydantic import HttpUrl, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
          # Use top level .env file (one level above ./app/)
          env_file="../../.env",
          env_ignore_empty=True,
          extra="ignore",
      )
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    SENTRY_DSN: Union[HttpUrl, None] = None
    POSTGRES_SERVER: str
    DB_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    PRODUCT_TOKEN: str = ""
    ORDER_TOKEN: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.DB_PORT,
            path=self.POSTGRES_DB,
        )
    
    @property
    def DATABASE_URL(self) -> str:
        # Construct database URL from components
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.DB_PORT}/{self.POSTGRES_DB}"
      
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        # For async SQLAlchemy operations
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.DB_PORT}/{self.POSTGRES_DB}"
  
settings = Settings()