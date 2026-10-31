from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .policy import Policy
from .evaluator import Evaluator
from .mutator import Mutator

console = Console()


class AdaptiveAgent:
    def __init__(self, config_path: str = "config/default.yaml"):
        self.policy = Policy.from_yaml(config_path)
        self.evaluator = Evaluator()
        self.mutator = Mutator()
        self.history: List[dict] = []

    def run_task(self, task_name: str) -> float:
        if task_name not in self.policy.tasks:
            console.print(f"[red]Unknown task: {task_name}[/red]")
            return 0.0

        task_cfg = self.policy.tasks[task_name]
        threshold = float(task_cfg.get("success_threshold", 0.7))

        console.print(Panel(f"Executing task: [bold]{task_name}[/bold]\nGoal: {task_cfg.get('goal', '')}", title="Robo-Drafter"))

        score = self.evaluator.evaluate(task_name, self.policy.params, task_cfg)
        success = score >= threshold

        # Decision logic
        if score >= 0.85:
            decision = "UPGRADE"
            self.policy = self.mutator.upgrade(self.policy)
        elif score >= threshold:
            decision = "MUTATE"
            self.policy = self.mutator.mutate(self.policy)
        else:
            decision = "REPLACE"
            self.policy = self.mutator.replace(self.policy)

        record = {
            "task": task_name,
            "score": score,
            "threshold": threshold,
            "success": success,
            "decision": decision,
            "policy_version": self.policy.version,
            "params": self.policy.params.copy(),
        }
        self.history.append(record)

        # Pretty output
        color = "green" if success else "red"
        console.print(f"Score: [{color}]{score:.3f}[/{color}]  (threshold {threshold})")
        console.print(f"Decision: [bold]{decision}[/bold] → new policy [cyan]{self.policy.name}[/cyan] (v{self.policy.version})")
        console.print(f"Params: {self.policy.params}")
        console.print()

        return score

    def run_workflow(self, tasks: List[str]) -> None:
        console.print("[bold]Starting multi-task workflow[/bold]\n")
        for t in tasks:
            self.run_task(t)

        self._print_summary()

    def _print_summary(self) -> None:
        if not self.history:
            return

        table = Table(title="Run History")
        table.add_column("Task")
        table.add_column("Score")
        table.add_column("Decision")
        table.add_column("Policy")

        for h in self.history:
            table.add_row(
                h["task"],
                f"{h['score']:.3f}",
                h["decision"],
                f"v{h['policy_version']}",
            )
        console.print(table)

    def save_policy(self, path: str = "config/current_policy.yaml") -> None:
        self.policy.save(path)
        console.print(f"[green]Policy saved → {path}[/green]")
