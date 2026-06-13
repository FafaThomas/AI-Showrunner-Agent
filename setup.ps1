Write-Host "=== AI Showrunner Agent Bootstrap ==="

# Create folders
$folders = @(
    "app",
    "app\agents",
    "app\database",
    "app\services",
    "app\api",
    "app\models",
    "data",
    "notebooks"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created: $folder"
    }
}

# Create Python virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}
else {
    Write-Host ".venv already exists."
}

# Activate venv
$activateScript = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..."
    & $activateScript
}
else {
    Write-Warning "Could not find activation script."
}

$files = @(
    "app\main.py",
    "app\database\schema.sql",
    "app\database\seed.py",
    ".env",
    "README.md"
)

foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
        Write-Host "Created: $file"
    }
}

# Install dependencies
Write-Host "Installing dependencies..."

pip install `
    sqlalchemy `
    pandas `
    faker `
    python-dotenv

# Save requirements
pip freeze > requirements.txt

Write-Host ""
Write-Host "Bootstrap complete!"