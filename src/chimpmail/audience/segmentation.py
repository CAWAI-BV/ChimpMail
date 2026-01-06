from __future__ import annotations

from typing import Any, Callable

from chimpmail.audience.models import Contact, ConsentStatus, Segment, SegmentRule


class SegmentEvaluationError(ValueError):
    pass


def evaluate_segment(segment: Segment, contact: Contact) -> bool:
    return all(_evaluate_rule(rule, contact) for rule in segment.rules)


def _evaluate_rule(rule: SegmentRule, contact: Contact) -> bool:
    evaluators: dict[str, Callable[[Any, Any], bool]] = {
        "eq": lambda lhs, rhs: lhs == rhs,
        "contains": _contains,
        "in": _in_list,
        "gt": lambda lhs, rhs: lhs is not None and lhs > rhs,
        "lt": lambda lhs, rhs: lhs is not None and lhs < rhs,
        "has_tag": _has_tag,
        "consent_status": _consent_matches,
    }

    operator = rule.operator
    if operator not in evaluators:
        raise SegmentEvaluationError(f"Unsupported operator: {operator}")

    lhs = _resolve_value(rule.field, contact)
    return evaluators[operator](lhs, rule.value)


def _resolve_value(field: str, contact: Contact) -> Any:
    if field == "email":
        return contact.email
    if field == "first_name":
        return contact.first_name
    if field == "last_name":
        return contact.last_name
    if field == "tags":
        return contact.tags
    if field == "consent_status":
        return contact.consent_status

    return contact.attributes.get(field)


def _contains(lhs: Any, rhs: Any) -> bool:
    if lhs is None:
        return False
    return rhs in lhs


def _in_list(lhs: Any, rhs: Any) -> bool:
    if rhs is None:
        return False
    return lhs in rhs


def _has_tag(lhs: Any, rhs: Any) -> bool:
    if lhs is None:
        return False
    return rhs in lhs


def _consent_matches(lhs: Any, rhs: Any) -> bool:
    if isinstance(lhs, ConsentStatus):
        lhs_value = lhs.value
    else:
        lhs_value = lhs
    if isinstance(rhs, ConsentStatus):
        rhs_value = rhs.value
    else:
        rhs_value = rhs
    return lhs_value == rhs_value
