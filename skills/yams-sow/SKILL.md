---
name: yams-sow
description: Use when the agent has verified a durable, reusable project fact that should be preserved to prevent rediscovery. Never trigger merely because a search ran or .agents/memory is absent.
---

# Sow Yams memory

The agent decides whether a finding is worth keeping. Search, a finished
task, and a missing corpus are not write triggers.

Sow one verified, durable, reusable fact. Never preserve secrets,
transcripts, speculation, or temporary task progress.

This skill does not initialize missing memory. Use `yams-till` for setup.
Use `yams-harvest` for retrieval. Use `yams-cultivate` for audits, refresh,
consolidation, repair, or staleness work.

## Preflight

1. Resolve the Git root. If `.agents/memory/` is absent, stop and point to
   `yams-till`. Do not initialize.
2. Confirm `command -v yams-wiki` succeeds.
3. Run `git status --short .agents/memory/`. Do not stack on another
   writer's uncommitted work.
4. Read `.agents/memory/SCHEMA.md` completely.

## Decide

Write only when all of these hold:

- The fact is verified against current code, tests, documentation, or Git
  history.
- It is durable and reusable, not this-session progress.
- It is likely to prevent rediscovery.
- Prefer updating an existing page over creating a duplicate.

If any check fails, do not write.

## Write

Save a bounded request outside the target and apply it with:

```sh
yams-wiki write .agents/memory < /path/to/write-request.json
```

A create request uses the schema's create shape. An update keeps the stored
owner and status, sets `update: true`, and names the existing `target` slug.
Do not hand-edit pages or the generated index.

`yams-wiki write` regenerates the catalog. After recovery or a direct page
edit, run `yams-wiki catalog .agents/memory`. Then run
`yams-wiki check .agents/memory` as required by the repository policy.

Do not commit or perform remote operations without separate authorization.
