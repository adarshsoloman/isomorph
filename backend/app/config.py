from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "ISOMORPH"
    ENVIRONMENT: str = "development"
    PIPELINE_VERSION: str = "v0.1"

    # Database
    POSTGRES_USER: str = "isomorph"
    POSTGRES_PASSWORD: str = "isomorph"
    POSTGRES_DB: str = "isomorph_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = "postgresql://isomorph:isomorph@localhost:5432/isomorph_db"

    # External APIs
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")

    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Constants
    MIN_SIMILARITY_SCORE: float = 0.6
    CACHE_TTL: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
