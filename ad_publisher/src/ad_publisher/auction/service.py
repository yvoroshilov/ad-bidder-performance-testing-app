import datetime
import logging as log
import uuid
from typing import List, Dict

from ad_bidder_common.data_gen import gen_bid_request
from ad_bidder_common.model.openrtb.response import Bid, BidResponse
from ad_publisher import ad_bidder_client
from ad_publisher.ad.model import AdRequest, AdBidder
from ad_publisher.auction.algorithm import DefaultAuctionAlgorithm
from ad_publisher.auction.model import Auction, BidStatus
from ad_publisher.constants import *


def init_auction(ad_request: AdRequest) -> Auction:
    # TODO need to insert into DB and get id
    auction = Auction(id=str(uuid.uuid4()), reserved_price=_get_reserved_price(), ad_request=ad_request,
                      bidders=_get_bidders(), algorithm=DefaultAuctionAlgorithm(), start_time=datetime.datetime.now())
    # TODO send auction to the
    log.debug(f"Auction created: {auction}")
    return auction


def run_auction(auction: Auction) -> Dict[str, str]:
    log.info(f"Auction id={auction.id} started")
    bidders = _get_bidders()
    seat_bids = []
    for bidder in bidders:
        bid_response = _get_bid(bidder, auction.ad_request)
        seat_bids.append(bid_response.seatbid[0])

    bids = [bid for seat_bid in seat_bids for bid in seat_bid.bid]
    imp_winner_bids = auction.algorithm.calc_winner(bids, auction.reserved_price)
    imp_html = _notify_bidders(imp_winner_bids, bids)
    _finish_auction(auction)
    log.info(f"Auction id={auction.id} finished")
    return imp_html


def _get_bid(bidder: AdBidder, ad_request: AdRequest) -> BidResponse:
    bid_request = gen_bid_request(ad_request.imps, ad_request.device, ad_request.user)
    return ad_bidder_client.post_bid_request(bidder, bid_request)


def _finish_auction(auction: Auction) -> Auction:
    auction.finish_time = datetime.datetime.now()
    return auction

def _notify_bidders(imp_winner_bids: Dict[str, Bid], bids: List[Bid]) -> Dict[str, str]:
    imp_html = {}
    for bid in bids:
        impid = bid.impid
        win_bid = imp_winner_bids[impid]
        if win_bid.id == bid.id:
            html = ad_bidder_client.post_notice(bid, impid, BidStatus.WIN)
            imp_html[impid] = html
        else:
            ad_bidder_client.post_notice(bid, impid, BidStatus.LOSS)
    return imp_html


def _get_reserved_price() -> float:
    return 1.0


def _get_bidders() -> List[AdBidder]:
    # TODO get from db
    return [AdBidder(id=_gen_id(), bid_request_url=AD_BIDDER_URL_BIDS_REQUEST)]


def _gen_id() -> str:
    return str(uuid.uuid4())
