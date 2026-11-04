"""
RoboDrafter - Realistic Modular Robotics Payload System.
Models the physical and electrical constraints of industrial modular robots
(e.g., Boston Dynamics Spot, Universal Robots UR10, NASA Robonaut).

Implements:
- Quick-change mechanical ports.
- Power distribution limits (Voltage / Current).
- Communication bus validation (CAN bus, EtherCAT).
- Center of Mass (CoM) tipping prevention.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger("RoboDrafter.ModularRobot")

@dataclass
class PortSpec:
    """Represents a physical mounting point with electrical and data limits."""
    port_id: str
    max_payload_kg: float
    max_voltage_v: float
    max_current_amps: float
    protocol: str  # e.g., "CAN", "EtherCAT", "RS-485"
    offset_x_meters: float  # Distance from robot center (lateral)
    offset_y_meters: float  # Distance from robot center (longitudinal)

@dataclass
class Module:
    """A swappable payload (Arm, LiDAR, Gripper, Drill)."""
    module_id: str
    name: str
    mass_kg: float
    operating_voltage_v: float
    max_draw_amps: float
    required_protocol: str
    
    def calculate_power_watts(self) -> float:
        return self.operating_voltage_v * self.max_draw_amps

@dataclass
class RobotChassis:
    """The base mobile robot or robotic arm."""
    unit_id: str
    base_mass_kg: float
    battery_capacity_wh: float
    max_power_output_watts: float
    ports: Dict[str, PortSpec] = field(default_factory=dict)
    attached_modules: Dict[str, Module] = field(default_factory=dict)

    def register_port(self, port: PortSpec):
        self.ports[port.port_id] = port
        logger.info(f"[{self.unit_id}] Port registered: {port.port_id} ({port.protocol}, {port.max_voltage_v}V, max {port.max_payload_kg}kg)")

    def attach_payload(self, port_id: str, module: Module) -> bool:
        """Validates and hot-swaps a payload onto the robot."""
        logger.info(f"[{self.unit_id}] Attempting to attach {module.name} to {port_id}...")
        
        if port_id not in self.ports:
            logger.error(f"[{self.unit_id}] REJECTED: Port {port_id} does not exist.")
            return False

        port = self.ports[port_id]

        # 1. Mechanical Payload Limit
        if module.mass_kg > port.max_payload_kg:
            logger.error(f"[{self.unit_id}] REJECTED: {module.name} ({module.mass_kg}kg) exceeds port payload limit ({port.max_payload_kg}kg).")
            return False

        # 2. Protocol Compatibility (CAN bus vs EtherCAT)
        if port.protocol != module.required_protocol:
            logger.error(f"[{self.unit_id}] REJECTED: Protocol mismatch. Port is {port.protocol}, module requires {module.required_protocol}.")
            return False

        # 3. Electrical Compatibility (Voltage)
        if module.operating_voltage_v != port.max_voltage_v:
            logger.error(f"[{self.unit_id}] REJECTED: Voltage mismatch. Port provides {port.max_voltage_v}V, module requires {module.operating_voltage_v}V.")
            return False

        # 4. Current Draw Limit
        if module.max_draw_amps > port.max_current_amps:
            logger.error(f"[{self.unit_id}] REJECTED: {module.name} draws {module.max_draw_amps}A, exceeding port limit of {port.max_current_amps}A.")
            return False

        # 5. Total Power Budget Check
        current_power_draw = sum(m.calculate_power_watts() for m in self.attached_modules.values())
        new_total_power = current_power_draw + module.calculate_power_watts()
        
        if new_total_power > self.max_power_output_watts:
            logger.error(f"[{self.unit_id}] REJECTED: Power budget exceeded! ({new_total_power}W > {self.max_power_output_watts}W).")
            return False

        # 6. Center of Mass (CoM) Tipping Check
        if not self._check_center_of_mass(port, module):
            return False

        # All checks passed, engage mechanical locks
        self.attached_modules[port_id] = module
        logger.info(f"[{self.unit_id}] SUCCESS: Payload {module.name} locked to {port_id}. Power draw: {new_total_power}W.")
        return True

    def _check_center_of_mass(self, port: PortSpec, module: Module) -> bool:
        """
        Calculates if the robot will tip over due to asymmetric weight.
        Uses a simplified torque calculation: Mass * Distance from center.
        """
        # Total mass including new module
        total_mass = self.base_mass_kg + sum(m.mass_kg for m in self.attached_modules.values()) + module.mass_kg
        
        # Calculate lateral torque (tipping force)
        # Assuming a roughly symmetric base before attachment
        torque_nm = module.mass_kg * 9.81 * port.offset_x_meters
        
        # Real-world rule of thumb: If torque exceeds 50 Nm, the robot is unstable on flat ground
        max_safe_torque_nm = 50.0 
        
        if abs(torque_nm) > max_safe_torque_nm:
            logger.critical(
                f"[{self.unit_id}] TIPPING HAZARD! Attaching {module.name} at X={port.offset_x_meters}m creates {torque_nm:.1f} Nm of lateral torque. Max safe: {max_safe_torque_nm} Nm."
            )
            return False
            
        logger.info(f"[{self.unit_id}] CoM Check Passed. Lateral torque: {torque_nm:.1f} Nm.")
        return True

    def detach_payload(self, port_id: str) -> Optional[Module]:
        """Safely releases a payload."""
        if port_id in self.attached_modules:
            module = self.attached_modules.pop(port_id)
            logger.warning(f"[{self.unit_id}] Payload {module.name} released from {port_id}. Rebalancing chassis.")
            return module
        return None

# --- REAL-WORLD SIMULATION: BOSTON DYNAMICS SPOT ---
if __name__ == "__main__":
    logger.info("=== INITIALIZING REAL-WORLD MODULAR ROBOT (SPOT-LIKE) ===")
    
    # 1. Create the Quadruped Base
    # Base mass 32kg, max output 500W (Spot's battery is around 600Wh, but continuous output is limited)
    spot = RobotChassis(unit_id="Spot_Enterprise", base_mass_kg=32.5, battery_capacity_wh=600, max_power_output_watts=300)
    
    # 2. Define physical mounting ports
    # Spot has a top rail and side payload ports. Let's define a top port.
    spot.register_port(PortSpec(
        port_id="TOP_RAIL", max_payload_kg=14.0, max_voltage_v=48.0, 
        max_current_amps=10.0, protocol="CAN", offset_x_meters=0.0, offset_y_meters=0.0
    ))
    
    # Define an arm port (like the Spot Arm)
    spot.register_port(PortSpec(
        port_id="FRONT_ARM_PORT", max_payload_kg=5.0, max_voltage_v=48.0, 
        max_current_amps=15.0, protocol="EtherCAT", offset_x_meters=0.0, offset_y_meters=0.8
    ))

    # 3. Create real-world payloads
    lidar_scanner = Module(
        module_id="LIDAR-01", name="Velodyne LiDAR", mass_kg=2.0, 
        operating_voltage_v=48.0, max_draw_amps=1.5, required_protocol="CAN"
    )
    
    spot_arm = Module(
        module_id="ARM-01", name="Spot Arm", mass_kg=8.0, 
        operating_voltage_v=48.0, max_draw_amps=12.0, required_protocol="EtherCAT"
    )
    
    heavy_drill = Module(
        module_id="DRILL-01", name="Concrete Drill", mass_kg=15.0, # Over 14kg payload limit!
        operating_voltage_v=48.0, max_draw_amps=10.0, required_protocol="CAN"
    )

    # 4. Test the attachment logic
    # Test 1: Attach LiDAR to top rail (Should Pass)
    spot.attach_payload("TOP_RAIL", lidar_scanner)
    
    # Test 2: Attach Spot Arm to front port (Should Pass)
    spot.attach_payload("FRONT_ARM_PORT", spot_arm)
    
    # Test 3: Attach Concrete Drill to top rail (Should FAIL - too heavy)
    spot.attach_payload("TOP_RAIL", heavy_drill)
