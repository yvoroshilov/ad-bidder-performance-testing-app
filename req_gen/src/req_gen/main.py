import datetime
import logging
import random
import uuid
from typing import Iterator, List, Tuple, Any, Callable

import httpx
import sys
from time import sleep

from ad_bidder_common.model.openrtb.request import BidRequest

BID_ROOT = "http://127.0.0.1:81/bids"

log = logging.getLogger("req_gen")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler(sys.stdout))


def create_bid_request(**kwargs) -> BidRequest:
    br = BidRequest.minimal(str(uuid.uuid4()), str(uuid.uuid4()))
    br.ext = {
        **kwargs,
        "generated_at": datetime.datetime.now()
    }
    return br


def gen_bid_requests(n: int, create_model: Callable[..., Any], chunk_size: int = 1) -> Iterator[List[Any]]:
    for i in range(n):
        log.debug("Creating chunk " + str(i))
        gen_params = {
            "chunk_total": n,
            "chunk_size": chunk_size,
            "chunk_number": i + 1
        }
        cur_chunk = [create_model(**gen_params, obj_number=i) for i in range(chunk_size)]
        yield cur_chunk
    log.info(f"{n} chunks of {chunk_size} size has been generated")


def start_bid_request_attack(n: int, *, delay_ms: Tuple[int, int] = (90, 100), chunk_size: int = 1):
    log.info("Starting sending BID requests")
    rand = random.Random()
    req_cnt = 0
    with httpx.Client() as client:
        bid_requests = gen_bid_requests(n, create_bid_request, chunk_size)
        for bid_chunk in bid_requests:
            for bid_request in bid_chunk:
                body = bid_request.model_dump(mode="json")
                client.post(BID_ROOT, json=body)
                req_cnt += 1
                if req_cnt % 1000 == 0:
                    log.debug("Requests sent: " + str(req_cnt))
                sleep(rand.randrange(delay_ms[0], delay_ms[1]) / 1000)


def main():
    start_bid_request_attack(10000, chunk_size=1, delay_ms=(0, 1))


if __name__ == '__main__':
    main()
