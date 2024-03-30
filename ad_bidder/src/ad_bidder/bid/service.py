import logging as log
import random
import uuid
from typing import List

import ad_bidder.db.config as db
from ad_bidder.bid.model import BidStatus
from ad_bidder.constant import AD_BIDDER_BID_NOTICE, AD_BIDDER_BID_ROOT, compose_path
from ad_bidder_common.model.openrtb.request import BidRequest, Impression
from ad_bidder_common.model.openrtb.response import BidResponse, SeatBid, Bid


def generate_bid(bid_request: BidRequest) -> BidResponse:
    log.debug(f"Processing request id={bid_request.id} with imp count={len(bid_request.imp)}")
    # TODO move to pydantic model
    if len(bid_request.imp) == 0:
        raise Exception("Amount of impressions cannot be 0")

    _create_imp(bid_request.imp)
    seat_bid = _create_seat_bid(bid_request.imp, bid_request)
    bid_response = _create_bid_response(seat_bid, bid_request)
    log.debug(f"Generated bid response id={bid_response.id}")
    return bid_response


def process_notice(bid_id: str, imp_id: str, status: int) -> str | None:
    bid_status = BidStatus(status)
    process_result = None
    if bid_status == BidStatus.WIN:
        db.get_bid_collection().update_one({"_id": bid_id}, {"$set": {"ext.win": True}})
        log.debug(f"Bid {bid_id} won")
        process_result = _generate_html(bid_id, imp_id)
    else:
        process_result = None

    return process_result


def _create_bid_response(seat_bid: SeatBid, bid_request: BidRequest) -> BidResponse:
    bid_response = BidResponse(id=bid_request.id, seatbid=[seat_bid], bidid=str(uuid.uuid4()))

    result = db.get_bid_response_collection().insert_one(bid_response.dump_mongo())
    bid_response.id = result.inserted_id

    return bid_response


def _create_seat_bid(imps: List[Impression], bid_request: BidRequest) -> SeatBid:
    bids = []
    for imp in imps:
        bid = Bid(id=str(uuid.uuid4()), impid=imp.id, price=round(random.random() * 10, 2))
        bid.nurl = compose_path(AD_BIDDER_BID_ROOT, AD_BIDDER_BID_NOTICE.format(bid_id = bid.id))
        bids.append(bid)
        log.debug(f"Bid for imp id={imp.id} was generated with price={bid.price}")

    result = db.get_bid_collection().insert_many(map(Bid.dump_mongo, bids))
    for i, inserted_id in enumerate(result.inserted_ids):
        bids[i].id = inserted_id

    return SeatBid(bid=bids)


def _create_imp(imps: List[Impression]):
    for imp in imps:
        result = db.get_imp_collection().insert_one(imp.dump_mongo())
        imp.id = result.inserted_id


def _generate_html(bid_id: str, imp_id: str) -> str:
    html_count = db.get_html_collection().estimated_document_count()
    log.debug(f"{html_count} elements in html collection")

    skip_n = random.randint(0, html_count - 1)
    log.debug(f"Getting {skip_n}th element")

    cursor = db.get_html_collection().aggregate([{"$skip": skip_n}, {"$limit": 1}])
    result_html = list(cursor)[0]
    log.debug(f"Generated html: {result_html.html}")

    db.get_bid_collection().update_one({"_id": bid_id}, {"$set": {"ext.html": result_html.html}})

    return result_html.html
