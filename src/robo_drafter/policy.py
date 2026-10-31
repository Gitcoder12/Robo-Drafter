from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
import copy
import yaml
from pathlib import Path


@dataclass
class Policy:
    name: str
    version: int
    params: Dict[str, float]
    tasks: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Policy":
        data = yaml.safe_load(Path(path).read_text())
        return cls(
            name=data.get("name", "unnamed"),
            version=int(data.get("version", 1)),
            params=data.get("params", {}),
            tasks=data.get("tasks", {}),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "params": self.params,
            "tasks": self.tasks,
        }

    def save(self, path: str | Path) -> None:
        Path(path).write_text(yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False))

    def clone(self) -> "Policy":
        return copy.deepcopy(self)
