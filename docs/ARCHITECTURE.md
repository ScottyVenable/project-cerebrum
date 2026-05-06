# Software Architecture Document (SAD)

## 1. System Overview
Project Cerebrum is a distributed BCI system utilizing a **Microservices-on-Edge** pattern. It separates data acquisition, signal processing, and user interaction into discrete, networked layers.

## 2. Component Diagram
```mermaid
graph LR
    subgraph Headset (ESP32-S3)
        A[ADS1299] --> B[LSL Outlet]
    end
    subgraph Hub (Raspberry Pi 5)
        B -- WiFi --> C[LSL Inlet]
        C --> D[DSP Service]
        D --> E[Inference Engine]
        E --> F[Command Bus]
    end
    subgraph Interaction
        G[Web Dashboard] -- WebSocket --> C
        H[TUI] -- Git/CLI --> Hub
    end
```

## 3. Data Flow Architecture
1.  **Acquisition Layer:** Raw 24-bit data is sampled at 250Hz. ESP32 performs no DSP, ensuring maximum throughput for the LSL stream.
2.  **Transport Layer:** Lab Streaming Layer (LSL) provides sub-millisecond clock synchronization and network transparency.
3.  **Processing Layer (The Hub):** 
    - **Temporal:** 4th-order Butterworth bandpass (1-40Hz).
    - **Spatial:** Common Spatial Patterns (CSP) for feature extraction.
4.  **Inference Layer:** TFLite-quantized EEGNet model performs classification in <4ms.

## 4. Security & Privacy (The Neural Firewall)
- **Air-Gap Preference:** System is designed to operate on a local subnet without WAN access.
- **In-Memory DSP:** Signal processing occurs in volatile memory; raw EEG is never written to disk during live operation.
- **Encryption:** (Proposed) AES-256 encryption for session data persistence.

## 5. Scalability
The architecture supports multi-subject LSL streams, allowing for synchronous multi-user BCI research ("Brain-to-Brain" interfacing experiments).
