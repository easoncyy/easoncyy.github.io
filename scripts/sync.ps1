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
    if ($LASTEXITCODE -ne 0) {
        $rebaseMerge = git rev-parse --git-path rebase-merge
        $rebaseApply = git rev-parse --git-path rebase-apply
        if ((Test-Path -LiteralPath $rebaseMerge) -or (Test-Path -LiteralPath $rebaseApply)) {
            throw 'Resolve the active Git rebase conflict before retrying.'
        }
        Write-Host 'Git fetch transport failed. Trying API; it will stop if histories diverged.'
        python (Join-Path $PSScriptRoot 'push-github-api.py')
        if ($LASTEXITCODE -ne 0) { throw 'Sync failed. Local commits are preserved; see the error above.' }
        Write-Host 'Source committed and pushed through GitHub API.'
        return
    }
    git push origin HEAD:main
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Git transport failed. Trying GitHub Git API with commit hash verification.'
        python (Join-Path $PSScriptRoot 'push-github-api.py')
        if ($LASTEXITCODE -ne 0) { throw 'Git and API push failed. The local commits are preserved; see the error above.' }
    }
    Write-Host 'Source committed and pushed to origin/main.'
}
finally { Pop-Location }
