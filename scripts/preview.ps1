$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$portable = Join-Path $projectRoot '.tools\quarto\bin\quarto.cmd'
if (Test-Path -LiteralPath $portable) { $quartoCommand = $portable }
elseif (Get-Command quarto -ErrorAction SilentlyContinue) { $quartoCommand = 'quarto' }
else { throw 'Please install Quarto: https://quarto.org/docs/download/' }
python scripts/render-log.py
if ($LASTEXITCODE -ne 0) { throw 'Log generation failed.' }
python scripts/render-library.py
if ($LASTEXITCODE -ne 0) { throw 'Library generation failed.' }
& $quartoCommand preview --port 4200 --no-browser

