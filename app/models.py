from pydantic import BaseModel
from typing import Any

class Opportunity(BaseModel):
    id: str
    source: str          # rss/github/...
    type: str            # incentive/testnet/governance/release/...
    title: str
    url: str
    ts: str              # ISO string
    score: float
    meta: dict[str, Any] = {}