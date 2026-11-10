$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== CodeIt 2.0 setup ===" -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found. Install Python 3.11 or newer."
}
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    throw "Ollama was not found. Install Ollama for Windows, then reopen PowerShell."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.15 -m venv .venv
        if ($LASTEXITCODE -ne 0) { py -3 -m venv .venv }
    } else {
        python -m venv .venv
    }
}

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Could not upgrade pip." }
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Could not install CodeIt dependencies." }

Write-Host "Checking existing Ollama models..." -ForegroundColor Cyan
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 5 | Out-Null
} catch {
    Write-Host "Ollama is not running yet. Start the Ollama desktop app before using CodeIt." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Dependencies installed. Existing Ollama models and codeit.db were not deleted." -ForegroundColor Green
Write-Host "Next: configure .streamlit\secrets.toml using secrets.toml.example." -ForegroundColor Yellow
Write-Host "Run .\start_codeit.ps1 to launch CodeIt." -ForegroundColor Green
