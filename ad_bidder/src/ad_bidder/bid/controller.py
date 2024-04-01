import logging as log

import prometheus_client as prom
from fastapi import APIRouter
from starlette.responses import Response

from ad_bidder.bid import service as bid_service
from ad_bidder.constant import *
from ad_bidder_common.model.openrtb.request import BidRequest
from ad_bidder_common.model.openrtb.response import BidResponse

router = APIRouter()


@router.post(AD_BIDDER_BID_REQUEST)
def post_bid_request(bid_request: BidRequest) -> BidResponse:
    log.debug(str(bid_request.ext))
    bid_response = bid_service.generate_bid(bid_request)
    return bid_response


@router.post(AD_BIDDER_BID_NOTICE)
def post_notice(bid_id: str, imp_id: str, status: int) -> str | None:
    return bid_service.process_notice(bid_id, imp_id, status)


@router.get(AD_BIDDER_BID_METRICS)
def get_metrics():
    return Response(
        content=prom.generate_latest(),
        media_type="text/plain"
    )
