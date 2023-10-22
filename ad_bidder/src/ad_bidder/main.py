from fastapi import FastAPI

from ad_bidder.bid.controller import router as bid_router
from ad_bidder.logging import configure_logging
from ad_bidder.metric.controller import router as metric_router

configure_logging()

app = FastAPI(title="AD BIDDER")

app.include_router(bid_router, prefix="/bids", tags=["bids"])
app.include_router(metric_router, prefix="/metrics", tags=["metrics"])
