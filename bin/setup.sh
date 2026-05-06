#!/bin/bash

# Project Cerebrum: Automated Setup Script
# Use this on a clean Raspberry Pi 5 installation.

echo "--- Project Cerebrum: System Setup ---"

# 1. System Dependencies
echo "[1/4] Installing system dependencies..."
sudo apt update
sudo apt install -y cmake build-essential liblsl-dev python3-pip python3-venv

# 2. Virtual Environment
echo "[2/4] Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Python Packages
echo "[3/4] Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Final Verification
echo "[4/4] Verifying installation..."
python3 -c "import pylsl; print('LSL Version:', pylsl.library_version())"
python3 -c "import numpy; print('Numpy Version:', numpy.__version__)"

echo "--- Setup Complete ---"
echo "Run 'source venv/bin/activate' to start."
