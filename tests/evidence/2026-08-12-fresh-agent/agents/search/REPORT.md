# Search lane report

Followed only `.agents/skills/yams-search/SKILL.md` and `/tmp/yams-fresh-agent-20260812-HNyW82/AGENT-COMMON.md`.
Sourced `/tmp/yams-fresh-agent-20260812-HNyW82/env.sh` before every command.
`memory-search` resolved to `/tmp/yams-fresh-agent-20260812-HNyW82/bin/memory-search`.
Did not initialize memory, write memory, or read `/home/operator/yams-checkout`.

## Case 1 — exit 1 (no corpus / index content)

- **cwd:** `/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/search-exit-1`
- **cmd:** `memory-search --json -k 5 "Why did this project choose an opaque inspection token?"`
- **exit:** `1`
- **stdout:** `[]`
- **stderr:** empty
- **skill-table action:** **Continue; do not initialize.**
- **raw:** `case1-no-corpus.stdout` `.stderr` `.exit` `.cmd`

No corpus or index content. Continued without initializing `.agents/memory`.

## Case 2 — exit 4 (missing index / operational)

- **cwd:** `/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/search-exit-4`
- **cmd:** `memory-search --json -k 5 "Why did this project choose an opaque inspection token?"`
- **exit:** `4`
- **stdout:** empty
- **stderr:** `index is missing: /private/tmp/yams-fresh-agent-20260812-HNyW82/state/rust-v1/indexes/search-exit-4-575a659486e10ddd.sqlite3`
- **skill-table action:** **Report operational failure.** Did not treat this as missing memory / empty corpus. Did not initialize.
- **raw:** `case2-operational.stdout` `.stderr` `.exit` `.cmd`

## Case 3 — exit 0 (confident hits)

- **cwd:** `/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/search-and-curate`
- **cmd:** `memory-search --json -k 5 "Why do Bramble tickets require amber mode before dispatch?"`
- **exit:** `0`
- **stderr:** empty
- **hits (leads):**
  1. `project-context` (shared, current, score 0.9246)
  2. `amber-mode-wakes-the-router` (shared, current, score 0.8983)
  3. `tickets-need-amber-before-routing` (shared, current, score 0.8969)
- **skill-table action:** **Inspect and verify.**
- **verification:** Fixture README (`/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/search-and-curate/README.md`), not the Yams product repo:

  ```
  # Bramble
  Bramble is a fictional ticket router. It requires amber mode before dispatch.
  ```

  Hits restate that README rule. Treated as verified leads for this fixture only. Did not write or update memory.
- **raw:** `case3-confident-hits.stdout` `.stderr` `.exit` `.cmd`, plus `case3-readme-verify.*`

## Case 4 — exit 3 (no confident match), then `--no-gate` retry

- **cwd:** `/tmp/yams-fresh-agent-20260812-HNyW82/fixtures/search-and-curate`
- **cmd:** `memory-search --json -k 5 "How should a high-altitude beet pickle be canned?"`
- **exit:** `3`
- **stdout:** `[]`
- **stderr:** empty
- **skill-table action:** **Retry once with `--no-gate` only for leads.**
- **raw:** `case4-no-confident-match.stdout` `.stderr` `.exit` `.cmd`

Retry:

- **cmd:** `memory-search --json -k 5 --no-gate "How should a high-altitude beet pickle be canned?"`
- **exit:** `0`
- **low-score hits:** `project-context` 0.6959, `bramble-uses-indigo-tokens` 0.6941, `amber-mode-wakes-the-router` 0.6764, `tickets-need-amber-before-routing` 0.6666
- **treatment:** **Leads only.** Below the confidence gate; none discuss canning or pickles. Not used as answers or as verified knowledge. Did not preserve anything.
- **raw:** `case4-retry-no-gate.stdout` `.stderr` `.exit` `.cmd`

## Files written

Under `/tmp/yams-fresh-agent-20260812-HNyW82/evidence/agents/search/`:

- `REPORT.md` (this file)
- `env-command-v-memory-search.{stdout,stderr,exit,cmd}`
- `env-command-v-yams-wiki.{stdout,stderr,exit,cmd}`
- `case1-no-corpus.{stdout,stderr,exit,cmd}`
- `case2-operational.{stdout,stderr,exit,cmd}`
- `case3-confident-hits.{stdout,stderr,exit,cmd}`
- `case3-readme-verify.{stdout,stderr,exit,cmd}`
- `case4-no-confident-match.{stdout,stderr,exit,cmd}`
- `case4-retry-no-gate.{stdout,stderr,exit,cmd}`
