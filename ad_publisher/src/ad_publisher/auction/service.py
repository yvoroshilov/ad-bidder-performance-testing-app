import datetime
import logging as log
from typing import List, Dict

from bson import ObjectId

import ad_publisher.db.config as db
from ad_bidder_common.model.openrtb.request import BidRequest, Impression
from ad_bidder_common.model.openrtb.response import Bid, BidResponse
from ad_publisher import ad_bidder_client
from ad_publisher.ad.model import AdRequest, AdBidder
from ad_publisher.auction.algorithm import DefaultAuctionAlgorithm
from ad_publisher.auction.model import Auction, BidStatus, AuctionStatus


def run_auction(ad_request: AdRequest) -> Dict[str, str]:
    _insert_imps_into_db(ad_request.imps)
    auction = _create_auction(ad_request)
    log.info(f"Auction id={auction.id} started")

    bidders = auction.bidders
    seat_bids = []
    for bidder in bidders:
        bid_response = _get_bid(bidder, auction.ad_request)
        seat_bids += bid_response.seatbid

    bids = [bid for seat_bid in seat_bids for bid in seat_bid.bid]
    imp_winner_bids = auction.algorithm.calc_winner(bids, auction.reserved_price)
    imp_html = _notify_won_bidders(imp_winner_bids, bids)
    _update_winners_in_imps(auction, imp_winner_bids)
    _finish_auction(auction)
    log.info(f"Auction id={auction.id} finished")
    return imp_html


def _update_winners_in_imps(auction: Auction, imp_winner_bids: dict[str, Bid]):
    for impid in imp_winner_bids:
        db.get_auction_collection().update_one({
            "_id": ObjectId(auction.id),
            "ad_request.imps.id": impid
        }, {"$set": {
            "ad_request.imps.$.ext.winner": imp_winner_bids[impid].dump_mongo()
        }})


def _create_auction(ad_request: AdRequest) -> Auction:
    reserved_price = _get_reserved_price()
    bidders = _get_bidders()
    algorithm = DefaultAuctionAlgorithm()
    start_time = datetime.datetime.now()
    auction = Auction(reserved_price=reserved_price, ad_request=ad_request,
                      bidders=bidders, algorithm=algorithm, start_time=start_time)

    insert_result = db.get_auction_collection().insert_one(auction.dump_mongo())
    auction.id = str(insert_result.inserted_id)
    log.debug(f"Auction created: {auction}")

    return auction


def _get_bid(bidder: AdBidder, ad_request: AdRequest) -> BidResponse:
    bid_request = BidRequest(imp=ad_request.imps, device=ad_request.device, user=ad_request.user)
    insert_result = db.get_bid_request_collection().insert_one(bid_request.dump_mongo())
    bid_request.id = str(insert_result.inserted_id)
    return ad_bidder_client.post_bid_request(bidder, bid_request)


def _finish_auction(auction: Auction) -> Auction:
    auction.finish_time = datetime.datetime.now()
    db.get_auction_collection().update_one({"_id": ObjectId(auction.id)}, {
        "$set": {"finish_time": auction.finish_time, "status": AuctionStatus.FINISHED.value}})
    return auction


def _notify_won_bidders(imp_winner_bids: Dict[str, Bid], bids: List[Bid]) -> Dict[str, str]:
    imp_html = {}
    for bid in bids:
        impid = bid.impid
        win_bid = imp_winner_bids.get(impid)
        if win_bid is not None and win_bid.id == bid.id:
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


def _insert_imps_into_db(imps: list[Impression]):
    for imp in imps:
        insert_result = db.get_imp_collection().insert_one(imp.dump_mongo())
        imp.id = str(insert_result.inserted_id)
