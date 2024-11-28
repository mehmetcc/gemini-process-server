from fastapi import APIRouter, UploadFile, File, HTTPException
from pdf_upload_service.core.config import settings
from pdf_upload_service.services.minio_client import (
    create_bucket_if_not_exists, upload_file_to_minio)
from pdf_upload_service.services.celery_tasks import publish_preprocessing_task
import uuid

router = APIRouter()

MAX_FILE_SIZE_MB = 5


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file extension.")

    contents = await file.read() # This is stored in memory. I'm not sure if there's a better way.
    file_size_mb = len(contents) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400, detail="File size exceeds the limit.")

    await file.seek(0)

    file_uuid = str(uuid.uuid4())

    create_bucket_if_not_exists(settings.MINIO_BUCKET_NAME)
    upload_file_to_minio(file.file, file_uuid)
    publish_preprocessing_task(file_uuid)

    return {"message": "File uploaded successfully.", "uuid": file_uuid}
