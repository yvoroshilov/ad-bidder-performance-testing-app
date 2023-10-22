import logging as log
import uuid
from random import Random

from fastapi import APIRouter

from ad_bidder_common.model.openrtb_request import BidRequest
from ad_bidder_common.model.openrtb_response import BidResponse

router = APIRouter()


@router.post("")
def post_bid_request(bid_request: BidRequest) -> BidResponse:
    log.debug(str(bid_request))
    bid_response = BidResponse.minimal(
        _gen_uuid() + "_resp", bid_request.id,
        bid_request.imp[0].id, Random().random() * 100)
    bid_response.ext = "passed post_bid_request: " + str(bid_request)
    return bid_response


def _gen_uuid() -> str:
    return str(uuid.uuid4())
