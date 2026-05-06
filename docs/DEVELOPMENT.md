# Project Cerebrum: Development & Integration Guide

This guide details how to build and test the prototype on your Raspberry Pi 5.

## 1. Environment Setup
Run the following on your Raspberry Pi:
```bash
# Install system dependencies
sudo apt update
sudo apt install -y liblsl-dev python3-pip

# Clone/Navigate to the project
cd /sdcard/Coding/project-cerebrum

# Install Python requirements
pip install -r requirements.txt
```

## 2. Running the Prototype (Simulation)
To test the software pipeline without hardware:
1.  **Start the Virtual Headset:**
    ```bash
    python3 bci_interface/sender.py
    ```
2.  **Start the Processing Hub:**
    (In a new terminal)
    ```bash
    python3 server/hub.py
    ```

## 3. Hardware Integration (PiEEG-8)
To connect real hardware:
1.  Ensure the PiEEG HAT is mounted.
2.  Enable SPI on the Raspberry Pi: `sudo raspi-config` -> Interface Options -> SPI -> Enable.
3.  Modify `bci_interface/sender.py` to import and read from the `spidev` or `pieeg` library instead of generating random numbers.

## 4. AI Model Export
If you modify the model architecture in `ai_models/model.py`, re-export the TFLite model:
```bash
python3 ai_models/model.py
```

## 5. Directory Mapping
- `/bci_interface`: Raw data ingestion.
- `/server`: Signal processing and AI inference orchestration.
- `/ai_models`: Model definition and weights.
- `/tests`: Automated validation scripts.
