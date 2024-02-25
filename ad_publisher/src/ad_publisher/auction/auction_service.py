import datetime
import logging as log
import random
import uuid
from abc import abstractmethod, ABC
from typing import List

from ad_bidder_common.model.openrtb.response import Bid
from ad_publisher.model import SeatBid, Auction, AdRequest, AdBidder


class AuctionAlgorithm(ABC):
    @abstractmethod
    def calc_winner(self, bids: List[SeatBid], reserved_price: float = None) -> SeatBid:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class DefaultAuctionAlgorithm(AuctionAlgorithm):
    def name(self) -> str:
        return "Default"

    def calc_winner(self, bids: List[SeatBid], reserved_price: float = None) -> SeatBid:
        pass


def init_auction(ad_request: AdRequest) -> Auction:
    # TODO need to insert into DB and get id
    auction = Auction(id=str(uuid.uuid4()), reserved_price=_get_reserved_price(), ad_request=ad_request,
                      bidders=_get_bidders(), algorithm=DefaultAuctionAlgorithm(), start_time=datetime.datetime.now())
    log.debug(f"Auction created: {auction}")
    return auction


def run_auction(auction: Auction) -> SeatBid:
    log.info(f"Auction id={auction.id} started")
    bidders = _get_bidders()
    seat_bids = []
    # TODO query ad bidder
    for bidder in bidders:
        bid = Bid(id=_gen_id(), impid=_gen_id(), price=random.randrange(1, 100))
        seat_bids.append(SeatBid(bid=[bid]))
    winner = auction.algorithm.calc_winner(seat_bids, auction.reserved_price)
    log.info(f"Auction id={auction.id} finished. Winner: {winner}")


def finish_auction(auction: Auction) -> Auction:
    auction.finish_time = datetime.datetime.now()
    return auction


def _get_reserved_price() -> float:
    return 1.0


def _get_bidders() -> List[AdBidder]:
    return [AdBidder(id=_gen_id())]


def _gen_id() -> str:
    return str(uuid.uuid4())
