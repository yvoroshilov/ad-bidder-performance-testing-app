from pymongo import MongoClient
from pymongo.collection import Collection

_mongodb_client: MongoClient | None = None

_test_collection: Collection | None = None
_html_collection: Collection | None = None
_bidder_collection: Collection | None = None


def init_db_client():
    global _mongodb_client, _html_collection, _bidder_collection
    url = f"mongodb://admin:admin@localhost:27017"
    _mongodb_client = MongoClient(url, serverSelectionTimeoutMS=3000)
    _mongodb_client.server_info()

    ad_bid_db = _mongodb_client["ad_bid"]
    _html_collection = ad_bid_db.html

    ad_publish_db = _mongodb_client["ad_publish"]
    _bidder_collection = ad_publish_db.bidder


def shutdown_db_client():
    _mongodb_client.close()


def get_html_collection() -> Collection:
    return _html_collection


def get_bidder_collection() -> Collection:
    return _bidder_collection
