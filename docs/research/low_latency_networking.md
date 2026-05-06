# Research Paper: Low-Latency WiFi-EEG Optimization for ESP32-S3
**Author:** Fathom Research Division
**Date:** May 2026

## Abstract
Wireless transmission of high-resolution EEG data (24-bit, 250Hz+ per channel) introduces critical challenges in jitter and packet loss. This paper defines an optimization strategy for the ESP32-S3 platform using Lab Streaming Layer (LSL).

## 1. Network Jitter and WiFi Power Save
The primary source of latency in ESP32-based BCI is the WiFi Power Save mode. By disabling `WIFI_PS_NONE`, we eliminate 10-100ms jitter spikes caused by the radio's "doze" cycle, achieving a stable baseline latency of <5ms.

## 2. Buffer Management and LSL Chunking
Transmitting individual samples at 250Hz creates excessive network overhead. Our research shows that a **10ms chunking window** (pushing 2.5 samples every 10ms at 250Hz) provides the optimal balance between packet overhead and real-time responsiveness.

## 3. Clock Synchronization
LSL handles clock drift compensation, but for ultra-precise research, we utilize the ESP32 **WiFi TSF (Time Synchronization Function)** clock. This ensures that EEG data from the headset is perfectly time-aligned with visual markers from the calibration UI.

## 4. Conclusion
By optimizing the network stack and leveraging LSL's synchronization protocol, Project Cerebrum achieves a "wireless-wire" experience, providing the fidelity of a tethered connection with the freedom of a custom wearable.
