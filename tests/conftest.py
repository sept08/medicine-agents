from datetime import UTC, datetime
from uuid import UUID

import pytest

from medicine_agents.domain.models import (
    CaseContent,
    CaseOrder,
    CasePackage,
    CaseStatus,
    Difficulty,
    EvidenceRef,
    TeachingQuestion,
)


@pytest.fixture
def synthetic_order() -> CaseOrder:
    return CaseOrder(
        order_id=UUID("00000000-0000-0000-0000-000000000001"),
        disease_code="DKD",
        difficulty=Difficulty.BASIC,
        target_audience="undergraduate",
        teaching_objectives=["识别关键临床线索"],
    )


@pytest.fixture
def sample_case_package(synthetic_order: CaseOrder) -> CasePackage:
    evidence = EvidenceRef(
        evidence_id="SYN-001",
        source_id="synthetic-fixture",
        excerpt="这是不对应任何真实患者或来源材料的合成证据。",
        synthetic=True,
    )
    question = TeachingQuestion(
        level="basic",
        question="该合成病例首先需要识别哪类线索？",
        answer="需要识别订单指定的关键临床线索。",
        evidence_ids=[evidence.evidence_id],
    )
    return CasePackage(
        case_id=UUID("00000000-0000-0000-0000-000000000101"),
        order_id=synthetic_order.order_id,
        status=CaseStatus.DRAFT,
        synthetic=True,
        content=CaseContent(
            chief_complaint="合成主诉",
            present_illness="合成现病史摘要",
            examination_summary="合成检查摘要",
            diagnosis_summary="合成诊断摘要",
            teaching_notes="仅用于验证软件流程。",
        ),
        questions=[question],
        evidence=[evidence],
        created_at=datetime(2026, 7, 22, tzinfo=UTC),
    )