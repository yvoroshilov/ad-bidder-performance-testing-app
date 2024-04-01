import datetime
from enum import Enum
from typing import List, Any

from pydantic import BaseModel, ConfigDict, field_serializer

from ad_bidder_common.model.openrtb.response import SeatBid
from ad_bidder_common.model.openrtb.util import MongoDbMixin
from ad_publisher.ad.model import AdRequest, AdBidder
from ad_publisher.auction.algorithm import AuctionAlgorithm


class AuctionStatus(int, Enum):
    PENDING = 1
    RUNNING = 2
    FINISHED = 3


class Auction(BaseModel, MongoDbMixin):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = None
    reserved_price: float
    start_time: datetime.datetime = None
    finish_time: datetime.datetime = None
    ad_request: AdRequest
    bidders: List[AdBidder]
    algorithm: AuctionAlgorithm
    bids: List[SeatBid] = None
    status: AuctionStatus = AuctionStatus.PENDING

    @field_serializer("algorithm", mode="wrap")
    @classmethod
    def algorithm_serializer(cls, algorithm: Any, handler, info):
        return str(algorithm)


class BidStatus(Enum):
    WIN = 1
    LOSS = 2
