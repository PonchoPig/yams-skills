# Yams skills

Portable agent workflows for tilling, sowing, harvesting, and cultivating
shared project memory with [Yams](https://github.com/PonchoPig/yams).

This repository is a private pre-release while the matching Yams capability
contracts are prepared for their first public release.

## Skills

- `yams-harvest` harvests durable project knowledge during ordinary work.
- `yams-sow` preserves one verified, durable, reusable finding.
- `yams-till` inspects, plans, and applies explicitly approved repository
  memory initialization or upgrades.
- `yams-cultivate` audits, refreshes, consolidates, and repairs an existing
  structured memory corpus.

The skills contain agent workflow only. Yams owns repository layouts,
schemas, validation, manifests, filesystem safety, and recovery.

## Install

Node.js 22.20 or newer is an installer only prerequisite. Node and `npx` are
not Yams runtime dependencies.

Install the everyday skills globally:

```sh
npx skills add PonchoPig/yams-skills --skill yams-harvest --skill yams-sow --skill yams-till --global
```

Install cultivation into a project when the maintenance workflow should travel
with the repository:

```sh
npx skills add PonchoPig/yams-skills --skill yams-cultivate
```

The `npx skills` tool asks which supported harnesses to target and owns their
links or copies plus `skills-lock.json`. This repository does not maintain a
Claude-, Codex-, Cursor-, or OpenCode-specific installer.

Installing these skills does not install Yams. Install or build Yams
separately and confirm the required contracts with:

```sh
yams-wiki capabilities --json
```

These skills require Yams 0.1.0 or newer (tag `v0.1.0`). `compatibility.json`
pins `minimum_yams` and `minimum_ref` to that release, verified by both
compatibility lanes.

## Development

```sh
python3 -m unittest discover -v
./scripts/test-skills.sh
./scripts/test-yams-contract.sh /path/to/yams-wiki
```

The installer test uses a temporary HOME and project. It never installs into a
developer's real harness directories.

## License

Licensed under either Apache-2.0 or MIT, at your option.
