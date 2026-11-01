"""Configuration loading and validation for Robo-Drafter."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from robo_drafter.types import PolicyConfig


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "default.yaml"


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Config root must be a mapping, got {type(data)}")
    return data


def load_policy_config(path: str | Path | None = None) -> PolicyConfig:
    """Load configuration and convert it into a PolicyConfig object."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    raw = load_yaml(config_path)

    return PolicyConfig(
        name=raw.get("name", "default"),
        version=str(raw.get("version", "1.0")),
        params=raw.get("params", {}),
        strategy=raw.get("strategy", "baseline"),
    )


def save_policy_config(config: PolicyConfig, path: str | Path) -> None:
    """Save a PolicyConfig back to a YAML file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "name": config.name,
        "version": config.version,
        "strategy": config.strategy,
        "params": config.params,
    }

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def get_param(config: PolicyConfig, key: str, default: Any = None) -> 
