import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/yams-harvest"


def source() -> str:
    return (SKILL / "SKILL.md").read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    return dict(line.split(":", 1) for line in match.group(1).splitlines())


class YamsHarvestTests(unittest.TestCase):
    def test_is_an_instruction_only_skill_with_exact_interface(self) -> None:
        files = sorted(
            path.relative_to(SKILL).as_posix()
            for path in SKILL.rglob("*")
            if path.is_file()
        )
        self.assertEqual(["SKILL.md", "agents/openai.yaml"], files)
        text = source()
        self.assertNotIn("[TODO", text)
        for forbidden in ("wiki.py", ".venv", "assets/", "scripts/"):
            self.assertNotIn(forbidden, text)

        metadata = {key: value.strip() for key, value in frontmatter(text).items()}
        self.assertEqual({"name", "description"}, set(metadata))
        self.assertEqual("yams-harvest", metadata["name"])
        self.assertTrue(metadata["description"].startswith("Use when "))
        self.assertIn("project history", metadata["description"])
        self.assertNotIn("yams-till", metadata["description"])
        self.assertNotIn("yams-sow", metadata["description"])
        self.assertNotIn("yams-cultivate", metadata["description"])

        interface = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Yams Harvest"', interface)
        self.assertIn(
            'short_description: "Recall durable project knowledge with Yams"',
            interface,
        )
        self.assertIn("$yams-harvest", interface)

    def test_covers_retrieval_outcomes_statuses_and_routing(self) -> None:
        text = source()
        self.assertIn('yams --json -k 5 "<focused question>"', text)
        for exit_code in range(5):
            self.assertRegex(text, rf"\| {exit_code} \|")
        for status in ("private", "historical", "in-progress", "current"):
            self.assertIn(f"`{status}`", text)
        self.assertIn("hits as leads", text)
        self.assertIn("primary", text)
        self.assertIn("store_missing", text)
        self.assertIn("yams --index", text)
        self.assertIn("yams-wiki catalog", text)
        self.assertIn("YAMS_ALLOW_NET=1", text)
        self.assertIn("model cache", text)
        self.assertNotIn("yams-wiki write", text)
        self.assertNotIn("Preserve one finding", text)
        self.assertIn("yams-sow", text)
        self.assertIn("yams-till", text)
        self.assertIn("yams-cultivate", text)
        self.assertNotIn("init plan", text)
        self.assertNotIn("init apply", text)
        self.assertNotIn("absent, minimal, full", text)
        self.assertIn("| 1 | Empty result |", text)
        self.assertNotIn("no corpus", text.lower())
        self.assertIn("YAMS_DEADLINE_EXCEEDED", text)
        self.assertIn("JSON `code`", text)


if __name__ == "__main__":
    unittest.main()
