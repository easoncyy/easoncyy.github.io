param(
  [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9-]+/[A-Za-z0-9_.-]+$')][string]$Repo,
  [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9_=-]+$')][string]$RepoId,
  [Parameter(Mandatory)][string]$Category,
  [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9_=-]+$')][string]$CategoryId
)
$ErrorActionPreference = 'Stop'
$config = [ordered]@{repo=$Repo; repoId=$RepoId; category=$Category; categoryId=$CategoryId}
$json = $config | ConvertTo-Json -Compress
$destination = Join-Path (Split-Path -Parent $PSScriptRoot) 'assets/comments-config.js'
[System.IO.File]::WriteAllText($destination, "window.SITE_COMMENTS = $json;`n", [System.Text.UTF8Encoding]::new($false))
Write-Host 'Comments configured. Rebuild the site to apply.'

