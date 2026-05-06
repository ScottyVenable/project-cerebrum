# Project Cerebrum

<div align="center">
  <img src="https://raw.githubusercontent.com/ScottyVenable/project-cerebrum/main/branding/logo_mockup.png" alt="Project Cerebrum Logo" width="200"/>
  <p><i>The high-performance, ethical, local-first Brain-Computer Interface.</i></p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-violet.svg)](https://opensource.org/licenses/MIT)
  [![Hardware: ADS1299](https://img.shields.io/badge/Hardware-ADS1299-cyan.svg)]()
  [![Platform: Raspberry Pi 5](https://img.shields.io/badge/Platform-RPi%205-blue.svg)]()
</div>

---

## Vision
**Project Cerebrum** is the flagship initiative of **Fathom**, a tech subsidiary of Cadential Studios. We are building a non-invasive, high-fidelity EEG headset from scratch, designed to empower users with direct neural-to-digital control without compromising privacy or financial accessibility.

## Key Features
- **Custom Acquisition:** 24-bit resolution via TI ADS1299 for research-grade signal quality.
- **Edge Processing:** Real-time EEG decoding on Raspberry Pi 5 using optimized EEGNet architectures.
- **Active Shielding:** Custom active-dry electrodes to eliminate noise and cable artifacts.
- **Local-First Ethics:** Your neural data never leaves your device. Period.

## Repository Structure
```text
project-cerebrum/
├── ai_models/        # EEGNet architecture & TFLite export
├── bci_interface/    # ESP32-S3 firmware & LSL sender
├── server/           # Signal processing hub & inference orchestration
├── docs/             # Technical blueprints, research, and SOPs
│   └── research/     # Foundational papers on neuro-engineering
├── branding/         # Visual identity and style guides
├── applications/     # Calibration UIs and control modules
└── tests/            # Automated pipeline validation
```

## Getting Started
Check out the [Development Guide](docs/DEVELOPMENT.md) and [Hardware Build Plan](docs/Hardware_Build_Plan.md) to begin building your own prototype.

## Ethics & Privacy
Fathom stands for **Neural-Self Sovereignty**. Read our full [Ethical Framework](docs/Fathom_Architecture.md) to understand how we protect the sanctuary of your mind.

---
<p align="center">Built by Fathom. Dedicated to the human mind.</p>
