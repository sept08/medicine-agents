from __future__ import annotations

from typing import Protocol
from uuid import UUID

from medicine_agents.domain.models import CasePackage


class CaseRepository(Protocol):
    def save(self, package: CasePackage) -> None: ...

    def get(self, case_id: UUID) -> CasePackage: ...