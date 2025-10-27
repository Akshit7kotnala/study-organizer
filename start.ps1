# Quick Start Script for Windows PowerShell
# This script sets up and runs the Study Organizer Flask app

Write-Host "=== Study Organizer - Quick Start ===" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Run the app
Write-Host ""
Write-Host "Starting Flask app..." -ForegroundColor Green
Write-Host "Open your browser to: http://127.0.0.1:5000/" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py
