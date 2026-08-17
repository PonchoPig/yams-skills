import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/yams-sow"


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


class YamsSowTests(unittest.TestCase):
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
        self.assertEqual("yams-sow", metadata["name"])
        self.assertTrue(metadata["description"].startswith("Use when "))
        self.assertIn("verified", metadata["description"])
        self.assertIn("Never trigger merely", metadata["description"])
        self.assertNotIn("yams-harvest", metadata["description"])
        self.assertNotIn("yams-till", metadata["description"])
        self.assertNotIn("yams-cultivate", metadata["description"])

        interface = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Yams Sow"', interface)
        self.assertIn(
            'short_description: "Preserve one verified durable Yams finding"',
            interface,
        )
        self.assertIn("$yams-sow", interface)

    def test_agent_decides_and_writes_through_yams(self) -> None:
        text = source()
        prose = " ".join(text.split())
        self.assertIn("agent decides", prose.casefold())
        self.assertIn("not write triggers", prose.casefold())
        self.assertIn("does not initialize missing memory", prose.casefold())
        self.assertIn("yams-wiki write .agents/memory < /path/to/write-request.json", text)
        self.assertIn("yams-wiki catalog .agents/memory", text)
        self.assertIn("yams-wiki check .agents/memory", text)
        self.assertIn("git status --short .agents/memory/", text)
        self.assertIn(".agents/memory/SCHEMA.md", text)
        self.assertIn("yams-harvest", text)
        self.assertIn("yams-till", text)
        self.assertIn("yams-cultivate", text)
        self.assertNotIn("init plan", text)
        self.assertNotIn("init apply", text)
        self.assertNotIn("memory-search --json", text)


if __name__ == "__main__":
    unittest.main()
