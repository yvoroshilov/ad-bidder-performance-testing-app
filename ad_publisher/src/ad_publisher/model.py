import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel

from ad_bidder_common.model.openrtb.request import Content, Producer, Device, Geo, User, Data
from ad_bidder_common.model.openrtb.response import SeatBid
from ad_publisher.auction.algorithm import AuctionAlgorithm


class AdRequest(BaseModel):
    timestamp: datetime.datetime
    content: Content
    producer: Producer
    device: Device
    geo: Geo
    user: User
    data: Data


class AdResponse(BaseModel):
    html: str


class AdBidder(BaseModel):
    id: str
    bid_request_url: str


class Ad:
    html: str


class AuctionStatus(Enum):
    PENDING = 1
    RUNNING = 2
    FINISHED = 3


class Auction(BaseModel):
    id: str
    reserved_price: float
    start_time: datetime.datetime = None
    finish_time: datetime.datetime = None
    ad_request: AdRequest
    bidders: List[AdBidder]
    algorithm: AuctionAlgorithm
    bids: List[SeatBid] = None
    status: AuctionStatus = AuctionStatus.PENDING
