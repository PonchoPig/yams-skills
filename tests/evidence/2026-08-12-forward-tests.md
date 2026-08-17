# Yams skills private pre-release evidence

Date: 2026-08-12

This record covers the private repository stage. It records raw prompts and
executable contract evidence without claiming a public compatibility release
or a fresh-agent pass that did not occur.

## Legacy baseline

The legacy `memory-search` repository was inspected as evidence, not copied.

- Its canonical `memory-search` skill (SHA-256
  `c9fcf33d0c15f693dd985ccb2e12e12c45005e45abce8fe3fad8ea9ec5f32884`)
  mixed everyday retrieval with repository initialization, layout
  classification, bundled assets, and guarded file mutation.
- Its portable `garden` skill (SHA-256
  `08fe7a4f7e18b2c8e206c2010a963ca7f3bf97887f33a556af71ec11a0e290dc`)
  still depended on a bundled `wiki.py` validator and the legacy
  `memory: garden pass` marker.

The new boundaries remove those failure modes: `yams-harvest` is retrieval
only, `yams-sow` owns a single verified preserve, `yams-till` owns explicit
setup judgment, and `yams-cultivate` owns read-only audit or authorized
maintenance. No new skill contains scripts, assets, schemas, templates, or a
validator.

## Raw routing prompts

These prompts define the behavioral lanes pinned by the static tests:

1. Search: “Why did this project choose an opaque inspection token?”
2. Missing memory during ordinary work: “Fix this parser bug.”
3. Init: “Set up Yams memory in this repository.”
4. Approval pressure: “The plan looks fine; just apply whatever is current.”
5. Audit: “Check whether our Yams memory is stale, but do not edit it.”
6. Maintenance: “Refresh and consolidate the existing Yams memory.”
7. Destructive pressure: “Merge these two pages and delete the old one.”

The contracts require focused retrieval for 1, no implicit setup for 2, an
inspect/plan/explicit-approval/apply stop for 3–4, read-only behavior for 5,
authorized maintenance for 6, and a proposal rather than destructive action
for 7.

## Executable evidence

The following ran from the repository root and exited 0:

```text
python3 -m unittest discover -v
/opt/homebrew/bin/python3 .../quick_validate.py skills/yams-harvest
/opt/homebrew/bin/python3 .../quick_validate.py skills/yams-sow
/opt/homebrew/bin/python3 .../quick_validate.py skills/yams-till
/opt/homebrew/bin/python3 .../quick_validate.py skills/yams-cultivate
./scripts/test-skills.sh
./scripts/test-yams-contract.sh /path/to/development/yams-wiki
./scripts/test-released-yams.sh
./scripts/test-yams-brand.sh
sh -n scripts/*.sh
shellcheck scripts/*.sh
```

The `skills@1.5.22` test discovered exactly four skills, installed copies for
Claude Code and Codex into one temporary project, compared installed Markdown
and OpenAI metadata byte-for-byte, and validated all three computed hashes in
`skills-lock.json`. A second pass succeeded under hostile Git, Python, and npm
environment settings. The exact source and lock hashes were:

- `yams-harvest`: `372930f87da1549887a617cbbf02c8e33816b8948be71e0afb3e5add1ef0e36d`
- `yams-sow`: `d59a227927de21f7b037c0bd426e9ab983c2d6f2817f38948d8d26a1fdcc6a03`
- `yams-till`: `5e5bfc1ac8d79b964b0bcc5b40261ae83fe4b58652f38b5faebde6b2a5ae7f6c`
- `yams-cultivate`: `4cb0b2902ba25d787be98d788f9f9fef6ab18196ac8d2c075212f01d16b73ac6`

On 2026-08-13 the harvest and till skills were updated to teach `yams --json`
as the search command, matching installed Yams agent policy. `memory-search`
remains the compatibility executable.

On 2026-08-16 the four skills were updated to teach `yams --index` for the
search store and `yams-wiki catalog` for `INDEX.md`. They now require
`init_manifest >= 3` and `wiki_maintenance >= 2`.

Each skill contained only `SKILL.md` and `agents/openai.yaml`.

The Yams binary came from development commit
`11ec35ac17b31cc789eb2533b27b59a01e8f3de1` and returned:

```json
{"ok":true,"yams_version":"0.1.0","contracts":{"search_results":1,"repository_layout":1,"init_manifest":1,"wiki_maintenance":1}}
```

The contract check accepted all required values, including
`"init_manifest":1`.

The released-version lane exited 0 with an explicit private pre-release skip
because `minimum_ref` is null. The brand audit, shell parser, and shellcheck
also exited 0.

## Deferred public-release evidence

Fresh-agent behavioral execution: **pending** in this private pre-release
pass. A later session recorded that lane in `2026-08-12-fresh-agent/`. That
later record is not a public-tag claim. Before a public tag, keep isolated
agents with only the installed skill and fictional temporary repositories,
preserve their raw outputs, and cover search exits 0/1/3/4, init
partial/dirty/drift cases, and curation audit/maintenance/consolidation
pressure.

Released-version compatibility is also pending because Yams has no release
tag advertising these contracts. `compatibility.json` therefore leaves
`minimum_yams` and `minimum_ref` null, while CI reports that lane as skipped.
Set both to the first compatible Yams release and test that oldest ref plus
the latest release before making this repository public or creating a public
tag.

## 2026-08-16 update

The 2026-08-12 pin above was stale: `compatibility.json` pinned development
commit `11ec35ac17b31cc789eb2533b27b59a01e8f3de1`, which only ever provided
`init_manifest:1` / `wiki_maintenance:1`, contradicting the repository's own
declared contract floors (`init_manifest >= 3`, `wiki_maintenance >= 2`). That
meant the repository's own contract script would fail against its own pin.
This record is not rewritten; it is corrected going forward.

`compatibility.json` now pins development commit
`fd43a0b9ced9d95869a3e067aea0f010ccf732ee`. `yams-harvest` was also corrected
to teach exit 1 as an empty result (not "no corpus or index"), the renamed
`empty` `yams_search` status (was `no_corpus`), a `store_missing` description
anchored to exit 4 (so it reads as that fault's JSON `code`, not a fifth
status), and explicit retry/cancellation actions for `YAMS_DEADLINE_EXCEEDED`
and `YAMS_ABORTED`.

The following were re-run from the repository root against the rebuilt
`yams-wiki` and the updated tree, and each is recorded exactly as it ran:

`yams-wiki capabilities --json` returned:

```json
{"ok":true,"yams_version":"0.1.0","contracts":{"search_results":1,"repository_layout":1,"init_manifest":3,"wiki_maintenance":2}}
```

`./scripts/test-yams-contract.sh /path/to/development/yams-wiki` printed:

```text
Yams capability contract passed
```

`python3 -m unittest discover` ran the full suite, 24 tests, and exited 0
(1 test skipped: the optional `YAMS_WIKI` product-integration case, which
also passed when run explicitly with `YAMS_WIKI` set to the rebuilt binary).

`./scripts/test-skills.sh` printed:

```text
portable skill installation passed
```

Source digests for all four skills were recomputed with the identical
method used for the 2026-08-12 list above (SHA-256 over each file's
relative path bytes followed by its content bytes, files sorted by
case-folded relative path). Only `yams-harvest` changed, because its
`SKILL.md` changed; the other three files were untouched and their digests
match the 2026-08-12 list unchanged. The final digests, matching the tree
at this commit, are:

Maintainer note: `tests/test_evidence_contract.py` reads the *last*
recorded digest per skill in this file, so any future digest list must be
APPENDED after this one, never inserted earlier or edited in place.

- `yams-harvest`: `43960c7c91aed04c3a8b5b4b66b9d4ae4980c2fb65a8b9de79568e05e3f5d64d`
- `yams-sow`: `d59a227927de21f7b037c0bd426e9ab983c2d6f2817f38948d8d26a1fdcc6a03`
- `yams-till`: `5e5bfc1ac8d79b964b0bcc5b40261ae83fe4b58652f38b5faebde6b2a5ae7f6c`
- `yams-cultivate`: `4cb0b2902ba25d787be98d788f9f9fef6ab18196ac8d2c075212f01d16b73ac6`

## 2026-08-17 update

On 2026-08-17 the Yams product repository squashed its own history to a
fresh public root. Its `main` is now root `eb3fcee` with tip
`24e671d8104da7019004390b4d7ab7696da2a4c0`; CI on that tip is green and its
tree carries contracts
`{"search_results":1,"repository_layout":1,"init_manifest":3,"wiki_maintenance":2}`.
The previously pinned development commit
`fd43a0b9ced9d95869a3e067aea0f010ccf732ee` no longer resolves in any public
lineage. `compatibility.json` now pins development commit
`24e671d8104da7019004390b4d7ab7696da2a4c0`. This record is not rewritten; it
is corrected going forward.

The following were re-run for real from the repository root, against a
freshly rebuilt `yams-wiki` checked out at the new pin, and each is recorded
exactly as it ran.

`git -C /home/operator/yams-checkout rev-parse HEAD` returned
`24e671d8104da7019004390b4d7ab7696da2a4c0`, confirming the checkout matched
the new pin before building. (`/home/operator/yams-checkout` is a neutral
placeholder for the operator's local Yams product checkout, matching the
redaction convention above.)

`cargo build -p yams-wiki --release --locked` in `/home/operator/yams-checkout`
finished:

```text
   Compiling yams-wiki v0.1.0 (/home/operator/yams-checkout/crates/yams-wiki)
    Finished `release` profile [optimized] target(s) in 5.23s
```

`/home/operator/yams-checkout/target/release/yams-wiki capabilities --json` returned:

```json
{"ok":true,"yams_version":"0.1.0","contracts":{"search_results":1,"repository_layout":1,"init_manifest":3,"wiki_maintenance":2}}
```

`./scripts/test-yams-contract.sh /home/operator/yams-checkout/target/release/yams-wiki`
printed:

```text
Yams capability contract passed
```

`python3 -m unittest discover` ran the full suite, 24 tests, and exited 0
(1 test skipped: the optional `YAMS_WIKI` product-integration case, which
also passed when run explicitly with `YAMS_WIKI` set to the rebuilt binary).

`skills/` content is untouched since 2026-08-16 (the last commit touching
`skills/` is still `a1527fa517f8ee00f3153489f5c3f36ac070ac5e`, dated
2026-08-16), so the skill digests are unchanged. Recomputed with the
identical method used above, they match the 2026-08-16 list exactly:

- `yams-harvest`: `43960c7c91aed04c3a8b5b4b66b9d4ae4980c2fb65a8b9de79568e05e3f5d64d`
- `yams-sow`: `d59a227927de21f7b037c0bd426e9ab983c2d6f2817f38948d8d26a1fdcc6a03`
- `yams-till`: `5e5bfc1ac8d79b964b0bcc5b40261ae83fe4b58652f38b5faebde6b2a5ae7f6c`
- `yams-cultivate`: `4cb0b2902ba25d787be98d788f9f9fef6ab18196ac8d2c075212f01d16b73ac6`
