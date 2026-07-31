# Жизненный цикл: состояния и переходы

Шаблон на `stateDiagram-v2` — единственном типе диаграмм состояний, поддержанном и Obsidian, и Pandoc.

## Состояния процесса

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
stateDiagram-v2
    [*] --> Инициализация
    Инициализация --> Обучение: данные загружены
    Обучение --> Валидация: эпоха завершена
    Валидация --> Обучение: качество растёт
    Валидация --> Остановка: качество не растёт 5 эпох
    Обучение --> Остановка: исчерпан лимит эпох
    Остановка --> [*]
```
````

## Эпизод в обучении с подкреплением

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
stateDiagram-v2
    [*] --> Начальное
    Начальное --> Промежуточное: агент выбрал действие
    Промежуточное --> Промежуточное: переход без завершения
    Промежуточное --> Терминальное: достигнута цель
    Промежуточное --> Терминальное: исчерпан лимит шагов
    Терминальное --> [*]

    note right of Промежуточное
        Награда начисляется
        на каждом переходе
    end note
```
````

## Что здесь важно

**`[*]` обозначает начало и конец** — это встроенный синтаксис, отдельных узлов создавать не нужно.

**Каждый переход подписан условием.** Диаграмма состояний без подписей на переходах не сообщает главного: что именно вызывает смену состояния.

**Петля на состоянии** (`Промежуточное --> Промежуточное`) показывает, что процесс может оставаться в состоянии произвольно долго. Это важное свойство, и пропускать его не следует.

**Заметки через `note`** — для пояснений, которые не привязаны к конкретному переходу. Не злоупотребляйте: больше двух заметок на диаграмму означает, что пояснение стоит вынести в текст.

## Ограничение

Вложенные состояния (`state X { ... }`) в Mermaid поддерживаются, но по-разному рендерятся в разных версиях. Во фреймворке они не используются: сложную иерархию состояний надёжнее показать двумя диаграммами — обзорной и детальной.
