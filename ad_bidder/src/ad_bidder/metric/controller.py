import logging as log
from typing import Annotated

from fastapi import APIRouter, Query

from ad_bidder.metric.model import MetricType

router = APIRouter()


@router.get("")
def get_metrics(metric_type: Annotated[MetricType, Query(alias="type")]):
    log.debug("received metric type: " + metric_type.value)
    return {"tmp": "stub", "metric_type": str(metric_type.value)}
