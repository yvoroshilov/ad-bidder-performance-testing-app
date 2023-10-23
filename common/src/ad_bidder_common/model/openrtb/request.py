from typing import Optional, List, Any, Tuple, Set

from pydantic import BaseModel


class Banner(BaseModel):
    """
    A banner object typically describes an ad opportunity for banner, rich media or in-banner video inventory.

    The “banner” object must be included directly in the impression object
    if the impression offered for auction is display or rich media,
    or it may be optionally embedded in the video object to describe
    the companion banners available for the linear or non-linear video ad.
    The banner object may include a unique identifier; this can be useful
    if these IDs can be leveraged in the VAST response
    to dictate placement of the companion creatives when multiple
    companion ad opportunities of the same size are available on a page.
    """

    w: Optional[int] = None
    """
    Width of the impression in pixels.
    If neither wmin nor wmax are specified, this value is an exact width
    requirement. Otherwise it is a preferred width.
    """

    h: Optional[int] = None
    """
    Height of the impression in pixels.
    If neither hmin nor hmax are specified, this value is an exact height
    requirement. Otherwise it is a preferred height.
    """

    # TODO Format
    # format = Field(Array(Format))

    wmax: Optional[int] = None
    """
    Maximum width of the impression in pixels.
    If included along with a w value then w should be interpreted as a
    recommended or preferred width.
    """

    hmax: Optional[int] = None
    """
    Maximum height of the impression in pixels.
    If included along with an h value then h should be interpreted as a
    recommended or preferred height.
    """

    wmin: Optional[int] = None
    """
    Minimum width of the impression in pixels.
    If included along with a w value then w should be interpreted as a
    recommended or preferred width.
    """

    hmin: Optional[int] = None
    """
    Minimum height of the impression in pixels.
    If included along with an h value then h should be interpreted as a
    recommended or preferred height.
    """

    id: str
    """
    Unique identifier for this banner object. Recommended when Banner
    objects are used with a Video object (Section 3.2.4) to represent an
    array of companion ads. Values usually start at 1 and increase with each
    object; should be unique within an impression.
    """

    # """
    # Blocked banner ad types. Refer to List 5.2.
    # # TODO banner type
    # # btype:
    # """
    #
    # """
    # Blocked creative attributes. Refer to List 5.3.
    # # TODO creative attributes
    # # battr = Field(Array(constants.CreativeAttribute))
    # """
    #
    # """
    # Ad position on screen. Refer to List 5.4.
    # # TODO position
    # # pos = Field(constants.AdPosition)
    # """

    mimes: Optional[List[str]] = None
    """
    Content MIME types supported. Popular MIME types may include
    “application/x-shockwave-flash”, “image/jpg”, and “image/gif”.
    """

    topframe: Optional[int] = None
    """
    Indicates if the banner is in the top frame as opposed to an iframe,
    where 0 = no, 1 = yes.
    """

    # """
    # Directions in which the banner may expand. Refer to List 5.5.
    # # TODO exp dir
    # # expdir = Field(Array(constants.ExpandableDirection))
    # """
    #
    # """
    # List of supported API frameworks for this impression. Refer to List
    # 5.6. If an API is not explicitly listed, it is assumed not to be
    # supported.
    # # TODO api
    # # api = Field(Array(constants.APIFramework))
    # """

    vcm: Optional[int] = None

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """

    def blocked_types(self) -> Optional[Set[str]]:
        return set(self.btype or [])

    def size(self) -> Optional[Tuple[int, int]]:
        if self.w and self.h:
            return self.w, self.h


class Impression(BaseModel):
    """
    At least one impression object is required in a bid request object.

    The “imp” object desribes the ad position or impression being auctioned.
    A single bid request can include multiple “imp” objects,
    a use case for which might be an exchange that supports selling all ad positions on a given page as a bundle.
    Each “imp” object has a required ID so that bids can reference them individually.
    """

    id: str
    """
    A unique identifier for this impression within the context of the bid request (typically, starts with 1 and increments).
    """

    # TODO banner
    banner: Banner
    """
    A Banner object (Section 3.2.3); required if this impression is offered as a banner ad opportunity.
    """

    # TODO Video
    # video = Field(Video)
    """
    A Video object (Section 3.2.4); required if this impression is offered as a video ad opportunity.
    """

    # TODO Audio
    # audio = Field(Audio)

    # TODO Audio
    # native = Field(Native)
    """
    A Native object (Section 3.2.5); required if this impression is offered as a native ad opportunity.
    """

    displaymanager: Optional[str] = None
    """
    Name of ad mediation partner, SDK technology, or player responsible for rendering ad (typically video or mobile).
    Used by some ad servers to customize ad code by partner. Recommended for video and/or apps.
    """

    displaymanagerver: Optional[str] = None
    """
    Version of ad mediation partner, SDK technology, or player responsible for rendering ad (typically video or mobile).
    Used by some ad servers to customize ad code by partner. Recommended for video and/or apps.
    """

    instl: Optional[int] = None
    """
    1 = the ad is interstitial or full screen, 0 = not interstitial.
    """

    tagid: Optional[str] = None
    """
    Identifier for specific ad placement or ad tag that was used to initiate the auction.
    This can be useful for debugging of any issues, or for optimization by the buyer.
    """

    bidfloor: Optional[float] = None
    """
    Minimum bid for this impression expressed in CPM.
    """

    bidfloorcur: str = "USD"
    """
    Currency specified using ISO-4217 alpha codes. This may be different from bid currency returned by bidder if this is allowed by the exchange.
    """

    clickbrowser: Optional[int] = None

    secure: Optional[int] = None
    """
    Flag to indicate if the impression requires secure HTTPS URL creative assets and markup, where 0 = non-secure, 1 = secure. If omitted, the secure state is unknown, but non-secure HTTP support can be assumed.
    """

    iframebuster: Optional[List[str]] = None
    """
    Array of exchange-specific names of supported iframe busters.
    """

    # TODO PMP
    # pmp = Field(PMP)
    exp: Optional[int] = None
    """
    A Pmp object (Section 3.2.17) containing any private marketplace deals in effect for this impression.
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """


class BidRequest(BaseModel):
    """
    Top-level bid request object.
    The top-level bid request object contains a globally unique bid request or auction ID.
    This “id” attribute is required as is at least one “imp” (i.e., impression) object.
    Other attributes are optional since an exchange may establish default values.
    """

    id: str
    """
    Unique ID of the bid request, provided by the exchange.
    """

    imp: List[Impression]
    """
    Array of Imp objects (Section 3.2.2) representing the impressions offered.
    At least 1 Imp object is required.
    """

    # TODO site
    # site = Field(Site)
    """
    Details via a Site object (Section 3.2.6) about the publisher’s website.
    Only applicable and recommended for websites.
    """

    # TODO app
    # app = Field(App)
    """
    Details via an App object (Section 3.2.7) about the publisher’s app (i.e., non-browser applications).
    Only applicable and recommended for apps.
    """

    # TODO device
    # device = Field(Device)
    """
    Details via a Device object (Section 3.2.11) about the user’s device to which the impression will be delivered.
    """

    # TODO user
    # user = Field(User)
    """
    Details via a User object (Section 3.2.13) about the human user of the device; the advertising audience.
    """

    test: Optional[int] = None
    """
    Indicator of test mode in which auctions are not billable, where 0 = live mode, 1 = test mode.
    """

    # TODO at
    # at = Field(constants.AuctionType, default=constants.AuctionType.SECOND_PRICE)
    """
    Auction type, where 1 = First Price, 2 = Second Price Plus. Exchange-specific auction types can be defined using values greater than 500.
    """

    tmax: Optional[int] = None
    """
    Maximum time in milliseconds to submit a bid to avoid timeout. This value is commonly communicated offline.
    """

    wseat: Optional[List[str]] = None
    """
    Whitelist of buyer seats allowed to bid on this impression. Seat IDs must be communicated between bidders and the exchange a priori. Omission implies no seat restrictions.
    """

    bseat: Optional[List[str]] = None

    allimps: Optional[str] = None
    """
    Flag to indicate if Exchange can verify that the impressions offered represent all of the impressions available in context (e.g., all on the web page, all video spots such as pre/mid/post roll) to support road-blocking. 0 = no or unknown, 1 = yes, the impressions offered represent all that are available.
    """

    cur: Optional[List[str]] = None
    """
    Array of allowed currencies for bids on this bid request using ISO-4217 alpha codes. Recommended only if the exchange accepts multiple currencies.
    """

    wlang: Optional[List[str]] = None

    bcat: Optional[List[str]] = None
    """
    Blocked advertiser categories using the IAB content categories. Refer to List 5.1.
    """

    badv: Optional[List[str]] = None
    """
    Block list of advertisers by their domains (e.g., “ford.com”).
    """

    bapp: Optional[List[str]] = None

    # TODO source
    # source = Field(Source)

    # TODO regulations
    # regs = Field(Regulations)
    """
    A Regs object (Section 3.2.16) that specifies any industry, legal, or governmental regulations in force for this request.
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """

    @staticmethod
    def minimal(req_id: str, imp_id: str) -> "BidRequest":
        return BidRequest(id=req_id, imp=[Impression(id=imp_id, banner=Banner(id="sample_banner_id"))])
