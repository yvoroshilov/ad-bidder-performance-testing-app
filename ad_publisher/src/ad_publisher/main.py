import logging as log
import uuid

import httpx
from fastapi import FastAPI, status

from ad_bidder_common.model.openrtb.request import BidRequest
from ad_bidder_common.model.openrtb.response import BidResponse
from ad_publisher.constants import AD_BIDDER_ROOT  # why uvicorn doesn't see "from constants import AD_BIDDER_ROOT"?

app = FastAPI(title="AD PUBLISHER")
log.basicConfig(level=log.DEBUG)


@app.get("/")
def root():
    return {"sample": "json"}


@app.post("/ad")
def post_ad() -> BidResponse:
    log.debug("Ad posted")
    with httpx.Client() as client:
        bid_request = BidRequest.minimal(_gen_uuid() + "_bid_req", _gen_uuid() + "_imp")
        body = bid_request.model_dump(mode="json")
        log.debug("Sending bid request: " + str(body))

        r = client.post(AD_BIDDER_ROOT, json=body)
        if r.status_code == status.HTTP_200_OK:
            return BidResponse.model_validate_json(r.content)
        else:
            log.warning(r.text)


def _gen_uuid() -> str:
    return str(uuid.uuid4())
