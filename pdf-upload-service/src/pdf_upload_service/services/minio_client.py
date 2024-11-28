from minio import Minio
from pdf_upload_service.core.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)


def create_bucket_if_not_exists(bucket_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)


def upload_file_to_minio(file_data, file_name: str):
    # I love stack overflow (I also love reddit)
    # Since we're streaming the file, we need to know the length
    # Let's read the content into memory for simplicity
    content = file_data.read()
    file_data.seek(0)  # Reset the pointer again after reading
    file_size = len(content)

    minio_client.put_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=file_name,
        data=file_data,
        length=file_size,
        content_type='application/pdf'
    )


create_bucket_if_not_exists(settings.MINIO_BUCKET_NAME)
