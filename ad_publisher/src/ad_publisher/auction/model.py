import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict

from ad_bidder_common.model.openrtb.response import SeatBid
from ad_publisher.ad.model import AdRequest, AdBidder
from ad_publisher.auction.algorithm import AuctionAlgorithm


class AuctionStatus(Enum):
    PENDING = 1
    RUNNING = 2
    FINISHED = 3


class Auction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    reserved_price: float
    start_time: datetime.datetime = None
    finish_time: datetime.datetime = None
    ad_request: AdRequest
    bidders: List[AdBidder]
    algorithm: AuctionAlgorithm
    bids: List[SeatBid] = None
    status: AuctionStatus = AuctionStatus.PENDING


class BidStatus(Enum):
    WIN = 1
    LOSS = 2
