from fastapi import FastAPI

from ad_bidder.bid.controller import router as bid_router
from ad_bidder.log import configure_logging

configure_logging()

app = FastAPI(title="AD BIDDER")

app.include_router(bid_router, prefix="/bids", tags=["bids"])
