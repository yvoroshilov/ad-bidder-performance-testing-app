import datetime
import logging
import random
from typing import List

from pydantic import BaseModel
from time import sleep

import data_generator
from ad_bidder_common.model.openrtb.request import Device, User, Impression
from ad_bidder_common.model.openrtb.util import MongoDbMixin
from data_gen import ad_publisher_client


class AdRequest(BaseModel, MongoDbMixin):
    timestamp: datetime.datetime
    device: Device
    user: User
    imps: List[Impression]


def start_bid_request_attack(*, auction_n: int, imp_n_range: tuple[int, int], auction_creation_delay_s: tuple[int, int],
                             str_size: int = 1, arr_size: int = 1):
    rand = random.Random()
    for i in range(auction_n):
        logging.info(f"Auction #{i}")

        imp_n = rand.randint(imp_n_range[0], imp_n_range[1])
        logging.info(f"Impression number={imp_n}")

        ad_request = data_generator.gen_for_composite(AdRequest, custom_values={"imps": []}, str_size=str_size, arr_size=arr_size)
        imps = [data_generator.gen_for_composite(Impression, str_size=str_size, arr_size=arr_size) for _ in range(imp_n)]
        ad_request.imps = imps

        ad_publisher_client.post_ad_request(ad_request)

        sleep_delay_s = rand.randrange(auction_creation_delay_s[0], auction_creation_delay_s[1] + 1)
        sleep(sleep_delay_s / 1000)


if __name__ == '__main__':
    start_bid_request_attack(auction_n=1, imp_n_range=(1, 1), str_size=1, arr_size=1, auction_creation_delay_s=(1, 1))
