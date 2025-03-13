from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Literal, Annotated
from pydantic import (AnyUrl, HttpUrl, BeforeValidator, computed_field, PostgresDsn)

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    """Settings Class that will be used to setup up the db connection

    Parent Class:
        BaseSettings (_type_): BaseSettings from pydantic_settings module
    """
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")
    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "prod"] = "local"
    
    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local" or self.ENVIRONMENT == "staging":
            print(f"starting on: http://{self.DOMAIN}")
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"
    
    @computed_field
    @property
    def db_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return "localhost"
        return "db"
    
    CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    
    PROJECT_NAME: str
    # POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    
    BASE_TRADER_JOES: str
    APPEND_TRADER_JOES: str
    
    BASE_WHOLEFOODS: str
    APPEND_WHOLEFOODS: str
        
    BASE_LIDL: str
    APPEND_LIDL: str
    
    BASE_FOODBAZAAR: str
    
    BASIC_GROCERIES: str
    
    OLLAMA_HOST: str
    OLLAMA_MODEL: str
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            host=self.db_host,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
        )
    
settings = Settings()