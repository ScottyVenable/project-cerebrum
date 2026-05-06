# Project Cerebrum: Master Plan & Research Blueprint

## 1. Executive Summary
Project Cerebrum is a non-invasive Brain-Computer Interface (BCI) designed for high-performance, affordable, and local neural processing. Utilizing a Raspberry Pi 5 as the central hub, the project aims to translate raw EEG signals into actionable digital commands using lightweight convolutional neural networks (EEGNet).

## 2. Hardware & Materials Blueprint
Based on 2024-2025 availability, the following hardware stack is recommended for the initial prototype:

### Primary Choice: PiEEG-8
*   **Type:** Raspberry Pi HAT (SPI Interface).
*   **Channels:** 8 channels.
*   **Cost:** ~$180.
*   **Advantage:** Direct GPIO connection eliminates Bluetooth latency and packet loss.

### Secondary Choice (Portable): Muse 2
*   **Channels:** 4 channels (Dry electrodes).
*   **Cost:** ~$250.
*   **Interface:** Bluetooth LE (requires `muse-lsl` or `BrainFlow`).

### Auxiliary Components
*   **Computing:** Raspberry Pi 5 (8GB RAM) + Active Cooler.
*   **Electrodes:** Ag/AgCl wet electrodes for high SNR (if using PiEEG) or dry-comb electrodes for hair-area signals.

## 3. Server & Architecture Setup
The Raspberry Pi functions as an "Edge Neuro-Processor."

### Data Pipeline (LSL)
*   **Ingestion:** Lab Streaming Layer (LSL) is used to handle multi-stream synchronization (EEG, timestamps, marker events).
*   **Buffering:** A sliding window buffer (2 seconds of data, updated every 100ms).

### Real-time Logic
1.  **Headset Driver:** Communicates via SPI (PiEEG) or BLE (Muse) to push samples to an LSL outlet.
2.  **Processing Hub:** A Python service pulls from the LSL inlet, applies bandpass filtering (1-40Hz), and normalizes data.

## 4. AI & Data Pipeline
### Model: EEGNet (Optimized)
A compact Convolutional Neural Network (CNN) specifically designed for EEG.
*   **Architecture:** Uses Depthwise and Separable Convolutions to reduce parameters while capturing spatial and temporal features.
*   **Deployment:** Converted to **TensorFlow Lite (TFLite)** with integer quantization for <5ms inference on Pi 5.

### Training Strategy
*   **Initial Training:** Utilize open datasets (e.g., BCI Competition IV, PhysioNet) for pre-training.
*   **Transfer Learning:** Fine-tune the model on the user's specific neural patterns locally on the Pi.

## 5. Scientific & Ethical Context
### Limitations
*   **SNR:** Non-invasive signals are heavily attenuated by the skull.
*   **Artifacts:** Eye blinks and jaw clenches produce signals 10-100x stronger than neural activity.

### Ethical Mandate
*   **Neural Sovereignty:** Raw neural data must NEVER leave the local device in unencrypted or raw form.
*   **Informed Agency:** The system must provide transparent feedback when an intent is predicted to prevent "algorithmic drift" of the user's will.
