---
name: yams-till
description: Use only when the user explicitly asks to initialize, set up, install, migrate, till, or upgrade Yams repository memory. Never trigger merely because .agents/memory is absent.
---

# Till Yams memory

Use Yams's inspect, plan, and apply contract. Supply verified project facts
and user judgment; never reproduce Yams's layout or filesystem logic.

The initial request is not write approval. Approval covers only the exact
displayed manifest. No commit, branch, push, or pull request is authorized;
each requires separate authorization.

## Preflight

1. Resolve the Git root. Refuse a non-Git directory. Read applicable
   `AGENTS.md`, `CLAUDE.md`, and repository instructions before drafting.
2. Confirm `command -v yams-wiki` succeeds. Otherwise stop with direct
   Yams installation guidance.
3. Run `yams-wiki capabilities --json`. Require `repository_layout >= 1`
   and `init_manifest >= 3`; if either is missing, stop with the minimum
   required capability and upgrade guidance.
4. Run:

   ```sh
   yams-wiki init inspect --json <git-root>
   ```

   Report the observed layout, attainable modes, `recommended_mode`,
   owned-path dirt, and every conflict. Do not reinterpret or hide a
   partial, dirty, unsafe, or conflicting result. If the user did not
   choose a mode, use `recommended_mode` and state that choice. If
   `recommended_mode` is null, stop.

## Draft

Inspect primary project sources such as the README, manifests, build files,
tests, and architecture documentation. Draft only verified commands,
architecture, conventions, and durable pitfalls. Do not use placeholders or
speculation.

When `AGENTS.md` must change, prepare the exact desired result. Preserve unrelated instructions
and produce exactly one `## Project memory` section. Let Yams provide the
canonical policy and layout; do not copy files or write the target directly.

Create a private working directory with `mktemp -d`. Save the inspection
JSON and a project-page JSON there. Do not copy `root` or
`inspection_sha256` by hand. The project page states one durable fact:
what it is, why it is true, how to apply it, and what would falsify it.
Do not pack toolchain, binaries, install path, and the local gate into
the same fact.

Omit `--agents-md` when `AGENTS.md` is missing or already contains the
canonical Project memory section. When `AGENTS.md` has other instructions
that must change, pass `--agents-md` with the exact desired file. Populate the required project-page keys with verified facts. Do not substitute conceptual aliases. Keep these temporary files outside the target.

### Complete project-page example

Replace the fictional values only with verified repository facts:

```json
{
  "title": "Project context",
  "page_type": "project-state",
  "fact": "The fictional project uses approved initialization manifests.",
  "why": "Reviewable manifests keep repository mutations explicit.",
  "how_to_apply": "Inspect, plan, obtain approval, and apply the saved manifest.",
  "falsified_by": "A repository mutation succeeds without the approved manifest.",
  "summary": "The fictional project's memory initialization is manifest-driven."
}
```

Save the inspection and project-page JSON in the private working directory
before planning.

## Plan

Run once and preserve stdout byte-for-byte:

```sh
yams-wiki init plan --from-inspect <inspection.json> --project-page <project-page.json> > <manifest.json>
```

Omit `--mode` to use `recommended_mode`. Pass `--mode` only when the user
chose one. `--request` still accepts a complete plan-request JSON if you
already have one.

Present the saved manifest's `manifest_sha256`, destination root, `proposal`,
`operations`, and every destination. Show authored file bodies in full:
`AGENTS.md` when its `post_sha256` is not a bundled asset digest, and the
project-context page always. For file operations whose `post_sha256` equals
a value in `manifest.asset_sha256`, present the path, digest, and
"canonical layout asset" instead of the file body. State the resulting
layout and conflicts. Then stop for explicit approval.

Approval applies only to that saved manifest. After approval, the agent must
not regenerate, edit, normalize, or substitute it. A revised plan requires a
new display and approval.

## Apply

After approval, run only:

```sh
yams-wiki init apply --manifest <manifest.json>
```

If Yams reports drift, do not retry with a regenerated manifest. Inspect
again, plan again, and obtain new approval. Report `created`, `changed`,
`removed`, `restored`, `unresolved`, `final_layout`, `next`, validation
state, and the manifest digest from the apply result. Never claim success when validation is
false or `unresolved` is nonempty.

Do not stage or perform version-control operations as part of initialization.

## Index

These are different commands:

- `yams --index` builds the per-project search store under the Yams cache.
- `yams-wiki catalog .agents/memory` regenerates `INDEX.md`.

Apply writes the Markdown wiki only. Search does not create the search
store. After a valid apply, run from the project:

```sh
yams --index
```

This is not a memory write and does not require `YAMS_ALLOW_NET=1` when the
model cache already exists. Use `YAMS_ALLOW_NET=1` only if that search
index reports that the model cache is empty. Do not fold this into
`init apply`. A failed search index does not authorize additional wiki
writes.

## Verify

After the search index exists, run a focused query the verified
project-context page can answer:

```sh
yams --json -k 5 "<focused project-context question>"
```

Interpret retrieval outcomes through `yams-harvest`. A retrieval miss or
operational failure does not authorize additional writes.

Memory files are uncommitted. Ask whether the user wants a commit. Do not
commit, branch, push, or open a pull request unless they ask.

## Optional skill installation

After valid memory setup, recommend harvest and sow if they are not already
available. Recommend cultivate only when the user wants project-local
maintenance. Do not silently install any of them:

```sh
npx skills add PonchoPig/yams-skills --skill yams-harvest --skill yams-sow --global
npx skills add PonchoPig/yams-skills --skill yams-cultivate
```

A declined or failed skill installation does not make memory partial. Yams
memory layout and harness-specific skill installation are independent.
