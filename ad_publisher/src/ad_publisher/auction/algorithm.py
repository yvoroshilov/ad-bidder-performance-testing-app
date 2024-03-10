import logging as log
from abc import abstractmethod, ABC
from typing import Dict

from ad_bidder_common.model.openrtb.response import Bid
from typing_extensions import List


class AuctionAlgorithm(ABC):
    @abstractmethod
    def calc_winner(self, bids: List[Bid], reserved_price: float) -> Dict[str, Bid]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class DefaultAuctionAlgorithm(AuctionAlgorithm):
    def calc_winner(self, bids: List[Bid], reserved_price: float) -> Dict[str, Bid]:
        log.debug("Start calc_winner")

        eligible_bids = list(filter(lambda bid: bid.price >= reserved_price, bids))
        log.debug(f"Eligible bids count={len(eligible_bids)}")

        impid_bids = {}
        for bid in eligible_bids:
            if bid.impid in impid_bids:
                impid_bids[bid.impid].append(bid)
            else:
                impid_bids[bid.impid] = [bid]

        winners = {}
        for impid in impid_bids:
            bids_for_impid = impid_bids[impid]
            highest_price_bid = max(bids_for_impid, key=lambda bid: bid.price)
            winners[impid] = highest_price_bid
            log.debug(f"Winner for impid={impid} is bid with price={winners[impid].price}")

        return winners

    def name(self) -> str:
        return "First highest"


class SecondHighestAuctionAlgorithm(AuctionAlgorithm):
    def calc_winner(self, bids: List[Bid], reserved_price: float) -> Dict[str, Bid]:
        log.debug("Start calc_winner")

        eligible_bids = filter(lambda bid: bid.price >= reserved_price, bids)
        log.debug(f"Eligible bids count={len(eligible_bids)}")

        impid_bids = {}
        for bid in eligible_bids:
            if bid.impid in impid_bids:
                impid_bids[bid.impid].append(bid)
            else:
                impid_bids[bid.impid] = [bid]

        winners = {}
        for impid in impid_bids:
            bids_for_impid = impid_bids[impid]
            bids_for_impid.sort(key=lambda bid: bid.price)
            winners[impid] = bids_for_impid[1] if len(bids_for_impid) > 1 else bids_for_impid[0]
            log.debug(f"Winner for impid={impid} is bid with price={winners[impid].price}")

        return winners

    def name(self) -> str:
        return "Second highest"
