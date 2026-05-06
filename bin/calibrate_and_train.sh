#!/bin/bash

# Project Cerebrum: Automated BCI Workflow
# Transition from Data Collection -> AI Training -> Inference Deployment

echo "--- Project Cerebrum: Integrated Workflow ---"

# 1. Calibration
echo "[1/4] Launching Calibration UI..."
python3 applications/calibration_ui.py
# Log the session metadata (using placeholder for automation)
python3 -c "from server.session_manager import SessionManager; SessionManager().log_session('Motor Imagery', 80, 'data/latest.xdf')"

# 2. Training
echo "[2/4] Initiating EEGNet training..."
python3 ai_models/train.py

# 3. Log Model Results
echo "[3/4] Logging model performance to Neural Ledger..."
# In production, this would pull the actual accuracy from train.py
python3 -c "from server.session_manager import SessionManager; SessionManager().log_model(0.85, 'ai_models/cerebrum_v1.h5', 1)"

# 4. Deployment
echo "[4/4] Model ready."
echo "Launch the RealTime Hub with: python3 server/hub.py"

echo "--- Workflow Sequence Finished ---"
