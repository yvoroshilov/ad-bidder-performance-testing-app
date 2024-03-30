import datetime
from typing import List, Dict

from pydantic import BaseModel

from ad_bidder_common.model.openrtb.request import Device, User, Impression
from ad_bidder_common.model.openrtb.util import MongoDbMixin


class AdRequest(BaseModel, MongoDbMixin):
    timestamp: datetime.datetime
    device: Device
    user: User
    imps: List[Impression]


class AdResponse(BaseModel, MongoDbMixin):
    imp_html: Dict[str, str]


class AdBidder(BaseModel, MongoDbMixin):
    id: str
    bid_request_url: str


class Ad(BaseModel, MongoDbMixin):
    html: str
