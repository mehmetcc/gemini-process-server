from celery import Celery
from metadata_extraction_worker.core.config import settings
from metadata_extraction_worker.services.minio_client import get_pdf_file
from metadata_extraction_worker.services.mongodb_client import store_metadata
import fitz
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery('metadata_extraction_worker',
                    broker=settings.CELERY_BROKER_URL)
celery_app.conf.task_routes = {
    'metadata_extraction_worker.process_pdf': {'queue': 'pdf_queue'}}


@celery_app.task(name='metadata_extraction_worker.process_pdf', bind=True, max_retries=3)
def process_pdf(self, file_uuid: str):
    try:
        pdf_data = get_pdf_file(file_uuid)

        doc = fitz.open(stream=pdf_data, filetype='pdf')
        metadata = {}
        metadata['title'] = doc.metadata.get('title')
        metadata['author'] = doc.metadata.get('author')
        metadata['subject'] = doc.metadata.get('subject')
        metadata['keywords'] = doc.metadata.get('keywords')
        metadata['creationDate'] = doc.metadata.get('creationDate')
        metadata['modDate'] = doc.metadata.get('modDate')
        metadata['number_of_pages'] = doc.page_count

        toc = doc.get_toc()
        metadata['table_of_contents'] = toc  # A list of lists

        text = ""
        for page in doc:
            text += page.get_text('markdown')

        metadata['content'] = text

        store_metadata(file_uuid, metadata)
        logger.info(f"Successfully processed file '{file_uuid}'")

    except Exception as e:
        logger.exception(f"Error processing file '{file_uuid}': {e}")
        self.retry(exc=e, countdown=5)
