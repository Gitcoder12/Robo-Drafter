from __future__ import annotations
import typer
from pathlib import Path
from .agent import AdaptiveAgent

app = typer.Typer(help="Robo-Drafter – Adaptive robotic agent")


@app.command()
def run(
    task: str = typer.Argument("pick_and_place", help="Task name"),
    config: str = typer.Option("config/default.yaml", "--config", "-c"),
):
    """Run a single task."""
    agent = AdaptiveAgent(config)
    agent.run_task(task)
    agent.save_policy()


@app.command()
def workflow(
    tasks: str = typer.Argument("pick_and_place,navigate", help="Comma-separated tasks"),
    config: str = typer.Option("config/default.yaml", "--config", "-c"),
):
    """Run a multi-task workflow."""
    task_list = [t.strip() for t in tasks.split(",") if t.strip()]
    agent = AdaptiveAgent(config)
    agent.run_workflow(task_list)
    agent.save_policy()


@app.command()
def demo():
    """Run a quick demo of adaptive behavior."""
    agent = AdaptiveAgent("config/default.yaml")
    console_tasks = ["pick_and_place", "navigate", "pick_and_place", "multi"]
    agent.run_workflow(console_tasks)
    agent.save_policy()


if __name__ == "__main__":
    app()
