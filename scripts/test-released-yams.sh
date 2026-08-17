#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)
COMPATIBILITY=${YAMS_COMPATIBILITY_JSON:-"$ROOT/compatibility.json"}
PYTHON3=$(command -v python3) || {
  printf '%s\n' 'released Yams test: python3 is required' >&2
  exit 2
}

MINIMUM_VALUES=$(
  "$PYTHON3" -I - "$COMPATIBILITY" <<'PY'
import json
import pathlib
import sys

values = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
minimum_yams = values.get("minimum_yams")
minimum_ref = values.get("minimum_ref")
if minimum_yams is None and minimum_ref is None:
    print()
    print()
elif (
    not isinstance(minimum_yams, str)
    or not minimum_yams
    or not isinstance(minimum_ref, str)
    or not minimum_ref
):
    print(
        "released Yams test: minimum_yams and minimum_ref must both be null or strings",
        file=sys.stderr,
    )
    raise SystemExit(2)
else:
    print(minimum_yams)
    print(minimum_ref)
PY
)
MINIMUM_YAMS=$(printf '%s\n' "$MINIMUM_VALUES" | sed -n '1p')
MINIMUM_REF=$(printf '%s\n' "$MINIMUM_VALUES" | sed -n '2p')

if [ -z "$MINIMUM_REF" ]; then
  printf '%s\n' 'released Yams compatibility skipped: private pre-release has no minimum_ref'
  exit 0
fi

for command in curl git cargo; do
  command -v "$command" >/dev/null 2>&1 || {
    printf '%s\n' "released Yams test: $command is required" >&2
    exit 2
  }
done

LATEST_JSON=$(curl --fail --silent --show-error \
  https://api.github.com/repos/PonchoPig/yams/releases/latest)
LATEST_REF=$(
  "$PYTHON3" -I - "$LATEST_JSON" <<'PY'
import json
import sys

try:
    value = json.loads(sys.argv[1])["tag_name"]
except (json.JSONDecodeError, KeyError) as error:
    raise SystemExit(f"released Yams test: latest release has no tag_name: {error}")
if not isinstance(value, str) or not value:
    raise SystemExit("released Yams test: latest release tag is empty")
print(value)
PY
)

TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/yams-releases-test.XXXXXX")
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

printf '%s\n%s\n' "$MINIMUM_REF" "$LATEST_REF" | awk '!seen[$0]++' | while IFS= read -r ref; do
  destination="$TEST_ROOT/$ref"
  git clone --quiet --filter=blob:none https://github.com/PonchoPig/yams.git "$destination"
  git -C "$destination" checkout --quiet --detach "$ref"
  cargo build \
    --manifest-path "$destination/Cargo.toml" \
    -p yams-wiki \
    --bin yams-wiki \
    --locked
  if [ "$ref" = "$MINIMUM_REF" ]; then
    "$ROOT/scripts/test-yams-contract.sh" \
      "$destination/target/debug/yams-wiki" "$MINIMUM_YAMS"
  else
    "$ROOT/scripts/test-yams-contract.sh" \
      "$destination/target/debug/yams-wiki"
  fi
done

printf '%s\n' 'released Yams compatibility passed'
