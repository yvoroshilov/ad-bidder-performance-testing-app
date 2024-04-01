import logging

from pydantic import BaseModel

import db_config as db
from ad_bidder_common.model.openrtb.util import MongoDbMixin

BIDDER_N = 1
HTML_N = 10


def gen_initial_db_data():
    db.init_db_client()
    _clean_db()
    _gen_bidders()
    _gen_html()
    db.shutdown_db_client()


def _clean_db():
    for col in (db.get_bidder_collection(), db.get_html_collection()):
        col.delete_many({})


def _gen_bidders():
    class AdBidder(BaseModel, MongoDbMixin):
        id: str
        bid_request_url: str

    bid_request_url = "http://ad_bidder/api/v1/bids/request"
    bidders = [AdBidder(id="dummy", bid_request_url=bid_request_url) for _ in range(BIDDER_N)]
    bidders = list(map(lambda bidder: bidder.dump_mongo(), bidders))
    insert_result = db.get_bidder_collection().insert_many(bidders)
    logging.debug(f"Inserted bidders: {insert_result}")


def _gen_html():
    htmls = [{"html": "html" + str(i)} for i in range(HTML_N)]
    insert_result = db.get_html_collection().insert_many(htmls)
    logging.debug(f"Inserted: {insert_result}")


if __name__ == '__main__':
    gen_initial_db_data()
