from uuid import uuid4

import pytest

from medicine_agents.domain.models import CaseStatus
from medicine_agents.infrastructure.file_case_repository import (
    CaseNotFoundError,
    FileCaseRepository,
)


def test_repository_round_trips_case_package(tmp_path, sample_case_package) -> None:
    repository = FileCaseRepository(tmp_path)
    repository.save(sample_case_package)

    loaded = repository.get(sample_case_package.case_id)

    assert loaded == sample_case_package
    assert (
        tmp_path / "cases" / str(sample_case_package.case_id) / "current.json"
    ).exists()
    assert not list(tmp_path.rglob("*.tmp"))


def test_repository_reports_missing_case(tmp_path) -> None:
    repository = FileCaseRepository(tmp_path)

    with pytest.raises(CaseNotFoundError):
        repository.get(uuid4())


def test_repository_overwrites_current_version_atomically(
    tmp_path, sample_case_package
) -> None:
    repository = FileCaseRepository(tmp_path)
    repository.save(sample_case_package)
    updated = sample_case_package.model_copy(update={"status": CaseStatus.QC_PASSED})

    repository.save(updated)

    assert repository.get(updated.case_id).status is CaseStatus.QC_PASSED
    assert not list(tmp_path.rglob("*.tmp"))