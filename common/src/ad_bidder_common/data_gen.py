import uuid
from typing import List

from ad_bidder_common.model.openrtb.request import BidRequest, Impression, User, Device


def gen_bid_request(imps: List[Impression], device: Device, user: User) -> BidRequest:
    return BidRequest(imp=imps, device=device, user=user, id=str(uuid.uuid4()))
