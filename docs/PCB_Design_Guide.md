# Project Cerebrum: PCB Design & Routing Guide

This guide defines the professional standards for the Cerebrum-V1 acquisition board.

## 1. Stackup & Grounding
- **4-Layer Stackup Recommended:** 
  1. Signal / Analog Front-End (AFE)
  2. Ground Plane (Solid AGND/DGND)
  3. Power Plane (Isolated 3.3V)
  4. Digital Signals / ESP32-S3
- **Star Grounding:** Tie Analog Ground (AGND) and Digital Ground (DGND) at a single point near the battery input to prevent digital return currents from polluting the neural signal.

## 2. Analog Front-End (AFE) Routing
- **Differential Pairs:** Route electrode inputs as differential pairs where possible to maximize Common-Mode Rejection.
- **Guard Rings:** Place guard traces around high-impedance inputs (the traces from electrodes to the ADS1299). Connect these guards to the internal BIAS/RLD reference.
- **Trace Width:** Use 6-8 mil traces for analog signals to minimize parasitic capacitance.

## 3. Active Shielding
- The output of the active electrode buffers must drive the shield of the coaxial cables. On the PCB, ensure the "Shield" net is kept separate from the main Ground plane to prevent noise injection.

## 4. Power Integrity
- **Decoupling:** Place 0.1uF and 10uF ceramic capacitors as close as possible to the ADS1299 AVDD and DVDD pins.
- **LDO Placement:** The LT1763 ultra-low noise LDO should be physically distant from the ESP32-S3 antenna to prevent RF interference from entering the analog power rail.

## 5. Mechanical Constraints
- Ensure M3 mounting holes are isolated from signal planes.
- PCB dimensions should not exceed 50x50mm to fit within the 3D-printed headset enclosure.
