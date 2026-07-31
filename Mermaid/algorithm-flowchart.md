# Блок-схема алгоритма

Шаблон для описания последовательности шагов с ветвлениями и циклом. Скопируйте блок целиком, включая первую строку с директивой — без неё диаграмма отрисуется чужими цветами.

Ветви условия обязаны быть подписаны (`ENF-DIAG-043`): без подписей читателю приходится угадывать, какая ветвь означает «да».

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
flowchart TD
    START([Начало]) --> INIT[Задать начальное приближение]
    INIT --> STEP[Вычислить очередное приближение]
    STEP --> CHECK{Критерий<br/>остановки?}
    CHECK -->|нет| STEP
    CHECK -->|да| OUT[Вернуть результат]
    OUT --> END([Конец])

    classDef variable fill:#E3EDF4,stroke:#1D5B85,stroke-width:2px,color:#1A1D21;
    classDef function fill:#F6EBDC,stroke:#8A5214,stroke-width:2px,color:#1A1D21;
    classDef target fill:#F7E2E8,stroke:#7A0A2C,stroke-width:2px,color:#1A1D21;

    class START,END variable;
    class INIT,STEP,OUT function;
    class CHECK target;
```
````

## Что здесь важно

**Направление `TD`** — сверху вниз, как читается алгоритм. Направления `BT` и `RL` противоречат привычке чтения (`ENF-DIAG-042`).

**Форма узла несёт смысл.** Скруглённый `([...])` — начало и конец, прямоугольник `[...]` — действие, ромб `{...}` — условие. Форма дублирует цвет и делает схему понятной в чёрно-белой печати (`ENF-DIAG-032`).

**Перенос строки внутри узла** — `<br/>`. Длинная подпись в один ряд растягивает всю схему по горизонтали.

**Не более пятнадцати узлов** (`ENF-DIAG-044`). Схема крупнее не помещается в полосу PDF читаемым кеглем; делите на обзорную схему и детализацию блоков.
