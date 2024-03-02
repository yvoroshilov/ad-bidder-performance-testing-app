import datetime
import logging as log
import uuid
from typing import List, Dict

import httpx
from starlette import status

from ad_bidder_common.data_gen import gen_bid_request
from ad_bidder_common.model.openrtb.response import Bid, BidResponse
from ad_publisher.auction.algorithm import DefaultAuctionAlgorithm
from ad_publisher.constants import AD_BIDDER_ROOT
from ad_publisher.model import Auction, AdRequest, AdBidder


def init_auction(ad_request: AdRequest) -> Auction:
    # TODO need to insert into DB and get id
    auction = Auction(id=str(uuid.uuid4()), reserved_price=_get_reserved_price(), ad_request=ad_request,
                      bidders=_get_bidders(), algorithm=DefaultAuctionAlgorithm(), start_time=datetime.datetime.now())
    log.debug(f"Auction created: {auction}")
    return auction


def run_auction(auction: Auction) -> Dict[str, Bid]:
    log.info(f"Auction id={auction.id} started")
    bidders = _get_bidders()
    seat_bids = []
    for bidder in bidders:
        bid_response = _get_bid(bidder)
        seat_bids.append(bid_response.seatbid[0])
    bids = [bid for seat_bid in seat_bids for bid in seat_bid.bid]
    winners = auction.algorithm.calc_winner(bids, auction.reserved_price)
    _finish_auction(auction)
    log.info(f"Auction id={auction.id} finished")
    return winners


def _get_bid(bidder: AdBidder) -> BidResponse:
    bid_request = gen_bid_request()
    body = bid_request.model_dump(mode="json")
    log.debug("Sending bid request: " + str(body))
    with httpx.Client() as client:
        response = client.post(bidder.bid_request_url, json=body)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(f"Couldn't get ad response. Received: {str(response)}")
        return BidResponse.model_validate_json(response.content)


def _finish_auction(auction: Auction) -> Auction:
    auction.finish_time = datetime.datetime.now()
    return auction


def _get_reserved_price() -> float:
    return 1.0


def _get_bidders() -> List[AdBidder]:
    # TODO get from db
    return [AdBidder(id=_gen_id(), bid_request_url=AD_BIDDER_ROOT)]


def _gen_id() -> str:
    return str(uuid.uuid4())
