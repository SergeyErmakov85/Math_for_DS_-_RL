# Changelog

Все заметные изменения проекта фиксируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/); версии следуют [Semantic Versioning](https://semver.org/lang/ru/).

Что означают уровни версий применительно к фреймворку документации:

- **MAJOR** — изменение, после которого существующие материалы перестают соответствовать нормам без правки (изменён смысл правила `ENF-*`, удалён цветовой токен, несовместимо изменён фронтматтер).
- **MINOR** — новые правила, токены, шаблоны, примеры; существующие материалы продолжают проходить проверки.
- **PATCH** — исправления опечаток, уточнения формулировок, починка скриптов без изменения норм.

---

## [Unreleased]

Изменения, ещё не вошедшие в релиз.

### Changed

- **Инструкции для Codex по урокам с кодом.** В корневой `AGENTS.md`, который Codex загружает автоматически, добавлен самодостаточный раздел «Уроки с кодом на Python»: что прочитать, обязательные требования и команды проверки. Новый промт `ENF-PROMPT-007` `docs/prompts/Code_Lesson_Generator.md`. В `agents/CODEX.md` добавлены порядок работы над уроком с кодом, пункты самопроверки 15–20 и команды `check_lesson.py` через `uv`.
- **Сквозная раскраска и построчный перевод формул в код.** Новое правило `ENF-MATH-025`: в Learning Mode символ с ролью окрашивается при каждом появлении, а лимит тонов используется полностью; `check-colors.mjs` предупреждает о недокрашенных символах. В модуле «Код» появился п. 5.6: у каждой ключевой формулы есть таблица «формула → код» из двух колонок; разбор по маркерам обязателен; итоговая таблица содержит полные формулы. Приложение А переписано как раскрашенный эталон. Обновлены `agents/CLAUDE.md`, `agents/CODEX.md`, `docs/03_Math_Notation.md`, `docs/10_Review_Checklist.md`.
- **Хранилищем Obsidian стал корень репозитория.** Вложенное хранилище `Obsidian/Vault/` упразднено. Настройки, тема, плагин Extended MathJax и сниппеты — в корневом `.obsidian/`; служебные заметки — в `Obsidian/`; лекции — в `materials/<Дисциплина>/`; Templater-шаблоны — в `templates/templater/`. `Scripts/gen-obsidian-css.mjs` пишет сниппеты в `.obsidian/snippets/`. Хранилище вставляет ссылки относительными путями (`.obsidian/app.json`), вложения сохраняет в `Figures/`, новые заметки создаёт в `materials/`.
- **Модуль «Код» включён в документацию** как `docs/13_Code_Module_Python.md` и подключён в `agents/CLAUDE.md`, `agents/CODEX.md`, `agents/AGENTS.md`. Добавлен недостающий сниппет подсветки кода `snippets/enf-code.css` (темы «Тетрадь» и «Доска»).

### Removed

- Дубликаты: копия учебника `Obsidian/Vault/100 math-textbook_Cuber/`, второй `preamble.sty`, вложенные `.obsidian/` в `Obsidian/` и `Obsidian/Vault/`, README-заглушки `Obsidian/CSS|Canvas|Dataview|Icons|Snippets|Templates`, пустые папки `00 Inbox`…`90 Ресурсы`, копия `lesson-code.theme` в `.obsidian/themes/`, `materials/demo_lesson.md` (дублировал приложение А модуля «Код»), `Scripts/__pycache__/`.

### Fixed

- **Около 1500 внутренних ссылок, испорченных внешним хранилищем Obsidian, восстановлены.** Ссылки были переписаны в пути вида `Education/Math/Math_for_DS_&_RL/…` или в имя файла без каталога и не открывались ни на GitHub, ни в сборке. Все ссылки снова относительные; `check-links.mjs` проходит без нарушений.

- **Раскраска формул в Obsidian, HTML, EPUB и Reveal.js не работала: макросы ролей использовали `\htmlClass{}{}`.** Этот макрос принадлежит KaTeX; в MathJax его нет — расширение `html` определяет `\class`, `\cssId`, `\style`, `\href`, `\data`. Вместо цветной формулы MathJax печатал «Undefined control sequence». Заменено на `\class{}{}` в `Obsidian/Vault/preamble.sty`, `Obsidian/Vault/_meta/mathjax-preamble.md` и `Build/templates/mathjax-macros.html`. Имена CSS-классов, палитра, токены и правила `ENF-*` не изменились, материалы править не нужно. Сборка PDF не затронута — там макросы приходят из `Build/templates/enf-colors.tex`.

### Added

- **Хранилище Obsidian раскрашивает формулы сразу после копирования на другую машину.** В поставку `Obsidian/Vault/` добавлены плагин Extended MathJax (`obsidian-latex` 0.4.1, файлы в `.obsidian/plugins/`), `.obsidian/community-plugins.json` и `preamble.sty` в корне хранилища. Плагин читает преамбулу при старте Obsidian, поэтому открывать `_meta/mathjax-preamble.md` вручную больше не нужно. Заметка сохранена как запасной путь при выключенных плагинах и как проверочный стенд; при правке макросов меняются оба файла. Снимает известное ограничение версии 1.0.0 «Макросы MathJax в Obsidian действуют в пределах сессии».

---

## [1.1.0] — 2026-08-03

Реструктуризация репозитория. Нормы не изменились: номера правил `ENF-*`, палитра, фронтматтер и режимы раскраски прежние, поэтому существующие материалы продолжают проходить проверки без правок. Менять нужно только пути в ссылках.

### Changed

- **Документация собрана в плоский нумерованный `docs/`** — двенадцать разделов вместо вложенных `StyleGuide/`, `Codex/` и `Claude/`. Порядок чтения задан именами файлов.
- **Каталоги приведены к нижнему регистру** — `templates/`, `svg/`, `mermaid/`, `examples/`. Прежние имена с заглавной буквы на регистронезависимых файловых системах расходились с регистрочувствительным Git и ломали сборку в CI.
- **CSS вынесен из `Build/`** — токены и оформление сборки в `css/`, сниппеты Obsidian в `snippets/`. `Build/` остался конфигурацией Pandoc: `defaults/`, `filters/`, `templates/`, `metadata.yaml`.
- **`Scripts/gen-obsidian-css.mjs` переносит в хранилище все три сниппета**, а не только `enf-tokens.css`. Причина прежняя: Obsidian не подключает CSS извне хранилища, а держать рабочую копию в двух местах запрещает `ENF-COLOR-001`. Правки в `Obsidian/Vault/.obsidian/snippets/` теперь теряются при генерации для всех трёх файлов — менять нужно источник.
- **Индексы `docs/Codex/README.md` и `docs/Claude/README.md` удалены** — они описывали состав каталогов, которых больше нет.

### Added

- **Файлы агентов собраны в `agents/`** — `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `DOCUMENT_CONVERSION.md`. В корне остались указатели на них: без файла в корне агент не прочитает конституцию первым.
- **`docs/05_CSS_Guide.md`** — что лежит в `css/` и `snippets/`, почему сниппеты хранятся вне хранилища, что пересоздавать после правки токенов.
- **`.github/workflows/checks.yml`** — уровень 1 контроля качества в CI. Задача `quality` прогоняет шесть проверок на Node 18; задача `generated` перегенерирует порождённые файлы и падает, если они разошлись с источниками.

### Соответствие путей

| Было | Стало |
|------|-------|
| `CLAUDE.md` (мастер-промт) | `docs/00_Project_Charter.md` |
| `docs/StyleGuide/Ermakov_Math_Style_Guide_v4.md` | `docs/01_Style_Guide.md` |
| `docs/StyleGuide/Color_System.md` | `docs/02_Color_System.md` |
| `docs/StyleGuide/Mathematics.md` | `docs/03_Math_Notation.md` |
| `Obsidian/README.md` | `docs/04_Obsidian_Guide.md` |
| `Mermaid/README.md` | `docs/06_Mermaid_Guide.md` |
| `SVG/README.md` | `docs/07_SVG_Guide.md` |
| `docs/StyleGuide/AI.md` | `docs/08_AI_Constitution.md` |
| `docs/Codex/Prompt_Standard.md` | `docs/09_Prompt_Library.md` |
| `docs/Codex/Review_Checklist.md` | `docs/10_Review_Checklist.md` |
| `Build/README.md` | `docs/11_Build_Pipeline.md` |
| `CONTRIBUTING.md` | `docs/12_Repository_Guide.md` |
| `docs/StyleGuide/{Typography,Diagrams,Publishing}.md` | `docs/style/` |
| `docs/Codex/Prompts/` | `docs/prompts/` |
| `docs/PROGRESS.md` | `docs/reference/PROGRESS.md` |
| `docs/Claude/Teaching_Mode.md` | `docs/reference/Teaching_Mode.md` |
| `docs/Codex/Review_Report_Example.md` | `docs/reference/Review_Report_Example.md` |
| `docs/Examples/` | `docs/reference/examples/` |
| `AGENTS.md` | `agents/AGENTS.md` |
| `docs/Claude/CLAUDE.md` | `agents/CLAUDE.md` |
| `docs/Codex/AGENTS.md` | `agents/CODEX.md` |
| `DOCUMENT_CONVERSION.md` | `agents/DOCUMENT_CONVERSION.md` |
| `Build/css/` | `css/` |
| `Obsidian/Vault/.obsidian/snippets/{enf-math,enf-callouts}.css` | `snippets/` |
| `Templates/`, `SVG/`, `Mermaid/`, `Examples/` | `templates/`, `svg/`, `mermaid/`, `examples/` |

---

## [1.0.0] — 2026-07-31

Первая полная версия Ermakov Notes Framework. Все десять компонент (D1–D10) реализованы и проходят проверки.

### Added

- **Style Guide** (`docs/StyleGuide/`) — модульное руководство: `Color_System.md`, `Typography.md`, `Mathematics.md`, `Diagrams.md`, `AI.md`, `Publishing.md` и сводный `Ermakov_Math_Style_Guide_v4.md`. Каждое правило имеет уникальный номер и пару примеров «плохо / хорошо».
- **Цветовой движок** — семантическая палитра, закреплённая за ролями сущностей, а не за символами. Единый источник истины: таблица токенов и CSS-переменные `Build/css/enf-tokens.css`, из которых цвета берут Obsidian, SVG, Mermaid и Pandoc-шаблоны. Контраст не ниже WCAG AA на светлом и тёмном фоне, различимость при дейтеранопии и протанопии.
- **Два режима раскраски формул** — `enf_mode: learning | publication` во фронтматтере документа; режим учитывается автоматическими проверками.
- **Шесть шаблонов документов** (`Templates/`) — Lecture, BookChapter, ResearchPaper, ExerciseSheet, Proof, Presentation, каждый с заполненным примером.
- **Хранилище Obsidian** (`Obsidian/`) — структура папок, светлая и тёмная CSS-темы, Templater-шаблоны, Dataview-запросы, Canvas-схемы; открывается без ошибок и работает сразу после копирования.
- **Конституция агентов** (`docs/Codex/AGENTS.md`, `docs/Claude/CLAUDE.md`, `docs/Claude/Teaching_Mode.md`) — самодостаточные инструкции для ИИ-агентов: правила генерации и проверки, требования к качеству, структура вывода, обучающий режим.
- **Библиотека SVG** (`SVG/`) — координатные оси, графики функций, вероятностные деревья, цепи Маркова, нейронные сети, диаграмма уравнения Беллмана, блок-схемы алгоритмов; единый холст и сетка, каталог-превью `SVG/CATALOG.md`.
- **Библиотека Mermaid** (`Mermaid/`) — шаблоны алгоритмов, графов, деревьев решений, жизненных циклов, архитектур ИИ и исследовательских процессов; единый init-конфиг с палитрой.
- **Pandoc Pipeline** (`Build/`, `Scripts/`) — сборка PDF (XeLaTeX), EPUB, HTML, DOCX и Reveal.js-презентации из одного Markdown-источника; Lua-фильтры, в том числе корректный перенос цветовой разметки формул во все форматы.
- **AI Quality Engine** (`docs/Codex/Review_Checklist.md`, `Scripts/`) — двухуровневый контроль: машинные проверки (битые ссылки, цвета вне палитры, отсутствие alt-текста, невалидный фронтматтер) и LLM-ревью по чек-листу с образцом отчёта.
- **Prompt Library** (`docs/Codex/Prompt_Standard.md`, `docs/Codex/Prompts/`) — промты PDF → Obsidian, Lecture Generator, Exercise Generator, SVG Generator, Research Assistant, Book Generator в едином формате.
- **Эталонные примеры** (`Examples/`) — предел функции, производная, интеграл, линейная регрессия, уравнение Беллмана, Q-Learning, Backpropagation; каждый в двух вариантах: Learning Mode и Publication Mode.

### Changed

- `README.md` репозитория переписан: вместо краткого описания личного собрания материалов — документация фреймворка. Прежнее описание сохранено в разделе «О репозитории».

### Notes

- Сборка и скрипты рассчитаны на Node.js и PowerShell. Python не требуется — решение зафиксировано в журнале `docs/PROGRESS.md` и вызвано составом целевого окружения.
- PDF собирается через XeLaTeX, а не pdfLaTeX: кириллица в содержимом требует Unicode-движка.
- Шрифты для PDF не задаются в конфигурации, а подбираются сборкой из списка кандидатов по факту наличия в системе. Пакет `fontspec` не подставляет замену, и жёстко заданная гарнитура сделала бы репозиторий собираемым только на машине автора.
- Палитра состоит из пяти семантических тонов, а не из восьми. Ограничение измерено, а не выбрано: при обязательном контрасте 4,5:1 дихроматия оставляет место ровно для пяти различимых ролей. Проверка воспроизводится командой `node Scripts/check-contrast.mjs`.

### Known limitations

Ограничения внешних инструментов, а не дефекты фреймворка. Каждое задокументировано там, где с ним столкнутся.

- **SVG в PDF требует конвертера.** Без `rsvg-convert` или Inkscape иллюстрация в PDF заменяется рамкой с её alt-текстом, а в вывод сборки печатается предупреждение с именем файла. Остальные четыре формата не затронуты. Векторные копии создаются командой `pwsh Scripts/convert-svg.ps1`.
- **Цвет формул не переносится в DOCX.** Word не поддерживает цвет внутри формул OMML, поэтому фильтр снимает цветовую разметку, сохраняя содержимое. Это и есть причина, по которой правило `ENF-COLOR-003` требует дублировать смысл цвета словами.
- **Макросы MathJax в Obsidian действуют в пределах сессии.** У Obsidian нет настройки постоянной преамбулы: заметку `Obsidian/Vault/_meta/mathjax-preamble.md` требуется открыть один раз после запуска приложения. Обходится закреплением вкладки; при сборке через Pandoc ограничения нет.

### Verification

Состояние на момент выпуска, воспроизводится указанными командами:

- `pwsh Scripts/check.ps1 .` — шесть проверок уровня 1 зелёные по всему репозиторию.
- `node Scripts/check-contrast.mjs` — палитра проходит пороги контраста и различимости в светлой и тёмной теме.
- Все 14 документов `Examples/` собраны во все пять форматов: 70 успешных сборок.

[Unreleased]: https://github.com/SergeyErmakov85/Math_for_DS_-_RL/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/SergeyErmakov85/Math_for_DS_-_RL/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/SergeyErmakov85/Math_for_DS_-_RL/releases/tag/v1.0.0
