# Project Cerebrum: Stylized Launcher (PowerShell)
# Centralized command hub for all BCI operations.

Function Show-Header {
    Clear-Host
    Write-Host "==================================================" -ForegroundColor Magenta
    Write-Host "          PROJECT CEREBRUM: COMMAND HUB           " -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Magenta
}

Function Main-Menu {
    Show-Header
    Write-Host "1) " -NoNewline; Write-Host "RUN HUB " -ForegroundColor Green -NoNewline; Write-Host "(PyQtGraph UI)"
    Write-Host "2) " -NoNewline; Write-Host "WEB DASHBOARD " -ForegroundColor Green -NoNewline; Write-Host "(FastAPI/WebSocket)"
    Write-Host "3) " -NoNewline; Write-Host "CALIBRATE & TRAIN " -ForegroundColor Cyan -NoNewline; Write-Host "(Workflow)"
    Write-Host "4) " -NoNewline; Write-Host "OFFLINE ANALYSIS " -ForegroundColor Cyan -NoNewline; Write-Host "(MNE/CSP)"
    Write-Host "5) " -NoNewline; Write-Host "SYSTEM MONITOR " -ForegroundColor Magenta -NoNewline; Write-Host "(Neural Ledger)"
    Write-Host "6) " -NoNewline; Write-Host "CONFIGURATION " -ForegroundColor Magenta -NoNewline; Write-Host "(Settings)"
    Write-Host "7) " -NoNewline; Write-Host "INSTALL DEPENDENCIES " -ForegroundColor Green
    Write-Host "8) " -NoNewline; Write-Host "VIEW LOGS " -ForegroundColor Red
    Write-Host "9) " -NoNewline; Write-Host "DEBUG MODE " -ForegroundColor Red -NoNewline; Write-Host "(LSL Test)"
    Write-Host "q) EXIT"
    Write-Host "--------------------------------------------------" -ForegroundColor Magenta
    
    $choice = Read-Host "Select an operation"

    Switch ($choice) {
        "1" { python server/hub.py }
        "2" { uvicorn server.web_dashboard:app --host 0.0.0.0 --port 8000 }
        "3" { .\bin\calibrate_and_train.sh }
        "4" { $path = Read-Host "Enter XDF path"; python ai_models/offline_analysis.py $path }
        "5" { python -c "import sqlite3; conn=sqlite3.connect('docs/research/neural_ledger.db'); c=conn.cursor(); c.execute('SELECT * FROM sessions ORDER BY id DESC LIMIT 5'); print('\nRecent Sessions:'); [print(r) for r in c.fetchall()]; conn.close()" }
        "6" { notepad config/settings.json }
        "7" { pip install -r requirements.txt }
        "8" { Get-Content -Tail 50 /root/.bridge.log }
        "9" { Start-Process python "bci_interface/sender.py"; Start-Sleep -s 2; python -c "from pylsl import resolve_stream; print('LSL Streams:', resolve_stream())"; Stop-Process -Name python -Force }
        "q" { Exit }
        Default { Write-Host "Invalid choice"; Start-Sleep -s 1; Main-Menu }
    }

    Write-Host "`nPress any key to return to Command Hub..."
    $null = [System.Console]::ReadKey($true)
    Main-Menu
}

# Start
Main-Menu
