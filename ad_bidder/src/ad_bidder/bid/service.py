import logging as log
import random
import uuid
from typing import List

from ad_bidder_common.model.openrtb.request import BidRequest, Impression
from ad_bidder_common.model.openrtb.response import BidResponse, SeatBid, Bid


def generate_bid(bid_request: BidRequest) -> BidResponse:
    log.debug(f"Processing request id={bid_request.id} with imp count={len(bid_request.imp)}")
    if len(bid_request.imp) == 0:
        raise Exception("Amount if impression cannot be 0")

    seat_bid = _process_bid_request_info(bid_request.imp, bid_request)
    bid_response = BidResponse(id=bid_request.id, seatbid=[seat_bid], bidid=str(uuid.uuid4()))
    log.debug(f"Generated bid response id={bid_response.id}")
    return bid_response


def _process_bid_request_info(imps: List[Impression], bid_request: BidRequest) -> SeatBid:
    bids = []
    for imp in imps:
        bid_price = round(random.random() * 10, 2)
        bid = Bid(id=str(uuid.uuid4()), impid=imp.id, price=bid_price)
        bids.append(bid)
        log.debug(f"Bid for imp id={imp.id} was generated with price={bid.price}")
    return SeatBid(bid=bids)
