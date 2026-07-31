# Mermaid — шаблоны диаграмм

Готовые диаграммы, которые вставляются в материал копированием и рендерятся без правок и в Obsidian, и в HTML-сборке пайплайна.

| Файл | Тип диаграммы |
|------|---------------|
| [`init-config.md`](init-config.md) | Единый init-блок с палитрой ENF — подключается в начале каждой диаграммы |
| [`algorithm-flowchart.md`](algorithm-flowchart.md) | Блок-схема алгоритма |
| [`decision-tree.md`](decision-tree.md) | Дерево решений |
| [`graph-structures.md`](graph-structures.md) | Графы: ориентированные, взвешенные, двудольные |
| [`lifecycle.md`](lifecycle.md) | Жизненный цикл процесса (состояния и переходы) |
| [`ai-architecture.md`](ai-architecture.md) | Архитектуры моделей и конвейеров машинного обучения |
| [`research-process.md`](research-process.md) | Исследовательский процесс: от гипотезы до публикации |

## Почему у каждой диаграммы есть init-блок

Mermaid не поддерживает внешние файлы тем. Единственный способ применить палитру — передать её в директиве `%%{init: ...}%%` в начале диаграммы. Чтобы палитра оставалась единым источником истины, init-блок генерируется из токенов командой:

```powershell
node Scripts/gen-mermaid-init.mjs
```

Скрипт читает `Build/css/enf-tokens.css` и переписывает `init-config.md` и init-блоки во всех шаблонах этого каталога. Править цвета руками в отдельных диаграммах запрещено (`ENF-DIAG-010`) — правка потеряется при следующей генерации.

## Ограничения

Obsidian и Pandoc используют разные версии Mermaid. Во фреймворке разрешены только типы диаграмм, поддерживаемые обеими: `flowchart`, `graph`, `stateDiagram-v2`, `sequenceDiagram`, `classDiagram`, `pie`, `gitGraph`. Экспериментальные типы (`mindmap`, `timeline`, `quadrantChart`, `sankey`) не используются — см. [`../docs/StyleGuide/Diagrams.md`](../docs/StyleGuide/Diagrams.md).
