from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class CrossPlatformContractTests(unittest.TestCase):
    def test_pre_commit_hook_uses_runnable_python_fallbacks(self) -> None:
        hook = (ROOT / ".githooks" / "pre-commit").read_text(encoding="utf-8")
        self.assertIn("supports_required_python", hook)
        self.assertIn("python3", hook)
        self.assertIn("python", hook)
        self.assertNotIn("pwsh", hook)
        self.assertNotIn("powershell.exe", hook)

    def test_ci_runs_security_tests_on_windows_and_macos(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("windows-latest", workflow)
        self.assertIn("macos-latest", workflow)
        self.assertIn(".[dev]", workflow)
        self.assertIn("python scripts/test.py", workflow)


if __name__ == "__main__":
    unittest.main()
