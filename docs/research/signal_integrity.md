# Research Paper: Signal Integrity in Discrete EEG Acquisition
**Author:** Fathom Research Division
**Date:** May 2026

## Abstract
This paper investigates the critical requirements for maintaining microvolt-level signal integrity in custom-built, non-invasive EEG systems. We analyze the intersection of high-impedance dry contact, common-mode interference, and the implementation of active-buffer electrodes paired with the ADS1299 architecture.

## 1. The Impedance Bottleneck
The primary challenge in dry-electrode EEG is the skin-electrode interface impedance, which frequently exceeds 500 kΩ. Traditional passive systems suffer from significant signal attenuation and cable-motion artifacts due to the high-impedance current loop.

## 2. Active Buffering (Voltage Following)
We propose a per-channel OPA333-based voltage follower at the electrode site. This architecture achieves:
- **Impedance Transformation:** Converting >1 GΩ input impedance to <100 Ω output impedance.
- **Noise Immunity:** Low-impedance signals are significantly more resistant to environmental electromagnetic interference (EMI) during transmission to the ADC.

## 3. Active Common-Mode Rejection (DRL)
Utilizing the ADS1299 internal BIAS amplifier, we implement a Driven Right Leg (DRL) circuit. By feeding back the inverted common-mode signal into the user's body, we achieve a theoretical Common-Mode Rejection Ratio (CMRR) enhancement of >20dB over passive grounding.

## 4. Conclusion
The Cerebrum-V1 architecture provides a research-grade path for DIY neurotechnology, effectively bridging the gap between consumer accessibility and high-fidelity biopotential measurement.
