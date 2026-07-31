--[[
  enf-color.lua — перенос цветовой разметки формул в целевой формат.

  Исходник материала знает только макросы ролей: \enfVar, \enfFun, \enfPar,
  \enfOp, \enfTgt, \enfNeu. Что с ними делать, зависит от формата:

    LaTeX и PDF   — макросы определены в преамбуле (Build/templates/enf-colors.tex),
                    трогать ничего не нужно.
    HTML, EPUB,
    Reveal.js     — макросы определены для MathJax в шапке документа,
                    трогать ничего не нужно.
    DOCX и ODT    — Word не поддерживает цвет внутри формул OMML. Оставленный
                    макрос попал бы в документ как видимый текст «\enfVar»,
                    поэтому здесь он снимается, а содержимое сохраняется.

  Снятие цвета в DOCX — не потеря качества, а следствие ограничения формата.
  Именно поэтому ENF-COLOR-003 требует дублировать смысл цвета начертанием
  или подписью: в DOCX от цвета в формулах не остаётся ничего.
]]

local strip_formats = {
  docx = true,
  odt = true,
  rtf = true,
  ['opendocument'] = true,
}

--- Снимает \enfXxx{...} с учётом вложенных фигурных скобок.
local function strip_macros(text)
  local macros = { 'enfVar', 'enfFun', 'enfPar', 'enfOp', 'enfTgt', 'enfNeu' }
  local changed = true

  while changed do
    changed = false
    for _, macro in ipairs(macros) do
      local start_pos = text:find('\\' .. macro .. '%s*{')
      if start_pos then
        local brace_pos = text:find('{', start_pos)
        local depth, i = 0, brace_pos
        local close_pos = nil

        while i <= #text do
          local c = text:sub(i, i)
          if c == '{' then
            depth = depth + 1
          elseif c == '}' then
            depth = depth - 1
            if depth == 0 then
              close_pos = i
              break
            end
          end
          i = i + 1
        end

        if close_pos then
          text = text:sub(1, start_pos - 1)
            .. text:sub(brace_pos + 1, close_pos - 1)
            .. text:sub(close_pos + 1)
          changed = true
        end
      end
    end
  end

  return text
end

function Math(el)
  if strip_formats[FORMAT] then
    el.text = strip_macros(el.text)
    return el
  end
  return nil
end

--- Сырые вставки LaTeX встречаются в редких случаях; обрабатываются так же.
function RawInline(el)
  if strip_formats[FORMAT] and (el.format == 'tex' or el.format == 'latex') then
    el.text = strip_macros(el.text)
    return el
  end
  return nil
end

function RawBlock(el)
  if strip_formats[FORMAT] and (el.format == 'tex' or el.format == 'latex') then
    el.text = strip_macros(el.text)
    return el
  end
  return nil
end
