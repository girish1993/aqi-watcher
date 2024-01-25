from dataclasses import dataclass
from typing import Optional, Dict
from multidict import MultiDict


@dataclass
class RequestModel:
    method: str
    url: str
    route: str
    params: Optional[MultiDict] = None
    data: Optional[Dict] = None
    headers: Optional[Dict] = None
