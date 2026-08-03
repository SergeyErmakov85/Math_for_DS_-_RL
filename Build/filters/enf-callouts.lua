--[[
  enf-callouts.lua — перенос коллаутов Obsidian в остальные форматы.

  Obsidian записывает коллаут как цитату, первая строка которой имеет вид
  «[!theorem] Заголовок». Pandoc видит обычный blockquote и теряет тип блока,
  а вместе с ним — оформление теорем, определений и доказательств.

  Фильтр распознаёт эту строку и превращает цитату в Div с классами
  «callout» и «callout-<тип>». Дальше оформление берут на себя:
    HTML и EPUB — css/enf-html.css;
    LaTeX и PDF — окружения из Build/templates/enf-callouts.tex.
]]

local TITLES = {
  definition = 'Определение',
  theorem    = 'Теорема',
  lemma      = 'Лемма',
  corollary  = 'Следствие',
  proof      = 'Доказательство',
  example    = 'Пример',
  remark     = 'Замечание',
  intuition  = 'Интуиция',
  warning    = 'Внимание',
  note       = 'Заметка',
}

function BlockQuote(el)
  local first = el.content[1]
  if not first or first.t ~= 'Para' then return nil end

  local inlines = first.content
  if #inlines == 0 or inlines[1].t ~= 'Str' then return nil end

  -- Первый элемент имеет вид «[!theorem]»; заголовок идёт следом.
  local kind = inlines[1].text:match('^%[!([%w%-]+)%]$')
  if not kind then return nil end
  kind = kind:lower()
  if not TITLES[kind] then return nil end

  -- Остаток первой строки — заголовок коллаута. Если его нет, берём
  -- название типа: блок без заголовка выглядит в PDF как безымянная врезка.
  local title_inlines = {}
  for i = 2, #inlines do
    table.insert(title_inlines, inlines[i])
  end
  if #title_inlines == 0 then
    title_inlines = { pandoc.Str(TITLES[kind]) }
  else
    while #title_inlines > 0 and title_inlines[1].t == 'Space' do
      table.remove(title_inlines, 1)
    end
  end

  local body = {}
  for i = 2, #el.content do
    table.insert(body, el.content[i])
  end

  local header = pandoc.Div(
    { pandoc.Para(title_inlines) },
    pandoc.Attr('', { 'callout-title' })
  )

  local content = { header }
  for _, block in ipairs(body) do
    table.insert(content, block)
  end

  return pandoc.Div(
    content,
    pandoc.Attr('', { 'callout', 'callout-' .. kind }, { ['data-callout'] = kind })
  )
end
