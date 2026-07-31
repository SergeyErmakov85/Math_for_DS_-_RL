<!-- ПОРОЖДЁННЫЙ ФАЙЛ — НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ.
     Источник: Build/css/enf-tokens.css
     Генератор: Scripts/gen-mermaid-init.mjs
     Пересоздать: node Scripts/gen-mermaid-init.mjs -->

# Единый init-блок Mermaid

Директива ниже подключает палитру ENF. Она вставляется **первой строкой** каждой диаграммы фреймворка.

Mermaid не поддерживает внешние файлы тем: цвета обязаны находиться в тексте диаграммы. Поэтому директива порождается из единого источника, а не пишется руками — правка цвета прямо в диаграмме потеряется при следующей генерации (`ENF-DIAG-041`).

## Директива

```text
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
```

## Классы ролей

Узлы окрашиваются не литералами, а классами, имена которых совпадают с ролями палитры. Добавьте нужные строки в конец диаграммы и примените классы через `class`:

```text
    classDef variable fill:#E3EDF4,stroke:#1D5B85,stroke-width:2px,color:#1A1D21;
    classDef function fill:#F6EBDC,stroke:#8A5214,stroke-width:2px,color:#1A1D21;
    classDef parameter fill:#E6F1E5,stroke:#3E7D3A,stroke-width:2px,color:#1A1D21;
    classDef operator fill:#F7E4F8,stroke:#A32EAD,stroke-width:2px,color:#1A1D21;
    classDef target fill:#F7E2E8,stroke:#7A0A2C,stroke-width:2px,color:#1A1D21;
    classDef neutral fill:#ECEFF2,stroke:#414A54,stroke-width:2px,color:#1A1D21;
```

Применение:

```text
    class A,B variable;
    class C function;
```

## Почему используется светлая палитра

Директива одна на диаграмму, а тем две. Разрешается это тем, что диаграмма задаёт собственный фон и не наследует фон страницы: светлые заливки с тёмным текстом читаются одинаково в светлой и тёмной теме. Требование `ENF-COLOR-032` выполняется по построению — диаграмма не зависит от темы, а не подстраивается под неё.

## Проверка

```powershell
node Scripts/gen-mermaid-init.mjs      # пересоздать директивы
node Scripts/check-colors.mjs Mermaid/ # цвета вне палитры
```
