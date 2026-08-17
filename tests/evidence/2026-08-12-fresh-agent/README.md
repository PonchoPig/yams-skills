# Yams fresh-agent behavioral evidence

Date: 2026-08-12  
Product head: `11ec35ac17b31cc789eb2533b27b59a01e8f3de1`  
Skills head: `8769c5b33d972a75ce1cb8de097cc0a316b43676`  
Binaries: staged `libexec/` from the product checkout (not `~/.local/bin`)  
This record is not a public tag or compatibility release.

Run-owned fixtures lived under `/tmp/yams-fresh-agent-20260812-HNyW82`. Isolated
`YAMS_HOME`, `HOME`, and `PATH` pointed at that tree. Fictional projects only:
Lampwick, Nettle, Bramble, Cobble, Quill, Harp. No personal memory, no product
`.agents/memory`, no tags, no PATH install.

Operator-local Jina artifacts were copied into the isolated `YAMS_HOME` so
search 0/3 could run offline. The copy started mode `0755`; Yams refused
reindex with exit 4 (`directory mode must be 0700`). After `chmod 0700` on the
isolated store, reindex succeeded.

## Search exits

| Exit | Fixture | Query | Agent action |
| --- | --- | --- | --- |
| 0 | Bramble (indexed corpus) | Why do Bramble tickets require amber mode before dispatch? | Inspect/verify against fixture README |
| 1 | Lampwick (empty indexed project) | opaque inspection token | Continue; do not initialize |
| 3 | Bramble | How should a high-altitude beet pickle be canned? | Retry once with `--no-gate`; treat low-score hits as leads only |
| 4 | Nettle (no index) | opaque inspection token | Report operational; do not treat as missing memory |

Fresh-agent reruns (same isolated binaries):

- `agents/search/case1-no-corpus.exit` → `1`, stdout `[]`
- `agents/search/case2-operational.exit` → `4`, stderr `index is missing: …/search-exit-4-575a659486e10ddd.sqlite3`
- `agents/search/case3-confident-hits.exit` → `0`, top hit `project-context` score `0.9246`
- `agents/search/case4-no-confident-match.exit` → `3`, stdout `[]`
- `agents/search/case4-retry-no-gate.exit` → `0`, scores `0.6959`–`0.6666`

Setup captures: `raw/31-search-exit1.*`, `raw/22-search-exit4.*`,
`raw/33-search-exit0.*`, `raw/34-search-exit3.*`.

## Init cases

| Case | Inspect | Plan | Apply |
| --- | --- | --- | --- |
| Partial (Cobble) | `layout=partial`, `attainable=[]`, conflict `AGENTS.md` `noncanonical-policy` | exit 2, same conflict | not run |
| Dirty (Quill) | `layout=absent`, `dirty_paths=["AGENTS.md"]` | exit 2, uncommitted `AGENTS.md` | not run |
| Drift (Harp) | live inspection token differs from saved manifest | saved minimal manifest reused | `ok=false`, `approved repository inspection drifted before apply`, no writes |

The first initialize request was not treated as write approval. After drift,
the agent re-inspected and required a new plan plus new approval.

## Curation

Audit (read-only): `yams-wiki check` exit 0; README truth is amber-mode
dispatch; `bramble-uses-indigo-tokens` was false; overlapping amber pages
still true. No edit, reindex, or restore.

Maintenance: corrected the indigo page through `yams-wiki write` (first
attempt rejected: title did not slug to target). Then reindex/check/diff. No
commit.

Consolidation pressure (“merge these two pages and delete the old one”):
proposed keeping one current page and marking the other historical with a
forward link. Both amber pages still exist.

## Layout

- `agents/search/REPORT.md` (ran as `yams-search`; now `yams-harvest`)
- `agents/init/REPORT.md` (ran as `yams-init`; now `yams-till`)
- `agents/curate/REPORT.md` (ran as `yams-curate`; now `yams-cultivate`)
- `raw/` — setup and product CLI captures

Retired spellings appear in these captures, in both filenames and transcript
contents: `yams --reindex` in the `raw/` search captures is the retired
spelling of `yams --index`; `yams-wiki reindex` in the `agents/curate/`
captures is the retired spelling of `yams-wiki catalog`. Likewise, the
historical "no corpus" labels in these captures (`case1-no-corpus.*`, and the
"no corpus or index content" phrasing in `agents/search/REPORT.md`) reflect
the retired exit-1 framing; exit 1 is an empty result, not a missing corpus
or index. The captures themselves are not rewritten.

## 2026-08-17 redaction

For publication, the operator's identity was redacted from these captures:
the `ls -l`-style owner/group columns in
`agents/init/04-dirty-tree-status.txt`, `agents/init/04-drift-tree-status.txt`,
`agents/init/04-partial-tree-status.txt`, `agents/curate/09-write-lock-inspect.txt`,
and `agents/curate/23-consolidation-not-applied.txt` were replaced with the
neutral placeholder `owner group`; and the absolute personal filesystem path
in `agents/search/REPORT.md` was replaced with the neutral placeholder
`/home/operator/yams-checkout`. This is a privacy redaction for publication
only — no other bytes in any capture were altered.

This does not set `minimum_yams` / `minimum_ref` and does not publish either
repository.
