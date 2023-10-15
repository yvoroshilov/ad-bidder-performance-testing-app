from typing import Optional

from pydantic import BaseModel


class AdRequest(BaseModel):
    timestamp: str
    language: Optional[str]


class AdResponse(BaseModel):
    html: str
