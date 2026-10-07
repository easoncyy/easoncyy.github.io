param([switch]$RebuildPdf, [string]$Message = 'Update personal website')

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    foreach ($commandName in @('python', 'gh')) {
        if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
            throw "Missing command: $commandName. Install it and reopen PowerShell."
        }
    }
    python scripts/check-github.py
    if ($LASTEXITCODE -ne 0) { throw 'GitHub access check failed. See the specific network, credential or permission error above.' }
    & (Join-Path $PSScriptRoot 'build.ps1') -SkipPdf:(-not $RebuildPdf)
    & (Join-Path $PSScriptRoot 'sync.ps1') -Message $Message
    python scripts/publish-github.py
    if ($LASTEXITCODE -ne 0) { throw 'Publish failed. See the GitHub API error above.' }
    Write-Host 'Update submitted: https://easoncyy.github.io/'
    Write-Host 'GitHub Pages needs a short time to deploy. Status: https://github.com/easoncyy/easoncyy.github.io/actions'
}
finally {
    Pop-Location
}
