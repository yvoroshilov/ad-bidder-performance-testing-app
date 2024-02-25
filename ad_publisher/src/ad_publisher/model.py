import datetime
from typing import List

from pydantic import BaseModel

from ad_bidder_common.model.openrtb.request import BidRequest
from ad_publisher.auction.auction_service import AuctionAlgorithm


class AdResponse(BaseModel):
    html: str


class Auction(BaseModel):
    id: str
    ad: "Ad"
    reserved_price: float
    start_time: datetime.datetime
    finish_time: datetime.datetime
    bid_request: BidRequest
    bidders: List["AdBidder"]
    algorithm: AuctionAlgorithm


class AdBidder(BaseModel):
    id: str


class AdBid(BaseModel):
    ad_bidder: "AdBidder"
    auction: "Auction"
    amount: float


class Ad:
    html: str
