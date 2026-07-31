---
title: "Предел функции"
enf_mode: learning
discipline: calculus
tags: [calculus, limits]
source: "predel-funktsii.pdf, с. 1–3"
---

# Предел функции

## Обозначения

| Символ | Значение | Роль |
|---|---|---|
| $x$ | аргумент функции | `variable` |
| $a$ | точка, в окрестности которой исследуется функция | `variable` |
| $f$, $g$, $h$ | исследуемые функции | `function` |
| $L$, $M$ | предельные значения | `target` |
| $\varepsilon$, $\delta$ | положительные величины, задающие точность | `parameter` |
| $\lim$ | оператор предела | `operator` |

В формулах ниже $\enfVar{x}$ и $\enfVar{a}$ обозначают объекты исследования, $\enfFun{f}$, $\enfFun{g}$ и $\enfFun{h}$ — функции, $\enfPar{\varepsilon}$ и $\enfPar{\delta}$ — параметры точности, $\enfTgt{L}$ и $\enfTgt{M}$ — искомые предельные значения, а $\enfOp{\lim}$ — оператор предела.

## Неформальная идея

Предел описывает поведение функции $\enfFun{f}(\enfVar{x})$ вблизи некоторой точки $\enfVar{a}$ независимо от значения функции в самой точке $\enfVar{a}$, даже если функция там не определена. Говорят, что предел функции $\enfFun{f}(\enfVar{x})$ при $\enfVar{x} \to \enfVar{a}$ равен $\enfTgt{L}$, если значения $\enfFun{f}(\enfVar{x})$ можно сделать сколь угодно близкими к $\enfTgt{L}$, взяв $\enfVar{x}$ достаточно близко к $\enfVar{a}$.

## Формальное определение по Коши

Пусть функция $\enfFun{f}$ определена в некоторой проколотой окрестности точки $\enfVar{a}$.

> [!definition] Определение. Предел функции по Коши, «$\varepsilon$–$\delta$»
> Говорят, что
> $$
> \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}} \enfFun{f}(\enfVar{x}) = \enfTgt{L},
> $$
> если для любого $\enfPar{\varepsilon} > 0$ существует $\enfPar{\delta} > 0$ такое, что для всех $\enfVar{x}$, удовлетворяющих условию
> $$
> 0 < |\enfVar{x} - \enfVar{a}| < \enfPar{\delta},
> $$
> выполняется неравенство
> $$
> |\enfFun{f}(\enfVar{x}) - \enfTgt{L}| < \enfPar{\varepsilon}.
> $$

Запись $0 < |\enfVar{x} - \enfVar{a}|$ означает, что сама точка $\enfVar{x} = \enfVar{a}$ исключается: нас интересует только поведение функции вблизи $\enfVar{a}$, но не в ней.

## Односторонние пределы

Предел существует тогда и только тогда, когда существуют и совпадают левый и правый пределы:

$$
\enfOp{\lim}_{\enfVar{x} \to \enfVar{a}^{-}} \enfFun{f}(\enfVar{x})
= \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}^{+}} \enfFun{f}(\enfVar{x})
= \enfTgt{L}.
$$

## Пример: классический предел синуса

Вычислим

$$
\enfOp{\lim}_{\enfVar{x} \to 0} \frac{\enfFun{\sin} \enfVar{x}}{\enfVar{x}}.
$$

В точке $\enfVar{x} = 0$ выражение не определено из-за деления на ноль. Однако при $\enfVar{x} \to 0$ числитель $\enfFun{\sin} \enfVar{x} \approx \enfVar{x}$, поэтому интуитивно дробь стремится к $1$.

Строгое обоснование опирается на геометрическое неравенство: при $0 < \enfVar{x} < \pi / 2$

$$
\cos \enfVar{x} < \frac{\enfFun{\sin} \enfVar{x}}{\enfVar{x}} < 1.
$$

Так как

$$
\enfOp{\lim}_{\enfVar{x} \to 0} \cos \enfVar{x} = 1,
$$

то по теореме о сжатой переменной, также называемой теоремой о «двух милиционерах»,

$$
\enfOp{\lim}_{\enfVar{x} \to 0} \frac{\enfFun{\sin} \enfVar{x}}{\enfVar{x}} = 1.
$$

## Ключевые свойства пределов

Если

$$
\enfOp{\lim}_{\enfVar{x} \to \enfVar{a}} \enfFun{f}(\enfVar{x}) = \enfTgt{L}
\quad \text{и} \quad
\enfOp{\lim}_{\enfVar{x} \to \enfVar{a}} \enfFun{g}(\enfVar{x}) = \enfTgt{M},
$$

то выполняются следующие свойства.

- **Сумма:**

  $$
  \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}}
  \bigl(\enfFun{f}(\enfVar{x}) + \enfFun{g}(\enfVar{x})\bigr)
  = \enfTgt{L} + \enfTgt{M}.
  $$

- **Произведение:**

  $$
  \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}}
  \bigl(\enfFun{f}(\enfVar{x}) \cdot \enfFun{g}(\enfVar{x})\bigr)
  = \enfTgt{L} \cdot \enfTgt{M}.
  $$

- **Частное:**

  $$
  \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}}
  \frac{\enfFun{f}(\enfVar{x})}{\enfFun{g}(\enfVar{x})}
  = \frac{\enfTgt{L}}{\enfTgt{M}},
  \qquad \enfTgt{M} \ne 0.
  $$

- **Теорема о сжатой переменной:** если $\enfFun{h}(\enfVar{x}) \leq \enfFun{f}(\enfVar{x}) \leq \enfFun{g}(\enfVar{x})$ и

  $$
  \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}} \enfFun{h}(\enfVar{x})
  = \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}} \enfFun{g}(\enfVar{x})
  = \enfTgt{L},
  $$

  то

  $$
  \enfOp{\lim}_{\enfVar{x} \to \enfVar{a}} \enfFun{f}(\enfVar{x}) = \enfTgt{L}.
  $$

## Задачи для самостоятельной работы

### Пример 1. Разложение на множители

Вычислите

$$
\enfOp{\lim}_{\enfVar{x} \to 2} \frac{\enfVar{x}^2 - 4}{\enfVar{x} - 2}.
$$

> [!intuition] Подсказка
> Разложите разность квадратов:
> $$
> \enfVar{x}^2 - 4 = (\enfVar{x} - 2)(\enfVar{x} + 2).
> $$
> Сокращение допустимо, поскольку при вычислении предела рассматриваются значения $\enfVar{x} \ne 2$.

> [!example] Решение
> Для $\enfVar{x} \ne 2$
> $$
> \frac{\enfVar{x}^2 - 4}{\enfVar{x} - 2}
> = \frac{(\enfVar{x} - 2)(\enfVar{x} + 2)}{\enfVar{x} - 2}
> = \enfVar{x} + 2.
> $$
> Следовательно,
> $$
> \enfOp{\lim}_{\enfVar{x} \to 2} \frac{\enfVar{x}^2 - 4}{\enfVar{x} - 2}
> = \enfOp{\lim}_{\enfVar{x} \to 2} (\enfVar{x} + 2)
> = 4.
> $$

### Пример 2. Умножение на сопряжённое выражение

Вычислите

$$
\enfOp{\lim}_{\enfVar{x} \to 0}
\frac{\sqrt{\enfVar{x} + 1} - 1}{\enfVar{x}}.
$$

> [!intuition] Подсказка
> Умножьте числитель и знаменатель на сопряжённое выражение $\sqrt{\enfVar{x} + 1} + 1$.

> [!example] Решение
> Для $\enfVar{x} \ne 0$
> $$
> \begin{aligned}
> \frac{\sqrt{\enfVar{x} + 1} - 1}{\enfVar{x}}
> &= \frac{\sqrt{\enfVar{x} + 1} - 1}{\enfVar{x}}
> \cdot \frac{\sqrt{\enfVar{x} + 1} + 1}{\sqrt{\enfVar{x} + 1} + 1} \\
> &= \frac{\enfVar{x}}{\enfVar{x}\bigl(\sqrt{\enfVar{x} + 1} + 1\bigr)} \\
> &= \frac{1}{\sqrt{\enfVar{x} + 1} + 1}.
> \end{aligned}
> $$
> Поэтому
> $$
> \enfOp{\lim}_{\enfVar{x} \to 0}
> \frac{\sqrt{\enfVar{x} + 1} - 1}{\enfVar{x}}
> = \frac{1}{\sqrt{1} + 1}
> = \frac{1}{2}.
> $$

### Пример 3. Проверка односторонних пределов

Исследуйте предел

$$
\enfOp{\lim}_{\enfVar{x} \to 0} \frac{|\enfVar{x}|}{\enfVar{x}}.
$$

> [!intuition] Подсказка
> Раскройте модуль отдельно при $\enfVar{x} > 0$ и при $\enfVar{x} < 0$, а затем сравните правый и левый пределы.

> [!example] Решение
> Если $\enfVar{x} > 0$, то $|\enfVar{x}| = \enfVar{x}$, поэтому
> $$
> \enfOp{\lim}_{\enfVar{x} \to 0^{+}} \frac{|\enfVar{x}|}{\enfVar{x}} = 1.
> $$
> Если $\enfVar{x} < 0$, то $|\enfVar{x}| = -\enfVar{x}$, поэтому
> $$
> \enfOp{\lim}_{\enfVar{x} \to 0^{-}} \frac{|\enfVar{x}|}{\enfVar{x}} = -1.
> $$
> Левый и правый пределы не совпадают, следовательно, двусторонний предел не существует.

## Вопросы к источнику

- В строгом обосновании предела $\sin x / x$ не указан переход от неравенства для $0 < x < \pi / 2$ к двустороннему пределу при $x \to 0$. Для полного доказательства требуется отдельно использовать чётность функции $\sin x / x$.
