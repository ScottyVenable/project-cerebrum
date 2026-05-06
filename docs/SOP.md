# Project Cerebrum: Standard Operating Procedures (SOP)

## SOP-001: Server Initialization (Raspberry Pi 5)
1.  **Flash OS:** Install Raspberry Pi OS Lite (64-bit).
2.  **System Updates:** `sudo apt update && sudo apt upgrade -y`.
3.  **LSL Dependencies:** Install `cmake`, `liblsl`, and `pylsl` as detailed in research docs.
4.  **Security:** Disable SSH password login; use SSH keys. Enable UFW with only necessary ports.

## SOP-002: Data Acquisition & Streaming
1.  **Hardware Check:** Ensure PiEEG HAT is seated or Muse is paired via Bluetooth.
2.  **Start LSL Outlet:** Run `bci_interface/sender.py` to begin broadcasting EEG data.
3.  **Verify Stream:** Run `bci_interface/viewer.py` to visualize raw waveforms and check for 50/60Hz line noise.

## SOP-003: AI Model Inference
1.  **Load Model:** Ensure `eegnet_quantized.tflite` is present in `/ai_models`.
2.  **Start Hub:** Execute `server/hub.py` to pull data from LSL and run real-time inference.
3.  **Thresholding:** Adjust confidence thresholds (Default: 0.7) based on user signal quality.

## SOP-004: Ethical Data Management
1.  **Session Logging:** Only store preprocessed features or "Intent Markers," never raw EEG data unless explicitly debugging.
2.  **Encryption:** All stored neural snapshots must be encrypted using AES-256.
3.  **Purge Policy:** Delete temporary session files after 24 hours.
