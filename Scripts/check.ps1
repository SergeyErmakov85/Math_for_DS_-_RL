#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Запускает все проверки уровня 1 фреймворка ENF.

.DESCRIPTION
    Прогоняет пять проверок и печатает сводку. Ненулевой код возврата
    означает нарушения уровня «Обязательно» и должен останавливать сборку.

    Коды возврата:
      0 — нарушений нет
      1 — найдены нарушения
      2 — ошибка запуска (нет Node.js, неверный путь)

.PARAMETER Path
    Каталог или файл для проверки. По умолчанию — весь репозиторий.

.PARAMETER SkipPalette
    Пропустить проверку палитры. Имеет смысл при частых прогонах:
    палитра меняется редко, а проверка занимает заметное время.

.EXAMPLE
    pwsh Scripts/check.ps1 Examples/
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Path = '.',

    [switch]$SkipPalette
)

$ErrorActionPreference = 'Stop'
$scriptDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $scriptDir

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host 'Не найден Node.js. Установите: winget install OpenJS.NodeJS.LTS' -ForegroundColor Red
    exit 2
}

$target = Resolve-Path -Path $Path -ErrorAction SilentlyContinue
if (-not $target) {
    Write-Host "Путь не найден: $Path" -ForegroundColor Red
    exit 2
}

Push-Location $repoRoot
try {
    Write-Host ''
    Write-Host "Проверка ENF · $($target.Path)" -ForegroundColor Cyan
    Write-Host ('-' * 60)

    $checks = @(
        @{ Name = 'frontmatter'; Script = 'check-frontmatter.mjs'; Args = @($target.Path) },
        @{ Name = 'links';       Script = 'check-links.mjs';       Args = @($target.Path) },
        @{ Name = 'colors';      Script = 'check-colors.mjs';      Args = @($target.Path) },
        @{ Name = 'alt';         Script = 'check-alt.mjs';         Args = @($target.Path) },
        @{ Name = 'structure';   Script = 'check-structure.mjs';   Args = @($target.Path) }
    )

    if (-not $SkipPalette) {
        $checks += @{ Name = 'palette'; Script = 'check-contrast.mjs'; Args = @() }
    }

    $failed = @()

    foreach ($check in $checks) {
        $scriptPath = Join-Path $scriptDir $check.Script
        if (-not (Test-Path $scriptPath)) {
            Write-Host "  пропущено: нет файла $($check.Script)" -ForegroundColor DarkYellow
            continue
        }

        if ($check.Name -eq 'palette') {
            # Палитра проверяется целиком и печатает собственный подробный отчёт,
            # поэтому её вывод сворачиваем до итоговой строки.
            $out = & node $scriptPath 2>&1
            if ($LASTEXITCODE -ne 0) {
                $failed += $check.Name
                Write-Host 'палитра                  нарушения:' -ForegroundColor Red
                $out | Where-Object { $_ -match 'FAIL|·' } | ForEach-Object { Write-Host "  $_" }
            }
            else {
                Write-Host 'палитра                  OK'
            }
            continue
        }

        & node $scriptPath @($check.Args)
        if ($LASTEXITCODE -ne 0) { $failed += $check.Name }
    }

    Write-Host ('-' * 60)

    if ($failed.Count -gt 0) {
        Write-Host "Проверки не пройдены: $($failed -join ', ')" -ForegroundColor Red
        Write-Host 'Материал не принимается до устранения нарушений.' -ForegroundColor Red
        exit 1
    }

    Write-Host 'Все проверки уровня 1 пройдены.' -ForegroundColor Green
    Write-Host 'Уровень 2 — ревью по docs/Codex/Review_Checklist.md — выполняется отдельно.'
    exit 0
}
finally {
    Pop-Location
}
