# Research Paper: Advanced SMR Decoding Architectures
**Author:** Fathom Research Division
**Date:** May 2026

## Abstract
Decoding Sensorimotor Rhythms (SMR) for Motor Imagery (MI) BCI is moving beyond traditional Linear Discriminant Analysis (LDA). This paper explores the transition to Hybrid Deep Learning architectures and their deployment on edge hardware.

## 1. Beyond Common Spatial Patterns (CSP)
While CSP is the benchmark for spatial filtering, it is sensitive to noise and non-stationary EEG signals. 2024-2025 research suggests that **EEGNet** (Lawhern et al.) provides superior robustness by using depthwise and separable convolutions to capture both temporal and spatial features simultaneously.

## 2. Hybrid Architectures: CNN-Transformers
Emerging architectures combine Convolutional Neural Networks (CNN) for local feature extraction with **Transformers** for long-range temporal dependency tracking. This allows the system to recognize neural "states" across longer windows (e.g., 4-8 seconds) without losing the resolution of transient Event-Related Desynchronization (ERD) triggers.

## 3. Edge Optimization: TFLite & Quantization
For local-first BCI, the model must run on ARM-based hardware (Raspberry Pi 5). We implement **Integer Quantization**, converting 32-bit floats to 8-bit integers. 
- **Latency Impact:** Reduction from ~15ms to <4ms per inference.
- **Accuracy impact:** <1% degradation in SMR classification accuracy.

## 4. Conclusion
The Cerebrum model suite prioritizes low-latency, high-accuracy decoders that can adapt to the user's specific neural signatures in real-time, enabling seamless human-machine integration.
