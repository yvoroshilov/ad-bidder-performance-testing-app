from typing import Optional

from pydantic import BaseModel


class BidRequest(BaseModel):
    id: str
    timestamp: str
    language: Optional[str]
