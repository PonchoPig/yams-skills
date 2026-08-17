---
name: yams-harvest
description: Use when project history, conventions, architectural decisions, prior failures, or durable shared knowledge may affect ordinary repository work, or when .agents/memory exists. Does not preserve findings.
---

# Harvest Yams memory

Harvest shared project memory early, then verify consequential claims against
primary sources. Memory supplies leads, never authority.

## Retrieve

1. Resolve the Git root and check `<root>/.agents/memory/`. If it is absent,
   continue normally. Never initialize memory without an explicit request.
2. Ask one focused question. Prefer the native typed `yams_search` tool when
   it is available:

   ```json
   {"query":"<focused question>","resultCount":5}
   ```

   Otherwise, fall back to the portable CLI contract:

   ```sh
   yams --json -k 5 "<focused question>"
   ```

   Use one transport, not both. Tool unavailability triggers the CLI fallback;
   an empty, below-confidence, invalid-invocation, or operational outcome
   does not.
3. Treat hits as leads. Verify them against current code, tests,
   documentation, or Git history. Prefer `snippet` when context is tight; use
   `text` or open the page when the full chunk matters.

Use the supported tool or command. Never open Yams databases, import its
implementation, or recreate its ranking logic.

## Outcomes

| Exit | Meaning | Action |
| --- | --- | --- |
| 0 | Results | Inspect and verify. |
| 1 | Empty result | Continue; do not initialize. |
| 2 | Invalid invocation | Correct the command. |
| 3 | No confident match | Retry once with `--no-gate` only for leads. |
| 4 | Operational failure | Read the JSON `code`; report it when relevant; use primary sources if safe. |

For `yams_search`, `results`, `empty`, and `below_confidence` correspond to
CLI exits `0`, `1`, and `3`. On `below_confidence`, retry once with
`{"query":"<focused question>","resultCount":5,"noGate":true}`. Treat
`YAMS_INVALID_INVOCATION` like exit `2` and `YAMS_OPERATIONAL_FAILURE` like
exit `4`. Treat `YAMS_DEADLINE_EXCEEDED` as a deadline expiry: retry once,
then treat it like exit `4` if it recurs. Treat `YAMS_ABORTED` as a
cancellation; do not retry silently. These outcomes never justify silently
rerunning through the CLI.

An exit-4 fault whose JSON `code` is `store_missing` means this project's
search store is absent, not that the wiki is missing. Run `yams --index`
from the project. That is not `yams-wiki catalog`, which regenerates
`INDEX.md`. Add `YAMS_ALLOW_NET=1` only if the model cache is empty. Do not
initialize memory.

Treat `private` pages as unreviewed and machine-local, `historical` pages as
superseded, and `in-progress` pages as unsettled. A `current` shared page still
requires verification.

Use `yams-sow` to preserve a verified finding. Use `yams-till` for setup or
upgrades. Use `yams-cultivate` for audits, refresh, consolidation, repair, or
staleness work.
