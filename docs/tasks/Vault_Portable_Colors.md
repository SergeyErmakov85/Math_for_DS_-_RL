---
title: "Задача: автономная раскраска формул в переносимом Vault"
enf_mode: publication
discipline: meta
version: 1.0.0
updated: 2026-08-03
---

# Задача: автономная раскраска формул в переносимом Vault

Инструкция для Claude Code. Цель: папка `Obsidian/Vault/`, скопированная на любой компьютер и открытая в Obsidian как хранилище, должна сразу показывать цветные формулы — без ручного открытия `_meta/mathjax-preamble.md`.

---

## Контекст: что уже работает, а что нет

Раскраска формул состоит из двух частей.

1. **CSS-сниппеты** `enf-tokens`, `enf-math`, `enf-callouts` лежат в `Obsidian/Vault/.obsidian/snippets/` и включены в `.obsidian/appearance.json`. Они переносятся вместе с папкой и работают сразу. **Здесь менять ничего не нужно.**
2. **MathJax-макросы** `\enfVar`, `\enfFun`, `\enfPar`, `\enfOp`, `\enfTgt`, `\enfNeu` сейчас объявляются через `\newcommand` в заметке `_meta/mathjax-preamble.md` и действуют только после того, как эта заметка отрисована в текущей сессии Obsidian. Это слабое звено: у Obsidian нет штатной постоянной преамбулы MathJax, а фоновые вкладки с версии 1.7 загружаются отложенно, поэтому даже закреплённая вкладка не гарантирует регистрацию макросов до открытия материала.

Решение: подключить к хранилищу community-плагин **Extended MathJax** (репозиторий `wei2912/obsidian-latex`), который загружает файл преамбулы автоматически при старте приложения. Плагин и его настройки версионируются внутри `Vault/.obsidian/`, поэтому переносятся вместе с папкой.

---

## Шаг 1. Скачать и проверить плагин

1. Открыть репозиторий `https://github.com/wei2912/obsidian-latex`, взять последний релиз: файлы `main.js` и `manifest.json`.
2. **Прочитать README и `manifest.json` релиза** и зафиксировать два факта, не полагаясь на память (`ENF-AI-002`): точный `id` плагина из `manifest.json` и точное имя/расположение файла преамбулы, который плагин читает (исторически — `preamble.sty` в корне хранилища; в новых версиях путь может настраиваться через `data.json`).
3. Положить файлы в `Obsidian/Vault/.obsidian/plugins/<id-из-manifest>/`.

## Шаг 2. Включить плагин в поставке хранилища

1. Создать `Obsidian/Vault/.obsidian/community-plugins.json` с содержимым `["<id-из-manifest>"]`.
2. Убедиться, что `.gitignore` не отсекает эти файлы: сейчас игнорируются только `workspace.json`, `workspace-mobile.json` и `cache/` — папка `plugins/` и `community-plugins.json` версионируются. Если это не так — поправить `.gitignore`.

## Шаг 3. Создать файл преамбулы

Создать файл преамбулы там, где его ожидает плагин (по умолчанию `Obsidian/Vault/preamble.sty`), с тем же содержимым, что в `_meta/mathjax-preamble.md`:

```latex
\newcommand{\enfVar}[1]{\htmlClass{enf-variable}{#1}}
\newcommand{\enfFun}[1]{\htmlClass{enf-function}{#1}}
\newcommand{\enfPar}[1]{\htmlClass{enf-parameter}{#1}}
\newcommand{\enfOp}[1]{\htmlClass{enf-operator}{#1}}
\newcommand{\enfTgt}[1]{\htmlClass{enf-target}{#1}}
\newcommand{\enfNeu}[1]{\htmlClass{enf-neutral}{#1}}
```

Макросы по-прежнему вешают CSS-класс, а не цвет — единый источник истины `css/enf-tokens.css` не нарушается (`ENF-COLOR-001`).

## Шаг 4. Обновить документацию

1. **`Obsidian/Vault/README.md`**, раздел «Первый запуск»: заменить шаг «открыть `_meta/mathjax-preamble.md`» на «при первом открытии хранилища разрешить community-плагины (кнопка *Turn on community plugins / Trust author*): преамбула загрузится автоматически». Добавить запасной вариант: если плагины отключены, открыть `_meta/mathjax-preamble.md` вручную, как раньше.
2. **`Obsidian/Vault/_meta/mathjax-preamble.md`**: пометить, что основной механизм теперь — плагин и `preamble.sty`, а заметка остаётся запасным путём и проверочным стендом (блок «Проверка» с пятицветной формулой сохранить). Явно указать: при изменении макросов правятся **оба** места — `preamble.sty` и эта заметка.
3. **`docs/reference/PROGRESS.md`**: добавить запись о решении — что выбран плагин, почему не закреплённая вкладка (отложенная загрузка фоновых вкладок в Obsidian 1.7+) и почему не `\newcommand` в каждом материале (нарушает `ENF-MATH-003`, а сценарий переноса одиночного файла всё равно не решает — без сниппетов из `.obsidian/snippets/` классы не окрашиваются).
4. **`CHANGELOG.md`**: строка об изменении.

## Шаг 5. Проверки

1. `pwsh Scripts/check.ps1 Obsidian/Vault/` (или адресно `node Scripts/check-frontmatter.mjs`, `check-links.mjs`, `check-colors.mjs`, `check-structure.mjs`, `check-alt.mjs`) — на изменённых Markdown-файлах.
2. Ручной тест переносимости: скопировать `Obsidian/Vault/` во временную папку вне репозитория → открыть в Obsidian → разрешить плагины → открыть `Calculus/Limit_of_a_Function.learning.md` **не открывая преамбулу** → формулы цветные в обеих темах (светлой и тёмной).
3. Негативный тест: в песочнице отключить плагин и убедиться, что запасной путь (открытие `_meta/mathjax-preamble.md`) по-прежнему работает.

---

## Чего не делать

- Не вписывать `\newcommand` в материалы — запрещено `ENF-MATH-003` и не решает задачу.
- Не заменять макросы на `\textcolor` с HEX-кодами — запрещено `ENF-COLOR-001` и `ENF-COLOR-030`.
- Не версионировать `workspace.json` — он намеренно в `.gitignore` как рабочее состояние пользователя.
- Не редактировать порождённые сниппеты в `Vault/.obsidian/snippets/` напрямую — источники лежат в `snippets/` и `css/`, пересборка через `node Scripts/gen-obsidian-css.mjs`.
