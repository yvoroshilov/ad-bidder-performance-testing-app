import datetime
import logging as log
import random

import httpx
from fastapi import FastAPI, Request, Response, status

from app.model import AdRequest, BidRequest

app = FastAPI(title="AD PUBLISHER")
log.basicConfig(level=log.DEBUG)


@app.get("/")
def root():
    return {"sample": "json"}


@app.post("/ad")
def post_ad(ad_request: AdRequest, req: Request, resp: Response):
    log.debug("Ad posted")
    with httpx.Client() as client:
        bid_request = BidRequest(
            id=str(random.Random().randint(0, 999999999999999999)),
            timestamp=str(datetime.datetime.now()),
            language=ad_request.language)
        body = bid_request.model_dump(mode="json")
        log.debug("Sending bid request: " + str(body))
        r = client.post("http://ad_bidder/bid", json=body)
        if r.status_code == status.HTTP_200_OK:
            return BidRequest.model_validate_json(r.content)
        else:
            log.warning(r.text)
