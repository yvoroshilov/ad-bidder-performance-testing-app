import logging as log

import prometheus_client as prom
from fastapi import APIRouter
from starlette.responses import Response

from ad_bidder.service import bid_service
from ad_bidder_common.model.openrtb.request import BidRequest
from ad_bidder_common.model.openrtb.response import BidResponse

router = APIRouter()

summary = prom.Summary(
    "post_bid_summary",
    "Post Bid summary",
)


@router.post("")
@summary.time()
def post_bid_request(bid_request: BidRequest) -> BidResponse:
    log.debug(str(bid_request.ext))
    bid_response = bid_service.generate_bid(bid_request)
    bid_response.ext = "passed post_bid_request: " + str(bid_request)
    return bid_response


@router.get("/metrics")
def get_metrics():
    return Response(
        content=prom.generate_latest(),
        media_type="text/plain"
    )
