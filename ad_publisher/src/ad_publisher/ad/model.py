import datetime
from typing import List

from pydantic import BaseModel

from ad_bidder_common.model.openrtb.request import Device, User, Impression


class AdRequest(BaseModel):
    timestamp: datetime.datetime
    device: Device
    user: User
    imps: List[Impression]


class AdResponse(BaseModel):
    html: str


class AdBidder(BaseModel):
    id: str
    bid_request_url: str


class Ad(BaseModel):
    html: str
