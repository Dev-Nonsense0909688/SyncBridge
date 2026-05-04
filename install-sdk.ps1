Write-Host "Installing SyncBridge SDK (editable mode)..."

$path = "sdk/python"

if (!(Test-Path $path)) {
    Write-Host "Path not found: $path"
    exit 1
}

pip install -e $path

if ($LASTEXITCODE -eq 0) {
    Write-Host "Installed successfully"
} else {
    Write-Host "Installation failed"
}