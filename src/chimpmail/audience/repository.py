from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable

from chimpmail.audience.importer import apply_list_hygiene
from chimpmail.audience.models import (
    Audience,
    ConsentRecord,
    ConsentStatus,
    Contact,
    Segment,
    SuppressionRecord,
)
from chimpmail.audience.segmentation import evaluate_segment


@dataclass
class InMemoryAudienceRepository:
    contacts: dict[str, Contact] = field(default_factory=dict)
    audiences: dict[str, Audience] = field(default_factory=dict)
    segments: dict[str, Segment] = field(default_factory=dict)
    consent_records: list[ConsentRecord] = field(default_factory=list)
    suppression_records: dict[str, SuppressionRecord] = field(default_factory=dict)
    engagement_history: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    def add_audience(self, audience: Audience) -> None:
        self.audiences[audience.audience_id] = audience

    def add_contact(self, contact: Contact, *, audience_id: str | None = None) -> None:
        self.contacts[contact.contact_id] = contact
        if audience_id:
            self.assign_contact_to_audience(contact.contact_id, audience_id)

    def assign_contact_to_audience(self, contact_id: str, audience_id: str) -> None:
        if audience_id not in self.audiences:
            raise KeyError(f"Audience not found: {audience_id}")
        if contact_id not in self.contacts:
            raise KeyError(f"Contact not found: {contact_id}")
        self.audiences[audience_id].contact_ids.add(contact_id)

    def record_consent(self, record: ConsentRecord) -> None:
        self.consent_records.append(record)
        contact = self.contacts.get(record.contact_id)
        if contact:
            contact.consent_status = record.status

    def suppress_email(self, record: SuppressionRecord) -> None:
        self.suppression_records[record.email.lower()] = record
        for contact in self.contacts.values():
            if contact.email.lower() == record.email.lower():
                contact.consent_status = ConsentStatus.UNSUBSCRIBED

    def import_contacts(
        self,
        contacts: Iterable[Contact],
        *,
        audience_id: str | None = None,
    ) -> tuple[list[Contact], list[Contact]]:
        suppressed_emails = set(self.suppression_records.keys())
        active, suppressed = apply_list_hygiene(contacts, suppressed_emails)
        for contact in active:
            self.add_contact(contact, audience_id=audience_id)
        return active, suppressed

    def create_segment(self, segment: Segment) -> None:
        self.segments[segment.segment_id] = segment

    def evaluate_segment(self, segment_id: str) -> list[Contact]:
        segment = self.segments[segment_id]
        return [
            contact
            for contact in self.contacts.values()
            if evaluate_segment(segment, contact)
        ]

    def record_engagement_detail(
        self, contact_id: str, event: str, *, timestamp: datetime | None = None
    ) -> None:
        from chimpmail.audience.models import EngagementEvent

        event_time = timestamp or datetime.utcnow()
        contact = self.contacts.get(contact_id)
        if contact:
            contact.engagement_history.append(
                EngagementEvent(event_type=event, timestamp=event_time)
            )
