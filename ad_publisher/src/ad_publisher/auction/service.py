import datetime
import logging as log
from typing import List, Dict

import ad_publisher.db.config as db
from ad_bidder_common.model.openrtb.request import BidRequest
from ad_bidder_common.model.openrtb.response import Bid, BidResponse
from ad_publisher import ad_bidder_client
from ad_publisher.ad.model import AdRequest, AdBidder
from ad_publisher.auction.algorithm import DefaultAuctionAlgorithm
from ad_publisher.auction.model import Auction, BidStatus


def run_auction(ad_request: AdRequest) -> Dict[str, str]:
    auction = create_auction(ad_request)
    log.info(f"Auction id={auction.id} started")

    bidders = _get_bidders()
    seat_bids = []
    for bidder in bidders:
        bid_response = _get_bid(bidder, auction.ad_request)
        seat_bids += bid_response.seatbid

    bids = [bid for seat_bid in seat_bids for bid in seat_bid.bid]
    imp_winner_bids = auction.algorithm.calc_winner(bids, auction.reserved_price)
    imp_html = _notify_bidders(imp_winner_bids, bids)
    _finish_auction(auction)
    log.info(f"Auction id={auction.id} finished")
    return imp_html


def create_auction(ad_request: AdRequest) -> Auction:
    reserved_price = _get_reserved_price()
    bidders = _get_bidders()
    algorithm = DefaultAuctionAlgorithm()
    start_time = datetime.datetime.now()
    auction = Auction(reserved_price=reserved_price, ad_request=ad_request,
                      bidders=bidders, algorithm=algorithm, start_time=start_time)

    insert_result = db.get_auction_collection().insert_one(auction.dump_mongo())
    auction.id = insert_result.inserted_id
    log.debug(f"Auction created: {auction}")

    return auction


def _get_bid(bidder: AdBidder, ad_request: AdRequest) -> BidResponse:
    bid_request = BidRequest(imp=ad_request.imps, device=ad_request.device, user=ad_request.user)
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
            html = ad_bidder_client.post_notice(BidStatus.WIN, bid)
            imp_html[impid] = html
        else:
            ad_bidder_client.post_notice(BidStatus.LOSS, bid)
    return imp_html


# might be in properties
def _get_reserved_price() -> float:
    return 1.0


def _get_bidders() -> List[AdBidder]:
    ad_bidders = list(db.get_bidder_collection().find())
    return AdBidder.validate_mongo_many(ad_bidders)
