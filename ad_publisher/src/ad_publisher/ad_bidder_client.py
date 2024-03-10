import logging as log
from typing import Optional

import httpx
from ad_bidder_common.model.openrtb.request import BidRequest
from ad_bidder_common.model.openrtb.response import BidResponse, Bid
from ad_publisher.ad.model import AdBidder
from ad_publisher.auction.model import BidStatus
from ad_publisher.constants import AD_BIDDER_URL_ROOT
from starlette import status


def post_bid_request(bidder: AdBidder, bid_request: BidRequest) -> BidResponse:
    body = bid_request.model_dump(mode="json")
    log.debug("Sending bid request: " + str(body))
    with httpx.Client() as client:
        response = client.post(bidder.bid_request_url, json=body)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(f"Couldn't get ad response. Received: {response}")
        return BidResponse.model_validate_json(response.content)


def post_notice(bid: Bid, imp_id: str, bid_status: BidStatus) -> Optional[str]:
    with httpx.Client() as client:
        response = client.post(url=AD_BIDDER_URL_ROOT + bid.nurl, params={"status": bid_status.value, "imp_id": imp_id})
        return response.text
