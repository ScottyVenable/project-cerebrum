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

## SOP-005: Project Management & Milestone Tracking
1.  **Issue Management:** All development tasks must be tracked as GitHub Issues with appropriate labels (`hardware`, `ai`, `software`).
2.  **Sub-tasks:** Large issues must contain a task list (checkboxes) to track granular progress.
3.  **Milestones:** All issues must be assigned to a specific Milestone:
    *   **M1: Hardware Foundation:** Focus on ADC and PCB reliability.
    *   **M2: Data & AI Alpha:** Focus on dataset quality and model accuracy.
    *   **M3: System Integration:** Focus on real-time feedback and control.
4.  **Syncing:** Use `./bin/cerebrum.sh` for routine Git operations to ensure local and remote states are consistent.
