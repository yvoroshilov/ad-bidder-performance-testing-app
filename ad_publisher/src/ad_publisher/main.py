import logging as log

from fastapi import FastAPI
from pymongo import MongoClient

from ad_publisher import config
from ad_publisher.ad.controller import router as ad_router
from ad_publisher.constants import *
from ad_publisher.log import configure_logging

if config.DEBUG:
    import pydevd_pycharm
    pydevd_pycharm.settrace('host.docker.internal', port=12345, stdoutToServer=True, stderrToServer=True)

app = FastAPI(title="AD PUBLISHER")
configure_logging()

app.include_router(ad_router, prefix=AD_PUBLISHER_ADS_ROOT, tags=["ad"])


@app.on_event("startup")
def startup_db_client():
    url = f"mongodb://{config.MONGODB_USERNAME}:{config.MONGODB_PASSWORD}@{config.MONGODB_HOST}"
    app.mongodb_client = MongoClient(url,  serverSelectionTimeoutMS=3000)
    app.mongodb_client.server_info()
    app.database = app.mongodb_client[config.MONGODB_DB_NAME]
    log.debug("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
