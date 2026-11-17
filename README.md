# Robo-Drafter
Adaptive robotic agent that evaluates task success. Upgrades policies on good runs, mutates strategy on bad runs, and replaces the config entirely on failure. Handles single and multi-task workflows.

#File Structure
Robo-Drafter/
├── README.md
├── pyproject.toml
├── requirements.txt
├── config/
│   └── default.yaml
├── src/
│   └── robo_drafter/
│       ├── __init__.py
│       ├── agent.py
│       ├── evaluator.py
│       ├── policy.py
│       ├── mutator.py
│       └── cli.py
└── examples/
    └── run_demo.py


---

## AI-maintained project notes (secondary — 2026-11-13)

This section supplements the maintainer-authored README above. The original text has been restored verbatim from Git-history baseline `b9e69362043ccde07f1ed83aba0f930ff8a7cf3c`; this addendum does not replace or certify the original claims.

- The current source tree, runtime data and tests are the implementation source of truth. Roadmap items, draft PRs and AI-generated descriptions are not shipped features by themselves.
- Preserve real and maintainer-provided data. Never silently substitute generated or placeholder data. Clearly label and isolate synthetic fixtures.
- Mark unverified sources, identifiers, metrics, benchmark results and external claims as unknown/unverified rather than guessing.
- Verify setup, execution, tests and public claims against the exact current commit before using this repository in a job, research or academic application.
- See [MODEL_AUDIT_ROUTER.md](MODEL_AUDIT_ROUTER.md) for independent model review instructions and the merge gate.


### Proposed dashboard clarification — open PR, not yet merged (2026-11-13)

[PR #2](https://github.com/Gitcoder12/Robo-Drafter/pull/2) proposes explicit installation instructions for the optional Streamlit dashboard and a more precise prototype scope. Its branch README states that the dashboard is a **synthetic demonstration**: it generates illustrative fitness values in a browser session and does not connect to a physical robot, robotics simulator, camera, or hardware controller. Do not present the dashboard as a live robot-control or validated robotics experiment unless a separate, tested integration proves that capability.

---

## Engineering Audit & Handover — 2026-11-17

**Reviewed commit:** `a9e62d87fafe69201a678af12a82d4cda6d416f9` (`main`). Static inspection covered the adaptive agent, policy loader, and config-loader tests; tests were not executed.

### Confirmed findings
- The inspected `AdaptiveAgent` evaluates named tasks against configured thresholds and mutates/replaces policy parameters based on score bands. The inspected implementation is a software policy/evaluation prototype; it does not demonstrate control of a physical robot or validated hardware safety.
- `Policy.from_yaml()` loads configuration with `yaml.safe_load`, but the inspected method assumes the loaded document is a mapping and that `params` / `tasks` have expected shapes. The separate config-loader tests do not establish validation of this `Policy` loader.
- The visible test file focuses on config loading and round-tripping, not on mutation safety, evaluator correctness, or task-level performance.

### Next actions
1. Validate policy YAML root type, required fields, numeric ranges, and task schemas before execution.
2. Add deterministic tests for every mutation decision and ensure invalid policy changes can be rolled back.
3. Clearly separate simulation results from hardware experiments; add hardware interlocks and independent safety review before physical deployment.

**Verification status:** static source/test inspection only; agent workflow, full test suite, and hardware behavior remain unverified.
