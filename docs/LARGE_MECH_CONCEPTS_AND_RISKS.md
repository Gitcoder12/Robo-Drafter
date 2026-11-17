# Robo-Drafter — concept drafting for large service mechs

## Purpose and boundary

Robo-Drafter is a software policy/evaluation prototype. This document adds a proposed concept workflow for non-weaponized large robots. No dimensions, loads, actuators, material grades or hardware performance are assumed. These sketches are layout discussions, not engineering drawings.

Intended missions: industrial inspection, disaster-area sensing, remote material handling and hazardous-environment maintenance. Excluded: weaponization, autonomous use of force and crowd-control functions.

## Concept A — inspection / rescue support walker

    FRONT ELEVATION — NOT TO SCALE

                   [360° sensor mast]
                           |
                   +---------------+
                   | protected     |
                   | compute bay   |
              _____+---------------+_____
             /       torso / battery      \
        [arm joint]                   [arm joint]
             |                           |
        [sensor tool]               [inspection tool]
             |                           |
                   [pelvis frame]
                       /   \
              [wide stable leg modules]
                 /                 \
          [large foot]         [large foot]

Mission: carry cameras, thermal sensors, lighting and communications into areas where human access is unsafe. It does not autonomously decide to apply force.

## Concept B — industrial material-handling mech

    SIDE VIEW — MODULAR CONCEPT

       [perception mast]
              |
       [compute / safety controller]
              |
       [load-bearing torso frame]----[tool interface]
              |
        [pelvis / battery]
          /           \
  [leg module]     [leg module]
        |               |
  [wide foot]       [wide foot]

Mission: move a bounded payload under human-supervised work-cell constraints. Prefer wheels, tracked bases or mobile manipulators when they meet the task; a humanoid-scale mech is not automatically the safest or cheapest design.

## Mandatory engineering checks

1. Define the mission, environment, duty cycle and exclusion zone.
2. Establish maximum payload, reach, speed, centre of mass and ground pressure.
3. Complete kinematic simulation and collision analysis.
4. Perform structural FEA, fatigue analysis and physical proof testing.
5. Assess battery thermal runaway, high-current faults and fire response.
6. Add an independent safety controller and physical emergency stop.
7. Test loss of comms, stale perception, controller reset and sensor disagreement.
8. Conduct human-factors, maintenance and lockout/tagout reviews.
9. Require independent engineering sign-off before fabrication or field trials.

## Risk register

| Hazard | Severity | Required controls |
|---|---|---|
| Toppling / unstable load | Critical | Low centre of gravity, wide support polygon, stability monitoring, speed limits, safe kneel state |
| Joint/frame fracture | Critical | FEA, fatigue test, proof load, inspection intervals, redundant retention |
| Crush / pinch injury | Critical | Force/speed limits, guarding, proximity sensing, exclusion zones, emergency stop |
| Battery thermal event | Critical | Certified battery/BMS, thermal isolation, fusing, fire response |
| Sensor occlusion / pose error | High | Independent modalities, uncertainty limits, stale-data safe stop |
| Control or network failure | Critical | Local safety controller, watchdog, safe-state fallback; no cloud-only stop |
| Ground/floor failure | High | Ground-bearing review, route survey, distributed loads |
| Maintenance injury | High | Lift points, service locks, isolation and documented procedures |

## Acceptance evidence

A CAD rendering is not evidence of stability. Simulation is not physical validation. A future design must provide its assumptions, input data, mesh quality, load cases, solver settings, test reports, safety analysis and independent sign-off.
