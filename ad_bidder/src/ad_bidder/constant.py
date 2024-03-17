AD_BIDDER_API_ROOT = "/api/v1"

AD_BIDDER_BID_ROOT = "/bids"
AD_BIDDER_BID_REQUEST = "/request"
AD_BIDDER_BID_METRICS = "/metrics"
AD_BIDDER_BID_NOTICE = "/{bid_id}/notice"


def compose_path(root: str, *path_elements: str) -> str:
    return "".join([AD_BIDDER_API_ROOT, root, *path_elements])
