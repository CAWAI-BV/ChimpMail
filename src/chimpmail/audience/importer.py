from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import re
from typing import Any, Iterable

from chimpmail.audience.models import (
    Contact,
    ConsentRecord,
    ConsentStatus,
    SuppressionReason,
    SuppressionRecord,
)


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class ImportFailure:
    row_number: int
    email: str | None
    reason: str


@dataclass
class ImportResult:
    accepted: list[Contact] = field(default_factory=list)
    rejected: list[ImportFailure] = field(default_factory=list)


def import_contacts(
    rows: Iterable[dict[str, Any]],
    *,
    default_consent: ConsentStatus = ConsentStatus.PENDING,
    now: datetime | None = None,
) -> tuple[ImportResult, list[ConsentRecord]]:
    timestamp = now or datetime.utcnow()
    result = ImportResult()
    consent_records: list[ConsentRecord] = []

    for index, row in enumerate(rows, start=1):
        email = _normalize_email(row.get("email"))
        if not email:
            result.rejected.append(
                ImportFailure(index, None, "Missing or invalid email")
            )
            continue
        if not EMAIL_PATTERN.match(email):
            result.rejected.append(ImportFailure(index, email, "Invalid email"))
            continue

        contact_id = row.get("contact_id") or email
        contact = Contact(
            contact_id=contact_id,
            email=email,
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            attributes=_extract_attributes(row),
            tags=set(row.get("tags", []) or []),
            consent_status=default_consent,
        )
        result.accepted.append(contact)
        consent_records.append(
            ConsentRecord(
                contact_id=contact_id,
                status=default_consent,
                timestamp=timestamp,
                source="import",
            )
        )

    return result, consent_records


def apply_list_hygiene(
    contacts: Iterable[Contact],
    suppressed_emails: set[str],
) -> tuple[list[Contact], list[Contact]]:
    active: list[Contact] = []
    suppressed: list[Contact] = []
    for contact in contacts:
        if contact.email.lower() in suppressed_emails:
            suppressed.append(contact)
        else:
            active.append(contact)
    return active, suppressed


def suppression_from_unsubscribe(
    email: str, *, timestamp: datetime | None = None
) -> SuppressionRecord:
    event_time = timestamp or datetime.utcnow()
    return SuppressionRecord(
        email=email.lower(),
        reason=SuppressionReason.UNSUBSCRIBE,
        timestamp=event_time,
        source="unsubscribe",
    )


def _normalize_email(value: Any) -> str | None:
    if not value:
        return None
    if not isinstance(value, str):
        return None
    cleaned = value.strip().lower()
    return cleaned or None


def _extract_attributes(row: dict[str, Any]) -> dict[str, Any]:
    reserved = {"email", "contact_id", "first_name", "last_name", "tags"}
    return {key: value for key, value in row.items() if key not in reserved}
