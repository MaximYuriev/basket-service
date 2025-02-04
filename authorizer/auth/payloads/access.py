from dataclasses import dataclass, field
from datetime import datetime, UTC

from .base import BasePayload
from .commons import ACCESS_TOKEN_EXPIRE_VALUE, ACCESS_TOKEN_TYPE


@dataclass(frozen=True, eq=False)
class AccessPayload(BasePayload):
    type: str = field(default=ACCESS_TOKEN_TYPE, kw_only=True)
    role: str
    exp: datetime = field(default_factory=lambda: datetime.now(UTC) + ACCESS_TOKEN_EXPIRE_VALUE, kw_only=True)
