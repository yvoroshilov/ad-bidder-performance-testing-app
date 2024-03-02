import datetime
import logging as log
import random
import uuid
from abc import abstractmethod, ABC
from typing import List, Dict

from ad_bidder_common.model.openrtb.response import Bid
from ad_publisher.model import SeatBid, Auction, AdRequest, AdBidder


class AuctionAlgorithm(ABC):
    @abstractmethod
    def calc_winner(self, bids: List[Bid], reserved_price: float) -> List[str, Bid]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class DefaultAuctionAlgorithm(AuctionAlgorithm):
    def calc_winner(self, bids: List[Bid], reserved_price: float) -> Dict[str, Bid]:
        log.debug("Start calc_winner")

        eligible_bids = filter(lambda bid: bid.price >= reserved_price, bids)
        log.debug(f"Eligible bids count={len(eligible_bids)}")

        impid_bids = {}
        for bid in eligible_bids:
            if bid.impid in impid_bids:
                impid_bids[bid.impid].append(bid)
            else:
                impid_bids[bid.impid] = [bid]

        winners = {}
        for impid in impid_bids:
            bids_for_impid = impid_bids[impid]
            highest_price_bid = max(bids_for_impid, key=lambda bid: bid.price)
            winners[impid] = highest_price_bid
            log.debug(f"Winner for impid={impid} is price={highest_price_bid}")

        return winners

    def name(self) -> str:
        return "First highest"


class SecondHighestAuctionAlgorithm(AuctionAlgorithm):
    def calc_winner(self, bids: List[Bid], reserved_price: float) -> List[str, Bid]:
        pass

    def name(self) -> str:
        return "Second highest"



def init_auction(ad_request: AdRequest) -> Auction:
    # TODO need to insert into DB and get id
    auction = Auction(id=str(uuid.uuid4()), reserved_price=_get_reserved_price(), ad_request=ad_request,
                      bidders=_get_bidders(), algorithm=DefaultAuctionAlgorithm(), start_time=datetime.datetime.now())
    log.debug(f"Auction created: {auction}")
    return auction


def run_auction(auction: Auction) -> List[str, Bid]:
    log.info(f"Auction id={auction.id} started")
    bidders = _get_bidders()
    seat_bids = []
    for bidder in bidders:
        # TODO Get bid from bidder
        bids = [Bid(id=_gen_id(), impid=_gen_id(), price=random.randrange(1, 100))]
        seat_bids.append(SeatBid(bid=bids))
    bids = [bid for seat_bid in seat_bids for bid in seat_bid.bid]
    winner = auction.algorithm.calc_winner(bids, auction.reserved_price)
    log.info(f"Auction id={auction.id} finished")
    return winner


def finish_auction(auction: Auction) -> Auction:
    auction.finish_time = datetime.datetime.now()
    return auction


def _get_reserved_price() -> float:
    return 1.0


def _get_bidders() -> List[AdBidder]:
    return [AdBidder(id=_gen_id()), AdBidder(id=_gen_id())]


def _gen_id() -> str:
    return str(uuid.uuid4())
