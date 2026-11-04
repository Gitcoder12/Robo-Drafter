"""
RoboDrafter - Universal Kinematic Chain Solver.
Uses the FABRIK algorithm to solve Inverse Kinematics for ANY number of joints.
Works for a 2-link arm, a humanoid leg, or a giant mecha.
"""

import math
import logging
from dataclasses import dataclass, field
from typing import List, Tuple

logger = logging.getLogger("RoboDrafter.Kinematics")

@dataclass
class Joint:
    """Represents a physical joint (servo/motor)."""
    name: str
    length_to_next: float # The length of the limb this joint controls
    
@dataclass
class KinematicChain:
    """A chain of joints (e.g., Shoulder -> Elbow -> Wrist)."""
    name: str
    origin: Tuple[float, float]
    joints: List[Joint]
    
    def solve_ik(self, target: Tuple[float, float], tolerance: float = 0.1, max_iterations: int = 10) -> List[Tuple[float, float]]:
        """
        FABRIK Algorithm: Forward And Backward Reaching Inverse Kinematics.
        Returns a list of (x, y) coordinates representing the positions of each joint.
        """
        logger.info(f"Solving IK for {self.name} to target {target}")
        
        num_joints = len(self.joints)
        total_length = sum(j.length_to_next for j in self.joints)
        
        # 1. Check if target is reachable
        dist_to_target = math.dist(self.origin, target)
        if dist_to_target > total_length:
            logger.error(f"Target out of reach! Max length: {total_length:.2f}, Distance: {dist_to_target:.2f}")
            return []
            
        # 2. Initialize joint positions in a straight line from origin
        # positions[0] is the base, positions[-1] is the end effector
        positions = [self.origin]
        current_pos = self.origin
        for joint in self.joints:
            # Assume initial straight line pointing towards target for faster convergence
            angle = math.atan2(target[1] - self.origin[1], target[0] - self.origin[0])
            next_x = current_pos[0] + joint.length_to_next * math.cos(angle)
            next_y = current_pos[1] + joint.length_to_next * math.sin(angle)
            current_pos = (next_x, next_y)
            positions.append(current_pos)

        # 3. Iterative FABRIK Loop
        for iteration in range(max_iterations):
            # Check if end effector is close enough to target
            end_pos = positions[-1]
            if math.dist(end_pos, target) <= tolerance:
                break

            # --- STAGE 1: BACKWARD REACHING (Pull end effector to target) ---
            positions[-1] = target
            for i in range(num_joints - 1, -1, -1):
                length = self.joints[i].length_to_next
                direction = (
                    positions[i][0] - positions[i+1][0],
                    positions[i][1] - positions[i+1][1]
                )
                dist = math.dist(positions[i], positions[i+1])
                
                # If joints overlap, nudge them slightly
                if dist == 0:
                    dist = 0.001 
                    
                # Calculate new position for joint i
                ratio = length / dist
                positions[i] = (
                    positions[i+1][0] + direction[0] * ratio,
                    positions[i+1][1] + direction[1] * ratio
                )

            # --- STAGE 2: FORWARD REACHING (Pull base back to origin) ---
            positions[0] = self.origin
            for i in range(num_joints):
                length = self.joints[i].length_to_next
                direction = (
                    positions[i+1][0] - positions[i][0],
                    positions[i+1][1] - positions[i][1]
                )
                dist = math.dist(positions[i], positions[i+1])
                
                if dist == 0:
                    dist = 0.001

                # Calculate new position for joint i+1
                ratio = length / dist
                positions[i+1] = (
                    positions[i][0] + direction[0] * ratio,
                    positions[i][1] + direction[1] * ratio
                )

        logger.info(f"IK Solved in {iteration + 1} iterations.")
        return positions
