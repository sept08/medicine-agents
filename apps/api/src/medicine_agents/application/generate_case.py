from __future__ import annotations

from medicine_agents.application.ports import CaseRepository
from medicine_agents.domain.models import (
    CaseContent,
    CaseOrder,
    CasePackage,
    EvidenceRef,
    TeachingQuestion,
)


class GenerateCaseWorkflow:
    """S1 合成病例工作流，不读取外部资料或调用模型。"""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def run(self, order: CaseOrder) -> CasePackage:
        evidence = EvidenceRef(
            evidence_id="SYN-S1-001",
            source_id="synthetic-s1-generator",
            excerpt="这是为软件流程验证编写的合成依据，不对应真实患者或医学资料。",
            synthetic=True,
        )
        objective = order.teaching_objectives[0]
        package = CasePackage(
            order_id=order.order_id,
            synthetic=True,
            content=CaseContent(
                chief_complaint="合成主诉：用于验证病例生成流程。",
                present_illness="合成现病史：不包含真实患者事实。",
                examination_summary="合成检查摘要：未引用真实检查结果。",
                diagnosis_summary=f"合成诊断摘要：病种编码为 {order.disease_code}。",
                teaching_notes=f"当前教学目标：{objective}。仅用于软件流程验证。",
            ),
            questions=[
                TeachingQuestion(
                    level=order.difficulty,
                    question="该合成病例的首要教学目标是什么？",
                    answer=objective,
                    evidence_ids=[evidence.evidence_id],
                )
            ],
            evidence=[evidence],
        )
        self._repository.save(package)
        return package