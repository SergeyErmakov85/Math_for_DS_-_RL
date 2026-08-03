# Графы

Шаблоны для ориентированных, взвешенных и двудольных графов.

## Ориентированный граф

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
flowchart LR
    A((A)) --> B((B))
    A --> C((C))
    B --> D((D))
    C --> D
    D --> E((E))

    classDef v fill:#E3EDF4,stroke:#1D5B85,stroke-width:2px,color:#1A1D21;
    class A,B,C,D,E v;
```
````

## Взвешенный граф

Вес пишется подписью ребра — отдельного механизма для весов в Mermaid нет.

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
flowchart LR
    A((A)) -->|4| B((B))
    A -->|2| C((C))
    C -->|1| B
    B -->|5| D((D))
    C -->|8| D

    classDef v fill:#E3EDF4,stroke:#1D5B85,stroke-width:2px,color:#1A1D21;
    class A,B,C,D v;
```
````

## Двудольный граф

Разделение на доли делается подграфами; принадлежность доле дублируется цветом.

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
flowchart LR
    subgraph L[Доля X]
        X1((x₁))
        X2((x₂))
        X3((x₃))
    end
    subgraph R[Доля Y]
        Y1((y₁))
        Y2((y₂))
    end

    X1 --- Y1
    X2 --- Y1
    X2 --- Y2
    X3 --- Y2

    classDef left  fill:#E3EDF4,stroke:#1D5B85,stroke-width:2px,color:#1A1D21;
    classDef right fill:#F6EBDC,stroke:#8A5214,stroke-width:2px,color:#1A1D21;

    class X1,X2,X3 left;
    class Y1,Y2 right;
```
````

## Неориентированное ребро

`---` вместо `-->`. В двудольном графе выше использовано именно оно: стрелка подразумевала бы направление, которого в задаче о паросочетании нет.

## Что здесь важно

**Круглые узлы `((...))` для вершин графа** — они отличают граф от блок-схемы, где узлы прямоугольные. Читатель распознаёт тип диаграммы до того, как прочтёт подписи.

**Направление `LR` для графов** — вертикальная раскладка графа в узкой полосе PDF даёт длинные пересекающиеся рёбра.

**Mermaid раскладывает узлы сам.** Если расположение вершин существенно — например, показывается планарность или геометрическая структура — используйте SVG, а не Mermaid.
