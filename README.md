# Robo-Drafter

**An adaptive evolutionary agent for robotic configuration optimization.**

Robo-Drafter evaluates robotic task performance, improves policies after successful runs, mutates strategies when performance declines, and replaces failing configurations when necessary.

Designed to support both single-task and multi-task robotic workflows.

## Features

- **Policy Evaluation** — Measures configuration performance after each execution.
- **Adaptive Mutation** — Adjusts strategies when performance is below expectations.
- **Configuration Replacement** — Discards failing policies and generates fresh configurations.
- **Generation Tracking** — Records fitness scores, mutation types, and evolutionary history.
- **Interactive Dashboard** — Visualizes the evolutionary process using Streamlit.

## Project Structure

```text
Robo-Drafter/
├── README.md
├── pyproject.toml
├── requirements.txt
├── dashboard.py
├── config/
│   └── default.yaml
├── src/
│   └── robo_drafter/
│       ├── __init__.py
│       ├── agent.py
│       ├── evaluator.py
│       ├── policy.py
│       ├── mutator.py
│       ├── cli.py
│       ├── types.py
│       ├── config_loader.py
│       └── simulator.py
└── examples/
    └── run_demo.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Gitcoder12/Robo-Drafter.git
cd Robo-Drafter
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e ".[dashboard]"
```

## Quick Start

Run the demonstration:

```bash
python examples/run_demo.py
```

Launch the interactive dashboard:

```bash
streamlit run dashboard.py
```

## How It Works

Robo-Drafter follows an evolutionary optimization loop:

```text
┌─────────────────┐
│     Policy      │
│ Current Config  │
└────────┬────────┘
         ▼
┌─────────────────┐
│    Evaluator    │
│  Score Results  │
└────────┬────────┘
         ▼
┌─────────────────┐
│     Mutator     │
│ Upgrade / Mutate│
│    / Replace    │
└────────┬────────┘
         ▼
┌─────────────────┐
│      Agent      │
│ Next Generation │
└─────────────────┘
```

### Evolutionary Workflow

1. **Initialize** — Load the initial policy and configuration.
2. **Evaluate** — Execute the policy and calculate its fitness score.
3. **Adapt** — Improve successful policies or mutate underperforming strategies.
4. **Replace** — Generate a fresh configuration when performance collapses.
5. **Track** — Record fitness scores and mutation history across generations.

## Dashboard

Install the optional dashboard dependencies with `pip install -e ".[dashboard]"`. The core CLI does not require Streamlit, pandas, or Plotly.

The Streamlit dashboard is a synthetic demonstration of the evolutionary loop. It generates illustrative fitness values in the browser session; it does not connect to a physical robot, robotics simulator, camera, or hardware controller. It provides visibility into the demo state, including:

- Current generation
- Best fitness score
- Most recent mutation type
- Fitness progression across generations

## Configuration

Customize the agent's behavior by editing:

```text
config/default.yaml
```

This file controls default parameters, policy strategies, and mutation behavior.

## License

Distributed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
