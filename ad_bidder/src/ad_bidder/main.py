from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from ad_bidder import config
from ad_bidder.bid.controller import router as bid_router
from ad_bidder.constant import AD_BIDDER_BID_ROOT, AD_BIDDER_API_ROOT
from ad_bidder.db.config import init_db_client, shutdown_db_client
from ad_bidder.log import configure_logging

if config.DEBUG:
    import pydevd_pycharm

    pydevd_pycharm.settrace('host.docker.internal', port=12346, stdoutToServer=True, stderrToServer=True)

configure_logging()

app = FastAPI(title="AD BIDDER")
app.include_router(bid_router, prefix=AD_BIDDER_API_ROOT + AD_BIDDER_BID_ROOT, tags=["bids"])
instrumentator = Instrumentator().instrument(app)


@app.on_event("startup")
def startup():
    init_db_client()
    instrumentator.expose(app)


@app.on_event("shutdown")
def shutdown():
    shutdown_db_client()
