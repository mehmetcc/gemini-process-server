from pymongo import MongoClient, errors
from metadata_extraction_worker.core.config import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
except errors.ServerSelectionTimeoutError as err:
    logger.error(f"Could not connect to MongoDB: {err}")
    raise

db = client[settings.MONGODB_DATABASE]
collection = db[settings.MONGODB_COLLECTION]


def store_metadata(file_uuid: str, metadata: dict):
    try:
        metadata['file_uuid'] = file_uuid
        collection.insert_one(metadata)
    except errors.PyMongoError as e:
        logger.error(f"Error storing metadata for file '{file_uuid}': {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error storing metadata for file '{
                         file_uuid}': {e}")
        raise
