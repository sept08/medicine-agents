from pydantic import ValidationError
import pytest

from medicine_agents.domain.models import CaseOrder, CaseStatus, Difficulty


def test_case_order_requires_teaching_objective() -> None:
    with pytest.raises(ValidationError):
        CaseOrder(
            disease_code="DKD",
            difficulty=Difficulty.BASIC,
            target_audience="undergraduate",
            teaching_objectives=[],
        )


def test_new_case_status_is_draft() -> None:
    assert CaseStatus.DRAFT.value == "draft"


def test_case_order_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        CaseOrder(
            disease_code="DKD",
            difficulty=Difficulty.BASIC,
            target_audience="undergraduate",
            teaching_objectives=["识别关键临床线索"],
            unknown="value",
        )