from typing import Optional, List, Any, Tuple, Set

from pydantic import BaseModel


class Content(BaseModel):
    """
    This object describes the content in which the impression will appear, which may be syndicated or non-syndicated
    content. This object may be useful when syndicated content contains impressions and does not necessarily match
    the publisher’s general content. The exchange might or might not have knowledge of the page where the content is
    running, because of the syndication method. For example, might be a video impression embedded in an iframe on an
    unknown web property or device.
    """

    id: Optional[str] = None
    """
    ID uniquely identifying the content.
    """

    episode: Optional[int] = None
    """
    Episode number.
    """

    title: Optional[str] = None
    """
    Content title.
    *Video Examples:* “Search Committee” (television), “A New Hope” (movie), or “Endgame” (made for web).
    *Non-Video Example:* “Why an Antarctic Glacier Is Melting So Quickly” (Time magazine article).
    """

    series: Optional[str] = None
    """
    Content series.
    *Video Examples:* “The Office” (television), “Star Wars” (movie), or “Arby ‘N’ The Chief” (made for web).
    *Non-Video Example:* “Ecocentric” (Time Magazine blog).
    """

    season: Optional[str] = None
    """
    Content season (e.g., “Season 3”).
    """

    artist: Optional[str] = None
    """
    Artist credited with the content.
    """

    genre: Optional[str] = None
    """
    Genre that best describes the content (e.g., rock, pop, etc).
    """

    album: Optional[str] = None
    """
    Album to which the content belongs; typically for audio.
    """

    isrc: Optional[str] = None
    """
    International Standard Recording Code conforming to ISO- 3901.
    """

    producer: Optional["Producer"] = None
    """
    Details about the content Producer (Section 3.2.17).
    """

    url: Optional[str] = None
    """
    URL of the content, for buy-side contextualization or review.
    """

    cattax: Optional[int] = 1
    """
    The taxonomy in use. Refer to list List: Category Taxonomies in AdCOM 1.0 for values.
    """

    cat: Optional[List[str]] = None
    """
    Array of IAB Tech Lab content categories that describe the content. The taxonomy to be used is defined by the cattax field. If no cattax field is supplied Content Category Taxonomy 1.0 is assumed.
    """

    prodq: Optional[int] = None
    """
    Production quality. Refer to List: Production Qualities in AdCOM 1.0.
    """

    context: Optional[int] = None
    """
    Type of content (game, video, text, etc.). Refer to List: Content Contexts in AdCOM 1.0.
    """

    contentrating: Optional[str] = None
    """
    Content rating (e.g., MPAA).
    """

    userrating: Optional[str] = None
    """
    User rating of the content (e.g., number of stars, likes, etc.).
    """

    qagmediarating: Optional[int] = None
    """
    Media rating per IQG guidelines. Refer to List: Media Ratings in AdCOM 1.0.
    """

    keywords: Optional[str] = None
    """
    Comma separated list of keywords describing the content. Only one of keywords or kwarray may be present.
    """

    kwarray: Optional[List[str]] = None
    """
    Array of keywords about the site. Only one of keywords or kwarray may be present.
    """

    livestream: Optional[int] = None
    """
    0 = not live, 1 = content is live (e.g., stream, live blog).
    """

    sourcerelationship: Optional[int] = None
    """
    0 = indirect, 1 = direct.
    """

    len: Optional[int] = None
    """
    Length of content in seconds; appropriate for video or audio.
    """

    language: Optional[str] = None
    """
    Content language using ISO-639-1-alpha-2. Only one of language or langb should be present.
    """

    langb: Optional[str] = None
    """
    Content language using IETF BCP 47. Only one of language or langb should be present.
    """

    embeddable: Optional[int] = None
    """
    Indicator of whether the content is embeddable (e.g., an embeddable video player), where 0 = no, 1 = yes.
    """

    data: Optional[List["Data"]] = None
    """
    Additional content data. Each Data object (Section 3.2.21) represents a different data source.
    """

    network: Optional["Network"] = None
    """
    Details about the network (Section 3.2.23) the content is on.
    """

    channel: Optional["Channel"] = None
    """
    Details about the channel (Section 3.2.24) the content is on.
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """


class Producer(BaseModel):
    """
    This object defines the producer of the content in which the ad will be shown. This is particularly useful when the content is syndicated and may be distributed through different publishers and thus when the producer and publisher are not necessarily the same entity.
    """

    id: Optional[str] = None
    """
    Content producer or originator ID. Useful if content is syndicated and may be posted on a site using embed tags.
    """

    name: Optional[str] = None
    """
    Content producer or originator name (e.g., “Warner Bros”).
    """

    cattax: Optional[int] = 1
    """
    The taxonomy in use. Refer to the AdCOM 1.0 list List: Category Taxonomies for values.
    """

    cat: Optional[List[str]] = None
    """
    Array of IAB Tech Lab content categories that describe the content producer. The taxonomy to be used is defined by the cattax field. If no cattax field is supplied Content Category Taxonomy 1.0 is assumed.
    """

    domain: Optional[str] = None
    """
    Highest level domain of the content producer (e.g., "producer.com").
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """


class Device(BaseModel):
    """
    This object provides information pertaining to the device through which the user is interacting. Device information includes its hardware, platform, location, and carrier data. The device can refer to a mobile handset, a desktop computer, set top box, or other digital device.
    """

    js: Optional[int] = None
    """
    Support for JavaScript, where 0 = no, 1 = yes.
    """

    flashver: Optional[str] = None
    """
    Version of Flash supported by the browser.
    """

    carrier: Optional[str] = None
    """
    Carrier or ISP (e.g., “VERIZON”) using exchange curated string names which should be published to bidders *a priori*.
    """

    geo: Optional["Geo"] = None
    """
    Location of the device assumed to be the user’s current location defined by a Geo object (Section 3.2.19).
    """

    dnt: Optional[int] = None
    """
    Standard “Do Not Track” flag as set in the header by the browser, where 0 = tracking is unrestricted, 1 = do not track.
    """

    lmt: Optional[int] = None
    """
    “Limit Ad Tracking” signal commercially endorsed (e.g., iOS, Android), where 0 = tracking is unrestricted, 1 = tracking must be limited per commercial guidelines.
    """

    ua: Optional[str] = None
    """
    Browser user agent string. This field represents a raw user agent string from the browser. For backwards compatibility, exchanges are recommended to always populate ua with the User-Agent string, when available from the end user’s device, even if an alternative representation, such as the User-Agent Client-Hints, is available and is used to populate sua. No inferred or approximated user agents are expected in this field.
    If a client supports User-Agent Client Hints, and sua field is present, bidders are recommended to rely on sua for detecting device type, browser type and version and other purposes that rely on the user agent information, and ignore ua field. This is because the ua may contain a frozen or reduced user agent string.
    """

    sua: Optional[str] = None
    """
    Structured user agent information defined by a UserAgent object (see Section 3.2.29). If both ua and sua are present in the bid request, sua should be considered the more accurate representation of the device attributes. This is because the ua may contain a frozen or reduced user agent string.
    """

    ip: Optional[str] = None
    """
    IPv4 address closest to device.
    """

    ipv6: Optional[str] = None
    """
    IP address closest to device as IPv6.
    """

    devicetype: Optional[int] = None
    """
    The general type of device. Refer to List: Device Types in AdCOM 1.0.
    """

    make: Optional[str] = None
    """
    Device make (e.g., “Apple”).
    """

    model: Optional[str] = None
    """
    Device model (e.g., “iPhone”).
    """

    os: Optional[str] = None
    """
    Device operating system (e.g., “iOS”).
    """

    osv: Optional[str] = None
    """
    Device operating system version (e.g., “3.1.2”).
    """

    hwv: Optional[str] = None
    """
    Hardware version of the device (e.g., “5S” for iPhone 5S).
    """

    h: Optional[str] = None
    """
    Physical height of the screen in pixels.
    """

    w: Optional[str] = None
    """
    Physical width of the screen in pixels.
    """

    ppi: Optional[str] = None
    """
    Screen size as pixels per linear inch.
    """

    pxratio: Optional[float] = None
    """
    The ratio of physical pixels to device independent pixels.
    """

    geofetch: Optional[int] = None
    """
    Indicates if the geolocation API will be available to JavaScript code running in the banner, where 0 = no, 1 = yes.
    """

    language: Optional[str] = None
    """
    Browser language using ISO-639-1-alpha-2. Only one of language or langb should be present.
    """

    langb: Optional[str] = None
    """
    Browser language using IETF BCP 47. Only one of language or langb should be present.
    """

    mccmnc: Optional[str] = None
    """
    Mobile carrier as the concatenated MCC-MNC code (e.g., “310-005” identifies Verizon Wireless CDMA in the USA). Refer to https://en.wikipedia.org/wiki/Mobile_country_code for further examples. Note that the dash between the MCC and MNC parts is required to remove parsing ambiguity. The MCC-MNC values represent the SIM installed on the device and do not change when a device is roaming. Roaming may be inferred by a combination of the MCC-MNC, geo, IP and other data signals.
    """

    connectiontype: Optional[int] = None
    """
    Network connection type. Refer to List: Connection Types in AdCOM 1.0.
    """

    ifa: Optional[str] = None
    """
    ID sanctioned for advertiser use in the clear (i.e., not hashed).
    """

    didsha1: Optional[str] = None
    """
    Hardware device ID (e.g., IMEI); hashed via SHA1.
    """

    didmd5: Optional[str] = None
    """
    Hardware device ID (e.g., IMEI); hashed via MD5.
    """

    dpidsha1: Optional[str] = None
    """
    Platform device ID (e.g., Android ID); hashed via SHA1.
    """

    dpidmd5: Optional[str] = None
    """
    Platform device ID (e.g., Android ID); hashed via MD5.
    """

    macsha1: Optional[str] = None
    """
    MAC address of the device; hashed via SHA1.
    """

    macmd5: Optional[str] = None
    """
    MAC address of the device; hashed via MD5.
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """


class Geo(BaseModel):
    """
    This object encapsulates various methods for specifying a geographic location. When subordinate to a Device object, it indicates the location of the device which can also be interpreted as the user’s current location. When subordinate to a User object, it indicates the location of the user’s home base (i.e., not necessarily their current location).

    The lat/lon attributes should only be passed if they conform to the accuracy depicted in the type attribute. For example, the centroid of a geographic region such as postal code should not be passed.
    """

    lat: float
    """
    Latitude from -90.0 to +90.0, where negative is south.
    """

    lon: float = None
    """
    Longitude from -180.0 to +180.0, where negative is west.
    """

    type: Optional[int] = None
    """
    Source of location data; recommended when passing lat/lon. Refer to List: Location Types in AdCOM 1.0.
    """

    accuracy: Optional[int] = None
    """
    Estimated location accuracy in meters; recommended when lat/lon are specified and derived from a device’s location services (i.e., type = 1). Note that this is the accuracy as reported from the device. Consult OS specific documentation (e.g., Android, iOS) for exact interpretation.
    """

    lastfix: Optional[int] = None
    """
    Number of seconds since this geolocation fix was established. Note that devices may cache location data across multiple fetches. Ideally, this value should be from the time the actual fix was taken.
    """

    ipservice: Optional[int] = None
    """
    Service or provider used to determine geolocation from IP address if applicable (i.e., type = 2). Refer to List: IP Location Services in AdCOM 1.0.
    """

    country: Optional[str] = None
    """
    Country code using ISO-3166-1-alpha-3.
    """

    region: Optional[str] = None
    """
    Region code using ISO-3166-2; 2-letter state code if USA.
    """

    regionfips104: Optional[str] = None
    """
    Region of a country using FIPS 10-4 notation. While OpenRTB supports this attribute, it was withdrawn by NIST in 2008.
    """

    metro: Optional[str] = None
    """
    Google metro code; similar to but not exactly Nielsen DMAs. See Appendix A for a link to the codes.
    """

    city: Optional[str] = None
    """
    City using United Nations Code for Trade & Transport Locations. See Appendix A for a link to the codes.
    """

    zip: Optional[str] = None
    """
    ZIP or postal code.
    """

    utcoffset: Optional[int] = None
    """
    Local time as the number +/- of minutes from UTC.
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """


class User(BaseModel):
    """
    This object contains information known or derived about the human user of the device (i.e., the audience for advertising). The user id is an exchange artifact and may be subject to rotation or other privacy policies. However, when present, this user ID should be stable long enough to serve reasonably as the basis for frequency capping and retargeting.
    """

    id: Optional[str] = None
    """
    Exchange-specific ID for the user.
    """

    buyeruid: Optional[str] = None
    """
    Buyer-specific ID for the user as mapped by the exchange for the buyer.
    """

    yob: Optional[int] = None
    """
    Year of birth as a 4-digit integer.
    """

    gender: Optional[str] = None
    """
    Gender, where “M” = male, “F” = female, “O” = known to be other (i.e., omitted is unknown).
    """

    keywords: Optional[str] = None
    """
    Comma separated list of keywords, interests, or intent. Only one of keywords or kwarray may be present.
    """

    kwarray: Optional[List[str]] = None
    """
    Array of keywords about the user. Only one of keywords or kwarray may be present.
    """

    customdata: Optional[str] = None
    """
    Optional feature to pass bidder data that was set in the exchange’s cookie. The string must be in base85 cookie safe characters and be in any format. Proper JSON encoding must be used to include “escaped” quotation marks.
    """

    geo: Optional["Geo"] = None
    """
    Location of the user’s home base defined by a Geo object (Section 3.2.19). This is not necessarily their current location.
    """

    data: Optional[List["Data"]] = None
    """
    Additional user data. Each Data object (Section 3.2.21) represents a different data source.
    """

    consent: Optional[str] = None
    """
    When GDPR regulations are in effect this attribute contains the Transparency and Consent Framework’s Consent String data structure.
    """

    eids: Optional[List[Any]] = None
    """
    Details for support of a standard protocol for multiple third party identity providers (Section 3.2.27).
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """


class Data(BaseModel):
    """
    This object describes the network an ad will be displayed on. A Network is defined as the parent entity of the Channel object’s entity for the purposes of organizing Channels. Examples are companies that own and/or license a collection of content channels (Viacom, Discovery, CBS, WarnerMedia, Turner and others), or studio that creates such content and self-distributes content. Name is a human-readable field while domain and id can be used for reporting and targeting purposes. See 7.6 for further examples.
    """

    id: Optional[str] = None
    """
    A unique identifier assigned by the publisher. This may not be a unique identifier across all supply sources.
    """

    name: Optional[str] = None
    """
    Network the content is on (e.g., a TV network like “ABC")
    """

    segment: Optional[List["Segment"]] = None
    """
    The primary domain of the network (e.g. “abc.com” in the case of the network ABC). It is recommended to include the top private domain (PSL+1) for DSP targeting normalization purposes.
    """

    ext: Optional[Any] = None
    """
    Placeholder for exchange-specific extensions to OpenRTB.
    """


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

    device: Optional["Device"] = None
    """
    Details via a Device object (Section 3.2.11) about the user’s device to which the impression will be delivered.
    """

    user: Optional["User"] = None
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
