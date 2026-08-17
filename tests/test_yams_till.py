import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/yams-till"


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


def literal_plan_request(text: str) -> dict[str, object]:
    match = re.search(
        r"### Complete project-page example\n.*?```json\n(.*?)\n```",
        text,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("SKILL.md must contain the complete project-page JSON")
    return json.loads(match.group(1))


class YamsTillTests(unittest.TestCase):
    def test_is_an_explicit_instruction_only_skill(self) -> None:
        files = sorted(
            path.relative_to(SKILL).as_posix()
            for path in SKILL.rglob("*")
            if path.is_file()
        )
        self.assertEqual(["SKILL.md", "agents/openai.yaml"], files)
        text = source()
        metadata = frontmatter(text)
        self.assertEqual({"name", "description"}, set(metadata))
        self.assertEqual("yams-till", metadata["name"])
        self.assertTrue(metadata["description"].startswith("Use only when "))
        self.assertIn("explicitly asks", metadata["description"])
        self.assertIn("Never trigger merely", metadata["description"])
        for forbidden in ("[TODO", "wiki.py", ".venv", "assets/", "scripts/"):
            self.assertNotIn(forbidden, text)

        interface = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Yams Till"', interface)
        self.assertIn(
            'short_description: "Set up or upgrade Yams project memory"',
            interface,
        )
        self.assertIn("$yams-till", interface)

    def test_uses_capability_inspect_plan_approval_apply_contract(self) -> None:
        text = source()
        prose = " ".join(text.split())
        required = (
            "command -v yams-wiki",
            "yams-wiki capabilities --json",
            "repository_layout",
            "init_manifest >= 3",
            "yams-wiki init inspect --json",
            "inspection_sha256",
            "mktemp -d",
            '"title"',
            '"page_type"',
            "one durable fact",
            "yams-wiki init plan --from-inspect",
            "--project-page",
            "--request",
            "manifest_sha256",
            "proposal",
            "operations",
            "destination",
            "canonical layout asset",
            "recommended_mode",
            "explicit approval",
            "yams-wiki init apply --manifest",
            "drift",
            "created",
            "changed",
            "removed",
            "restored",
            "unresolved",
            "final_layout",
            "`next`",
            "yams --index",
            "yams-wiki catalog",
            "yams --json -k 5",
        )
        for value in required:
            self.assertIn(value, prose)
        self.assertLess(prose.index("init inspect"), prose.index("init plan"))
        self.assertLess(prose.index("init plan"), prose.index("explicit approval"))
        self.assertLess(prose.index("explicit approval"), prose.index("init apply"))
        apply_at = prose.index("yams-wiki init apply --manifest")
        index_at = prose.index("yams --index", apply_at)
        search_at = prose.index("yams --json -k 5", index_at)
        self.assertLess(apply_at, index_at)
        self.assertLess(index_at, search_at)
        self.assertIn("initial request is not write approval", prose)
        self.assertIn("saved manifest", prose)
        self.assertIn("must not regenerate", prose)
        self.assertIn("uncommitted", prose)
        self.assertIn("yams-harvest", prose)
        self.assertIn("yams-sow", prose)

    def test_literal_plan_request_matches_and_executes_verified_contract(self) -> None:
        text = source()
        request = literal_plan_request(text)
        self.assertEqual(
            {
                "title",
                "page_type",
                "fact",
                "why",
                "how_to_apply",
                "falsified_by",
                "summary",
            },
            set(request),
        )
        self.assertIn("Populate the required project-page keys", text)
        self.assertIn("Do not substitute conceptual aliases", text)
        self.assertIn("Save the inspection and project-page JSON", text)

        binary = os.environ.get("YAMS_WIKI")
        if binary is None:
            self.skipTest("set YAMS_WIKI to run the product integration")

        with tempfile.TemporaryDirectory(prefix="yams-till-skill-test-") as temporary:
            repository = Path(temporary) / "fictional-project"
            repository.mkdir()
            environment = os.environ.copy()
            environment.update(
                {
                    "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": os.devnull,
                    "HOME": str(repository),
                }
            )
            subprocess.run(
                ["git", "-C", str(repository), "init", "--quiet"],
                check=True,
                env=environment,
            )
            inspected = subprocess.run(
                [binary, "init", "inspect", "--json", str(repository)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            inspection_path = Path(temporary) / "inspection.json"
            inspection_path.write_text(inspected.stdout, encoding="utf-8")
            page_path = Path(temporary) / "project-page.json"
            page_path.write_text(json.dumps(request), encoding="utf-8")
            planned = subprocess.run(
                [
                    binary,
                    "init",
                    "plan",
                    "--from-inspect",
                    str(inspection_path),
                    "--project-page",
                    str(page_path),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
            self.assertEqual(0, planned.returncode, planned.stderr)
            envelope = json.loads(planned.stdout)
            self.assertIs(envelope["ok"], True)
            self.assertEqual(64, len(envelope["manifest_sha256"]))

    def test_preserves_policy_and_separates_optional_skill_installation(self) -> None:
        text = source()
        self.assertIn("AGENTS.md", text)
        self.assertIn("unrelated instructions", text)
        self.assertIn("exactly one `## Project memory`", text)
        self.assertIn(
            "npx skills add PonchoPig/yams-skills --skill yams-harvest --skill yams-sow --global",
            text,
        )
        self.assertIn(
            "npx skills add PonchoPig/yams-skills --skill yams-cultivate",
            text,
        )
        self.assertIn("does not make memory partial", text)
        self.assertIn("separate authorization", text)
        for operation in ("commit", "branch", "push", "pull request"):
            self.assertRegex(
                text,
                rf"(?i)no [^\n]*{operation}|does not authorize [^\n]*{operation}",
            )
        self.assertNotIn("cp ", text)
        self.assertNotIn("mkdir -p .agents", text)


if __name__ == "__main__":
    unittest.main()
