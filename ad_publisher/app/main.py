import logging

from fastapi import FastAPI

from app.model import AdRequest

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)


@app.get("/")
def root():
    return {"sample": "json"}


@app.post("/ad")
def post_ad(ad_request: AdRequest):
    logging.debug(f"Ad request received: {ad_request}")
