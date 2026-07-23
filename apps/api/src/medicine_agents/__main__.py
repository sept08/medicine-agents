from __future__ import annotations

import argparse
from pathlib import Path

from medicine_agents.application.generate_case import GenerateCaseWorkflow
from medicine_agents.domain.models import CaseOrder
from medicine_agents.infrastructure.file_case_repository import FileCaseRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="医学教学病例智能体 S1 工具")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="从合成订单生成并保存病例包")
    demo.add_argument("--order", type=Path, required=True, help="订单 JSON 路径")
    demo.add_argument("--data-dir", type=Path, required=True, help="本地运行数据目录")
    return parser


def run_demo(order_path: Path, data_dir: Path) -> int:
    order = CaseOrder.model_validate_json(order_path.read_text(encoding="utf-8"))
    repository = FileCaseRepository(data_dir)
    package = GenerateCaseWorkflow(repository).run(order)
    print(f"病例编号：{package.case_id}")
    print(f"输出路径：{repository.case_path(package.case_id)}")
    return 0


def main() -> int:
    arguments = build_parser().parse_args()
    if arguments.command == "demo":
        return run_demo(arguments.order, arguments.data_dir)
    raise AssertionError(f"不支持的命令：{arguments.command}")


if __name__ == "__main__":
    raise SystemExit(main())