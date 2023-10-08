from dataclasses import dataclass
from typing import Optional, Dict

from pydantic import BaseModel


@dataclass
class AdRequest(BaseModel):
    timestamp: str
    language: Optional[str]
    cookies: Dict[str, str]


class AdResponse(BaseModel):
    html: str
