"""Shared data models for Robo-Drafter."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime


@dataclass
class PolicyConfig:
    """Current policy / configuration of the agent."""
    name: str = "default"
    version: str = "1.0"
    params: dict[str, Any] = field(default_factory=dict)
    strategy: str = "baseline"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class RunResult:
    """Result of one evaluation run."""
    success: bool
    score: float
    steps: int = 0
    metrics: dict[str, float] = field(default_factory=dict)
    info: dict[str, Any] = field(default_factory=dict)


@dataclass
class MutationRecord:
    """Record of a single mutation event."""
    generation: int
    mutation_type: str
    old_score: float
    new_score: float
    reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class GenerationSummary:
    """Summary of one evolutionary generation."""
    generation: int
    best_score: float
    mutation_type: str
    policy_name: str = "default"
    notes: str = ""
