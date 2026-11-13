# Agent Instructions — Robo-Drafter

## Mission

Help maintain Robo-Drafter through narrow, testable engineering and research contributions. Start by reading README.md, CONTRIBUTING.md, FEATURE_UPGRADE_PLAN.md and ACTIVITY_LOG.md.

## Required workflow

1. Inspect the relevant code, tests, current issues and open PRs before changing anything.
2. State the exact objective, files expected to change, risk and validation plan.
3. Work on a dedicated feature branch with minimal diffs.
4. Preserve existing public APIs unless the task explicitly requires a change.
5. Add tests for new behavior, boundaries and failure cases.
6. Run the documented checks; report exact commands and actual outcomes.
7. Update docs and append an accurate log entry.
8. Open a PR; never merge or deploy autonomously.

## Safety and honesty

- Never invent test results, benchmarks, data provenance or implementation status.
- Do not add secrets, private data, credentials or unlicensed datasets.
- Do not modify generated, vendored or upstream files without a task-specific reason.
- Stop and request maintainer review when requirements conflict or an action is destructive.
- Treat simulation and synthetic data as such; never imply physical robot control unless a verified hardware integration exists.
