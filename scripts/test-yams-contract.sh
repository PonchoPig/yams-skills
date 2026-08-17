#!/bin/sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  printf '%s\n' 'usage: test-yams-contract.sh /path/to/yams-wiki [expected-version]' >&2
  exit 2
fi

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)
YAMS_WIKI=$1
EXPECTED_VERSION=${2:-}
PYTHON3=$(command -v python3) || {
  printf '%s\n' 'Yams contract test: python3 is required' >&2
  exit 2
}

if [ ! -x "$YAMS_WIKI" ]; then
  printf '%s\n' "Yams contract test: not executable: $YAMS_WIKI" >&2
  exit 2
fi

CAPABILITIES=$("$YAMS_WIKI" capabilities --json) || {
  status=$?
  printf '%s\n' "Yams contract test: capabilities failed with exit $status" >&2
  exit "$status"
}

"$PYTHON3" -I - "$ROOT/compatibility.json" "$CAPABILITIES" "$EXPECTED_VERSION" <<'PY'
import json
import pathlib
import sys

compatibility_path = pathlib.Path(sys.argv[1])
try:
    compatibility = json.loads(compatibility_path.read_text(encoding="utf-8"))
    capabilities = json.loads(sys.argv[2])
except (OSError, json.JSONDecodeError) as error:
    raise SystemExit(f"Yams contract test: invalid JSON: {error}")

if capabilities.get("ok") is not True:
    raise SystemExit("Yams contract test: capability response is not ok")
expected_version = sys.argv[3]
if expected_version:
    actual_version = capabilities.get("yams_version")
    if actual_version != expected_version:
        raise SystemExit(
            f"Yams contract test: yams_version actual={actual_version!r} "
            f"required={expected_version!r}"
        )
actual_contracts = capabilities.get("contracts")
if not isinstance(actual_contracts, dict):
    raise SystemExit("Yams contract test: contracts object is missing")

for name, required in compatibility["contracts"].items():
    actual = actual_contracts.get(name)
    if isinstance(actual, bool) or not isinstance(actual, int) or actual < required:
        raise SystemExit(
            f"Yams contract test: {name} actual={actual!r} required={required}"
        )
PY

printf '%s\n' 'Yams capability contract passed'
