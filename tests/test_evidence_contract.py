import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvidenceContractTests(unittest.TestCase):
    def test_private_prerelease_evidence_is_honest_and_actionable(self) -> None:
        evidence = (
            ROOT / "tests/evidence/2026-08-12-forward-tests.md"
        ).read_text(encoding="utf-8")
        for value in (
            "Legacy baseline",
            "memory-search",
            "garden",
            "yams-harvest",
            "yams-sow",
            "yams-till",
            "yams-cultivate",
            "skills@1.5.22",
            "test-yams-brand.sh",
            "test-released-yams.sh",
            "hostile Git, Python, and npm",
            "11ec35ac17b31cc789eb2533b27b59a01e8f3de1",
            '"init_manifest":1',
            "Fresh-agent behavioral execution",
            "pending",
            "public tag",
            "2026-08-16 update",
            "fd43a0b9ced9d95869a3e067aea0f010ccf732ee",
            "2026-08-17 update",
            "24e671d8104da7019004390b4d7ab7696da2a4c0",
            '"init_manifest":3',
            '"wiki_maintenance":2',
            "Yams capability contract passed",
            "24 tests",
            "portable skill installation passed",
        ):
            self.assertIn(value, evidence)
        self.assertNotIn("Fresh-agent behavioral execution: passed", evidence)

        # The digest for each skill must match the *latest* recorded value,
        # not merely appear somewhere in the document. A plain assertIn would
        # still pass after reverting a skill's content, because the
        # superseded digest from an earlier dated section remains in the
        # file. Extracting the last occurrence per skill and requiring
        # equality closes that hole: a revert changes the freshly computed
        # digest but not the recorded one, so the two diverge and the test
        # fails.
        for skill in ("yams-harvest", "yams-sow", "yams-till", "yams-cultivate"):
            root = ROOT / "skills" / skill
            files = sorted(
                (path for path in root.rglob("*") if path.is_file()),
                key=lambda path: path.relative_to(root).as_posix().casefold(),
            )
            digest = hashlib.sha256()
            for path in files:
                digest.update(path.relative_to(root).as_posix().encode("utf-8"))
                digest.update(path.read_bytes())

            recorded = re.findall(
                rf"`{re.escape(skill)}`: `([0-9a-f]{{64}})`", evidence
            )
            self.assertTrue(recorded, f"no recorded digest found for {skill}")
            self.assertEqual(
                digest.hexdigest(),
                recorded[-1],
                f"latest recorded digest for {skill} does not match "
                "skills/ on disk",
            )


if __name__ == "__main__":
    unittest.main()
