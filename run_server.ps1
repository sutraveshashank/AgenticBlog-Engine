# BlogBoard Automated Server Launcher
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$VenvPython = "$ScriptDir\..\myenv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    Write-Host "🚀 Launching BlogBoard Server & Automation Scheduler..." -ForegroundColor Green
    & $VenvPython blogboard/run.py --serve
} else {
    Write-Host "⚠️ myenv Python not found at $VenvPython. Using system python..." -ForegroundColor Yellow
    python blogboard/run.py --serve
}
