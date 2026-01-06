"""Audience and CRM foundational services."""

from chimpmail.audience.importer import ImportResult, import_contacts
from chimpmail.audience.models import (
    Audience,
    ConsentRecord,
    ConsentStatus,
    Contact,
    EngagementEvent,
    Segment,
    SegmentRule,
    SuppressionReason,
)
from chimpmail.audience.repository import InMemoryAudienceRepository
from chimpmail.audience.segmentation import SegmentEvaluationError, evaluate_segment

__all__ = [
    "Audience",
    "ConsentRecord",
    "ConsentStatus",
    "Contact",
    "EngagementEvent",
    "ImportResult",
    "InMemoryAudienceRepository",
    "Segment",
    "SegmentEvaluationError",
    "SegmentRule",
    "SuppressionReason",
    "evaluate_segment",
    "import_contacts",
]
