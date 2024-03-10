import logging as log
from typing import Optional

import prometheus_client as prom
from fastapi import APIRouter
from starlette.responses import Response

from ad_bidder.bid import service as bid_service
from ad_bidder.bid.model import BidStatus
from ad_bidder.bid.service import generate_html
from ad_bidder.constant import *
from ad_bidder_common.model.openrtb.request import BidRequest
from ad_bidder_common.model.openrtb.response import BidResponse

router = APIRouter()

summary = prom.Summary(
    "post_bid_summary",
    "Post Bid summary",
)


@summary.time()
@router.post(AD_BIDDER_BID_REQUEST)
def post_bid_request(bid_request: BidRequest) -> BidResponse:
    log.debug(str(bid_request.ext))
    bid_response = bid_service.generate_bid(bid_request)
    bid_response.ext = "passed post_bid_request: " + str(bid_request)
    return bid_response


@router.post(AD_BIDDER_BID_NOTICE)
def post_notice(bid_id: str, imp_id: str, status: int) -> Optional[str]:
    bid_status = BidStatus(status)
    if bid_status == BidStatus.WIN:
        return generate_html(bid_id, imp_id)
    else:
        return None


@router.get(AD_BIDDER_BID_METRICS)
def get_metrics():
    return Response(
        content=prom.generate_latest(),
        media_type="text/plain"
    )
