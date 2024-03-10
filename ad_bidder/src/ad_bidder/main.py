from fastapi import FastAPI

from ad_bidder import config
from ad_bidder.bid.controller import router as bid_router
from ad_bidder.constant import AD_BIDDER_BID_ROOT, AD_BIDDER_API_ROOT
from ad_bidder.log import configure_logging

if config.DEBUG:
    import pydevd_pycharm
    pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)

configure_logging()

app = FastAPI(title="AD BIDDER")

app.include_router(bid_router, prefix=AD_BIDDER_API_ROOT + AD_BIDDER_BID_ROOT, tags=["bids"])
