param([string]$Message = 'Update personal website')

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required.' }
    $branch = git branch --show-current
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') { throw 'Switch to main before syncing.' }
    git rev-parse --verify HEAD | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Initialize local history from origin/main first.' }
    git add --all
    if ($LASTEXITCODE -ne 0) { throw 'Git staging failed.' }
    git diff --cached --quiet
    $changeStatus = $LASTEXITCODE
    if ($changeStatus -eq 1) {
        git commit -m $Message
        if ($LASTEXITCODE -ne 0) { throw 'Git commit failed.' }
    }
    elseif ($changeStatus -ne 0) { throw 'Unable to inspect staged changes.' }
    else { Write-Host 'No new changes to commit.' }
    git pull --rebase origin main
    if ($LASTEXITCODE -ne 0) { throw 'Sync stopped. Resolve the reported Git conflict or network error before retrying.' }
    git push origin HEAD:main
    if ($LASTEXITCODE -ne 0) { throw 'Git push failed. The local commit is preserved; retry after resolving the error.' }
    Write-Host 'Source committed and pushed to origin/main.'
}
finally { Pop-Location }
