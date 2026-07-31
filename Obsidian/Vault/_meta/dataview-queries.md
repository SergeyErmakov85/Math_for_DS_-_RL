---
title: "Запросы Dataview"
enf_mode: publication
discipline: meta
tags: [служебное, dataview]
---

# Запросы Dataview

Готовые запросы для навигации по хранилищу. Требуют плагина Dataview; без него блоки останутся неотрисованным кодом, содержимое хранилища при этом не пострадает.

Скопируйте нужный блок в свою заметку — обычно в дневник курса или на страницу дисциплины.

## Все материалы по дисциплине

````markdown
```dataview
TABLE enf_mode AS "Режим", duration AS "Мин.", file.mtime AS "Изменён"
FROM ""
WHERE discipline = "rl"
SORT file.mtime DESC
```
````

## Незавершённые материалы

Черновиком считается заметка со `status: draft` либо содержащая пометку `TODO`.

````markdown
```dataview
TABLE status, file.mtime AS "Изменён"
FROM ""
WHERE status = "draft" OR contains(file.outlinks, "TODO") OR econtains(file.content, "TODO(")
SORT file.mtime ASC
```
````

## Материалы без обязательных полей

Ловит то же, что проверка `ENF-PUB-002`, но прямо в хранилище — до запуска скриптов.

````markdown
```dataview
LIST
FROM ""
WHERE !enf_mode OR !discipline OR !title
```
````

## Лекции по возрастанию длительности

````markdown
```dataview
TABLE duration AS "Минут", discipline AS "Дисциплина"
FROM "10 Лекции"
WHERE duration
SORT duration ASC
```
````

## Карта тем: что на что ссылается

````markdown
```dataview
TABLE length(file.inlinks) AS "Ссылаются сюда", length(file.outlinks) AS "Ссылок отсюда"
FROM ""
WHERE discipline != "meta"
SORT length(file.inlinks) DESC
LIMIT 25
```
````

Заметка с нулём входящих ссылок либо не встроена в курс, либо является его началом. Полезно просматривать этот список раз в семестр: осиротевшие материалы обычно означают незавершённую перестройку курса.

## Задачи из всех материалов

Требует плагина Tasks либо штатного синтаксиса Dataview.

````markdown
```dataview
TASK
FROM ""
WHERE !completed
GROUP BY file.link
```
````

## Материалы, давно не обновлявшиеся

````markdown
```dataview
TABLE file.mtime AS "Изменён", discipline
FROM ""
WHERE file.mtime < date(today) - dur(180 days) AND discipline != "meta"
SORT file.mtime ASC
```
````
