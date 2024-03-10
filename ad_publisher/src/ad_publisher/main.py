from ad_publisher import config
from ad_publisher.ad.controller import router as ad_router
from ad_publisher.constants import *
from ad_publisher.log import configure_logging
from fastapi import FastAPI

print(config.DEBUG)
if config.DEBUG:
    import pydevd_pycharm
    pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)

app = FastAPI(title="AD PUBLISHER")
configure_logging()

app.include_router(ad_router, prefix=AD_PUBLISHER_ADS_ROOT, tags=["ad"])
