```markdown
# Robo-Drafter

**Adaptive evolutionary agent for robotic configuration optimization.**

Robo-Drafter evaluates task performance, upgrades policies on successful runs, mutates strategy on weak runs, and fully replaces the configuration when performance collapses. Designed for single-task and multi-task robotic workflows.

---

## Features

- **Policy Evaluation** — Scores configuration performance after each run
- **Adaptive Mutation** — Mutates strategy when results are poor
- **Full Config Replacement** — Discards failing policies and starts fresh
- **Generation Tracking** — Maintains history of fitness scores and mutation types
- **Streamlit Dashboard** — Visual interface to watch the evolutionary process

---

## Project Structure

```text
Robo-Drafter/
├── README.md
├── pyproject.toml
├── requirements.txt
├── dashboard.py                  # Streamlit evolutionary dashboard
├── config/
│   └── default.yaml              # Default policy configuration
├── src/
│   └── robo_drafter/
│       ├── __init__.py
│       ├── agent.py              # Main adaptive agent loop
│       ├── evaluator.py          # Performance scoring
│       ├── policy.py             # Current strategy / config
│       ├── mutator.py            # Mutation and replacement logic
│       ├── cli.py                # Command-line interface
│       ├── types.py              # Shared data models
│       ├── config_loader.py      # YAML config loading
│       └── simulator.py          # Task simulation environment
└── examples/
    └── run_demo.py               # Quick demo script
```

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Gitcoder12/Robo-Drafter.git
cd Robo-Drafter

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
pip install streamlit plotly pandas pyyaml

# Run the demo
python examples/run_demo.py

# Launch the dashboard
streamlit run dashboard.py
```

---

## How It Works

```text
┌─────────────┐
│   Policy    │
└──────┬──────┘
       ▼
┌─────────────┐
│  Evaluator  │  →  Score the run
└──────┬──────┘
       ▼
┌─────────────┐
│   Mutator   │  →  Upgrade / Mutate / Replace
└──────┬──────┘
       ▼
┌─────────────┐
│    Agent    │  →  Decide next action
└─────────────┘
```

1. **Policy** holds the current configuration and strategy.
2. **Evaluator** measures success and returns a fitness score.
3. **Mutator** improves the policy or replaces it entirely on failure.
4. **Agent** orchestrates the full loop across generations.

---

## Dashboard

Launch the visual interface:

```bash
streamlit run dashboard.py
```

The dashboard shows:
- Current generation
- Best fitness score
- Last mutation type
- Fitness progression chart over generations

---

## Configuration

Edit `config/default.yaml` to change default parameters, strategy, and mutation behavior.

---

## License

Apache License 2.0
```
