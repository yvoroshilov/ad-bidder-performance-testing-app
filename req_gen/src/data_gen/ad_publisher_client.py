import httpx

from data_gen.req_gen import AdRequest

_AD_REQUEST_URL="http://localhost:80/api/v1/ads/request"


def post_ad_request(ad_request: AdRequest):
    with httpx.Client(timeout=None) as client:
        body = ad_request.model_dump(mode="json")
        response = client.post(_AD_REQUEST_URL, json=body)
