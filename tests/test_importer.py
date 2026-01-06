from datetime import datetime

from chimpmail.audience.importer import apply_list_hygiene, import_contacts, suppression_from_unsubscribe
from chimpmail.audience.models import ConsentStatus, SuppressionReason


def test_import_contacts_validates_and_records_consent():
    rows = [
        {"email": "Ada@example.com", "first_name": "Ada"},
        {"email": "", "first_name": "Nope"},
    ]
    now = datetime(2024, 1, 1)

    result, consent_records = import_contacts(rows, default_consent=ConsentStatus.SUBSCRIBED, now=now)

    assert [contact.email for contact in result.accepted] == ["ada@example.com"]
    assert result.rejected[0].row_number == 2
    assert consent_records[0].status is ConsentStatus.SUBSCRIBED
    assert consent_records[0].timestamp == now


def test_apply_list_hygiene_splits_suppressed():
    result, _ = import_contacts([{"email": "ada@example.com"}])
    active, suppressed = apply_list_hygiene(result.accepted, {"ada@example.com"})

    assert active == []
    assert len(suppressed) == 1


def test_suppression_from_unsubscribe_returns_record():
    record = suppression_from_unsubscribe("Ada@Example.com")

    assert record.email == "ada@example.com"
    assert record.reason is SuppressionReason.UNSUBSCRIBE
    assert record.source == "unsubscribe"
