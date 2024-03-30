import logging as log

from bson import ObjectId
from fastapi import APIRouter
from pydantic import BaseModel, Field, AliasChoices
from starlette import status
from starlette.responses import Response

import ad_publisher.auction.service as auction_service
from ad_publisher.ad.model import AdRequest, AdResponse
from ad_publisher.db.config import get_test_collection

router = APIRouter()


@router.post("/")
def post_ad(ad_request: AdRequest) -> AdResponse:
    imp_html = auction_service.run_auction(ad_request)
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



class TestObj(BaseModel, IdAlwaysStrMixIn):
    # AliasChoices are needed to make id appear as "id" and not "_id" in the openAPI documentation
    id: str | None = Field(validation_alias=AliasChoices("id", "_id"))
    a: int
    b: str


@router.get("/test")
def test(find_id: str, resp: Response):
    log.debug("test")
    result = get_test_collection().find_one({"_id": ObjectId(find_id)})
    if result is not None:
        return TestObj.model_validate(result)
    else:
        resp.status_code = status.HTTP_404_NOT_FOUND


@router.post("/test_insert")
def test_insert(body: TestObj) -> TestObj:
    insert_result = get_test_collection().insert_one(body.model_dump(exclude={"id"}))
    inserted_obj = get_test_collection().find_one({"_id": insert_result.inserted_id})
    return TestObj.model_validate(inserted_obj)
