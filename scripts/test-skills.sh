#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)
NPX=$(command -v npx) || {
  printf '%s\n' 'skill install test: npx is required' >&2
  exit 2
}
GIT=$(command -v git) || {
  printf '%s\n' 'skill install test: git is required' >&2
  exit 2
}
PYTHON3=$(command -v python3) || {
  printf '%s\n' 'skill install test: python3 is required' >&2
  exit 2
}
NPX_DIR=$(CDPATH='' cd -- "$(dirname -- "$NPX")" && pwd -P)
TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/yams-skills-test.XXXXXX")

cleanup() {
  status=$?
  trap - EXIT HUP INT TERM
  if [ -n "${TEST_ROOT:-}" ] && [ -d "$TEST_ROOT" ]; then
    chmod -R u+rwX "$TEST_ROOT" 2>/dev/null || true
    rm -rf -- "$TEST_ROOT"
  fi
  exit "$status"
}
trap cleanup EXIT HUP INT TERM

HOME_DIR="$TEST_ROOT/home"
PROJECT="$TEST_ROOT/project"
NPM_CACHE="$TEST_ROOT/npm-cache"
NPM_USER_CONFIG="$TEST_ROOT/npmrc-user"
NPM_GLOBAL_CONFIG="$TEST_ROOT/npmrc-global"
LIST_OUTPUT="$TEST_ROOT/list.out"
mkdir -p "$HOME_DIR" "$PROJECT" "$NPM_CACHE"
touch "$NPM_USER_CONFIG" "$NPM_GLOBAL_CONFIG"

clean_env() {
  /usr/bin/env -i \
    PATH="$NPX_DIR:/usr/local/bin:/usr/bin:/bin" \
    HOME="$HOME_DIR" \
    XDG_CONFIG_HOME="$HOME_DIR/.config" \
    LC_ALL=C \
    CI=1 \
    NO_COLOR=1 \
    GIT_CONFIG_NOSYSTEM=1 \
    GIT_CONFIG_GLOBAL=/dev/null \
    GIT_TERMINAL_PROMPT=0 \
    npm_config_cache="$NPM_CACHE" \
    npm_config_userconfig="$NPM_USER_CONFIG" \
    npm_config_globalconfig="$NPM_GLOBAL_CONFIG" \
    npm_config_update_notifier=false \
    npm_config_fund=false \
    npm_config_audit=false \
    "$@"
}

clean_env "$GIT" -C "$PROJECT" init --quiet

(
  cd "$PROJECT"
  clean_env "$NPX" --yes skills@1.5.22 add "$ROOT" --list >"$LIST_OUTPUT"
  clean_env "$NPX" --yes skills@1.5.22 add "$ROOT" \
    --skill yams-harvest \
    --skill yams-sow \
    --skill yams-till \
    --skill yams-cultivate \
    --copy \
    --agent claude-code \
    --agent codex \
    --yes >/dev/null
)

grep -F 'Found 4 skills' "$LIST_OUTPUT" >/dev/null
for skill in yams-harvest yams-sow yams-till yams-cultivate; do
  grep -F "$skill" "$LIST_OUTPUT" >/dev/null
  for agent_dir in .agents/skills .claude/skills; do
    cmp -s \
      "$ROOT/skills/$skill/SKILL.md" \
      "$PROJECT/$agent_dir/$skill/SKILL.md"
    cmp -s \
      "$ROOT/skills/$skill/agents/openai.yaml" \
      "$PROJECT/$agent_dir/$skill/agents/openai.yaml"
  done
done

"$PYTHON3" -I - "$PROJECT/skills-lock.json" "$ROOT" <<'PY'
import hashlib
import json
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
expected_root = pathlib.Path(sys.argv[2]).resolve()
try:
    lock = json.loads(path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as error:
    raise SystemExit(f"skill install test: invalid skills-lock.json: {error}")

expected = {"yams-harvest", "yams-sow", "yams-till", "yams-cultivate"}
if lock.get("version") != 1:
    raise SystemExit(f"skill install test: unexpected lock version: {lock.get('version')!r}")
skills = lock.get("skills")
if not isinstance(skills, dict) or set(skills) != expected:
    raise SystemExit(f"skill install test: unexpected locked skills: {skills!r}")
for name, record in skills.items():
    if set(record) != {"source", "sourceType", "computedHash"}:
        raise SystemExit(f"skill install test: {name} lock entry is not exact")
    if record.get("sourceType") != "local":
        raise SystemExit(f"skill install test: {name} sourceType is not local")
    if not isinstance(record.get("source"), str) or not record["source"]:
        raise SystemExit(f"skill install test: {name} source is missing")
    resolved_source = (path.parent / record["source"]).resolve()
    if resolved_source != expected_root:
        raise SystemExit(
            f"skill install test: {name} source={resolved_source} "
            f"expected={expected_root}"
        )
    digest = record.get("computedHash")
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise SystemExit(f"skill install test: {name} computedHash is invalid")
    skill_root = expected_root / "skills" / name
    hasher = hashlib.sha256()
    files = sorted(
        (path for path in skill_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(skill_root).as_posix().casefold(),
    )
    for file_path in files:
        relative = file_path.relative_to(skill_root).as_posix()
        hasher.update(relative.encode("utf-8"))
        hasher.update(file_path.read_bytes())
    expected_digest = hasher.hexdigest()
    if digest != expected_digest:
        raise SystemExit(
            f"skill install test: {name} computedHash={digest} "
            f"expected={expected_digest}"
        )
PY

printf '%s\n' 'portable skill installation passed'
