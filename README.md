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
