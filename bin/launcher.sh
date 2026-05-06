#!/bin/bash

# Project Cerebrum: Stylized Launcher (Bash)
# Centralized command hub for all BCI operations.

# Colors
CYAN='\033[0;36m'
VIOLET='\033[0;35m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

show_header() {
    clear
    echo -e "${VIOLET}==================================================${NC}"
    echo -e "${CYAN}          PROJECT CEREBRUM: COMMAND HUB           ${NC}"
    echo -e "${VIOLET}==================================================${NC}"
}

main_menu() {
    show_header
    echo -e "1) ${GREEN}RUN HUB${NC} (PyQtGraph UI)"
    echo -e "2) ${GREEN}WEB DASHBOARD${NC} (FastAPI/WebSocket)"
    echo -e "3) ${CYAN}CALIBRATE & TRAIN${NC} (Workflow)"
    echo -e "4) ${CYAN}OFFLINE ANALYSIS${NC} (MNE/CSP)"
    echo -e "5) ${VIOLET}SYSTEM MONITOR${NC} (Neural Ledger)"
    echo -e "6) ${VIOLET}CONFIGURATION${NC} (Settings)"
    echo -e "7) ${RED}VIEW LOGS${NC}"
    echo -e "8) ${RED}DEBUG MODE${NC} (LSL Test)"
    echo -e "q) EXIT"
    echo -e "${VIOLET}--------------------------------------------------${NC}"
    read -p "Select an operation: " choice

    case $choice in
        1) python3 server/hub.py ;;
        2) uvicorn server.web_dashboard:app --host 0.0.0.0 --port 8000 ;;
        3) ./bin/calibrate_and_train.sh ;;
        4) read -p "Enter XDF path: " path; python3 ai_models/offline_analysis.py "$path" ;;
        5) python3 -c "import sqlite3; conn=sqlite3.connect('docs/research/neural_ledger.db'); c=conn.cursor(); c.execute('SELECT * FROM sessions ORDER BY id DESC LIMIT 5'); print('\nRecent Sessions:'); [print(r) for r in c.fetchall()]; conn.close()" ;;
        6) nano config/settings.json ;;
        7) tail -n 50 /root/.bridge.log ;;
        8) python3 bci_interface/sender.py & sleep 2; python3 -c "from pylsl import resolve_stream; print('LSL Streams:', resolve_stream())"; pkill -f sender.py ;;
        q) exit 0 ;;
        *) echo "Invalid choice"; sleep 1; main_menu ;;
    esac

    echo -e "\nPress any key to return to Command Hub..."
    read -n 1
    main_menu
}

# Start
main_menu
