from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated, Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


NonEmptyText = Annotated[str, Field(min_length=1)]


class DiseaseCode(StrEnum):
    DKD = "DKD"
    CKD = "CKD"
    AKI = "AKI"
    CHF = "CHF"
    AMI = "AMI"
    HTN_EMERGENCY = "HTN_EMERGENCY"


class Difficulty(StrEnum):
    BASIC = "basic"
    ADVANCED = "advanced"


class CaseLength(StrEnum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class CaseStatus(StrEnum):
    DRAFT = "draft"
    QC_PASSED = "qc_passed"
    AWAITING_MEDICAL_REVIEW = "awaiting_medical_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    RETIRED = "retired"


class CaseOrder(StrictModel):
    order_id: UUID = Field(default_factory=uuid4)
    disease_code: DiseaseCode
    difficulty: Difficulty
    target_audience: str = Field(min_length=1)
    teaching_objectives: list[NonEmptyText] = Field(min_length=1)
    length: CaseLength = CaseLength.SHORT


class EvidenceRef(StrictModel):
    evidence_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    synthetic: bool


class TeachingQuestion(StrictModel):
    level: Difficulty
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    evidence_ids: list[NonEmptyText] = Field(min_length=1)


class CaseContent(StrictModel):
    chief_complaint: str = Field(min_length=1)
    present_illness: str = Field(min_length=1)
    examination_summary: str = Field(min_length=1)
    diagnosis_summary: str = Field(min_length=1)
    teaching_notes: str = Field(min_length=1)


class CasePackage(StrictModel):
    case_id: UUID = Field(default_factory=uuid4)
    order_id: UUID
    status: CaseStatus = CaseStatus.DRAFT
    synthetic: bool
    content: CaseContent
    questions: list[TeachingQuestion] = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def references_known_evidence(self) -> Self:
        known_ids = {reference.evidence_id for reference in self.evidence}
        unknown_ids = {
            evidence_id
            for question in self.questions
            for evidence_id in question.evidence_ids
            if evidence_id not in known_ids
        }
        if unknown_ids:
            unknown = ", ".join(sorted(unknown_ids))
            raise ValueError(f"问题引用了不存在的证据：{unknown}")
        return self