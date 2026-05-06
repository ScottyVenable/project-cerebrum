#!/bin/bash

# Project Cerebrum: Management TUI (Bash)
# Stylized Git/GitHub orchestration tool.

# Colors
CYAN='\033[0;36m'
VIOLET='\033[0;35m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Header
show_header() {
    clear
    echo -e "${VIOLET}==================================================${NC}"
    echo -e "${CYAN}          PROJECT CEREBRUM: MANAGEMENT TUI        ${NC}"
    echo -e "${VIOLET}==================================================${NC}"
    echo -e " Current Branch: $(git branch --show-current)"
    echo -e " GitHub Repo: $(gh repo view --json url -q .url)"
    echo -e "${VIOLET}--------------------------------------------------${NC}"
}

# Menu
main_menu() {
    show_header
    echo -e "1) ${GREEN}SYNC${NC} (Add, Commit, Push)"
    echo -e "2) ${GREEN}PULL${NC} (Fetch & Merge)"
    echo -e "3) ${CYAN}ISSUES${NC} (List & Create)"
    echo -e "4) ${CYAN}PULL REQUESTS${NC} (List & Create)"
    echo -e "5) ${VIOLET}RESEARCH${NC} (Open Research Docs)"
    echo -e "q) EXIT"
    echo -e "${VIOLET}--------------------------------------------------${NC}"
    read -p "Select an option: " choice

    case $choice in
        1) sync_repo ;;
        2) git pull origin $(git branch --show-current) ;;
        3) issue_menu ;;
        4) pr_menu ;;
        5) ls docs/research/ ;;
        q) exit 0 ;;
        *) echo "Invalid option"; sleep 1; main_menu ;;
    esac
    
    echo -e "\nPress any key to return to menu..."
    read -n 1
    main_menu
}

sync_repo() {
    echo -e "${CYAN}Staging changes...${NC}"
    git add .
    read -p "Enter commit message: " msg
    git commit -m "$msg"
    echo -e "${VIOLET}Pushing to GitHub...${NC}"
    git push origin $(git branch --show-current)
}

issue_menu() {
    show_header
    echo -e "${CYAN}Recent Issues:${NC}"
    gh issue list --limit 5
    echo -e "\n1) Create New Issue"
    echo -e "2) Back"
    read -p "Choice: " subchoice
    if [ "$subchoice" == "1" ]; then
        read -p "Title: " title
        read -p "Body: " body
        gh issue create --title "$title" --body "$body"
    fi
}

pr_menu() {
    show_header
    echo -e "${CYAN}Open Pull Requests:${NC}"
    gh pr list
    echo -e "\n1) Create New PR"
    echo -e "2) Back"
    read -p "Choice: " subchoice
    if [ "$subchoice" == "1" ]; then
        gh pr create --fill
    fi
}

# Start
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    exit 1
fi

main_menu
