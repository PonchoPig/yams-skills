import errno
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write_executable(path: Path, source: str) -> None:
    path.write_text(source, encoding="utf-8")
    path.chmod(0o755)


class ToolingContractTests(unittest.TestCase):
    def test_shell_helpers_use_portable_cdpath_assignment(self) -> None:
        for path in sorted((ROOT / "scripts").glob("*.sh")):
            source = path.read_text(encoding="utf-8")
            self.assertNotIn("CDPATH= cd", source, path.name)

    def test_installer_smoke_is_hermetic_and_pinned(self) -> None:
        path = ROOT / "scripts/test-skills.sh"
        source = path.read_text(encoding="utf-8")
        self.assertTrue(os.access(path, os.X_OK))
        for value in (
            "mktemp -d",
            "skills@1.5.22",
            'add "$ROOT" --list',
            "--skill yams-harvest",
            "--skill yams-sow",
            "--skill yams-till",
            "--skill yams-cultivate",
            "--agent claude-code",
            "--agent codex",
            "--copy",
            "skills-lock.json",
            ".agents/skills",
            ".claude/skills",
            "cmp -s",
            "hashlib.sha256",
            "expected_digest",
            'set(record) != {"source", "sourceType", "computedHash"}',
            "HOME=",
            "npm_config_cache=",
            "NO_COLOR=1",
        ):
            self.assertIn(value, source)
        self.assertNotIn("npm_config_userconfig=/dev/null", source)
        self.assertNotIn("npm_config_globalconfig=/dev/null", source)
        self.assertIn("resolved_source", source)
        self.assertIn("expected_root", source)
        self.assertNotIn("$HOME/.agents", source)
        self.assertNotIn("$HOME/.claude", source)

    def test_yams_contract_smoke_is_data_driven(self) -> None:
        path = ROOT / "scripts/test-yams-contract.sh"
        source = path.read_text(encoding="utf-8")
        self.assertTrue(os.access(path, os.X_OK))
        self.assertIn("compatibility.json", source)
        self.assertIn('"$YAMS_WIKI" capabilities --json', source)
        self.assertIn('"$PYTHON3" -I', source)
        self.assertIn('for name, required in compatibility["contracts"].items()', source)
        self.assertIn("actual", source)
        self.assertIn("required", source)
        self.assertNotIn('capabilities.get("yams_version") != minimum', source)

    def test_released_lane_requires_version_and_ref_together(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yams-release-pair-test-") as temp:
            compatibility = Path(temp) / "compatibility.json"
            compatibility.write_text(
                json.dumps({"minimum_yams": "1.2.3", "minimum_ref": None}),
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment["YAMS_COMPATIBILITY_JSON"] = str(compatibility)
            result = subprocess.run(
                [str(ROOT / "scripts/test-released-yams.sh")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
        self.assertEqual(2, result.returncode)
        self.assertIn("minimum_yams and minimum_ref must both be null or strings", result.stderr)

    def test_released_lane_rejects_minimum_ref_with_wrong_version(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yams-release-version-test-") as temp:
            fixture = Path(temp)
            compatibility = fixture / "compatibility.json"
            compatibility.write_text(
                json.dumps(
                    {"minimum_yams": "1.2.3", "minimum_ref": "v1.2.3"}
                ),
                encoding="utf-8",
            )
            commands = fixture / "bin"
            commands.mkdir()
            write_executable(
                commands / "curl",
                "#!/bin/sh\nprintf '%s\\n' '{\"tag_name\":\"v1.2.3\"}'\n",
            )
            write_executable(commands / "cargo", "#!/bin/sh\nexit 0\n")
            write_executable(
                commands / "git",
                f"""#!{sys.executable}
import pathlib
import sys

arguments = sys.argv[1:]
if arguments and arguments[0] == "clone":
    destination = pathlib.Path(arguments[-1])
    binary = destination / "target/debug/yams-wiki"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\\nprintf '%s\\\\n' '{{\\\"ok\\\":true,\\\"yams_version\\\":\\\"9.9.9\\\",\\\"contracts\\\":{{\\\"search_results\\\":1,\\\"repository_layout\\\":1,\\\"init_manifest\\\":2,\\\"wiki_maintenance\\\":1}}}}'\\n", encoding="utf-8")
    binary.chmod(0o755)
raise SystemExit(0)
""",
            )
            environment = os.environ.copy()
            environment["PATH"] = f"{commands}:{environment['PATH']}"
            environment["YAMS_COMPATIBILITY_JSON"] = str(compatibility)
            result = subprocess.run(
                [str(ROOT / "scripts/test-released-yams.sh")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=environment,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "Yams contract test: yams_version actual='9.9.9' required='1.2.3'",
            result.stderr,
        )

    def test_brand_audit_is_executable_and_ci_enforced(self) -> None:
        path = ROOT / "scripts/test-yams-brand.sh"
        source = path.read_text(encoding="utf-8")
        self.assertTrue(os.access(path, os.X_OK))
        self.assertIn('bytes.fromhex("6d6f6e657461")', source)
        self.assertIn("git", source)
        self.assertIn("ls-files", source)
        self.assertIn("tracked path violation", source)
        self.assertIn("tracked bytes violation", source)

    @unittest.skipUnless(os.name == "posix", "requires byte-oriented POSIX paths")
    def test_brand_audit_escapes_hostile_filename_bytes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yams-brand-path-test-") as temp:
            repository = Path(temp) / "repository"
            repository.mkdir()
            subprocess.run(
                ["git", "-C", str(repository), "init", "--quiet"], check=True
            )
            forbidden = bytes.fromhex("6d6f6e657461")
            filename = b"prefix\n\x1b\xff-" + forbidden + b".txt"
            path = os.path.join(os.fsencode(repository), filename)
            supports_non_utf8 = True
            try:
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT, 0o600)
            except OSError as error:
                if error.errno != errno.EILSEQ:
                    raise
                supports_non_utf8 = False
                filename = b"prefix\n\x1b-" + forbidden + b".txt"
                path = os.path.join(os.fsencode(repository), filename)
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT, 0o600)
            os.close(descriptor)
            subprocess.run(
                [b"git", b"-C", os.fsencode(repository), b"add", b"--", filename],
                check=True,
            )
            environment = os.environ.copy()
            environment["YAMS_BRAND_ROOT"] = str(repository)
            result = subprocess.run(
                [str(ROOT / "scripts/test-yams-brand.sh")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
            )
        self.assertEqual(1, result.returncode)
        diagnostic = result.stderr.decode("ascii")
        self.assertEqual(2, len(diagnostic.splitlines()), diagnostic)
        self.assertIn(r"\n", diagnostic)
        self.assertIn(r"\x1b", diagnostic)
        if supports_non_utf8:
            self.assertIn(r"\xff", diagnostic)
        self.assertNotIn(b"\x1b", result.stderr)
        if supports_non_utf8:
            self.assertNotIn(b"\xff", result.stderr)

    def test_ci_runs_static_install_and_release_compatibility_lanes(self) -> None:
        workflow = (ROOT / ".github/workflows/verify.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("macos-latest", workflow)
        self.assertIn("22.20.0", workflow)
        self.assertIn("python3 -m unittest discover -v", workflow)
        self.assertIn("./scripts/test-skills.sh", workflow)
        self.assertIn("./scripts/test-yams-brand.sh", workflow)
        self.assertIn("./scripts/test-released-yams.sh", workflow)
        self.assertIn("permissions:\n  contents: read", workflow)


if __name__ == "__main__":
    unittest.main()
