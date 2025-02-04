from dataclasses import dataclass, field
from datetime import datetime, UTC

from .base import BasePayload
from .commons import REFRESH_TOKEN_TYPE, REFRESH_TOKEN_EXPIRE_VALUE


@dataclass(frozen=True, eq=False)
class RefreshPayload(BasePayload):
    type: str = field(default=REFRESH_TOKEN_TYPE, kw_only=True)
    exp: datetime = field(default_factory=lambda: datetime.now(UTC) + REFRESH_TOKEN_EXPIRE_VALUE, kw_only=True)
