# Project Cerebrum: Noise Mitigation & Signal Integrity Guide

## 1. Advanced Grounding: The BIAS/DRL Circuit
To achieve research-grade signals on a custom board, we must implement an active **Driven Right Leg (DRL)** circuit using the ADS1299 internal BIAS amplifier.

### Hardware Configuration
*   **Feedback Network:** 392 kΩ resistor in parallel with a 10 nF capacitor.
*   **Safety Isolation:** A 22 kΩ resistor must be in series with the BIAS electrode (earlobe/mastoid).
*   **Electrode Selection:** In the `BIAS_SENS` registers, select all 8 channels (P and N) to contribute to the common-mode sense. This allows the system to effectively "null out" the 50/60Hz hum from your body.

## 2. Shielding & PCB Design
*   **Faraday Cage:** Enclose the ADS1299 and analog front-end in a small copper-tape or CNC-machined aluminum shield soldered to DGND.
*   **Active Shielding:** Use the output of the OPA333 buffers to drive the shield of the coaxial cables leading to each electrode. This eliminates cable-microphonics and parasitic capacitance.
*   **Star Grounding:** Ensure all AGND and DGND planes meet at a single point near the battery input to prevent ground loops.

## 3. Power Isolation
*   **Battery Power:** Use a high-quality 3.7V LiPo battery. 
*   **LDO Selection:** Use an ultra-low-noise LDO (e.g., LT1763) for the AVDD (Analog 3.3V) supply.
*   **Isolation Gap:** Maintain a 2mm physical gap on the PCB between the analog traces and the high-frequency ESP32 digital traces.
