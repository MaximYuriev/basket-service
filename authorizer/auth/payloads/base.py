from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(frozen=True, eq=False)
class BasePayload:
    sub: str
    iat: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
