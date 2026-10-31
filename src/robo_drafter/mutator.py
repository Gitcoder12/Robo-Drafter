from __future__ import annotations
import random
from .policy import Policy


class Mutator:
    """Handles upgrade / mutate / replace decisions."""

    def upgrade(self, policy: Policy) -> Policy:
        """Strengthen the current policy (good run)."""
        new = policy.clone()
        new.version += 1
        new.name = f"{policy.name}_upgraded_v{new.version}"

        # Increase precision and slightly increase speed
        new.params["precision"] = min(0.95, new.params.get("precision", 0.5) + 0.07)
        new.params["speed"] = min(0.9, new.params.get("speed", 0.5) + 0.03)
        new.params["exploration"] = max(0.05, new.params.get("exploration", 0.15) - 0.02)
        return new

    def mutate(self, policy: Policy) -> Policy:
        """Small random changes (mediocre run)."""
        new = policy.clone()
        new.version += 1
        new.name = f"{policy.name}_mutated_v{new.version}"

        for key in ["speed", "precision", "exploration"]:
            if key in new.params:
                delta = random.uniform(-0.12, 0.12)
                new.params[key] = max(0.05, min(0.95, new.params[key] + delta))
        return new

    def replace(self, policy: Policy) -> Policy:
        """Complete strategy replacement (failure)."""
        new = policy.clone()
        new.version += 1
        new.name = f"fresh_policy_v{new.version}"

        # Completely new parameter set
        new.params = {
            "speed": round(random.uniform(0.3, 0.8), 2),
            "precision": round(random.uniform(0.4, 0.85), 2),
            "retry_limit": random.randint(1, 4),
            "exploration": round(random.uniform(0.1, 0.3), 2),
        }
        return new
