from minio import Minio, S3Error
from metadata_extraction_worker.core.config import settings
import logging

logger = logging.getLogger(__name__)

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)


def get_pdf_file(file_uuid: str):
    try:
        response = minio_client.get_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=file_uuid
        )
        data = response.read()
        response.close()
        response.release_conn()
        return data
    except S3Error as e:
        logger.error(f"Error fetching file '{file_uuid}' from MinIO: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error fetching file '{file_uuid}': {e}")
        raise
