import logging as log
import random
import uuid
from typing import List

from bson import ObjectId

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

    _insert_imps_into_db(bid_request.imp)
    seat_bid = _create_seat_bid(bid_request.imp, bid_request)
    bid_response = _create_bid_response(seat_bid, bid_request)
    log.debug(f"Generated bid response id={bid_response.id}")
    return bid_response


def process_notice(bid_id: str, imp_id: str, status: int) -> str | None:
    bid_status = BidStatus(status)
    if bid_status == BidStatus.WIN:
        db.get_bid_collection().update_one({"_id": ObjectId(bid_id)}, {"$set": {"ext.win": True}})
        log.debug(f"Bid {bid_id} won")
        process_result = _get_html(bid_id, imp_id)
    else:
        db.get_bid_collection().update_one({"_id": ObjectId(bid_id)}, {"$set": {"ext.win": False}})
        log.debug(f"Bid {bid_id} won")
        process_result = None

    return process_result


def _create_bid_response(seat_bid: SeatBid, bid_request: BidRequest) -> BidResponse:
    bid_response = BidResponse(id=bid_request.id, seatbid=[seat_bid], bidid=str(uuid.uuid4()))

    result = db.get_bid_response_collection().insert_one({"_id": ObjectId(bid_request.id), **bid_response.dump_mongo()})
    bid_response.id = str(result.inserted_id)

    return bid_response


def _create_seat_bid(imps: List[Impression], bid_request: BidRequest) -> SeatBid:
    bids = []
    for imp in imps:
        bid = Bid(id="dummy", impid=imp.id, price=round(random.random() * 10, 2), ext={})
        bids.append(bid)
        log.debug(f"Bid for imp id={imp.id} was generated with price={bid.price}")

    result = db.get_bid_collection().insert_many(map(Bid.dump_mongo, bids))
    for i, inserted_id in enumerate(result.inserted_ids):
        inserted_id_str = str(inserted_id)
        bids[i].id = inserted_id_str
        nurl = compose_path(AD_BIDDER_BID_ROOT, AD_BIDDER_BID_NOTICE.format(bid_id=inserted_id_str))
        bids[i].nurl = nurl
        db.get_bid_collection().update_one({"_id": inserted_id}, {"$set": {"nurl": nurl}})

    return SeatBid(bid=bids)


def _insert_imps_into_db(imps: list[Impression]):
    for imp in imps:
        # TODO WARNING possible id clash
        find_result = db.get_imp_collection().find_one({"_id": ObjectId(imp.id)})
        if find_result is None:
            insert_result = db.get_imp_collection().insert_one({"_id": ObjectId(imp.id), **imp.dump_mongo()})
            imp.id = str(insert_result.inserted_id)


def _get_html(bid_id: str, imp_id: str) -> str:
    html_count = db.get_html_collection().estimated_document_count()
    log.debug(f"{html_count} elements in html collection")

    skip_n = random.randint(0, html_count - 1)
    log.debug(f"Getting {skip_n}th element")

    cursor = db.get_html_collection().aggregate([{"$skip": skip_n}, {"$limit": 1}])
    result_html = list(cursor)[0]["html"]
    log.debug(f"Generated html: {result_html}")

    db.get_bid_collection().update_one({"_id": ObjectId(bid_id)}, {"$set": {"ext.result_html": result_html}})

    return result_html
