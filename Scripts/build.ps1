#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Сборка материала ENF в пять форматов: PDF, EPUB, HTML, DOCX, Reveal.js.

.DESCRIPTION
    Роль `make all` во фреймворке выполняет этот скрипт: GNU Make в целевом
    окружении нет, а требовать его установки противоречит принципу «стек
    без барьеров» (см. журнал решений docs/PROGRESS.md).

    Перед сборкой обязательно пересоздаются порождаемые файлы палитры:
    LaTeX-цвета и init-блоки Mermaid. Так собранный документ не может
    разойтись с единым источником истины.

    Коды возврата:
      0 — все запрошенные форматы собраны
      1 — хотя бы один формат не собрался
      2 — ошибка запуска или нет обязательной зависимости

.PARAMETER Source
    Markdown-файл для сборки.

.PARAMETER Format
    Один или несколько форматов: pdf, epub, html, docx, revealjs.

.PARAMETER All
    Собрать во все пять форматов.

.PARAMETER OutDir
    Каталог результата. По умолчанию out/.

.PARAMETER CheckEnv
    Проверить окружение и выйти: что установлено и какого формата это касается.

.PARAMETER SkipChecks
    Не запускать проверки качества перед сборкой. По умолчанию сборка
    материала, не прошедшего проверки, не начинается.

.EXAMPLE
    pwsh Scripts/build.ps1 -CheckEnv

.EXAMPLE
    pwsh Scripts/build.ps1 -Source Examples/Bellman_Equation.learning.md -All
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Source,

    [ValidateSet('pdf', 'epub', 'html', 'docx', 'revealjs')]
    [string[]]$Format,

    [switch]$All,
    [string]$OutDir = 'out',
    [switch]$CheckEnv,
    [switch]$SkipChecks
)

$ErrorActionPreference = 'Stop'
$scriptDir = $PSScriptRoot
$repoRoot = Split-Path -Parent $scriptDir

$FORMAT_INFO = [ordered]@{
    pdf      = @{ Ext = 'pdf';  Needs = @('pandoc', 'xelatex'); Note = 'требует TeX-дистрибутива с XeLaTeX' }
    epub     = @{ Ext = 'epub'; Needs = @('pandoc');            Note = '' }
    html     = @{ Ext = 'html'; Needs = @('pandoc');            Note = '' }
    docx     = @{ Ext = 'docx'; Needs = @('pandoc');            Note = 'цвет в формулах снимается: OMML его не поддерживает' }
    revealjs = @{ Ext = 'html'; Needs = @('pandoc');            Note = 'имя файла получает суффикс .slides' }
}

function Test-Tool {
    param([string]$Name)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return @{ Found = $true; Path = $cmd.Source } }
    return @{ Found = $false; Path = $null }
}

<#
Подбор шрифтов для PDF.

fontspec не подставляет замену: названная, но не установленная гарнитура
останавливает сборку с ошибкой «font cannot be found». Поэтому шрифты не
прописаны в конфигурации, а выбираются здесь — первый фактически доступный
из списка кандидатов. Списки упорядочены по предпочтению и заканчиваются
гарнитурами, которые почти наверняка есть в системе.

Все кандидаты покрывают кириллицу: гарнитура без кириллицы дала бы вместо
русского текста пустые прямоугольники, что хуже несобравшегося PDF —
такую ошибку легко не заметить.
#>
$FONT_CANDIDATES = [ordered]@{
    mainfont = @('Charter', 'PT Serif', 'Georgia', 'Cambria', 'DejaVu Serif', 'Liberation Serif', 'Times New Roman')
    sansfont = @('Inter', 'PT Sans', 'Segoe UI', 'DejaVu Sans', 'Liberation Sans', 'Arial')
    monofont = @('JetBrains Mono', 'Consolas', 'DejaVu Sans Mono', 'Liberation Mono', 'Courier New')
    mathfont = @('Latin Modern Math', 'STIX Two Math', 'XITS Math', 'Cambria Math')
}

function Get-InstalledFontFamilies {
    try {
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop
        return (New-Object System.Drawing.Text.InstalledFontCollection).Families.Name
    }
    catch {
        # Не Windows либо System.Drawing недоступен — пробуем fontconfig.
        if (Get-Command fc-list -ErrorAction SilentlyContinue) {
            return (& fc-list --format '%{family[0]}\n' | Sort-Object -Unique)
        }
        return $null
    }
}

function Resolve-Fonts {
    $families = Get-InstalledFontFamilies
    $resolved = [ordered]@{}

    if ($null -eq $families) {
        Write-Host '  перечислить установленные шрифты не удалось; PDF собирается со шрифтами по умолчанию' -ForegroundColor Yellow
        return $resolved
    }

    $set = [System.Collections.Generic.HashSet[string]]::new([string[]]$families, [StringComparer]::OrdinalIgnoreCase)

    foreach ($role in $FONT_CANDIDATES.Keys) {
        $picked = $FONT_CANDIDATES[$role] | Where-Object { $set.Contains($_) } | Select-Object -First 1
        if ($picked) { $resolved[$role] = $picked }
        else {
            Write-Host "  для $role не найдено ни одной гарнитуры из списка кандидатов" -ForegroundColor Yellow
        }
    }
    return $resolved
}

function Show-Environment {
    Write-Host ''
    Write-Host 'Окружение сборки ENF' -ForegroundColor Cyan
    Write-Host ('-' * 60)

    $tools = [ordered]@{
        'pandoc'  = 'обязателен для всех форматов'
        'xelatex' = 'нужен только для PDF'
        'node'    = 'обязателен: порождение палитры и проверки'
        'pwsh'    = 'этот скрипт'
    }

    $missingRequired = @()

    foreach ($name in $tools.Keys) {
        $t = Test-Tool $name
        if ($t.Found) {
            $version = ''
            try {
                $version = switch ($name) {
                    'pandoc'  { (& pandoc --version   | Select-Object -First 1) }
                    'xelatex' { (& xelatex --version  | Select-Object -First 1) }
                    'node'    { (& node --version) }
                    default   { $PSVersionTable.PSVersion.ToString() }
                }
            }
            catch { $version = '' }
            Write-Host ("  {0,-9} есть   {1}" -f $name, $version)
        }
        else {
            Write-Host ("  {0,-9} НЕТ    {1}" -f $name, $tools[$name]) -ForegroundColor Yellow
            if ($name -in @('pandoc', 'node')) { $missingRequired += $name }
        }
    }

    Write-Host ('-' * 60)
    Write-Host 'Доступность форматов:'
    foreach ($fmt in $FORMAT_INFO.Keys) {
        $needs = $FORMAT_INFO[$fmt].Needs
        $ok = $true
        foreach ($n in $needs) { if (-not (Test-Tool $n).Found) { $ok = $false } }
        $mark = if ($ok) { 'доступен  ' } else { 'недоступен' }
        $colour = if ($ok) { 'Green' } else { 'Yellow' }
        Write-Host ("  {0,-9} {1} {2}" -f $fmt, $mark, $FORMAT_INFO[$fmt].Note) -ForegroundColor $colour
    }

    Write-Host ''
    if ($missingRequired.Count -gt 0) {
        Write-Host 'Установка недостающего:' -ForegroundColor Yellow
        if ('pandoc' -in $missingRequired) { Write-Host '  winget install JohnMacFarlane.Pandoc' }
        if ('node' -in $missingRequired)   { Write-Host '  winget install OpenJS.NodeJS.LTS' }
        return 2
    }
    if (-not (Test-Tool 'xelatex').Found) {
        Write-Host 'Для PDF: winget install MiKTeX.MiKTeX' -ForegroundColor Yellow
    }
    return 0
}

if ($CheckEnv) { exit (Show-Environment) }

if (-not $Source) {
    Write-Host 'Не указан исходный файл. Пример:' -ForegroundColor Red
    Write-Host '  pwsh Scripts/build.ps1 -Source Examples/Bellman_Equation.learning.md -All'
    exit 2
}

Push-Location $repoRoot
try {
    $sourcePath = Resolve-Path -Path $Source -ErrorAction SilentlyContinue
    if (-not $sourcePath) {
        Write-Host "Файл не найден: $Source" -ForegroundColor Red
        exit 2
    }

    if (-not (Test-Tool 'pandoc').Found) {
        Write-Host 'Не найден Pandoc. Запустите: pwsh Scripts/build.ps1 -CheckEnv' -ForegroundColor Red
        exit 2
    }

    $formats = if ($All) { @($FORMAT_INFO.Keys) } elseif ($Format) { $Format } else { @('html') }

    # --- проверки качества ---
    if (-not $SkipChecks) {
        Write-Host 'Проверки качества перед сборкой…' -ForegroundColor Cyan
        & (Join-Path $scriptDir 'check.ps1') $sourcePath.Path -SkipPalette
        if ($LASTEXITCODE -ne 0) {
            Write-Host ''
            Write-Host 'Сборка не начата: материал не прошёл проверки.' -ForegroundColor Red
            Write-Host 'Исправьте нарушения либо запустите с -SkipChecks, если понимаете зачем.'
            exit 1
        }
    }

    # --- порождаемые файлы палитры ---
    Write-Host 'Пересоздание файлов палитры…' -ForegroundColor Cyan
    foreach ($gen in 'gen-latex-colors.mjs', 'gen-mermaid-init.mjs', 'gen-obsidian-css.mjs') {
        & node (Join-Path $scriptDir $gen) | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Не удалось выполнить $gen" -ForegroundColor Red
            exit 2
        }
    }

    if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($sourcePath.Path)
    $failed = @()
    $built = @()

    # Шрифты нужны только PDF; для остальных форматов подбор пропускаем.
    $fontArgs = @()
    if ($formats -contains 'pdf') {
        Write-Host 'Подбор шрифтов для PDF…' -ForegroundColor Cyan
        $fonts = Resolve-Fonts
        foreach ($role in $fonts.Keys) {
            Write-Host ("  {0,-9} {1}" -f $role, $fonts[$role])
            $fontArgs += '--variable'
            $fontArgs += "$role=$($fonts[$role])"
        }
    }

    Write-Host ''
    Write-Host "Сборка: $baseName" -ForegroundColor Cyan
    Write-Host ('-' * 60)

    foreach ($fmt in $formats) {
        $info = $FORMAT_INFO[$fmt]

        $unavailable = @($info.Needs | Where-Object { -not (Test-Tool $_).Found })
        if ($unavailable.Count -gt 0) {
            Write-Host ("  {0,-9} пропущен: нет {1}" -f $fmt, ($unavailable -join ', ')) -ForegroundColor Yellow
            $failed += $fmt
            continue
        }

        $suffix = if ($fmt -eq 'revealjs') { '.slides' } else { '' }
        $outFile = Join-Path $OutDir "$baseName$suffix.$($info.Ext)"
        $defaults = "Build/defaults/$fmt.yaml"

        $extra = if ($fmt -eq 'pdf') { $fontArgs } else { @() }
        $output = & pandoc --defaults=$defaults @extra --output=$outFile $sourcePath.Path 2>&1
        if ($LASTEXITCODE -eq 0) {
            $size = [math]::Round((Get-Item $outFile).Length / 1KB, 1)
            Write-Host ("  {0,-9} OK      {1}  ({2} КБ)" -f $fmt, $outFile, $size) -ForegroundColor Green
            $built += $fmt
        }
        else {
            Write-Host ("  {0,-9} ОШИБКА" -f $fmt) -ForegroundColor Red
            $output | ForEach-Object { Write-Host "      $_" }
            $failed += $fmt
        }
    }

    Write-Host ('-' * 60)
    Write-Host ("Собрано: {0} из {1}" -f $built.Count, $formats.Count)

    if ($failed.Count -gt 0) {
        Write-Host ("Не собрались: {0}" -f ($failed -join ', ')) -ForegroundColor Red
        exit 1
    }
    exit 0
}
finally {
    Pop-Location
}
