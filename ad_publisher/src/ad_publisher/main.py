from fastapi import FastAPI

from ad_publisher.ad.controller import router as ad_router
from ad_publisher.log import configure_logging

app = FastAPI(title="AD PUBLISHER")
configure_logging()

app.include_router(ad_router, prefix="/ad", tags=["ad"])
