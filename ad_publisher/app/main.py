import logging as log
import logging as log
import uuid

import httpx
from fastapi import FastAPI, status

from ad_bidder_common.model import BidRequest

app = FastAPI(title="AD PUBLISHER")
log.basicConfig(level=log.DEBUG)


@app.get("/")
def root():
    return {"sample": "json"}


@app.post("/ad")
def post_ad() -> BidRequest:
    log.debug("Ad posted")
    with httpx.Client() as client:
        bid_request = BidRequest.minimal(str(uuid.uuid4()), "imp_" + str(uuid.uuid4()))
        body = bid_request.model_dump(mode="json")
        log.debug("Sending bid request: " + str(body))
        r = client.post("http://ad_bidder/bid", json=body)
        if r.status_code == status.HTTP_200_OK:
            return BidRequest.model_validate_json(r.content)
        else:
            log.warning(r.text)
