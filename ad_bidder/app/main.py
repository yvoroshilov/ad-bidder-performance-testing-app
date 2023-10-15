import logging as log

from fastapi import FastAPI

from ad_bidder_common.model import BidRequest

app = FastAPI(title="AD BIDDER")
log.basicConfig(level=log.DEBUG)


@app.post("/bid")
def post_bid_request(bid_request: BidRequest):
    log.debug(str(bid_request))
    bid_request.ext = "passed post_bid_request"
    return bid_request
