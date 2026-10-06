$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$portable = Join-Path $projectRoot '.tools\quarto\bin\quarto.cmd'
if (Test-Path -LiteralPath $portable) { $quartoCommand = $portable }
elseif (Get-Command quarto -ErrorAction SilentlyContinue) { $quartoCommand = 'quarto' }
else { throw 'Please install Quarto: https://quarto.org/docs/download/' }
New-Item -ItemType Directory -Force assets/pdf | Out-Null
& $quartoCommand render documents/math-notes.qmd --to typst
if ($LASTEXITCODE -ne 0) { throw 'PDF render failed.' }
Copy-Item -LiteralPath documents/math-notes.pdf -Destination assets/pdf/math-notes.pdf
& $quartoCommand render
if ($LASTEXITCODE -ne 0) { throw 'Website render failed.' }

