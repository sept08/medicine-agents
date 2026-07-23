from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ProjectBaselineTests(unittest.TestCase):
    def test_required_project_boundaries_exist(self) -> None:
        required = [
            "apps/api/src/medicine_agents",
            "apps/web",
            "config/diseases",
            "config/prompts",
            "config/quality-rules",
            "data/samples/orders",
            "docs/requirements",
            "docs/quality",
            "docs/governance",
            "docs/guides",
            "project/stages",
            "scripts",
        ]
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual([], missing)

    def test_python_build_metadata_is_ignored(self) -> None:
        result = subprocess.run(
            [
                "git",
                "check-ignore",
                "-q",
                "--no-index",
                "apps/api/src/medicine_agents.egg-info/PKG-INFO",
            ],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(0, result.returncode)

    def test_current_status_has_required_operational_fields(self) -> None:
        text = (ROOT / "project/CURRENT_STATUS.md").read_text(encoding="utf-8")
        for heading in [
            "当前阶段",
            "本阶段验收目标",
            "已完成",
            "正在进行",
            "当前阻塞",
            "等待医学团队输入",
            "下一可体验入口",
            "下一步",
        ]:
            self.assertIn(heading, text)

    def test_roadmap_lists_every_frozen_stage(self) -> None:
        text = (ROOT / "project/ROADMAP.md").read_text(encoding="utf-8")
        for stage in ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]:
            self.assertIn(stage, text)

    def test_input_register_declares_blocking_level(self) -> None:
        text = (ROOT / "project/INPUT_REGISTER.md").read_text(encoding="utf-8")
        for field in ["输入编号", "目标阶段", "最晚需要时间", "阻塞等级", "验收人"]:
            self.assertIn(field, text)

    def test_prd_uses_frozen_case_scale(self) -> None:
        text = (ROOT / "docs/requirements/产品需求文档.md").read_text(encoding="utf-8")
        self.assertIn("6 个病种", text)
        self.assertIn("30 个", text)
        self.assertIn("20 个病种", text)
        self.assertIn("100 个", text)
        self.assertNotIn("30 个病种", text)
        self.assertNotIn("每病种 20", text)

    def test_prd_declares_single_operator_file_first_mvp(self) -> None:
        text = (ROOT / "docs/requirements/产品需求文档.md").read_text(encoding="utf-8")
        self.assertIn("单操作者", text)
        self.assertIn("文件优先", text)
        self.assertIn("本 PRD 已覆盖 MVP 开工所需", text)

    def test_quality_plan_covers_metrics_and_statistics(self) -> None:
        text = (ROOT / "docs/quality/质量评价与统计分析方案.md").read_text(encoding="utf-8")
        for term in [
            "原子事实准确率",
            "无依据陈述率",
            "逻辑自洽率",
            "严重医学错误",
            "ICC(2,k)",
            "Fleiss' Kappa",
            "TOST",
            "意向性分析",
            "缺失数据",
            "版本冻结",
        ]:
            self.assertIn(term, text)
if __name__ == "__main__":
    unittest.main()
