from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
