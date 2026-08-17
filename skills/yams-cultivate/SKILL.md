---
name: yams-cultivate
description: Use when a user explicitly asks to validate, audit, check, refresh, consolidate, repair, curate, cultivate, or maintain a repository's existing Yams memory under .agents/memory. Does not initialize missing memory.
---

# Cultivate Yams memory

Maintain shared memory as verified durable knowledge. Structural success is
only the floor; current truth is the goal.

Choose the mode from the request:

- A validate, audit, or check request is read-only. Report uncommitted memory
  dirt and continue without writes. Run structural checks, investigate the
  requested truth, and propose repairs. Do not edit, do not run `catalog`, and
  do not restore files.
- A refresh, consolidate, repair, curate, or maintain request authorizes the
  maintenance workflow within the requested scope. Stop on another writer's
  uncommitted changes or unclear ownership.

This skill does not initialize missing memory. Use `yams-till` for setup or
upgrades.

## Preflight and scope

1. Resolve the Git root and run `git status --short .agents/memory/`.
2. Require an existing `.agents/memory/` and read
   `.agents/memory/SCHEMA.md` completely.
3. Run `yams-wiki capabilities --json` and require
   `wiki_maintenance >= 2`. Stop with upgrade guidance if unsupported.
4. Honor a narrower user scope. Otherwise inspect the ten oldest `current`
   and `in-progress` pages plus pages covering repository changes since the
   last cultivation pass. Name everything skipped by the cap.

Find the change window from the last commit whose subject begins
`memory: cultivate pass`. During migration, fall back to the last
`memory: curate pass`, then `memory: garden pass`, then to the first
commit touching `.agents/memory`.
If no valid boundary exists, inspect the available history without creating an
invalid revision range.

## Structural pass

Run this in both modes:

```sh
yams-wiki check .agents/memory
```

In read-only mode, report failures and proposed repairs. In maintenance mode,
repair structural failures through supported Yams commands before making
truth judgments. Treat notes as leads, not automatic defects.

## Truth and lifecycle pass

Read the scoped pages against current primary sources: code, tests,
documentation, and Git history.

- Correct false claims in maintenance mode; propose corrections in read-only
  mode. Preserve material that is old but still true.
- Change `updated:` only when content changes. Change `verified:` whenever the
  page's claims were actually checked.
- Skip `historical` pages from current-truth correction by default. When a
  page is superseded, preserve it as historical and add a forward link.
- Propose, rather than apply, destructive merges, deletions, or rewrites that
  drop durable content.
- Look for durable traps or workflow changes since the change boundary that
  no page records; do not turn ordinary task history into memory.

Apply each focused create or update through a bounded request:

```sh
yams-wiki write .agents/memory < /path/to/write-request.json
```

Never hand-edit generated index content and never carry a second validator.

## Finish maintenance

Maintenance mode only:

```sh
yams-wiki catalog .agents/memory
yams-wiki check .agents/memory
git diff -- .agents/memory
```

Summarize scoped, skipped, verified, corrected, historical, and proposed work.
Report the oldest remaining verification date. Do not commit without separate
authorization. If authorized, use the subject
`memory: cultivate pass YYYY-MM-DD`.
