from dataclasses import dataclass
from typing import Tuple, Optional, Dict


@dataclass
class RequestModel:
    method: str
    url: str
    params: Optional[Tuple] = None
    data: Optional[Dict] = None
    headers: Optional[Dict] = None
