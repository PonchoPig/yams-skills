import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_repository_exposes_exact_yams_skill_set(self) -> None:
        skills = {
            path.name for path in (ROOT / "skills").iterdir() if path.is_dir()
        }
        self.assertEqual(
            {"yams-harvest", "yams-sow", "yams-till", "yams-cultivate"}, skills
        )

    def test_private_prerelease_compatibility_is_explicit(self) -> None:
        compatibility = json.loads(
            (ROOT / "compatibility.json").read_text(encoding="utf-8")
        )
        self.assertEqual(1, compatibility["schema"])
        self.assertEqual(
            {
                "schema",
                "minimum_yams",
                "minimum_ref",
                "development_commit",
                "contracts",
            },
            set(compatibility),
        )
        self.assertIsNone(compatibility["minimum_yams"])
        self.assertIsNone(compatibility["minimum_ref"])
        self.assertEqual(
            "24e671d8104da7019004390b4d7ab7696da2a4c0",
            compatibility["development_commit"],
        )
        self.assertEqual(
            {
                "search_results": 1,
                "repository_layout": 1,
                "init_manifest": 3,
                "wiki_maintenance": 2,
            },
            compatibility["contracts"],
        )

    def test_readme_pins_installation_and_repository_boundaries(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "npx skills add PonchoPig/yams-skills --skill yams-harvest "
            "--skill yams-sow --skill yams-till --global",
            readme,
        )
        self.assertIn(
            "npx skills add PonchoPig/yams-skills --skill yams-cultivate",
            readme,
        )
        self.assertIn("Node.js 22.20 or newer", readme)
        self.assertIn("installer only", readme)
        self.assertIn("private pre-release", readme)
        self.assertIn("npx skills", readme)
        self.assertIn("skills-lock.json", readme)
        self.assertIn("does not install Yams", readme)
        self.assertIn("https://github.com/PonchoPig/yams", readme)
        self.assertIn("yams-wiki capabilities --json", readme)
        self.assertIn("minimum_yams", readme)

    def test_licenses_match_yams(self) -> None:
        expected = {
            "LICENSE-MIT": "8965302a147eddc4b1fc4f6967d76d9e7826c71a58cbe6685131ed9349ec8117",
            "LICENSE-APACHE": "074e6e32c86a4c0ef8b3ed25b721ca23aca83df277cd88106ef7177c354615ff",
        }
        for name, digest in expected.items():
            self.assertEqual(
                digest,
                hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
