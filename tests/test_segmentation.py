from chimpmail.audience.models import ConsentStatus, Contact, Segment, SegmentRule
from chimpmail.audience.segmentation import SegmentEvaluationError, evaluate_segment


def test_evaluate_segment_supports_multiple_rules():
    contact = Contact(contact_id="1", email="ada@example.com", tags={"vip"}, attributes={"age": 42})
    segment = Segment(
        segment_id="seg-1",
        name="VIP",
        rules=[
            SegmentRule(field="tags", operator="has_tag", value="vip"),
            SegmentRule(field="age", operator="gt", value=21),
        ],
    )

    assert evaluate_segment(segment, contact) is True


def test_evaluate_segment_handles_consent_status():
    contact = Contact(
        contact_id="1",
        email="ada@example.com",
        consent_status=ConsentStatus.SUBSCRIBED,
    )
    segment = Segment(
        segment_id="seg-2",
        name="Subscribed",
        rules=[
            SegmentRule(field="consent_status", operator="consent_status", value="subscribed"),
        ],
    )

    assert evaluate_segment(segment, contact) is True


def test_evaluate_segment_rejects_unknown_operator():
    contact = Contact(contact_id="1", email="ada@example.com")
    segment = Segment(
        segment_id="seg-3",
        name="Bad",
        rules=[SegmentRule(field="email", operator="wat", value="nope")],
    )

    try:
        evaluate_segment(segment, contact)
    except SegmentEvaluationError as exc:
        assert "Unsupported operator" in str(exc)
    else:
        raise AssertionError("SegmentEvaluationError not raised")
