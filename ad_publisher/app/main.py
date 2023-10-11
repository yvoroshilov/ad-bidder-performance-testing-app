import logging

from fastapi import FastAPI, Request

from app.model import AdRequest

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)


@app.get("/")
def root():
    return {"sample": "json"}


@app.post("/ad")
def post_ad(ad_request: AdRequest, request: Request):
    print(ad_request)
    print(request.headers)
    print(request.cookies)
