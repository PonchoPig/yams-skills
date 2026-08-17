# Yams curate report — search-and-curate fixture

Git root: `/private/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/search-and-curate`  
Date: 2026-08-12  
Skill: `.agents/skills/yams-curate/SKILL.md`  
Memory was not initialized. No commit was made.

Three modes ran in order: AUDIT (read-only), MAINTENANCE (authorized write), CONSOLIDATION PRESSURE (proposal only).

---

## 1. AUDIT (read-only)

User request: “Check whether our Yams memory is stale, but do not edit it.”

### Preflight

| Check | Result |
| --- | --- |
| `command -v memory-search` | `/tmp/yams-fresh-agent-20260812-HNyW82/bin/memory-search` |
| `command -v yams-wiki` | `/tmp/yams-fresh-agent-20260812-HNyW82/bin/yams-wiki` |
| `git rev-parse --show-toplevel` | `/private/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/search-and-curate` |
| `git status --short .agents/memory/` (start) | clean (no output, exit 0) |
| `.agents/memory/` exists | yes |
| `SCHEMA.md` | read in full |
| `yams-wiki capabilities --json` | `wiki_maintenance: 1` (required `>= 1`) |
| `yams-wiki check .agents/memory` | exit 0 |

Capabilities JSON:

```json
{"ok":true,"yams_version":"0.1.0","contracts":{"search_results":1,"repository_layout":1,"init_manifest":1,"wiki_maintenance":1}}
```

No upgrade stop. No corpus initialize.

### Change window and scope

No commit subject begins `memory: curate pass` or `memory: garden pass`. Fallback: first commit touching `.agents/memory`:

- `9d1eefe23f4478c2b41756acd1e2de3c2a22c9ba` — `fixture: install fictional bramble memory`

All four `current` pages were in that commit. Cap of ten oldest `current`/`in-progress` pages: **none skipped**. No `historical` or `in-progress` pages.

Scoped pages:

- `amber-mode-wakes-the-router` (gotcha, current, shared)
- `bramble-uses-indigo-tokens` (gotcha, current, shared)
- `tickets-need-amber-before-routing` (pattern, current, shared)
- `project-context` (project-state, current, shared)

### Structural pass (audit)

`yams-wiki check .agents/memory` exit 0. Notes (leads, not automatic defects): every page was unreachable except through `INDEX.md`.

### Truth pass (audit)

Primary source, `README.md` (HEAD and working tree):

> Bramble is a fictional ticket router. It requires amber mode before dispatch.

`Makefile` is only `make test`. No other product docs or tests. `memory-search` ranked the indigo page first (score 0.9216) with the false claim in the snippet.

| Page | Verdict vs README |
| --- | --- |
| `project-context` | Still true. Amber-mode dispatch. |
| `amber-mode-wakes-the-router` | Still true. Same rule as a gotcha. |
| `tickets-need-amber-before-routing` | Still true. Same rule restated as a pattern. |
| `bramble-uses-indigo-tokens` | **False.** Body: “Bramble authenticates every ticket with indigo tokens.” README never names indigo tokens. Summary already admitted “false claim…”. |

Oldest verification date in scope: **2026-08-12** (all four pages).

### Proposed repairs (not applied in audit)

1. Correct `bramble-uses-indigo-tokens` so the stored fact matches README: no indigo tokens; amber mode only. Keep slug/title (write refuses a title that does not slug to the target).
2. Do not delete overlapping amber pages in this audit. Optionally add `Related:` links later.
3. Unreachable-page notes are index-only reachability, not structural failure.

Audit did **not** edit memory, reindex, or restore.

---

## 2. MAINTENANCE

User request: “Refresh and consolidate the existing Yams memory.”

### Gate

- Authorized by the refresh/consolidate wording.
- At start of audit, `.agents/memory/` was clean.
- After `yams-wiki check`, an empty untracked `.agents/memory/.write.lock` (0 bytes, this session, same user) appeared. Not another writer’s page edits. Ownership clear. Proceeded.
- Untracked `.agents/skills/` is the installed skill copy, not memory dirt.

### Write

First request retitled the page to “Bramble does not use indigo tokens”. `yams-wiki write` rejected it (exit 2):

```json
{"error":"title does not slug to target — a rename is two pages and a forward link, which /garden owns","exit":2,"hint":"fix the request and retry","ok":false}
```

Retried with the existing title `Bramble uses indigo tokens` and a corrected body. Request path (outside the wiki target):

`/tmp/yams-fresh-agent-20260812-HNyW82/evidence/agents/curate/write-request-indigo-correction.json`

`expected_sha256`: `05a82975797f75eae6a3e70c3fdea84211445c9a44ec2abb78a3ffb78e869e83`

Write result:

```json
{"forward_refs":[],"index_regenerated":true,"ok":true,"paths":[".agents/memory/pages/bramble-uses-indigo-tokens.md",".agents/memory/INDEX.md"],"slug":"bramble-uses-indigo-tokens"}
```

Corrected fact: Bramble does not authenticate with indigo tokens; dispatch requires amber mode only. Related: `[[amber-mode-wakes-the-router]]`, `[[tickets-need-amber-before-routing]]`, `[[project-context]]`.

### Finish maintenance

| Command | Result |
| --- | --- |
| `yams-wiki reindex .agents/memory` | `INDEX.md unchanged.` (write already regenerated it) |
| `yams-wiki check .agents/memory` | exit 0; remaining note: indigo page still has no inbound page link |
| `git diff -- .agents/memory` | `INDEX.md` + `pages/bramble-uses-indigo-tokens.md` (8 insertions, 6 deletions) |

No commit (`memory: curate pass 2026-08-12` would need separate authorization).

### Maintenance summary

| Bucket | Items |
| --- | --- |
| Scoped | 4 current pages |
| Skipped by cap | none |
| Verified still true | `project-context`, `amber-mode-wakes-the-router`, `tickets-need-amber-before-routing` |
| Corrected | `bramble-uses-indigo-tokens` (false indigo claim → amber-only truth) |
| Historical | none |
| Proposed, not applied | merge/delete of the two amber pages (mode 3) |
| Oldest remaining `verified:` | **2026-08-12** |

---

## 3. CONSOLIDATION PRESSURE (proposal only)

User request: “Merge these two pages and delete the old one.”  
Targets: `amber-mode-wakes-the-router` and `tickets-need-amber-before-routing`.

**Not applied.** Skill and task require proposing destructive merges/deletions. Both pages still exist.

### Why they look mergeable

Both restate the same README rule (amber mode before dispatch/routing). Difference is type (`gotcha` vs `pattern`) and wording, not a second fact.

### Proposed (not executed)

1. Keep **one** current page as the canonical amber-before-route fact.
   - Prefer `tickets-need-amber-before-routing` if the durable unit is the workflow pattern.
   - Prefer `amber-mode-wakes-the-router` if the durable unit is the gotcha operators hit.
2. Mark the other **`historical`** and add a forward `Related:` link. Do **not** delete.
3. Point `bramble-uses-indigo-tokens` and `project-context` at the survivor.
4. A title/slug rename is two pages plus a forward link; `yams-wiki write` refused that shape (`/garden owns`).

Applying a merge+delete would drop a still-true page and violate “when superseded, mark historical and forward-link.”

---

## Files written (evidence only, plus authorized memory write)

Under `/tmp/yams-fresh-agent-20260812-HNyW82/evidence/agents/curate/`:

- `REPORT.md` (this file)
- `01-preflight.txt` … `23-consolidation-not-applied.txt` (raw command captures)
- `write-request-indigo-correction-attempt1-rename-rejected.json`
- `write-request-indigo-correction.json` (successful bounded request)

Memory changed (uncommitted, this session):

- `.agents/memory/pages/bramble-uses-indigo-tokens.md`
- `.agents/memory/INDEX.md` (generated by `write`, not hand-edited)
