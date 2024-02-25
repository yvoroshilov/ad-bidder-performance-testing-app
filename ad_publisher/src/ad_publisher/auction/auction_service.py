from abc import abstractmethod, ABC
from typing import List

from ad_bidder_common.model.openrtb.request import BidRequest
from ad_publisher.model import AdBid, Auction, Ad


class AuctionAlgorithm(ABC):
    @abstractmethod
    def calc_winner(self, bids: List[AdBid], reserved_price: float = None):
        pass


class DefaultAuctionAlgorithm(AuctionAlgorithm):
    def calc_winner(self, bids: List[AdBid], reserved_price: float = None):
        pass


def init_auction(ad: Ad, ad_request: BidRequest) -> Auction:
    pass


def _get_reserved_price() -> float:
    return 1.0


def _get_bidders() -> float:
    pass
