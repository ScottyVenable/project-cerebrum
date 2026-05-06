#!/bin/bash

# Project Cerebrum: Automated BCI Workflow
# Transition from Data Collection -> AI Training -> Inference Deployment

echo "--- Project Cerebrum: Integrated Workflow ---"

# 1. Calibration
echo "[1/3] Launching Calibration UI..."
python3 applications/calibration_ui.py

# 2. Training
echo "[2/3] Data collection complete. Initiating EEGNet training..."
# Note: This expects the user to have finished the session and saved data.
python3 ai_models/train.py

# 3. Deployment
echo "[3/3] Model trained and quantized. Ready for deployment."
echo "Launch the RealTime Hub with: python3 server/hub.py"

echo "--- Workflow Sequence Finished ---"
