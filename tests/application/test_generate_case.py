from medicine_agents.application.generate_case import GenerateCaseWorkflow
from medicine_agents.infrastructure.file_case_repository import FileCaseRepository


def test_workflow_generates_and_persists_synthetic_package(
    tmp_path, synthetic_order
) -> None:
    repository = FileCaseRepository(tmp_path)
    workflow = GenerateCaseWorkflow(repository=repository)

    package = workflow.run(synthetic_order)

    assert package.order_id == synthetic_order.order_id
    assert package.status.value == "draft"
    assert package.synthetic is True
    assert len(package.questions) == 1
    assert repository.get(package.case_id) == package


def test_workflow_question_references_its_synthetic_evidence(
    tmp_path, synthetic_order
) -> None:
    package = GenerateCaseWorkflow(FileCaseRepository(tmp_path)).run(synthetic_order)

    assert package.questions[0].evidence_ids == [package.evidence[0].evidence_id]
    assert all(reference.synthetic for reference in package.evidence)