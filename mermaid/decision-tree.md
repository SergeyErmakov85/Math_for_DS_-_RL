# Дерево решений

Шаблон для классификации по последовательности признаков и для схем выбора метода.

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
flowchart TD
    ROOT{Признак 1<br/>больше порога?}
    ROOT -->|да| N1{Признак 2<br/>больше порога?}
    ROOT -->|нет| N2{Признак 3<br/>больше порога?}

    N1 -->|да| L1[Класс A]
    N1 -->|нет| L2[Класс B]
    N2 -->|да| L3[Класс B]
    N2 -->|нет| L4[Класс C]

    classDef node fill:#E3EDF4,stroke:#1D5B85,stroke-width:2px,color:#1A1D21;
    classDef leaf fill:#F7E2E8,stroke:#7A0A2C,stroke-width:2px,color:#1A1D21;

    class ROOT,N1,N2 node;
    class L1,L2,L3,L4 leaf;
```
````

## Вариант: выбор метода

Тот же шаблон удобен для схем «какой метод применять».

````markdown
```mermaid
%%{init: {'theme':'base','themeVariables':{"fontFamily":"Inter, 'PT Sans', system-ui, sans-serif","fontSize":"15px","background":"#FFFFFF","primaryColor":"#E3EDF4","primaryTextColor":"#1A1D21","primaryBorderColor":"#1D5B85","secondaryColor":"#F6EBDC","secondaryTextColor":"#1A1D21","secondaryBorderColor":"#8A5214","tertiaryColor":"#E6F1E5","tertiaryTextColor":"#1A1D21","tertiaryBorderColor":"#3E7D3A","lineColor":"#414A54","textColor":"#1A1D21","mainBkg":"#E3EDF4","nodeBorder":"#1D5B85","nodeTextColor":"#1A1D21","clusterBkg":"#FFFFFF","clusterBorder":"#D3D9DF","edgeLabelBackground":"#FFFFFF","titleColor":"#1A1D21"}}}%%
flowchart TD
    Q1{Модель среды<br/>известна?}
    Q1 -->|да| Q2{Пространство<br/>состояний малое?}
    Q1 -->|нет| Q3{Нужна оценка<br/>политики или управление?}

    Q2 -->|да| M1[Динамическое программирование]
    Q2 -->|нет| M2[Приближённое ДП]
    Q3 -->|оценка| M3[Метод временных различий]
    Q3 -->|управление| M4[Q-Learning или SARSA]

    classDef q fill:#F6EBDC,stroke:#8A5214,stroke-width:2px,color:#1A1D21;
    classDef m fill:#E6F1E5,stroke:#3E7D3A,stroke-width:2px,color:#1A1D21;

    class Q1,Q2,Q3 q;
    class M1,M2,M3,M4 m;
```
````

## Что здесь важно

**Условие формулируется как вопрос с однозначным ответом.** «Признак 1 больше порога?» допускает «да» и «нет»; «Проверка признака 1» не допускает ничего.

**Листья визуально отличаются от узлов ветвления** — и формой, и цветом. Читатель должен видеть, где дерево заканчивается, не разбирая связи.

**Подписи ветвей не ограничены парой «да/нет»**: во втором примере это «оценка» и «управление». Главное, чтобы подпись была.
