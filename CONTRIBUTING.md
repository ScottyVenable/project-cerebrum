# Contributing to Project Cerebrum

First off, thank you for considering contributing to Project Cerebrum! It's people like you who will help make ethical, high-performance neurotechnology a reality for everyone.

## Our Philosophy: Neural Sovereignty
Every contribution must align with our core mandate: **Local-First Processing**. We will not accept features that require cloud-based neural data processing or compromise user privacy.

## How Can I Contribute?

### Reporting Bugs
- Use the [GitHub Issue Tracker](https://github.com/ScottyVenable/project-cerebrum/issues).
- Describe the hardware setup (e.g., Pi 5, ESP32-S3 version) and the signal acquisition environment.

### Suggesting Enhancements
- Enhancement suggestions are tracked as GitHub issues.
- Explain the technical rationale and how it improves signal-to-noise ratio (SNR) or reduces latency.

### Pull Requests
1. **Fork the repo** and create your branch from `main`.
2. **Implement automated tests** if adding software or signal processing logic.
3. **Update documentation** if your change affects the hardware build plan or SOPs.
4. **Link the issue** your PR resolves.

## Style Guidelines
- **Python:** Adhere to PEP 8. Use type hints for all signal processing functions.
- **Arduino/C++:** Use CamelCase for functions and snake_case for variables. Comment all SPI register configurations.
- **Documentation:** Use clear, academic tone for research papers and concise, directive tone for SOPs.

## Hardware Contributions
If contributing to the `Hardware_Build_Plan.md`:
- Include KiCad schematics or links to verified PCB designs.
- Specify component tolerances (e.g., 0.1% for biopotential resistors).

---
*By contributing, you agree that your contributions will be licensed under the project's MIT License.*
