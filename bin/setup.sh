#!/bin/bash

# Project Cerebrum: Automated Setup Script
# Handles independent installation of all system and python dependencies.

echo -e "\033[0;35m--- Project Cerebrum: Dependency Installation ---\033[0m"

# 1. System Dependencies
echo -e "\033[0;36m[1/3] Installing system-level dependencies (requires sudo)...\033[0m"
sudo apt-get update
sudo apt-get install -y cmake build-essential liblsl-dev python3-pip python3-venv python3-tk libqt5gui5

# 2. Python Environment
echo -e "\033[0;36m[2/3] Setting up Python virtual environment...\033[0m"
cd "$(dirname "$0")/.." || exit
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi
source venv/bin/activate

# 3. Python Packages
echo -e "\033[0;36m[3/3] Installing/Updating Python packages...\033[0m"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "\033[0;32m--- Installation Complete ---\033[0m"
echo "You can now run 'cerebrum' to start the program."
