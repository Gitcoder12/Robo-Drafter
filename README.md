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
