from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Iterable


class ConsentStatus(str, Enum):
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBED = "unsubscribed"
    PENDING = "pending"
    UNKNOWN = "unknown"


class SuppressionReason(str, Enum):
    BOUNCE = "bounce"
    UNSUBSCRIBE = "unsubscribe"
    COMPLAINT = "complaint"
    MANUAL = "manual"


@dataclass(frozen=True)
class EngagementEvent:
    event_type: str
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Contact:
    contact_id: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)
    consent_status: ConsentStatus = ConsentStatus.UNKNOWN
    engagement_history: list[EngagementEvent] = field(default_factory=list)


@dataclass
class Audience:
    audience_id: str
    name: str
    description: str | None = None
    contact_ids: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class Tag:
    name: str


@dataclass(frozen=True)
class ConsentRecord:
    contact_id: str
    status: ConsentStatus
    timestamp: datetime
    source: str
    notes: str | None = None


@dataclass(frozen=True)
class SuppressionRecord:
    email: str
    reason: SuppressionReason
    timestamp: datetime
    source: str


@dataclass(frozen=True)
class SegmentRule:
    field: str
    operator: str
    value: Any


@dataclass
class Segment:
    segment_id: str
    name: str
    rules: list[SegmentRule]

    def required_fields(self) -> Iterable[str]:
        return {rule.field for rule in self.rules}
