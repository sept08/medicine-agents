from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


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
    disease_code: str = Field(min_length=1)
    difficulty: Difficulty
    target_audience: str = Field(min_length=1)
    teaching_objectives: list[str] = Field(min_length=1)
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
    evidence_ids: list[str] = Field(min_length=1)


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