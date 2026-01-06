from datetime import datetime

from chimpmail.audience.models import (
    Audience,
    ConsentRecord,
    ConsentStatus,
    Contact,
    Segment,
    SegmentRule,
    SuppressionReason,
    SuppressionRecord,
)
from chimpmail.audience.repository import InMemoryAudienceRepository


def test_repository_assigns_contacts_and_segments():
    repo = InMemoryAudienceRepository()
    audience = Audience(audience_id="aud-1", name="Main")
    repo.add_audience(audience)

    contact = Contact(contact_id="1", email="ada@example.com", tags={"vip"})
    repo.add_contact(contact, audience_id="aud-1")

    segment = Segment(
        segment_id="seg-1",
        name="VIP",
        rules=[SegmentRule(field="tags", operator="has_tag", value="vip")],
    )
    repo.create_segment(segment)

    matches = repo.evaluate_segment("seg-1")

    assert matches == [contact]
    assert "1" in repo.audiences["aud-1"].contact_ids


def test_repository_updates_consent_and_suppression():
    repo = InMemoryAudienceRepository()
    contact = Contact(contact_id="1", email="ada@example.com")
    repo.add_contact(contact)

    repo.record_consent(
        ConsentRecord(
            contact_id="1",
            status=ConsentStatus.SUBSCRIBED,
            timestamp=datetime(2024, 1, 1),
            source="signup",
        )
    )

    assert repo.contacts["1"].consent_status is ConsentStatus.SUBSCRIBED

    repo.suppress_email(
        record=SuppressionRecord(
            email="ada@example.com",
            reason=SuppressionReason.BOUNCE,
            timestamp=datetime(2024, 1, 2),
            source="bounce",
        ),
    )

    assert repo.contacts["1"].consent_status is ConsentStatus.UNSUBSCRIBED
