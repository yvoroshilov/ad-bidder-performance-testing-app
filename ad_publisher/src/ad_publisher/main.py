from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from ad_publisher import config
from ad_publisher.ad.controller import router as ad_router
from ad_publisher.constants import *
from ad_publisher.db.config import init_db_client, shutdown_db_client
from ad_publisher.log import configure_logging

if config.DEBUG:
    import pydevd_pycharm

    pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)

configure_logging()

app = FastAPI(title="AD PUBLISHER")
app.include_router(ad_router, prefix=AD_PUBLISHER_ADS_ROOT, tags=["ads"])
instrumentator = Instrumentator().instrument(app)


@app.on_event("startup")
def startup():
    init_db_client()
    instrumentator.expose(app)


@app.on_event("shutdown")
def shutdown():
    shutdown_db_client()
