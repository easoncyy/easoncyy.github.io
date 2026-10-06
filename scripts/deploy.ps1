param([switch]$RebuildPdf)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    foreach ($commandName in @('python', 'gh')) {
        if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
            throw "Missing command: $commandName. Install it and reopen PowerShell."
        }
    }
    gh auth status
    if ($LASTEXITCODE -ne 0) { throw 'GitHub login required. Run: gh auth login' }
    & (Join-Path $PSScriptRoot 'build.ps1') -SkipPdf:(-not $RebuildPdf)
    python scripts/publish-github.py
    if ($LASTEXITCODE -ne 0) { throw 'Publish failed. See the GitHub API error above.' }
    Write-Host 'Update submitted: https://easoncyy.github.io/'
    Write-Host 'GitHub Pages needs a short time to deploy. Status: https://github.com/easoncyy/easoncyy.github.io/actions'
}
finally {
    Pop-Location
}
