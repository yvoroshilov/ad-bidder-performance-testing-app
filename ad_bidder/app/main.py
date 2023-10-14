import datetime
import logging as log
import random

from fastapi import FastAPI

from app.model import BidRequest

app = FastAPI(title="AD BIDDER")
log.basicConfig(level=log.DEBUG)


@app.post("/bid")
def post_bid_request(bid_request: BidRequest):
    log.debug(str(bid_request))
    return BidRequest(
        id=str(random.Random().random()),
        timestamp=str(datetime.datetime.now()),
        language=bid_request.language
    )
