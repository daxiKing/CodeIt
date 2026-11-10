$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "CodeIt environment is missing. Run .\setup_codeit.ps1 first."
}
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    throw "Ollama is not installed or not on PATH."
}

try {
    Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 8 | Out-Null
    Write-Host "Ollama connected." -ForegroundColor Green
} catch {
    Write-Host "Ollama is not responding. Start the Ollama desktop app, then retry." -ForegroundColor Red
    exit 1
}

Write-Host "Starting CodeIt 2.0 at http://localhost:8501 ..." -ForegroundColor Cyan
& $python -m streamlit run (Join-Path $PSScriptRoot "app.py")
