from fastapi import FastAPI

from app.model import BidRequest

app = FastAPI()


@app.post("/bid")
def post_bid_request(bid_request: BidRequest):
    return print(bid_request)
