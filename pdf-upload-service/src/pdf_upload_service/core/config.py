from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    # MinIO Configuration
    MINIO_ENDPOINT: str = Field(..., alias='MINIO_ENDPOINT')
    MINIO_ACCESS_KEY: str = Field(..., alias='MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = Field(..., alias='MINIO_SECRET_KEY')
    MINIO_BUCKET_NAME: str = Field(..., alias='MINIO_BUCKET_NAME')

    # Celery Configuration
    CELERY_BROKER_URL: str = Field(..., alias='CELERY_BROKER_URL')

    # Use SettingsConfigDict for Pydantic v2
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent.parent / '.env'),
        env_file_encoding='utf-8',
    )


settings = Settings()
