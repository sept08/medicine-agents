from __future__ import annotations

import unittest

from scripts.check_sensitive_content import find_violations


class SensitiveContentCheckTests(unittest.TestCase):
    def test_rejects_wiki_paths_with_posix_or_windows_separators(self) -> None:
        self.assertTrue(find_violations("wiki/source.md", "safe", ["private-name"]))
        self.assertTrue(find_violations(r"wiki\source.md", "safe", ["private-name"]))

    def test_rejects_local_sensitive_terms_case_insensitively(self) -> None:
        violations = find_violations("docs/example.md", "Contains Private-Name", ["private-name"])
        self.assertIn("本机敏感词", violations[0])

    def test_rejects_common_personal_identifier_patterns(self) -> None:
        samples = [
            "contact: user" + chr(64) + "example.org",
            "mobile: " + "138" + "1234" + "5678",
            "identity: " + "110105" + "19491231" + "002X",
        ]
        for content in samples:
            with self.subTest(content=content):
                self.assertTrue(find_violations("docs/example.md", content, ["private-name"]))

    def test_accepts_safe_cross_platform_text(self) -> None:
        violations = find_violations(
            "docs/guide.md",
            "仅包含合成数据和跨平台运行说明。",
            ["private-name"],
        )
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
