#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Конвертирует библиотеку SVG в PDF для вставки в собираемый PDF.

.DESCRIPTION
    LaTeX не вставляет SVG напрямую, поэтому для качественной иллюстрации
    в PDF нужна векторная копия в формате PDF. Скрипт находит доступный
    конвертер и создаёт такие копии рядом с исходниками.

    Без конвертера сборка PDF не ломается: фильтр Build/filters/enf-svg.lua
    подставит вместо иллюстрации рамку с её текстовым описанием. Это
    сознательная деградация, а не молчаливая потеря — предупреждение
    печатается на каждую пропущенную иллюстрацию.

    Поддерживаемые конвертеры, в порядке предпочтения:
      rsvg-convert  — librsvg, самый быстрый и точный для наших файлов
      inkscape      — тяжелее, но обычно уже установлен у иллюстраторов

.PARAMETER Path
    Каталог с SVG. По умолчанию SVG/.

.PARAMETER Force
    Пересоздавать PDF, даже если он новее исходника.

.EXAMPLE
    pwsh Scripts/convert-svg.ps1
#>

[CmdletBinding()]
param(
    [string]$Path = 'SVG',
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

Push-Location $repoRoot
try {
    $target = Resolve-Path -Path $Path -ErrorAction SilentlyContinue
    if (-not $target) {
        Write-Host "Каталог не найден: $Path" -ForegroundColor Red
        exit 2
    }

    $rsvg = Get-Command rsvg-convert -ErrorAction SilentlyContinue
    $inkscape = Get-Command inkscape -ErrorAction SilentlyContinue

    if (-not $rsvg -and -not $inkscape) {
        Write-Host 'Конвертер SVG не найден.' -ForegroundColor Yellow
        Write-Host ''
        Write-Host 'Установите один из вариантов:'
        Write-Host '  rsvg-convert — входит в librsvg; на Windows проще всего через MSYS2 или Chocolatey'
        Write-Host '  inkscape     — winget install Inkscape.Inkscape'
        Write-Host ''
        Write-Host 'Без конвертера PDF соберётся, но вместо иллюстраций будут рамки'
        Write-Host 'с их текстовыми описаниями. Остальные четыре формата не затронуты.'
        exit 2
    }

    $tool = if ($rsvg) { 'rsvg-convert' } else { 'inkscape' }
    Write-Host "Конвертер: $tool" -ForegroundColor Cyan

    $files = Get-ChildItem -Path $target -Filter '*.svg' -Recurse
    $converted = 0
    $skipped = 0
    $failed = @()

    foreach ($file in $files) {
        $out = [System.IO.Path]::ChangeExtension($file.FullName, '.pdf')

        if ((-not $Force) -and (Test-Path $out) -and ((Get-Item $out).LastWriteTime -gt $file.LastWriteTime)) {
            $skipped++
            continue
        }

        if ($rsvg) {
            & rsvg-convert --format=pdf --output=$out $file.FullName 2>&1 | Out-Null
        }
        else {
            & inkscape $file.FullName --export-type=pdf --export-filename=$out 2>&1 | Out-Null
        }

        if ($LASTEXITCODE -eq 0 -and (Test-Path $out)) {
            $converted++
            Write-Host ("  OK   {0}" -f (Resolve-Path -Relative $out))
        }
        else {
            $failed += $file.Name
            Write-Host ("  СБОЙ {0}" -f $file.Name) -ForegroundColor Red
        }
    }

    Write-Host ''
    Write-Host ("Конвертировано: {0}, пропущено как актуальные: {1}" -f $converted, $skipped)

    if ($failed.Count -gt 0) {
        Write-Host ("Не удалось: {0}" -f ($failed -join ', ')) -ForegroundColor Red
        exit 1
    }
    exit 0
}
finally {
    Pop-Location
}
