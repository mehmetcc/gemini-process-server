from fastapi import APIRouter, UploadFile, File, HTTPException
from pdf_upload_service.core.config import settings
from pdf_upload_service.services.minio_client import upload_file_to_minio
from pdf_upload_service.services.celery_tasks import publish_preprocessing_task
import uuid

router = APIRouter()

MAX_FILE_SIZE_MB = 5
ALLOWED_FILE_EXTENSION = ".pdf"


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(ALLOWED_FILE_EXTENSION):
        raise HTTPException(status_code=400, detail="Invalid file extension.")

    # This is stored in memory. I'm not sure if there's a better way.
    contents = await file.read()
    file_size_mb = len(contents) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400, detail="File size exceeds the limit.")

    await file.seek(0)

    file_uuid = str(uuid.uuid4())

    upload_file_to_minio(file.file, file_uuid)
    publish_preprocessing_task(file_uuid)

    return {"message": "File uploaded successfully.", "uuid": file_uuid}
