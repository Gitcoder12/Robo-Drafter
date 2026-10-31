from __future__ import annotations
import random
from typing import Dict, Any


class Evaluator:
    """
    Extremely simple success evaluator.
    In real robotics you would plug in vision / force / state feedback here.
    For now we simulate realistic outcomes so the adaptive loop works.
    """

    def evaluate(self, task_name: str, policy_params: Dict[str, float], task_cfg: Dict[str, Any]) -> float:
        """
        Returns a score between 0.0 and 1.0
        """
        speed = policy_params.get("speed", 0.5)
        precision = policy_params.get("precision", 0.5)
        exploration = policy_params.get("exploration", 0.1)

        # Base success chance rises with precision and moderate speed
        base = 0.35 + (precision * 0.45) + (min(speed, 0.8) * 0.15)

        # Exploration adds variance
        noise = random.uniform(-exploration, exploration)
        score = max(0.0, min(1.0, base + noise))

        # Tiny bias so repeated good policies improve over time
        if precision > 0.75 and speed > 0.5:
            score = min(1.0, score + 0.05)

        return round(score, 3)
