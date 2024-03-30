import logging as log

from pymongo import MongoClient
from pymongo.collection import Collection

from ad_bidder import config

_mongodb_client: MongoClient | None = None

_test_collection: Collection | None = None
_bid_response_collection: Collection | None = None
_bid_collection: Collection | None = None
_imp_collection: Collection | None = None
_html_collection: Collection | None = None


def init_db_client():
    global _mongodb_client, _test_collection, _bid_response_collection, _bid_collection, _imp_collection, _html_collection
    url = f"mongodb://{config.MONGODB_USERNAME}:{config.MONGODB_PASSWORD}@{config.MONGODB_HOST}"
    _mongodb_client = MongoClient(url, serverSelectionTimeoutMS=3000)
    _mongodb_client.server_info()
    log.debug("Connected to the MongoDB database!")

    collections = _mongodb_client[config.MONGODB_DB_NAME]
    _test_collection = collections.test
    _bid_response_collection = collections.bid_response
    _bid_collection = collections.bid
    _imp_collection = collections.imp
    _html_collection = collections.html


def shutdown_db_client():
    _mongodb_client.close()


def get_test_collection() -> Collection:
    return _test_collection


def get_bid_response_collection() -> Collection:
    return _bid_response_collection


def get_bid_collection() -> Collection:
    return _bid_collection


def get_imp_collection() -> Collection:
    return _imp_collection


def get_html_collection() -> Collection:
    return _html_collection
