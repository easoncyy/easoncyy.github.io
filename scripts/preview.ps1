$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$portable = Join-Path $projectRoot '.tools\quarto\bin\quarto.cmd'
if (Test-Path -LiteralPath $portable) { $quartoCommand = $portable }
elseif (Get-Command quarto -ErrorAction SilentlyContinue) { $quartoCommand = 'quarto' }
else { throw 'Please install Quarto: https://quarto.org/docs/download/' }
& $quartoCommand preview --port 4200 --no-browser

