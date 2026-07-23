from pathlib import Path

from pydantic import ValidationError
import pytest

from medicine_agents.domain.models import (
    CaseOrder,
    CasePackage,
    CaseStatus,
    Difficulty,
)


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

def test_synthetic_sample_matches_order_contract() -> None:
    root = Path(__file__).resolve().parents[2]
    order = CaseOrder.model_validate_json(
        (root / "data/samples/orders/synthetic-order.json").read_text(encoding="utf-8")
    )

    assert order.length.value == "short"

def test_case_order_rejects_blank_teaching_objective() -> None:
    with pytest.raises(ValidationError):
        CaseOrder(
            disease_code="DKD",
            difficulty=Difficulty.BASIC,
            target_audience="undergraduate",
            teaching_objectives=["   "],
        )


def test_case_order_rejects_unsupported_disease() -> None:
    with pytest.raises(ValidationError):
        CaseOrder(
            disease_code="NOT_CONFIGURED",
            difficulty=Difficulty.BASIC,
            target_audience="undergraduate",
            teaching_objectives=["识别关键临床线索"],
        )


def test_case_package_rejects_unknown_evidence_reference(sample_case_package) -> None:
    payload = sample_case_package.model_dump()
    payload["questions"][0]["evidence_ids"] = ["MISSING"]

    with pytest.raises(ValidationError):
        CasePackage.model_validate(payload)