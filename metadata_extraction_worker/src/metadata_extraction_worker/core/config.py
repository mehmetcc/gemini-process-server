import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'root')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'arootpassword')
    MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME', 'pdf-uploads')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')

    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'metadata_db')
    MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'metadata_collection')


settings = Settings()
