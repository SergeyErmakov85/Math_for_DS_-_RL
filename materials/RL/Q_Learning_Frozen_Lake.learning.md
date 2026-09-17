---
title: "Q-Learning на табличном Frozen Lake"
enf_mode: learning
discipline: rl
tags: [rl, q-learning, tabular-method, frozen-lake, python]
duration: 90
code_python: "3.12"
code_requires: ["numpy>=2.0"]
code_level: basic
code_seed: 7
code_runnable: true
---

# Q-Learning на табличном Frozen Lake

## Зачем это нужно

Q-Learning — табличный метод (*tabular method*) обучения с подкреплением
(*reinforcement learning*, RL). Он подходит для задач, где состояний и
действий настолько мало, что для каждой их пары можно хранить отдельное
число. На поле Frozen Lake агент должен найти безопасный путь по льду к цели,
не попав в лунку. За каждый ход он видит только новое состояние
$\enfVar{s}'$ и награду $\enfTgt{r}$, но заранее не знает, какие действия
приведут к цели.

Этот урок показывает полный цикл: от одной формулы обновления до обучения
таблицы и проверки найденной политики. Каждая формула урока переведена в код
по частям, в таблицах «формула → код». Мы используем детерминированную
версию поля 4×4, поэтому результаты воспроизводимы, а код не требует
внешней среды или скрытых зависимостей.

## Обозначения

**Таблица 1. Обозначения Q-Learning.**

| Символ | Значение | Роль |
|---|---|---|
| $\enfVar{s}$, $\enfVar{s}'$ | текущее и следующее состояния (*state*) | `variable` |
| $\enfVar{d}$ | индикатор терминального перехода: 1 для лунки или цели, иначе 0 | `variable` |
| $\enfVar{\delta}$ | TD-ошибка (*temporal-difference error*) | `variable` |
| $\enfVar{u}$ | случайное число из равномерного распределения на $[0, 1)$ | `variable` |
| $\enfFun{a}$ | выбранное действие (*action*) | `function` |
| $\enfFun{\pi}$ | жадная политика (*greedy policy*): состояние → действие | `function` |
| $\enfPar{\alpha}$ | скорость обучения (*learning rate*) | `parameter` |
| $\enfPar{\gamma}$ | коэффициент дисконтирования (*discount factor*) | `parameter` |
| $\enfPar{\varepsilon}$ | вероятность исследовательского действия | `parameter` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | оценка ценности пары «состояние — действие» (*action-value function*) | `operator` |
| $\enfTgt{r}$ | награда за выполненный переход (*reward*) | `target` |
| $\enfTgt{y}$ | TD-цель (*temporal-difference target*) | `target` |
| $a'$ | действие, по которому берётся $\max$ или $\arg\max$ | нейтральная связанная переменная |
| $k$, $K$, $i$, $j$ | номер эпизода, число эпизодов, строка и столбец клетки | нейтральные индексы |

Символы окрашиваются при каждом появлении. Нейтральной остаётся только
связанная переменная $a'$ под $\max$: она перебирает все действия и не
обозначает конкретное. Если в формуле встречаются все пять ролей, одна из
них остаётся нейтральной, и текст рядом это оговаривает.

## Поле Frozen Lake

Поле состоит из 16 клеток с номерами от 0 до 15, записанных по строкам.
Символ `S` — старт, `F` — безопасный лёд, `H` — лунка, `G` — цель. Агент
получает награду $\enfTgt{r}=1$ только при входе в цель; вход в лунку
завершает эпизод с наградой $\enfTgt{r}=0$. Номер клетки в строке $i$ и
столбце $j$ равен

$$
\enfVar{s} = 4i + j, \qquad i, j \in \{0, 1, 2, 3\}.
$$

**Таблица 2. Карта и кодирование действий.**

| Строка поля | Номера состояний | Действия и номера |
|---|---|---|
| `S F F F` | `0 1 2 3` | `L=0` — влево, `D=1` — вниз |
| `F H F H` | `4 5 6 7` | `R=2` — вправо, `U=3` — вверх |
| `F F F H` | `8 9 10 11` | |
| `H F F G` | `12 13 14 15` | |

> [!intuition] Что значит «обучиться»
>
> Таблица $\enfOp{Q}$ сначала заполнена нулями и не говорит, куда идти.
> Удачный эпизод сообщает агенту, что последнее действие $\enfFun{a}$ перед
> целью полезно. При следующих эпизодах эта информация переносится на
> предыдущее действие, затем ещё на одно. Так ценность цели постепенно
> распространяется назад по пути. В шаге 4 это видно в трассировке.

## Одна TD-цель и одно обновление

После перехода $(\enfVar{s},\enfFun{a},\enfTgt{r},\enfVar{s}')$ агент
строит TD-цель. Множитель $(1-\enfVar{d})$ обнуляет будущую ценность после
терминального перехода:

$$
\enfTgt{y} = \enfTgt{r} + \enfPar{\gamma}(1-\enfVar{d})
\max_{a'} \enfOp{Q}(\enfVar{s}',a').
$$

Здесь $\enfTgt{r}$ — то, что агент получил сразу, а
$\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ — лучшая известная оценка продолжения
из $\enfVar{s}'$. Коэффициент $\enfPar{\gamma}$ уменьшает вес будущего, а
индикатор $\enfVar{d}$ выключает его, когда эпизод закончен.

TD-ошибка показывает, насколько цель расходится с текущей оценкой:

$$
\enfVar{\delta} = \enfTgt{y} - \enfOp{Q}(\enfVar{s},\enfFun{a}).
$$

Затем обновляется только ячейка $\enfOp{Q}(\enfVar{s},\enfFun{a})$
выполненного действия:

$$
\enfOp{Q}(\enfVar{s},\enfFun{a}) \leftarrow
\enfOp{Q}(\enfVar{s},\enfFun{a}) + \enfPar{\alpha}\,\enfVar{\delta}.
$$

Если $\enfVar{\delta}>0$, оценка растёт, если $\enfVar{\delta}<0$ —
уменьшается. Параметр $\enfPar{\alpha}$ задаёт, какую долю ошибки
$\enfVar{\delta}$ ячейка исправит за один шаг.

> [!definition] Определение 1. Обновление Q-Learning
>
> Q-Learning заменяет неизвестное математическое ожидание в уравнении
> Беллмана одной наблюдённой целью $\enfTgt{y}$ и сдвигает старую оценку
> $\enfOp{Q}(\enfVar{s},\enfFun{a})$ в её сторону на долю
> $\enfPar{\alpha}$. В цели берётся максимум по действиям следующего
> состояния, поэтому алгоритм учится оптимальной политике, даже когда
> текущий выбор $\enfFun{a}$ иногда случаен.

### Ручной расчёт последнего шага

Пусть агент находится в состоянии $\enfVar{s}=14$, идёт вправо
($\enfFun{a}=2$) в цель $\enfVar{s}'=15$ и получает $\enfTgt{r}=1$. Переход
терминальный, поэтому $\enfVar{d}=1$. Таблица заполнена нулями,
$\enfPar{\alpha}=0{,}5$, $\enfPar{\gamma}=0{,}9$. Первая строка каждого
расчёта повторяет формулу, во второй подставленные числа сохраняют тон
своих символов.

$$
\begin{aligned}
\enfTgt{y}
  &= \enfTgt{r} + \enfPar{\gamma}(1-\enfVar{d})
     \max_{a'} \enfOp{Q}(\enfVar{s}',a') \\
  &= \enfTgt{1} + \enfPar{0{,}9}(1-\enfVar{1})
     \max_{a'} \enfOp{Q}(\enfVar{15},a') = 1.
\end{aligned}
$$

Будущая ценность исчезает, потому что $1-\enfVar{d}=0$: после цели
продолжения нет.

$$
\begin{aligned}
\enfVar{\delta}
  &= \enfTgt{y} - \enfOp{Q}(\enfVar{s},\enfFun{a}) \\
  &= \enfTgt{1} - \enfOp{Q}(\enfVar{14},\enfFun{2}) = 1 - 0 = 1.
\end{aligned}
$$

$$
\begin{aligned}
\enfOp{Q}(\enfVar{s},\enfFun{a})
  &\leftarrow \enfOp{Q}(\enfVar{s},\enfFun{a})
     + \enfPar{\alpha}\,\enfVar{\delta} \\
  &= \enfOp{0} + \enfPar{0{,}5} \cdot \enfVar{1} = 0{,}5.
\end{aligned}
$$

Ячейка $\enfOp{Q}(\enfVar{14},\enfFun{2})$ прошла половину пути от старой
оценки 0 к цели $\enfTgt{y}=1$ — ровно долю $\enfPar{\alpha}=0{,}5$. Эти же
числа повторит код в шаге 3.

## От формулы к коду

**Таблица 3. Символы и имена в коде.**

| Символ | Смысл | В коде | Тип и форма |
|---|---|---|---|
| $\enfVar{s}$, $\enfVar{s}'$ | номера текущего и следующего состояний | `state`, `next_state` | `int` от 0 до 15 |
| $\enfVar{d}$ | признак завершения эпизода | `terminated` | `bool` |
| $\enfVar{\delta}$ | TD-ошибка | `td_error` | `float` |
| $\enfVar{u}$ | случайное число для выбора режима | `rng.random()` | `float` из $[0, 1)$ |
| $\enfFun{a}$ | номер выбранного действия | `action` | `int` от 0 до 3 |
| $\enfFun{\pi}(\enfVar{s})$ | жадное действие в состоянии $\enfVar{s}$ | `np.argmax(Q[state])` | `int` от 0 до 3 |
| $\enfPar{\alpha}$, $\enfPar{\gamma}$ | параметры обновления | `alpha`, `gamma` | `float` |
| $\enfPar{\varepsilon}$ | вероятность случайного действия | `epsilon` | `float` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | ячейка таблицы оценок | `Q[state, action]` | элемент `np.ndarray` формы `(16, 4)` |
| $\enfOp{Q}(\enfVar{s},\cdot)$ | строка таблицы: оценки всех действий в $\enfVar{s}$ | `Q[state]` | `np.ndarray` формы `(4,)` |
| $\enfTgt{r}$ | награда за переход | `reward` | `float`, 0.0 или 1.0 |
| $\enfTgt{y}$ | TD-цель | `target` | `float` |
| $i$, $j$ | строка и столбец клетки | `row`, `column` | `int` от 0 до 3 |
| $k$, $K$ | номер эпизода и число эпизодов | `k`, `episodes` | `int` |

> [!info] Запятая и точка
>
> В тексте и формулах дробная часть отделяется запятой
> ($\enfPar{\gamma}=0{,}9$), в коде и выводе — только точкой (`0.9`).

### Шаг 1. Данные и воспроизводимость

Один генератор случайных чисел с фиксированным зерном делает обучение
воспроизводимым. При другом зерне изменится порядок исследовательских ходов,
но не правила среды и не формула обновления.

```python
import numpy as np

rng = np.random.default_rng(7)                                    # (1)
np.set_printoptions(precision=3, suppress=True, floatmode="fixed")
```

**Разбор.**

**(1)** `default_rng(7)` создаёт генератор случайных чисел с зерном 7. Все
случайные решения урока — число $\enfVar{u}$ и выбор среди равных действий —
берутся из этого одного объекта `rng`, поэтому весь урок повторяется при
каждом запуске.

### Шаг 2. Детерминированная среда

Функция `step` реализует один ход на поле: переводит номер
$\enfVar{s}=4i+j$ в строку и столбец, сдвигает агента и возвращает
$(\enfVar{s}', \enfTgt{r}, \enfVar{d})$. Выход за границу оставляет агента в
той же клетке; лунка и цель завершают эпизод.

```python
MAP = ("SFFF", "FHFH", "FFFH", "HFFG")
ACTION_NAMES = ("L", "D", "R", "U")
DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))                   # (1)
START_STATE = 0
MAX_STEPS = 100


def step(state: int, action: int) -> tuple[int, float, bool]:
    """Один ход: возвращает (s', r, d)."""
    row, column = divmod(state, 4)                            # (2)
    delta_row, delta_column = DELTAS[action]
    new_row = min(max(row + delta_row, 0), 3)                 # (3)
    new_column = min(max(column + delta_column, 0), 3)
    next_state = 4 * new_row + new_column                     # (4)
    cell = MAP[new_row][new_column]
    terminated = cell in {"H", "G"}                           # (5)
    reward = float(cell == "G")                               # (6)
    return next_state, reward, terminated
```

Проверим последний переход ручного расчёта. Номер действия 2 означает
движение вправо, поэтому из состояния 14 агент попадает в состояние 15.

```python
next_state, reward, terminated = step(14, 2)
print(f"state = {next_state}, reward = {reward:.1f}, "
      f"terminated = {terminated}")
```

```output
state = 15, reward = 1.0, terminated = True
```

Получили $\enfVar{s}'=15$, $\enfTgt{r}=1$ и $\enfVar{d}=1$ — те же
значения, что в ручном расчёте.

**Таблица 4. Переход среды: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{s} = 4i + j$, найти $i$ и $j$ | `row, column = divmod(state, 4)` — частное от деления на 4 даёт строку $i$, остаток — столбец $j$ |
| $i + \Delta i$ с границей $0 \le i \le 3$ | `min(max(row + delta_row, 0), 3)` — шаг за край поля не выполняется, агент остаётся на месте |
| $\enfVar{s}' = 4i' + j'$ | `next_state = 4 * new_row + new_column` — обратный переход от клетки к номеру |
| $\enfVar{d} = 1$, если клетка — лунка или цель | `terminated = cell in {"H", "G"}` — `True` играет роль единицы в $(1-\enfVar{d})$ |
| $\enfTgt{r} = 1$ только в цели | `reward = float(cell == "G")` — `True` превращается в `1.0`, `False` — в `0.0` |
| вся функция: $\enfVar{s},\enfFun{a} \mapsto (\enfVar{s}', \enfTgt{r}, \enfVar{d})$ | `next_state, reward, terminated = step(state, action)` |

**Разбор.**

**(1)** Кортеж сдвигов: элемент с номером действия хранит пару «на сколько
строк, на сколько столбцов». `DELTAS[2]` равно `(0, 1)` — шаг вправо.

**(2)** `divmod(state, 4)` возвращает сразу частное и остаток. Запись
`row, column = ...` раскладывает пару по двум переменным. Для
$\enfVar{s}=14$ получаем строку 3 и столбец 2.

**(3)** Внутренний `max(..., 0)` не пускает номер строки ниже нуля,
внешний `min(..., 3)` — выше трёх. Так моделируется край поля.

**(4)** Формула $\enfVar{s}'=4i'+j'$ дословно.

**(5)** `cell in {"H", "G"}` проверяет принадлежность множеству и сразу
даёт `bool`: это и есть индикатор $\enfVar{d}$.

**(6)** Сравнение `cell == "G"` даёт `True` или `False`, а `float`
превращает его в награду $\enfTgt{r}$: `1.0` или `0.0`.

### Шаг 3. Одно обновление в коде

Переводим три формулы раздела «Одна TD-цель и одно обновление» в одну
функцию и повторяем ручной расчёт: $\enfPar{\alpha}=0{,}5$,
$\enfPar{\gamma}=0{,}9$, переход из $\enfVar{s}=14$ вправо.

```python
def q_update(
    Q: np.ndarray,
    state: int,
    action: int,
    reward: float,
    next_state: int,
    terminated: bool,
    alpha: float,
    gamma: float,
) -> float:
    """Q(s,a) <- Q(s,a) + alpha * delta; возвращает цель y."""
    bootstrap = 0.0 if terminated else Q[next_state].max()  # (1)
    target = reward + gamma * bootstrap                     # (2)
    td_error = target - Q[state, action]                    # (3)
    Q[state, action] += alpha * td_error                    # (4)
    return target
```

```python
Q = np.zeros((16, 4))                                       # (5)
next_state, reward, terminated = step(14, 2)
target = q_update(Q, 14, 2, reward, next_state, terminated,
                  alpha=0.5, gamma=0.9)
print(f"y = {target:.3f}, Q[14, R] = {Q[14, 2]:.3f}")
assert np.isclose(Q[14, 2], 0.5)
```

```output
y = 1.000, Q[14, R] = 0.500
```

Получили $\enfTgt{y}=1$ и $\enfOp{Q}(\enfVar{14},\enfFun{2})=0{,}5$ — как в
ручном расчёте.

**Таблица 5. TD-цель: формула → код.**

| Формула | Python |
|---|---|
| $\enfTgt{r}$ | `reward` — награда, которую вернула `step` за этот переход |
| $\enfOp{Q}(\enfVar{s}',\cdot)$ | `Q[next_state]` — вся строка таблицы для $\enfVar{s}'$, массив из четырёх оценок |
| $\max_{a'} \enfOp{Q}(\enfVar{s}',a')$ | `Q[next_state].max()` — перебор $a'$ по всем действиям скрыт внутри `.max()` |
| $(1-\enfVar{d})\cdot\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `0.0 if terminated else Q[next_state].max()` — умножение на ноль заменено условием: при $\enfVar{d}=1$ максимум даже не вычисляется |
| $\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `gamma * bootstrap` — дисконт применяется к уже обнулённой будущей части |
| вся формула: $\enfTgt{y} = \enfTgt{r} + \enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `target = reward + gamma * bootstrap` |

**Таблица 6. TD-ошибка и обновление: формула → код.**

| Формула | Python |
|---|---|
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `Q[state, action]` — одна ячейка: строка `state`, столбец `action` |
| $\enfVar{\delta} = \enfTgt{y} - \enfOp{Q}(\enfVar{s},\enfFun{a})$ | `td_error = target - Q[state, action]` — ошибка считается до изменения ячейки |
| $\enfPar{\alpha}\,\enfVar{\delta}$ | `alpha * td_error` — доля ошибки, которую исправляет один шаг |
| $\leftarrow$ | `+=` — ячейка меняется на месте, остальные 15 × 4 − 1 ячеек не трогаются |
| вся формула: $\enfOp{Q}(\enfVar{s},\enfFun{a}) \leftarrow \enfOp{Q}(\enfVar{s},\enfFun{a}) + \enfPar{\alpha}\,\enfVar{\delta}$ | `Q[state, action] += alpha * td_error` |

**Разбор.**

**(1)** Условное выражение `A if условие else B` вычисляет `A`, если
условие истинно, иначе `B`. Это множитель $(1-\enfVar{d})$ в виде кода:
после терминального перехода будущая часть равна нулю.

**(2)** TD-цель $\enfTgt{y}$ одной строкой.

**(3)** TD-ошибка $\enfVar{\delta}$. Порядок строк важен: ошибку нужно
посчитать до того, как ячейка изменится в строке (4).

**(4)** Запись `x += v` означает `x = x + v`. Для массива NumPy она
меняет ячейку на месте, поэтому функция ничего не возвращает про таблицу:
вызывающий код видит изменённую `Q`.

**(5)** `np.zeros((16, 4))` создаёт таблицу из 16 строк (состояния) и 4
столбцов (действия), заполненную нулями, — начальное
$\enfOp{Q}(\enfVar{s},\enfFun{a})=0$ для всех пар.

### Шаг 4. Как ценность течёт назад

Повторим три последних перехода безопасного маршрута —
$\enfVar{9} \xrightarrow{\enfFun{D}} \enfVar{13} \xrightarrow{\enfFun{R}} \enfVar{14} \xrightarrow{\enfFun{R}} \enfVar{15}$ — три раза
подряд с $\enfPar{\alpha}=0{,}5$ и $\enfPar{\gamma}=0{,}9$. Так видно, как
награда из цели за несколько проходов доходит до более ранних ячеек.

```python
Q = np.zeros((16, 4))
transitions = ((9, 1), (13, 2), (14, 2))       # (1) пары (s, a)
for episode in range(1, 4):
    for state, action in transitions:          # (2)
        next_state, reward, terminated = step(state, action)
        q_update(Q, state, action, reward, next_state, terminated,
                 alpha=0.5, gamma=0.9)
    print(f"episode {episode}: Q[9, D] = {Q[9, 1]:.4f}, "
          f"Q[13, R] = {Q[13, 2]:.4f}, Q[14, R] = {Q[14, 2]:.4f}")
```

```output
episode 1: Q[9, D] = 0.0000, Q[13, R] = 0.0000, Q[14, R] = 0.5000
episode 2: Q[9, D] = 0.0000, Q[13, R] = 0.2250, Q[14, R] = 0.7500
episode 3: Q[9, D] = 0.1013, Q[13, R] = 0.4500, Q[14, R] = 0.8750
```

**Разбор.**

**(1)** Кортеж пар «состояние, действие» задаёт маршрут. Действия берём из
таблицы 2: `1` — вниз, `2` — вправо.

**(2)** Цикл `for state, action in transitions` на каждой итерации
раскладывает очередную пару по двум переменным. Переходы обрабатываются по
порядку маршрута, поэтому ячейка для $\enfVar{s}=13$ обновляется раньше, чем
ячейка для $\enfVar{s}=14$ в том же проходе.

**Таблица 7. Трассировка обновлений ячейки
$\enfOp{Q}(\enfVar{13},\enfFun{R})$.**

| Проход | $\max_{a'}\enfOp{Q}(\enfVar{14},a')$ до обновления | $\enfTgt{y} = 0 + 0{,}9 \cdot \max$ | `Q[13, R]` до | $\enfVar{\delta}$ | `Q[13, R]` после |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | `0.0000` | `0.0000` | `0.0000` | `0.0000` | `0.0000` |
| 2 | `0.5000` | `0.4500` | `0.0000` | `0.4500` | `0.2250` |
| 3 | `0.7500` | `0.6750` | `0.2250` | `0.4500` | `0.4500` |

В первом проходе $\enfOp{Q}(\enfVar{14},\cdot)$ ещё нулевая, поэтому
ячейка для $\enfVar{s}=13$ не меняется. Во втором проходе она уже «видит»
оценку 0,5, полученную из цели, в третьем ненулевой становится и ячейка
для $\enfVar{s}=9$. Каждый проход переносит информацию о награде на один
шаг назад — именно это описывала выноска «Что значит обучиться».

### Шаг 5. Исследование и использование

$\enfPar{\varepsilon}$-жадная стратегия (*epsilon-greedy strategy*)
сначала тянет случайное число $\enfVar{u}$ и сравнивает его с
$\enfPar{\varepsilon}$:

$$
\enfFun{a} =
\begin{cases}
\text{случайное из } \{0, 1, 2, 3\}, & \enfVar{u} < \enfPar{\varepsilon},\\
\enfOp{\arg\max}_{a'} \enfOp{Q}(\enfVar{s},a'), & \enfVar{u} \ge \enfPar{\varepsilon}.
\end{cases}
$$

С вероятностью $\enfPar{\varepsilon}$ действие $\enfFun{a}$ случайно, в
остальных случаях оно лучшее по таблице $\enfOp{Q}$ в состоянии
$\enfVar{s}$. Если лучших действий несколько, $\enfOp{\arg\max}$ не
определяет выбор однозначно, и мы берём любое из них случайно.

```python
def choose_action(
    Q: np.ndarray,
    state: int,
    epsilon: float,
    rng: np.random.Generator,
) -> int:
    """Epsilon-жадный выбор со случайным разбором ничьих."""
    if rng.random() < epsilon:                                # (1)
        return int(rng.integers(4))                           # (2)
    best_value = Q[state].max()
    best_actions = np.flatnonzero(Q[state] == best_value)     # (3)
    return int(rng.choice(best_actions))                      # (4)
```

Проверим частоты. В строке для $\enfVar{s}=0$ сделаем два лучших действия
`D` и `R` с оценкой 0,5 и выберем действие 1000 раз при
$\enfPar{\varepsilon}=0{,}2$. Случайная ветка выдаёт каждое из четырёх
действий с вероятностью $\enfPar{0{,}2}/4=0{,}05$, жадная — `D` или `R` с
вероятностью $(1-\enfPar{0{,}2})/2=0{,}4$. Ожидаем около 50 выборов `L` и
`U` и около 450 выборов `D` и `R`.

```python
Q_demo = np.zeros((16, 4))
Q_demo[0] = [0.0, 0.5, 0.5, 0.0]
counts = np.zeros(4, dtype=int)
for _ in range(1000):
    counts[choose_action(Q_demo, 0, epsilon=0.2, rng=rng)] += 1
print("counts L, D, R, U =", counts)
```

```output
counts L, D, R, U = [ 51 440 454  55]
```

Частоты близки к ожидаемым 50, 450, 450, 50: код реализует формулу.

**Таблица 8. $\enfPar{\varepsilon}$-жадный выбор: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{u}$ из $[0, 1)$ | `rng.random()` — новое случайное число при каждом вызове |
| условие $\enfVar{u} < \enfPar{\varepsilon}$ | `if rng.random() < epsilon:` — выполняется с вероятностью $\enfPar{\varepsilon}$ |
| случайное из $\{0, 1, 2, 3\}$ | `rng.integers(4)` — верхняя граница 4 не входит, получаем 0, 1, 2 или 3 |
| $\max_{a'} \enfOp{Q}(\enfVar{s},a')$ | `best_value = Q[state].max()` — лучшая оценка в строке |
| $\enfOp{\arg\max}_{a'} \enfOp{Q}(\enfVar{s},a')$ как множество | `np.flatnonzero(Q[state] == best_value)` — номера всех действий с лучшей оценкой |
| выбор из $\enfOp{\arg\max}$ при ничьей | `rng.choice(best_actions)` — `np.argmax` здесь не годится: он всегда вернул бы первый индекс |
| вся формула: $\enfFun{a}$ по $\enfPar{\varepsilon}$-жадному правилу | `action = choose_action(Q, state, epsilon, rng)` |

**Разбор.**

**(1)** Ветка `if` выполняется, только если условие истинно. Случайное
число сравнивается с $\enfPar{\varepsilon}$ — это первая строка формулы.

**(2)** `return` сразу завершает функцию: жадная часть ниже не
выполняется.

**(3)** `Q[state] == best_value` даёт массив из `True` и `False`, а
`np.flatnonzero` возвращает номера позиций с `True`. Для строки
`[0.0, 0.5, 0.5, 0.0]` получится `[1, 2]`.

**(4)** `rng.choice` выбирает один элемент массива равновероятно. `int`
превращает результат NumPy в обычное целое число Python.

### Шаг 6. Обучение таблицы

В эпизоде $k$ вероятность исследования линейно уменьшается от
$\enfPar{\varepsilon}_{\text{start}}=1{,}0$ до
$\enfPar{\varepsilon}_{\text{end}}=0{,}05$:

$$
\enfPar{\varepsilon}_k = \enfPar{\varepsilon}_{\text{start}}
+ \frac{k}{K-1}\bigl(\enfPar{\varepsilon}_{\text{end}}
- \enfPar{\varepsilon}_{\text{start}}\bigr),
\qquad k = 0, \dots, K-1.
$$

При $k=0$ дробь равна нулю и $\enfPar{\varepsilon}_0 =
\enfPar{\varepsilon}_{\text{start}}$, при $k=K-1$ она равна единице и
$\enfPar{\varepsilon}_{K-1} = \enfPar{\varepsilon}_{\text{end}}$. Внутренний
цикл останавливается после терминального перехода или после `MAX_STEPS`
ходов, чтобы ошибка в среде не создала бесконечный эпизод.

```python
def train_q_learning(
    episodes: int,
    alpha: float,
    gamma: float,
    eps_start: float,
    eps_end: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Табличный Q-Learning с линейно убывающим epsilon."""
    Q = np.zeros((16, 4))
    successes = np.zeros(episodes)                            # (1)
    for k in range(episodes):
        epsilon = eps_start + k / (episodes - 1) * (
            eps_end - eps_start)                              # (2)
        state = START_STATE
        for _ in range(MAX_STEPS):                            # (3)
            action = choose_action(Q, state, epsilon, rng)
            next_state, reward, terminated = step(state, action)
            q_update(Q, state, action, reward, next_state,
                     terminated, alpha, gamma)                # (4)
            state = next_state                                # (5)
            if terminated:
                successes[k] = reward                         # (6)
                break
    return Q, successes
```

```python
Q, successes = train_q_learning(
    episodes=6000,
    alpha=0.8,
    gamma=0.95,
    eps_start=1.0,
    eps_end=0.05,
    rng=rng,
)

print(f"successes in last 500 = {successes[-500:].mean():.3f}")
print(f"Q[14, R] = {Q[14, 2]:.3f}")
assert Q.shape == (16, 4)
```

```output
successes in last 500 = 0.882
Q[14, R] = 1.000
```

**Таблица 9. Расписание $\enfPar{\varepsilon}$: формула → код.**

| Формула | Python |
|---|---|
| $k = 0, \dots, K-1$ | `for k in range(episodes):` — `range` не включает `episodes`, последний $k$ равен $K-1$ |
| $\frac{k}{K-1}$ | `k / (episodes - 1)` — доля пройденного обучения от 0 до 1 |
| $\enfPar{\varepsilon}_{\text{end}} - \enfPar{\varepsilon}_{\text{start}}$ | `eps_end - eps_start` — отрицательное число, поэтому $\enfPar{\varepsilon}$ убывает |
| вся формула: $\enfPar{\varepsilon}_k = \enfPar{\varepsilon}_{\text{start}} + \frac{k}{K-1}(\enfPar{\varepsilon}_{\text{end}} - \enfPar{\varepsilon}_{\text{start}})$ | `epsilon = eps_start + k / (episodes - 1) * (eps_end - eps_start)` |

**Таблица 10. Цикл обучения: математика → код.**

| Формула | Python |
|---|---|
| $\enfFun{a}$ по $\enfPar{\varepsilon}_k$-жадному правилу | `action = choose_action(Q, state, epsilon, rng)` — шаг 5 |
| $(\enfVar{s}', \enfTgt{r}, \enfVar{d})$ от среды | `next_state, reward, terminated = step(state, action)` — шаг 2 |
| $\enfOp{Q}(\enfVar{s},\enfFun{a}) \leftarrow \enfOp{Q}(\enfVar{s},\enfFun{a}) + \enfPar{\alpha}\,\enfVar{\delta}$ | `q_update(Q, state, action, reward, next_state, terminated, alpha, gamma)` — шаг 3 |
| $\enfVar{s} \leftarrow \enfVar{s}'$ | `state = next_state` — следующий ход начинается из нового состояния |
| конец эпизода при $\enfVar{d}=1$ | `if terminated: ... break` — внутренний цикл прерывается |

**Разбор.**

**(1)** Массив `successes` хранит по одному числу на эпизод: 1, если
агент дошёл до цели, иначе 0. Среднее по его части — доля успехов.

**(2)** Формула расписания $\enfPar{\varepsilon}_k$. Скобки позволяют
перенести длинное выражение на следующую строку.

**(3)** Переменная `_` означает «номер итерации не нужен»: цикл лишь
ограничивает эпизод сотней ходов.

**(4)** Обновление из шага 3 — та же функция, что повторила ручной расчёт.
Обучение не содержит второй, отдельной реализации формулы.

**(5)** Без этой строки агент бы каждый ход начинал из одного и того же
$\enfVar{s}$.

**(6)** `break` прерывает только внутренний цикл `for _ in ...`, внешний
цикл переходит к следующему эпизоду. Если за `MAX_STEPS` ходов эпизод не
закончился, в `successes[k]` остаётся 0.

Первая строка вывода показывает долю успешных эпизодов в последних 500.
Она меньше 1, потому что $\enfPar{\varepsilon}$ к концу обучения всё ещё
равно 0,05: агент иногда делает случайный ход и может попасть в лунку.
Значение $\enfOp{Q}(\enfVar{14},\enfFun{R})$ равно 1: действие вправо из
состояния 14 сразу приносит $\enfTgt{r}=1$, а после цели
$\enfVar{d}=1$ обнуляет будущую часть, поэтому $\enfTgt{y}=1$ при каждом
обновлении.

### Шаг 7. Извлечение и проверка политики

После обучения исследование отключаем: в каждом состоянии берём действие с
наибольшей оценкой.

$$
\enfFun{\pi}(\enfVar{s}) = \enfOp{\arg\max}_{a'} \enfOp{Q}(\enfVar{s},a').
$$

Функция `greedy_rollout` проходит по полю, следуя $\enfFun{\pi}$, и
возвращает посещённые состояния; лунка или цель прекращают проход.

```python
def greedy_rollout(Q: np.ndarray) -> list[int]:
    """Путь агента по жадной политике pi(s) = argmax_a Q(s, a)."""
    state = START_STATE
    path = [state]                                  # (1)
    for _ in range(MAX_STEPS):
        action = int(np.argmax(Q[state]))           # (2)
        state, reward, terminated = step(state, action)
        path.append(state)                          # (3)
        if terminated:
            return path
    raise RuntimeError("Greedy policy did not terminate")  # (4)


path = greedy_rollout(Q)
print("states =", path)
assert path[-1] == 15
```

```output
states = [0, 4, 8, 9, 13, 14, 15]
```

**Таблица 11. Жадная политика: формула → код.**

| Формула | Python |
|---|---|
| $\enfOp{Q}(\enfVar{s},\cdot)$ | `Q[state]` — строка из четырёх оценок |
| $\enfOp{\arg\max}_{a'}$ | `np.argmax(...)` — номер наибольшего элемента; при ничьей берётся первый |
| $\enfFun{\pi}(\enfVar{s})$ | `action = int(np.argmax(Q[state]))` — детерминированное действие без исследования |
| $\enfVar{s} \leftarrow \enfVar{s}'$ до $\enfVar{d}=1$ | `state, reward, terminated = step(state, action)` в цикле с `return path` |
| вся формула: $\enfFun{\pi}(\enfVar{s}) = \enfOp{\arg\max}_{a'} \enfOp{Q}(\enfVar{s},a')$ | `int(np.argmax(Q[state]))` |

**Разбор.**

**(1)** Список пути начинается со стартового состояния.

**(2)** Здесь первый индекс при ничьей не мешает: после обучения ничья
означает, что оба действия одинаково хороши. Например, в состоянии 0 оценки
`D` и `R` совпадают, и `np.argmax` выбирает `D`.

**(3)** `append` добавляет новое состояние в конец списка.

**(4)** `raise` останавливает программу с сообщением. Если политика ходит
по кругу и не доходит до конца за `MAX_STEPS`, мы узнаем об этом сразу, а
не получим тихо неверный путь.

Это безопасный маршрут из шести ходов. Он идёт вниз до состояния 8, затем
обходит лунку в состоянии 12 справа и приходит к цели через состояния 13 и
14.

**Таблица 12. Сопоставление пути с действиями.**

| Состояние $\enfVar{s}$ | Следующее $\enfVar{s}'$ | $\enfFun{\pi}(\enfVar{s})$ | Причина |
|---:|---:|---|---|
| 0 | 4 | `D` | первый шаг вниз от старта |
| 4 | 8 | `D` | движение вдоль левого края |
| 8 | 9 | `R` | обход лунки 12 |
| 9 | 13 | `D` | безопасный переход вниз |
| 13 | 14 | `R` | движение к цели |
| 14 | 15 | `R` | получение награды $\enfTgt{r}=1$ |

## Типичная ошибка: обучение без исследования

Если начать с нулевой таблицы и всегда применять $\enfOp{\arg\max}$ через
`np.argmax`, библиотека выберет действие `L` с номером 0. На левом краю это
действие не меняет состояние, поэтому агент может бесконечно стоять на
старте и никогда не увидеть цель.

> [!warning] Ошибка: жадный выбор при нулевой таблице
>
> ```python
> Q_zero = np.zeros((16, 4))
> action = int(np.argmax(Q_zero[START_STATE]))
> next_state, _, _ = step(START_STATE, action)
> print(f"action = {ACTION_NAMES[action]}, next state = {next_state}")
> ```
>
> ```output
> action = L, next state = 0
> ```
>
> Здесь `L` означает движение влево, а граница поля удерживает агента в
> состоянии $\enfVar{s}=0$. При $\enfPar{\varepsilon}=0$ таблица
> $\enfOp{Q}$ никогда не получит ненулевой награды $\enfTgt{r}$. Случайные
> действия на ранних эпизодах нужны не для шума, а для получения данных о
> других переходах.

## Упражнения

1. Выполните ручной расчёт для перехода из $\enfVar{s}=13$ вправо в
   $\enfVar{s}'=14$, если $\enfOp{Q}(\enfVar{13},\enfFun{R})=0$,
   $\max_{a'}\enfOp{Q}(\enfVar{14},a')=0{,}8$, $\enfTgt{r}=0$,
   $\enfVar{d}=0$, $\enfPar{\alpha}=0{,}5$ и $\enfPar{\gamma}=0{,}95$.
2. Измените `eps_end` с `0.05` на `0.0`. Как изменится доля успешных
   эпизодов в последнем окне и почему это не доказывает лучшую обученность?
3. Сделайте действие `D` из состояния 8 лункой. Какая часть найденного пути
   станет невозможной и почему таблицу нужно обучать заново?
4. Замените $\enfPar{\alpha}=0{,}5$ на $\enfPar{\alpha}=0{,}1$ в шаге 4.
   Сколько проходов понадобится, чтобы $\enfOp{Q}(\enfVar{9},\enfFun{D})$
   стала ненулевой, и изменится ли это число?

> [!example] Решение упражнения 1
>
> ```python
> old_value = 0.0
> bootstrap = 0.8
> target = 0.0 + 0.95 * bootstrap
> updated_value = old_value + 0.5 * (target - old_value)
> print(f"target = {target:.3f}, Q[13, R] = {updated_value:.3f}")
> ```
>
> ```output
> target = 0.760, Q[13, R] = 0.380
> ```
>
> Переход не терминальный, $\enfVar{d}=0$, поэтому в цель входит будущая
> оценка 0,8, умноженная на $\enfPar{\gamma}=0{,}95$:
> $\enfTgt{y}=0{,}76$. Ошибка $\enfVar{\delta}=0{,}76$, и скорость
> $\enfPar{\alpha}=0{,}5$ сдвигает нулевую оценку на половину расстояния —
> до 0,38.

## Итоги

1. Табличный Q-Learning хранит одну оценку
   $\enfOp{Q}(\enfVar{s},\enfFun{a})$ для каждой пары «состояние —
   действие» и поэтому применим к небольшим дискретным средам.
2. TD-цель $\enfTgt{y}$ складывает немедленную награду $\enfTgt{r}$ и
   лучшую будущую оценку; после терминального перехода $\enfVar{d}=1$
   будущая часть обнуляется.
3. Обновление сдвигает ячейку на долю $\enfPar{\alpha}$ от ошибки
   $\enfVar{\delta}$, и за каждый проход ценность цели продвигается на один
   шаг назад по маршруту.
4. $\enfPar{\varepsilon}$-жадная стратегия даёт агенту новые данные, без
   которых нулевая таблица может никогда не измениться.
5. После обучения жадная политика $\enfFun{\pi}$ на этом поле проходит
   маршрут `0 → 4 → 8 → 9 → 13 → 14 → 15` и достигает цели.

**Таблица 13. Итоговое соответствие формул и кода.**

| Математика | Python |
|---|---|
| $\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `target = reward + gamma * (0.0 if terminated else Q[next_state].max())` |
| $\enfVar{\delta}=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `td_error = target - Q[state, action]` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\,\enfVar{\delta}$ | `Q[state, action] += alpha * td_error` |
| $\enfFun{a}=\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ при $\enfVar{u}\ge\enfPar{\varepsilon}$, иначе случайное | `choose_action(Q, state, epsilon, rng)` с `rng.random() < epsilon` и `rng.choice(best_actions)` |
| $\enfPar{\varepsilon}_k=\enfPar{\varepsilon}_{\text{start}}+\frac{k}{K-1}(\enfPar{\varepsilon}_{\text{end}}-\enfPar{\varepsilon}_{\text{start}})$ | `epsilon = eps_start + k / (episodes - 1) * (eps_end - eps_start)` |
| $\enfFun{\pi}(\enfVar{s})=\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `int(np.argmax(Q[state]))` |
| $\enfVar{s}=4i+j$ | `row, column = divmod(state, 4)` и `4 * new_row + new_column` |

## Что дальше

- [Дисконтированная доходность](Discounted_Return.learning.md) объясняет,
  откуда в TD-цели берётся множитель $\enfPar{\gamma}$.
- [DQN: Q-обучение с нейросетевой аппроксимацией](DQN.learning.md) заменяет
  таблицу $\enfOp{Q}$ нейросетью, когда число состояний слишком велико.
