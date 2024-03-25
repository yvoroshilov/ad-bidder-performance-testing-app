import logging as log

from pymongo import MongoClient
from pymongo.collection import Collection

from ad_publisher import config

_mongodb_client: MongoClient | None = None

test_collection: Collection | None = None


def init_db_client():
    global _mongodb_client, test_collection
    url = f"mongodb://{config.MONGODB_USERNAME}:{config.MONGODB_PASSWORD}@{config.MONGODB_HOST}"
    _mongodb_client = MongoClient(url, serverSelectionTimeoutMS=3000)
    _mongodb_client.server_info()
    test_collection = _mongodb_client[config.MONGODB_DB_NAME].test
    log.debug("Connected to the MongoDB database!")


def shutdown_db_client():
    _mongodb_client.close()


def get_test_collection() -> Collection:
    return test_collection
