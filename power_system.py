"""
RoboDrafter - Power Distribution & Fuse Simulation.
Calculates electrical load, wire sizing, and implements safety fuses to prevent mech fires.
"""

import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("RoboDrafter.PowerSystem")

class WireMaterial(Enum):
    COPPER = {"resistivity": 1.68e-8, "max_temp_c": 150}
    ALUMINUM = {"resistivity": 2.82e-8, "max_temp_c": 120}
    SUPERCONDUCTOR = {"resistivity": 0.0, "max_temp_c": 300} # Sci-fi

@dataclass
class Fuse:
    rating_amps: float
    trip_time_ms: float
    is_blown: bool = False

    def check_trip(self, current_amps: float, time_exposed_ms: float) -> bool:
        """
        Simulates a fast-acting fuse. If current exceeds rating and time exceeds trip_time, it blows.
        """
        if self.is_blown:
            return True
            
        if current_amps > self.rating_amps and time_exposed_ms >= self.trip_time_ms:
            self.is_blown = True
            logger.critical(f"FUSE BLOWN! Current {current_amps:.1f}A exceeded rating {self.rating_amps}A for {time_exposed_ms}ms.")
            return True
        return False

class PowerBus:
    def __init__(self, system_voltage_v: float):
        self.voltage = system_voltage_v
        self.max_system_amps = 0.0
        
    def calculate_current(self, power_draw_watts: float) -> float:
        """Ohm's Law: I = P / V."""
        return power_draw_watts / self.voltage

    def calculate_wire_heat(self, current_amps: float, wire_length_m: float, cross_section_mm2: float, material: WireMaterial) -> dict:
        """
        Calculates Joule Heating (P = I^2 * R) to see if the wire will melt.
        """
        # Resistance R = rho * (L / A)
        # Convert mm2 to m2 for calculation
        area_m2 = cross_section_mm2 * 1e-6
        resistance = material.value["resistivity"] * (wire_length_m / area_m2)
        
        # Power lost as heat (Watts)
        heat_watts = (current_amps ** 2) * resistance
        
        # Simplified temperature rise estimation (assumes no cooling)
        temp_rise = heat_watts * 0.05 # Arbitrary scaling for simulation
        estimated_temp = 25 + temp_rise # Assuming 25C ambient
        
        status = "SAFE"
        if estimated_temp > material.value["max_temp_c"]:
            status = "MELTDOWN"
            logger.error(f"WIRE MELTDOWN! Estimated temp {estimated_temp:.1f}C exceeds max {material.value['max_temp_c']}C.")
            
        return {
            "resistance_ohms": resistance,
            "heat_watts": heat_watts,
            "estimated_temp_c": estimated_temp,
            "status": status
        }

# --- SIMULATION: ACTIVATING A GIANT MECH JOINT ---
if __name__ == "__main__":
    # Standard EV voltage (800V). At 48V, the amps would be so high the wires would vaporize.
    mech_grid = PowerBus(system_voltage_v=800.0)
    
    # The Mech Knee Actuator requires 500 kW (500,000 Watts) to lift the leg.
    actuator_power_w = 500_000 
    
    # Calculate Current Draw
    current = mech_grid.calculate_current(actuator_power_w)
    logger.info(f"Actuator demands {actuator_power_w}W at {mech_grid.voltage}V. Current draw: {current:.1f} Amps")
    
    # We install a 700 Amp Fast-Acting Fuse
    knee_fuse = Fuse(rating_amps=700, trip_time_ms=5.0)
    
    # The mech steps in mud, the leg gets jammed, and the motor stalls.
    # Current spikes to 900 Amps.
    stall_current = 900.0
    logger.warning(f"LEG JAMMED! Motor stall detected. Current spiking to {stall_current}A!")
    
    # We check the fuse after 2ms
    if not knee_fuse.check_trip(stall_current, time_exposed_ms=2.0):
        logger.info("Fuse held. Checking wire heat...")
        # Wire is 10mm2 Copper (Too thin for 900A!)
        heat_data = mech_grid.calculate_wire_heat(stall_current, 2.0, 10.0, WireMaterial.COPPER)
        logger.info(f"Heat data: {heat_data}")
        
    # We check the fuse again after 6ms
    if knee_fuse.check_trip(stall_current, time_exposed_ms=4.0):
        logger.critical("EMERGENCY POWER CUTOFF TRIGGERED. Mech is safe. Rewire with 100mm2 wire.")
