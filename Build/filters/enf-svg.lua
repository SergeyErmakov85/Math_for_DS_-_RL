--[[
  enf-svg.lua — обработка SVG при сборке в LaTeX и PDF.

  LaTeX не умеет вставлять SVG напрямую. Pandoc пытается вызвать внешний
  конвертер rsvg-convert, и если его нет, сборка PDF падает целиком —
  из-за одной иллюстрации теряется весь документ.

  Фильтр делает поведение предсказуемым:

    1. Если рядом с файлом .svg лежит одноимённый .pdf (его создаёт
       Scripts/convert-svg.ps1), подставляется он — это полноценная
       векторная вставка без потери качества.

    2. Если конвертированного файла нет, изображение заменяется рамкой
       с текстом альтернативного описания. Документ собирается, а место
       пропуска видно и в тексте, и в предупреждении сборки.

  Второй случай — деградация, а не норма. Именно поэтому alt-текст обязан
  описывать содержание, а не называть тип объекта (ENF-DIAG-030): в PDF
  без конвертера он остаётся единственным носителем смысла иллюстрации.
]]

local latex_formats = { latex = true, beamer = true, context = true }

local function file_exists(path)
  local f = io.open(path, 'r')
  if f then f:close() return true end
  return false
end

--- Ищет конвертированный файл: сначала рядом с исходником, затем в Figures/pdf.
local function find_converted(src)
  local base = src:gsub('%.svg$', '')
  local candidates = {
    base .. '.pdf',
    'Figures/pdf/' .. (base:match('([^/\\]+)$') or base) .. '.pdf',
  }
  for _, candidate in ipairs(candidates) do
    if file_exists(candidate) then return candidate end
  end
  return nil
end

function Image(el)
  if not latex_formats[FORMAT] then return nil end
  if not el.src:match('%.svg$') then return nil end

  local converted = find_converted(el.src)
  if converted then
    el.src = converted
    return el
  end

  local alt = pandoc.utils.stringify(el.caption)
  if alt == '' then alt = 'иллюстрация без описания' end

  io.stderr:write(
    'enf-svg: нет конвертированной версии ' .. el.src ..
    '; в PDF подставлено текстовое описание. ' ..
    'Выполните Scripts/convert-svg.ps1, установив rsvg-convert или Inkscape.\n'
  )

  return pandoc.Span({
    pandoc.RawInline('latex', '\\fbox{\\begin{minipage}{0.9\\linewidth}\\small\\textit{Иллюстрация: }'),
    pandoc.Str(alt),
    pandoc.RawInline('latex', '\\end{minipage}}'),
  })
end
