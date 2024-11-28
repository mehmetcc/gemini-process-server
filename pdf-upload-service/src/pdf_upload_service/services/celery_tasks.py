from celery import Celery
from pdf_upload_service.core.config import settings

celery_app = Celery('pdf_upload_service', broker=settings.CELERY_BROKER_URL)


def publish_preprocessing_task(file_uuid: str):
    celery_app.send_task(
        'metadata_extraction_worker.process_pdf', args=[file_uuid])
