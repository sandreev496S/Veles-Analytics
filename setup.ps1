$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Python = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else { "python" }
$VenvDir = if ($env:VENV_DIR) { $env:VENV_DIR } else { ".venv" }

try {
    & $Python --version | Out-Host
} catch {
    throw "Python was not found. Install Python 3.12, then run this script again."
}

if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating virtual environment in $VenvDir..."
    & $Python -m venv $VenvDir
}

$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    throw "Virtual environment Python was not created at $VenvPython"
}

& $VenvPython -m pip install --upgrade pip setuptools wheel
& $VenvPython -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
    } else {
        "APP_MODE=demo" | Set-Content ".env"
    }
    Write-Host "Created .env in demo mode."
}

& $VenvPython scripts/check_environment.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Starting Veles at http://localhost:8501"
& $VenvPython -m streamlit run app.py --server.address=localhost --server.port=8501
