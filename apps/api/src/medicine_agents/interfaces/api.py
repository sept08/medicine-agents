from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, status

from medicine_agents.application.generate_case import GenerateCaseWorkflow
from medicine_agents.domain.models import CaseOrder, CasePackage
from medicine_agents.infrastructure.file_case_repository import FileCaseRepository


def create_app(data_dir: Path | str) -> FastAPI:
    repository = FileCaseRepository(data_dir)
    workflow = GenerateCaseWorkflow(repository)
    application = FastAPI(title="医学教学病例智能体", version="0.1.0")

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "stage": "S1"}

    @application.post(
        "/api/orders",
        response_model=CasePackage,
        status_code=status.HTTP_201_CREATED,
    )
    def create_order(order: CaseOrder) -> CasePackage:
        return workflow.run(order)

    return application


app = create_app(Path(os.environ.get("MEDICINE_AGENTS_DATA_DIR", "data/runtime")))