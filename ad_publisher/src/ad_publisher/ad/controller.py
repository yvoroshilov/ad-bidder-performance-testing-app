import logging as log

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

import ad_publisher.auction.service as auction_service
from ad_publisher.ad.model import AdRequest, AdResponse

router = APIRouter()


@router.post("/")
def post_ad(ad_request: AdRequest) -> AdResponse:
    auction = auction_service.init_auction(ad_request)
    imp_html = auction_service.run_auction(auction)
    return AdResponse(imp_html=imp_html)


@router.post("/generate_log")
def generate_log(log_type: str) -> Response:
    if log_type is None:
        log.error("Log type cannot be none")
        raise ValueError("Log type is none")
    log_msg_methods = {
        "WARN": lambda: log.warning("Generated warn message!"),
        "INFO": lambda: log.info("Some useful info"),
        "DEBUG": lambda: log.debug("This is a debug message")
    }
    msg_method = log_msg_methods.get(log_type)
    if msg_method is None:
        log.warning(f"Not found log message for log type {log_type}")
        return status.HTTP_501_NOT_IMPLEMENTED
    msg_method()


@router.post("/test")
def test():
    pass
