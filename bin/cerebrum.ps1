# Project Cerebrum: Management TUI (PowerShell)
# Stylized Git/GitHub orchestration tool.

Function Show-Header {
    Clear-Host
    Write-Host "==================================================" -ForegroundColor Magenta
    Write-Host "          PROJECT CEREBRUM: MANAGEMENT TUI        " -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Magenta
    $branch = git branch --show-current
    Write-Host " Current Branch: $branch"
    Write-Host "--------------------------------------------------" -ForegroundColor Magenta
}

Function Main-Menu {
    Show-Header
    Write-Host "1) " -NoNewline; Write-Host "SYNC " -ForegroundColor Green -NoNewline; Write-Host "(Add, Commit, Push)"
    Write-Host "2) " -NoNewline; Write-Host "PULL " -ForegroundColor Green -NoNewline; Write-Host "(Fetch & Merge)"
    Write-Host "3) " -NoNewline; Write-Host "ISSUES " -ForegroundColor Cyan -NoNewline; Write-Host "(List & Create)"
    Write-Host "4) " -NoNewline; Write-Host "PULL REQUESTS " -ForegroundColor Cyan -NoNewline; Write-Host "(List & Create)"
    Write-Host "5) " -NoNewline; Write-Host "RESEARCH " -ForegroundColor Magenta -NoNewline; Write-Host "(Open Research Docs)"
    Write-Host "q) EXIT"
    Write-Host "--------------------------------------------------" -ForegroundColor Magenta
    
    $choice = Read-Host "Select an option"

    Switch ($choice) {
        "1" { Sync-Repo }
        "2" { git pull origin (git branch --show-current) }
        "3" { Issue-Menu }
        "4" { PR-Menu }
        "5" { Get-ChildItem docs/research/ }
        "q" { Exit }
        Default { Write-Host "Invalid option"; Start-Sleep -s 1; Main-Menu }
    }

    Write-Host "`nPress any key to return to menu..."
    $null = [System.Console]::ReadKey($true)
    Main-Menu
}

Function Sync-Repo {
    Write-Host "Staging changes..." -ForegroundColor Cyan
    git add .
    $msg = Read-Host "Enter commit message"
    git commit -m "$msg"
    Write-Host "Pushing to GitHub..." -ForegroundColor Magenta
    git push origin (git branch --show-current)
}

Function Issue-Menu {
    Show-Header
    Write-Host "Recent Issues:" -ForegroundColor Cyan
    gh issue list --limit 5
    Write-Host "`n1) Create New Issue"
    Write-Host "2) Back"
    $subchoice = Read-Host "Choice"
    if ($subchoice -eq "1") {
        $title = Read-Host "Title"
        $body = Read-Host "Body"
        gh issue create --title "$title" --body "$body"
    }
}

Function PR-Menu {
    Show-Header
    Write-Host "Open Pull Requests:" -ForegroundColor Cyan
    gh pr list
    Write-Host "`n1) Create New PR"
    Write-Host "2) Back"
    $subchoice = Read-Host "Choice"
    if ($subchoice -eq "1") {
        gh pr create --fill
    }
}

# Check for gh cli
if (!(Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "Error: GitHub CLI (gh) is not installed." -ForegroundColor Red
    Exit
}

Main-Menu
