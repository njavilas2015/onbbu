from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DNSRecord:
    id: str
    name: str
    record_type: str
    content: str
    proxied: bool
    ttl: int
    comment: Optional[str]
    created_on: str
    modified_on: str
