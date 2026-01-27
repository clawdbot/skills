from dataclasses import dataclass
from typing import Optional


@dataclass
class XrpcError:
    error: str
    message: Optional[str]
