import datetime
from typing import List, Dict

from ad_bidder_common.model.openrtb.request import Device, User, Impression
from pydantic import BaseModel


class AdRequest(BaseModel):
    timestamp: datetime.datetime
    device: Device
    user: User
    imps: List[Impression]


class AdResponse(BaseModel):
    imp_html: Dict[str, str]


class AdBidder(BaseModel):
    id: str
    bid_request_url: str


class Ad(BaseModel):
    html: str
