import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/yams-cultivate"


def source() -> str:
    return (SKILL / "SKILL.md").read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    return {
        key: value.strip()
        for key, value in (line.split(":", 1) for line in match.group(1).splitlines())
    }


class YamsCultivateTests(unittest.TestCase):
    def test_is_an_instruction_only_skill_with_explicit_triggers(self) -> None:
        files = sorted(
            path.relative_to(SKILL).as_posix()
            for path in SKILL.rglob("*")
            if path.is_file()
        )
        self.assertEqual(["SKILL.md", "agents/openai.yaml"], files)
        text = source()
        metadata = frontmatter(text)
        self.assertEqual({"name", "description"}, set(metadata))
        self.assertEqual("yams-cultivate", metadata["name"])
        self.assertTrue(metadata["description"].startswith("Use when "))
        for trigger in ("validate", "audit", "refresh", "consolidate", "repair"):
            self.assertIn(trigger, metadata["description"])
        for forbidden in ("[TODO", "wiki.py", ".venv", "assets/", "scripts/"):
            self.assertNotIn(forbidden, text)

        interface = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Yams Cultivate"', interface)
        self.assertIn(
            'short_description: "Audit and maintain durable Yams memory"',
            interface,
        )
        self.assertIn("$yams-cultivate", interface)

    def test_separates_read_only_and_authorized_maintenance(self) -> None:
        text = source()
        prose = " ".join(text.split())
        folded = prose.casefold()
        self.assertIn("read-only", folded)
        self.assertIn("maintenance", folded)
        self.assertIn("do not edit", folded)
        self.assertIn("do not run `catalog`", folded)
        self.assertIn("continue", folded)
        self.assertIn("uncommitted", folded)
        self.assertIn("stop", folded)
        self.assertIn("unclear ownership", folded)
        self.assertIn("does not initialize missing memory", folded)

    def test_uses_yams_contract_for_structure_truth_and_writes(self) -> None:
        text = source()
        prose = " ".join(text.split())
        required = (
            "yams-wiki capabilities --json",
            "wiki_maintenance",
            ".agents/memory/SCHEMA.md",
            "ten oldest",
            "current",
            "in-progress",
            "memory: cultivate pass",
            "memory: curate pass",
            "memory: garden pass",
            "first commit touching `.agents/memory`",
            "yams-wiki check .agents/memory",
            "yams-wiki write .agents/memory < /path/to/write-request.json",
            "yams-wiki catalog .agents/memory",
            "git diff -- .agents/memory",
            "primary",
            "historical",
            "forward link",
            "propose",
            "updated:",
            "verified:",
            "memory: cultivate pass YYYY-MM-DD",
        )
        for value in required:
            self.assertIn(value, prose)
        self.assertIn("Structural success is only the floor", prose)
        self.assertIn("separate authorization", prose)
        self.assertNotIn("python ", text)


if __name__ == "__main__":
    unittest.main()
