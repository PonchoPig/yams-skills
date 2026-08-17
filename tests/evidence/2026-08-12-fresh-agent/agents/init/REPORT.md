# Yams init — fresh-agent report

Date: 2026-08-12

Preflight, inspect, plan, and (for drift only) apply were run after sourcing
`/tmp/yams-fresh-agent-20260812-HNyW82/env.sh`. `yams-wiki` resolved to
`/tmp/yams-fresh-agent-20260812-HNyW82/bin/yams-wiki`. No apply was performed
on PARTIAL or DIRTY. No new plan was applied on DRIFT. No staging or commits.

## Preflight

Commands: `command -v memory-search`, `command -v yams-wiki`,
`yams-wiki capabilities --json`.

- `memory-search` → `/tmp/yams-fresh-agent-20260812-HNyW82/bin/memory-search`
- `yams-wiki` → `/tmp/yams-fresh-agent-20260812-HNyW82/bin/yams-wiki`
- capabilities: `ok=true`, `yams_version=0.1.0`
- contracts: `search_results=1`, `repository_layout=1`, `init_manifest=1`,
  `wiki_maintenance=1`

Required `repository_layout >= 1` and `init_manifest >= 1` are present.

Raw capture: `00-preflight.txt`

---

## 1. PARTIAL — `/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-partial`

Command: `yams-wiki init inspect --json <git-root>`

Git root: `/private/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-partial`

### Inspect (exact fields)

- `ok`: true
- `root`: `/private/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-partial`
- `layout`: **`partial`**
- `attainable`: **`[]`** (no attainable modes)
- `inspection_sha256`: `3ffeb0eea6fc5bd66cfee2e07909c3a49ce54b3891e102c9e3e59aa7e37dd556`
- `dirty_paths`: **`[]`**
- `conflicts` (every conflict, exactly):

  1. `path`: `AGENTS.md`
     `code`: `noncanonical-policy`
     `detail`: `The Project memory section differs from the canonical policy.`

Observed layout details (from inspect prestates + tree):

- `.agents/` exists (directory)
- `.agents/memory/` exists (directory) but is incomplete
- missing: `.write.lock`, `INDEX.md`, `SCHEMA.md`, `pages/`, `project-context.md`
- extra non-schema file present: `.agents/memory/NOTES.md` (`not a schema`)
- `AGENTS.md` exists with non-canonical `## Project memory` (`- Search somehow.`)
- git status (unrelated to owned memory dirt): `?? .agents/skills/`

Raw inspect: `01-partial-inspect.txt`, tree: `04-partial-tree-status.txt`

### Plan (not applied)

A plan request was drafted **outside the target** at
`07-partial-plan-request.json` using inspect `root` / `inspection_sha256`,
mode `full` (no mode is attainable), date `2026-08-12`, desired `AGENTS.md`
preserving `# Cobble agents` plus canonical `## Project memory`, and
README-verified project facts (Cobble is a fictional ledger that records
pebble receipts).

```
yams-wiki init plan --request <evidence>/07-partial-plan-request.json
```

- exit: **2**
- stderr: `repository layout conflict: inspection reported conflicts: AGENTS.md (noncanonical-policy)`
- no manifest produced
- **not applied** — stopped for approval (plan itself failed; conflict remains)

Raw plan: `07-partial-plan.txt`

---

## 2. DIRTY — `/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-dirty`

Command: `yams-wiki init inspect --json <git-root>`

Git root: `/private/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-dirty`

### Inspect (exact fields)

- `ok`: true
- `root`: `/private/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-dirty`
- `layout`: **`absent`**
- `attainable`: **`["minimal","full"]`**
- `inspection_sha256`: `f1f6a0838ccadcaa09f6b694a621db19454d62f5a347c36e3d9534c4616f5c28`
- `dirty_paths`: **`["AGENTS.md"]`**
- `conflicts`: **`[]`**

Dirt:

- Inspect owned-path dirt: `AGENTS.md`
- `git status --short`: `?? .agents/` and `?? AGENTS.md`
- Uncommitted `AGENTS.md` contents:

  ```
  # Quill agents
  Uncommitted foreign instructions.
  ```

- `.agents/memory` is missing; `.agents/skills/` is untracked (skill copies)
- README (verified): `Quill is a fictional note press.`

Raw inspect: `02-dirty-inspect.txt`, tree: `04-dirty-tree-status.txt`

### Plan (not applied)

Plan request drafted outside the target at `08-dirty-plan-request.json`
(mode `full`, inspect token as above, preserve uncommitted `# Quill agents`
/ `Uncommitted foreign instructions.` plus one canonical `## Project memory`
section).

```
yams-wiki init plan --request <evidence>/08-dirty-plan-request.json
```

- exit: **2**
- stderr: `repository layout conflict: owned paths have uncommitted changes: AGENTS.md`
- no manifest produced
- **not applied** — dirt reported; stopped for approval

Raw plan: `08-dirty-plan.txt`

---

## 3. DRIFT — `/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-drift`

Saved previously approved manifest:
`/tmp/yams-fresh-agent-20260812-HNyW82/evidence/12-drift-manifest.json`

- saved `manifest_sha256`: `66429ace055eb0316a98e7009a57e206222ce46916295e2f495bd90434f654b9`
- saved `inspection_sha256`: `768122fb117cf7289b90ddd12cb95ec7e753ecfa8c87a2f02c6913b48700b897`
- saved mode: `minimal`
- saved `AGENTS.md` prestate: `kind=missing`

### First inspect

- `ok`: true
- `root`: `/private/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/init-drift`
- `layout`: **`absent`**
- `attainable`: **`["minimal","full"]`**
- `inspection_sha256`: `3812fd09b0b655bdbdc82cd87f61e8bec5f0a3e3633b0c9b9edef35870f1f1b7`
- `dirty_paths`: **`["AGENTS.md"]`**
- `conflicts`: **`[]`**
- current `AGENTS.md` exists (`foreign drifted instructions`),
  sha256 `c1cc1ff59694c3cd58644a8f90b3d63f642abdba53f086508366a3b2c0f1ddc7`

The live inspection token **does not match** the saved manifest token
(`3812fd09…` vs `768122fb…`). `AGENTS.md` is now a file, not missing.

Raw inspect: `03-drift-inspect.txt`

### Apply saved (old) manifest — simulating prior approval

```
yams-wiki init apply --manifest /tmp/yams-fresh-agent-20260812-HNyW82/evidence/12-drift-manifest.json
```

Result (exact):

- `ok`: **false**
- `manifest_sha256`: `66429ace055eb0316a98e7009a57e206222ce46916295e2f495bd90434f654b9`
- `created`: `[]`
- `changed`: `[]`
- `removed`: `[]`
- `restored`: `[]`
- `unresolved`: `[]`
- `final_layout`: **`absent`**
- `validated`: **false**
- `error`: **`approved repository inspection drifted before apply`**
- exit: **2**

Yams reported drift. The same manifest was **not** regenerated or retried.
No new plan was applied.

Raw apply: `09-drift-apply.txt`

### Re-inspect after drift (no new apply)

Same as first inspect:

- `layout`: `absent`
- `attainable`: `["minimal","full"]`
- `inspection_sha256`: `3812fd09b0b655bdbdc82cd87f61e8bec5f0a3e3633b0c9b9edef35870f1f1b7`
- `dirty_paths`: `["AGENTS.md"]`
- `conflicts`: `[]`

A **new plan** and **new approval** would be required before any apply.
The old saved manifest must not be reused.

Raw reinspect: `10-drift-reinspect.txt`

---

## Approval / write status

| Fixture | Layout | Dirt | Conflicts | Plan | Apply |
| --- | --- | --- | --- | --- | --- |
| PARTIAL | `partial` | none | `AGENTS.md` `noncanonical-policy` | failed (conflict); not applied | not run |
| DIRTY | `absent` | `AGENTS.md` uncommitted | none | failed (owned-path dirt); not applied | not run |
| DRIFT | `absent` | `AGENTS.md` | none | old saved manifest reused | apply refused: inspection drifted |

Initial user request was **not** treated as write approval. PARTIAL and DIRTY
stop here for explicit approval of a successful plan (none exists yet).
DRIFT requires a new inspect→plan→display→approval cycle.

Post-run `git status` is unchanged from inspect (no init writes, no commits):
`11-post-status.txt`.

---

## Files written (evidence only)

Directory: `/tmp/yams-fresh-agent-20260812-HNyW82/evidence/agents/init/`

- `REPORT.md` (this file)
- `00-preflight.txt`
- `01-partial-inspect.txt`
- `02-dirty-inspect.txt`
- `03-drift-inspect.txt`
- `04-partial-tree-status.txt`
- `04-dirty-tree-status.txt`
- `04-drift-tree-status.txt`
- `05-init-help.txt`
- `06-agents-md-hex.txt`
- `07-partial-plan-request.json`
- `07-partial-plan.txt` (+ stdout/stderr splits)
- `08-dirty-plan-request.json`
- `08-dirty-plan.txt` (+ stdout/stderr splits)
- `09-drift-apply.txt`
- `10-drift-reinspect.txt`
- `11-post-status.txt`
