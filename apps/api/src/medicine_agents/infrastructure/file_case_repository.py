from __future__ import annotations

import os
from pathlib import Path
from uuid import UUID, uuid4

from medicine_agents.domain.models import CasePackage


class CaseNotFoundError(LookupError):
    """请求的病例包不存在。"""


class FileCaseRepository:
    def __init__(self, data_dir: Path | str) -> None:
        self._data_dir = Path(data_dir)

    def save(self, package: CasePackage) -> None:
        target = self.case_path(package.case_id)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
        payload = f"{package.model_dump_json(indent=2)}\n".encode()

        try:
            with temporary.open("xb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)

    def get(self, case_id: UUID) -> CasePackage:
        target = self.case_path(case_id)
        try:
            payload = target.read_text(encoding="utf-8")
        except FileNotFoundError as error:
            raise CaseNotFoundError(f"病例不存在：{case_id}") from error
        return CasePackage.model_validate_json(payload)

    def case_path(self, case_id: UUID) -> Path:
        return self._data_dir / "cases" / str(case_id) / "current.json"