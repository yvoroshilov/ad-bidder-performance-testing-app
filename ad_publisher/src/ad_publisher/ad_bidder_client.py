import logging as log
from typing import Optional

import httpx
from starlette import status

from ad_bidder_common.model.openrtb.request import BidRequest
from ad_bidder_common.model.openrtb.response import BidResponse, Bid
from ad_publisher.ad.model import AdBidder
from ad_publisher.auction.model import BidStatus
from ad_publisher.constants import AD_BIDDER_URL_ROOT


def post_bid_request(bidder: AdBidder, bid_request: BidRequest) -> BidResponse:
    body = bid_request.model_dump(mode="json")
    log.debug("Sending bid request: " + str(body))
    with httpx.Client(timeout=None) as client:
        response = client.post(bidder.bid_request_url, json=body)
        if response.status_code != status.HTTP_200_OK:
            raise Exception(f"Couldn't get ad response. Received: {str(response)}")
        return BidResponse.model_validate_json(response.content)


def post_notice(bid_status: BidStatus, bid: Bid) -> Optional[str]:
    with httpx.Client(timeout=None) as client:
        notice_url = AD_BIDDER_URL_ROOT + bid.nurl
        response = client.post(url=notice_url, params={"status": bid_status.value, "imp_id": bid.impid})
        if response.status_code != status.HTTP_200_OK:
            raise Exception(f"Couldn't post notice. Received: {response}")
        return response.text
