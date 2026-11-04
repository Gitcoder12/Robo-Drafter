import math
import logging
from typing import Tuple

logger = logging.getLogger("RoboDrafter.Kinematics")

class RobotArm2DOF:
    """Calculates motor angles for a 2-joint robotic arm."""
    
    def __init__(self, link1_length: float, link2_length: float):
        self.L1 = link1_length
        self.L2 = link2_length

    def calculate_angles(self, target_x: float, target_y: float) -> Tuple[float, float]:
        """
        Returns (theta1, theta2) in degrees.
        Theta 1 is the shoulder, Theta 2 is the elbow.
        """
        # Distance to target
        dist_sq = target_x**2 + target_y**2
        dist = math.sqrt(dist_sq)
        
        # Check if target is reachable
        if dist > (self.L1 + self.L2):
            logger.warning(f"Target ({target_x}, {target_y}) is out of reach.")
            return 0.0, 0.0

        # Law of Cosines for Theta 2 (Elbow joint)
        cos_theta2 = (dist_sq - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        cos_theta2 = max(-1.0, min(1.0, cos_theta2)) # Clamp to prevent math domain errors
        
        # We use the negative root for an "elbow up" configuration
        sin_theta2 = -math.sqrt(1 - cos_theta2**2)
        theta2 = math.atan2(sin_theta2, cos_theta2)
        
        # Law of Sines for Theta 1 (Shoulder joint)
        theta1 = math.atan2(target_y, target_x) - math.atan2(
            self.L2 * sin_theta2, 
            self.L1 + self.L2 * cos_theta2
        )
        
        # Convert to degrees
        return math.degrees(theta1), math.degrees(theta2)
