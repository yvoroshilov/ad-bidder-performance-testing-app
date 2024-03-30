import logging as log

from pymongo import MongoClient
from pymongo.collection import Collection

from ad_publisher import config

_mongodb_client: MongoClient | None = None

_test_collection: Collection | None = None
_auction_collection: Collection | None = None
_bidder_collection: Collection | None = None


def init_db_client():
    global _mongodb_client, _test_collection, _auction_collection, _bidder_collection
    url = f"mongodb://{config.MONGODB_USERNAME}:{config.MONGODB_PASSWORD}@{config.MONGODB_HOST}"
    _mongodb_client = MongoClient(url, serverSelectionTimeoutMS=3000)
    _mongodb_client.server_info()
    log.debug("Connected to the MongoDB database!")

    db = _mongodb_client[config.MONGODB_DB_NAME]
    _test_collection = db.test
    _auction_collection = db.auction
    _bidder_collection = db.bidder


def shutdown_db_client():
    _mongodb_client.close()


def get_test_collection() -> Collection:
    return _test_collection


def get_auction_collection() -> Collection:
    return _auction_collection


def get_bidder_collection() -> Collection:
    return _bidder_collection
