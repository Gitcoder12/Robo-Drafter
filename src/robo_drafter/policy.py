"""Validated policy configuration for Robo-Drafter."""

from __future__ import annotations

import copy
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Policy:
    name: str
    version: int
    params: dict[str, float]
    tasks: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Policy":
        """Load YAML and reject malformed policy values before use."""
        config_path = Path(path)
        try:
            data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ValueError(f"invalid policy YAML: {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError("policy YAML root must be a mapping")

        name = data.get("name", "unnamed")
        version = data.get("version", 1)
        params = data.get("params", {})
        tasks = data.get("tasks", {})

        if not isinstance(name, str) or not name.strip():
            raise ValueError("policy name must be a non-empty string")
        if isinstance(version, bool) or not isinstance(version, int) or version < 1:
            raise ValueError("policy version must be a positive integer")
        if not isinstance(params, dict):
            raise ValueError("policy params must be a mapping")
        if not isinstance(tasks, dict):
            raise ValueError("policy tasks must be a mapping")

        normalized_params: dict[str, float] = {}
        for key, value in params.items():
            if not isinstance(key, str) or not key.strip():
                raise ValueError("policy parameter names must be non-empty strings")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"policy parameter {key!r} must be numeric")
            if not math.isfinite(value):
                raise ValueError(f"policy parameter {key!r} must be finite")
            if key in {"speed", "precision", "exploration"} and not 0 <= value <= 1:
                raise ValueError(f"policy parameter {key!r} must be between 0 and 1")
            if key == "retry_limit" and (not isinstance(value, int) or value < 0):
                raise ValueError("retry_limit must be a non-negative integer")
            normalized_params[key] = float(value)

        normalized_tasks: dict[str, dict[str, Any]] = {}
        for task_name, task in tasks.items():
            if not isinstance(task_name, str) or not task_name.strip():
                raise ValueError("task names must be non-empty strings")
            if not isinstance(task, dict):
                raise ValueError(f"task {task_name!r} must be a mapping")
            goal = task.get("goal")
            threshold = task.get("success_threshold")
            if not isinstance(goal, str) or not goal.strip():
                raise ValueError(f"task {task_name!r} requires a non-empty goal")
            if (
                isinstance(threshold, bool)
                or not isinstance(threshold, (int, float))
                or not math.isfinite(threshold)
                or not 0 <= threshold <= 1
            ):
                raise ValueError(
                    f"task {task_name!r} success_threshold must be between 0 and 1"
                )
            normalized_tasks[task_name] = {
                **task,
                "goal": goal,
                "success_threshold": float(threshold),
            }

        return cls(
            name=name.strip(),
            version=version,
            params=normalized_params,
            tasks=normalized_tasks,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "params": self.params,
            "tasks": self.tasks,
        }

    def save(self, path: str | Path) -> None:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            yaml.safe_dump(self.to_dict(), default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )

    def clone(self) -> "Policy":
        return copy.deepcopy(self)
