---
title: "Минимальное решение Frozen Lake методом Q-Learning"
enf_mode: learning
discipline: rl
tags: [rl, q-learning, frozen-lake, python, minimal-example]
duration: 60
code_python: "3.12"
code_requires: ["numpy>=2.0"]
code_level: basic
code_seed: 23
code_runnable: true
---

# Минимальное решение Frozen Lake методом Q-Learning

## Зачем это нужно

Frozen Lake — небольшая задача обучения с подкреплением (*reinforcement
learning*, RL): агент идёт от старта `S` к цели `G`, стараясь не попасть в
лунки `H`. Этот урок оставляет только необходимый минимум: детерминированное
поле 4×4, таблицу оценок, исследование случайными действиями и одно правило
обновления Q-Learning.

Среда написана прямо в уроке, поэтому достаточно NumPy. После выполнения
всех блоков агент находит безопасный маршрут, а каждое число можно связать с
конкретной частью формулы.

## Обозначения

**Таблица 1. Обозначения минимального решения.**

| Символ | Значение | Роль |
|---|---|---|
| $\enfVar{s}$, $\enfVar{s}'$ | текущее и следующее состояния (*state*) | `variable` |
| $\enfVar{d}$ | индикатор конца эпизода: 1 для лунки или цели | `variable` |
| $\enfVar{\delta}$ | TD-ошибка (*temporal-difference error*) | `variable` |
| $\enfVar{u}$ | случайное число из $[0,1)$ | `variable` |
| $\enfFun{a}$ | действие агента (*action*) | `function` |
| $\enfFun{\pi}$ | жадная политика: состояние → действие | `function` |
| $\enfPar{\alpha}$ | скорость обучения (*learning rate*) | `parameter` |
| $\enfPar{\gamma}$ | коэффициент дисконтирования (*discount factor*) | `parameter` |
| $\enfPar{\varepsilon}$ | вероятность случайного действия | `parameter` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | оценка действия в состоянии (*action value*) | `operator` |
| $\enfTgt{r}$ | награда за переход (*reward*) | `target` |
| $\enfTgt{y}$ | TD-цель (*temporal-difference target*) | `target` |
| $a'$ | действие под $\max$ или $\arg\max$ | нейтральная связанная переменная |
| $i$, $j$, $k$, $K$ | строка, столбец, номер и число эпизодов | нейтральные индексы |

Связанная переменная $a'$ нейтральна: она лишь перебирает действия под
$\max$ или $\arg\max$. Индексы тоже нейтральны. Остальные символы сохраняют
назначенный тон при каждом появлении.

## Поле и идея решения

Используем стандартную карту:

```text
S F F F
F H F H
F F F H
H F F G
```

Клетки нумеруются по строкам от 0 до 15. Состояние в строке $i$ и столбце
$j$ равно

$$
\enfVar{s}=4i+j, \qquad i,j\in\{0,1,2,3\}.
$$

Действия кодируются числами: `L=0`, `D=1`, `R=2`, `U=3`. За вход в цель
агент получает $\enfTgt{r}=1$; в остальных случаях $\enfTgt{r}=0$. Лунка и
цель завершают эпизод, то есть дают $\enfVar{d}=1$.

> [!intuition] Что хранит таблица
>
> Строка $\enfOp{Q}(\enfVar{s},\cdot)$ содержит четыре оценки — по одной
> для каждого действия в состоянии $\enfVar{s}$. Сначала все оценки равны
> нулю. Когда агент достигает цели, награда $\enfTgt{r}=1$ повышает оценку
> последнего действия; повторные эпизоды переносят эту информацию назад.

## Формула Q-Learning

Для перехода из $\enfVar{s}$ действием $\enfFun{a}$ в $\enfVar{s}'$ сначала
строится TD-цель:

$$
\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})
\max_{a'}\enfOp{Q}(\enfVar{s}',a').
$$

Немедленная награда $\enfTgt{r}$ известна после хода. Максимум выбирает
лучшую известную оценку продолжения, $\enfPar{\gamma}$ уменьшает её вес, а
$1-\enfVar{d}$ обнуляет продолжение после конца эпизода.

Расхождение цели и старой оценки — TD-ошибка:

$$
\enfVar{\delta}=\enfTgt{y}-
\enfOp{Q}(\enfVar{s},\enfFun{a}).
$$

Затем меняется одна ячейка таблицы:

$$
\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow
\enfOp{Q}(\enfVar{s},\enfFun{a})+
\enfPar{\alpha}\,\enfVar{\delta}.
$$

> [!definition] Определение 1. Табличный Q-Learning
>
> Q-Learning сдвигает оценку $\enfOp{Q}(\enfVar{s},\enfFun{a})$ к цели
> $\enfTgt{y}$ на долю $\enfPar{\alpha}$. Максимум в цели не зависит от
> фактически выбранного следующего действия, поэтому метод учится жадной
> целевой политике, даже если поведение иногда случайно.

### Ручной расчёт

Рассмотрим последний ход: $\enfVar{s}=14$, $\enfFun{a}=2$ (`R`),
$\enfVar{s}'=15$, $\enfTgt{r}=1$, $\enfVar{d}=1$. Пусть старая оценка
равна нулю, $\enfPar{\alpha}=0{,}5$, $\enfPar{\gamma}=0{,}9$. Сначала
подставим числа в TD-цель; числа наследуют тон соответствующих символов:

$$
\begin{aligned}
\enfTgt{y}
&=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})
  \max_{a'}\enfOp{Q}(\enfVar{s}',a')\\
&=\enfTgt{1}+\enfPar{0{,}9}(1-\enfVar{1})
  \max_{a'}\enfOp{Q}(\enfVar{15},a')=1.
\end{aligned}
$$

Поскольку $1-\enfVar{d}=0$, будущая оценка не влияет на результат. Теперь
ошибка равна

$$
\begin{aligned}
\enfVar{\delta}
&=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})\\
&=\enfTgt{1}-\enfOp{Q}(\enfVar{14},\enfFun{2})=1.
\end{aligned}
$$

Обновление сдвигает нулевую оценку на половину ошибки:

$$
\begin{aligned}
\enfOp{Q}(\enfVar{s},\enfFun{a})
&\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+
  \enfPar{\alpha}\,\enfVar{\delta}\\
&=\enfOp{0}+\enfPar{0{,}5}\cdot\enfVar{1}=0{,}5.
\end{aligned}
$$

## От формулы к коду

**Таблица 2. Символы и имена в Python.**

| Символ | Смысл | В коде | Тип и форма |
|---|---|---|---|
| $\enfVar{s}$, $\enfVar{s}'$ | номера клеток | `state`, `next_state` | `int` от 0 до 15 |
| $\enfVar{d}$ | конец эпизода | `terminated` | `bool` |
| $\enfVar{\delta}$ | TD-ошибка | `td_error` | `float` |
| $\enfVar{u}$ | случайное число | `rng.random()` | `float` из $[0,1)$ |
| $\enfFun{a}$ | номер действия | `action` | `int` от 0 до 3 |
| $\enfFun{\pi}(\enfVar{s})$ | жадное действие | `np.argmax(Q[state])` | `int` от 0 до 3 |
| $\enfPar{\alpha}$ | скорость обновления | `alpha` | `float` |
| $\enfPar{\gamma}$ | вес будущей оценки | `gamma` | `float` |
| $\enfPar{\varepsilon}$ | вероятность исследования | `epsilon` | `float` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | одна оценка | `Q[state, action]` | элемент массива `(16, 4)` |
| $\enfTgt{r}$ | награда | `reward` | `float`, 0.0 или 1.0 |
| $\enfTgt{y}$ | TD-цель | `target` | `float` |

> [!info] Запятая и точка
>
> В формулах пишем $\enfPar{0{,}9}$, а в Python и выводе — `0.9`.

### Шаг 1. Задаём поле

Первый блок подключает NumPy, создаёт единственный генератор случайных чисел
и записывает карту. Фиксированное зерно делает дальнейший вывод
воспроизводимым.

```python
import numpy as np

rng = np.random.default_rng(23)                         # (1)
np.set_printoptions(precision=3, suppress=True, floatmode="fixed")

MAP = ("SFFF", "FHFH", "FFFH", "HFFG")
ACTION_NAMES = ("L", "D", "R", "U")
DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))             # (2)
START_STATE = 0
MAX_STEPS = 100
print("map =", "/".join(MAP))
```

```output
map = SFFF/FHFH/FFFH/HFFG
```

**Разбор.**

**(1)** `default_rng(23)` создаёт генератор `rng`. При другом зерне
изменятся исследовательские ходы, но формулы и карта останутся прежними.

**(2)** `DELTAS[action]` хранит изменение строки и столбца. Например,
`DELTAS[2]` равно `(0, 1)`, поэтому действие $\enfFun{a}=2$ сдвигает
агента вправо.

### Шаг 2. Реализуем один переход

Функция переводит номер $\enfVar{s}=4i+j$ в координаты, выполняет
$\enfFun{a}$ и возвращает $(\enfVar{s}',\enfTgt{r},\enfVar{d})$. На границе
координата прижимается к диапазону от 0 до 3.

```python
def step(state: int, action: int) -> tuple[int, float, bool]:
    """Один ход среды: возвращает (s', r, d)."""
    row, column = divmod(state, 4)                         # (1)
    delta_row, delta_column = DELTAS[action]
    new_row = min(max(row + delta_row, 0), 3)              # (2)
    new_column = min(max(column + delta_column, 0), 3)
    next_state = 4 * new_row + new_column                  # (3)
    cell = MAP[new_row][new_column]
    terminated = cell in {"H", "G"}                      # (4)
    reward = float(cell == "G")
    return next_state, reward, terminated


next_state, reward, terminated = step(14, 2)
print(next_state, reward, terminated)
```

```output
15 1.0 True
```

**Таблица 3. Переход среды: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{s}=4i+j$ | `row, column = divmod(state, 4)` — частное даёт $i$, остаток даёт $j$ |
| $0\le i',j'\le3$ | `min(max(..., 0), 3)` — попытка выйти за край оставляет координату на границе |
| $\enfVar{s}'=4i'+j'$ | `next_state = 4 * new_row + new_column` — координаты снова становятся номером клетки |
| $\enfVar{d}=1$ для `H` или `G` | `terminated = cell in {"H", "G"}` — проверяются обе терминальные клетки |
| $\enfTgt{r}=1$ только для `G` | `reward = float(cell == "G")` — логическое значение превращается в 1.0 или 0.0 |
| вся функция: $\enfVar{s},\enfFun{a}\mapsto(\enfVar{s}',\enfTgt{r},\enfVar{d})$ | `next_state, reward, terminated = step(state, action)` — один вызов выполняет переход |

**Разбор.**

**(1)** `divmod` одновременно возвращает частное и остаток от деления на 4.
Для $\enfVar{s}=14$ это строка 3 и столбец 2.

**(2)** Вложенные `max` и `min` реализуют границы поля.

**(3)** Это формула $\enfVar{s}'=4i'+j'$ без изменений.

**(4)** `in` проверяет принадлежность множеству. Полученный `bool` играет
роль индикатора $\enfVar{d}$.

Результат $\enfVar{s}'=15$, $\enfTgt{r}=1$, $\enfVar{d}=1$ совпал с
ручным примером.

### Шаг 3. Переводим обновление

Следующая функция буквально реализует TD-цель, ошибку и изменение одной
ячейки. Для терминального перехода будущая часть задаётся нулём.

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
) -> tuple[float, float]:
    """Обновляет Q(s,a) и возвращает (y, delta)."""
    bootstrap = 0.0 if terminated else Q[next_state].max()  # (1)
    target = reward + gamma * bootstrap                     # (2)
    td_error = target - Q[state, action]                    # (3)
    Q[state, action] += alpha * td_error                    # (4)
    return target, td_error
```

Повторим ручной расчёт с $\enfPar{\alpha}=0{,}5$ и
$\enfPar{\gamma}=0{,}9$.

```python
Q_demo = np.zeros((16, 4))
next_state, reward, terminated = step(14, 2)
target, td_error = q_update(
    Q_demo, 14, 2, reward, next_state, terminated,
    alpha=0.5, gamma=0.9,
)
print(f"y = {target:.3f}, delta = {td_error:.3f}, "
      f"Q[14, R] = {Q_demo[14, 2]:.3f}")
assert np.isclose(Q_demo[14, 2], 0.5)
```

```output
y = 1.000, delta = 1.000, Q[14, R] = 0.500
```

**Таблица 4. TD-цель: формула → код.**

| Формула | Python |
|---|---|
| $\enfTgt{r}$ | `reward` — награда только что выполненного перехода |
| $\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `Q[next_state].max()` — `.max()` перебирает четыре действия |
| $(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `0.0 if terminated else Q[next_state].max()` — после конца продолжение равно нулю |
| $\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `gamma * bootstrap` — дисконт применяется к будущей части |
| вся формула: $\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `target = reward + gamma * bootstrap` — полная TD-цель |

**Таблица 5. TD-ошибка и обновление: формула → код.**

| Формула | Python |
|---|---|
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `Q[state, action]` — изменяется ровно одна ячейка |
| $\enfVar{\delta}=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `td_error = target - Q[state, action]` — ошибка считается до изменения ячейки |
| $\enfPar{\alpha}\,\enfVar{\delta}$ | `alpha * td_error` — величина одного сдвига |
| $\leftarrow$ | `+=` — новое значение записывается в ту же ячейку |
| вся формула: $\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\,\enfVar{\delta}$ | `Q[state, action] += alpha * td_error` — полная строка обновления |

**Разбор.**

**(1)** Условное выражение реализует множитель $1-\enfVar{d}$ без
вычисления максимума после завершения эпизода.

**(2)** Здесь строится $\enfTgt{y}$.

**(3)** Ошибка $\enfVar{\delta}$ вычисляется по старому значению ячейки.

**(4)** `+=` сдвигает оценку на $\enfPar{\alpha}\enfVar{\delta}$.

Код получил $\enfTgt{y}=1$, $\enfVar{\delta}=1$ и
$\enfOp{Q}(\enfVar{14},\enfFun{2})=0{,}5$ — ровно числа ручного расчёта.

### Шаг 4. Выбираем действие и обучаемся

Чтобы нулевая таблица получила данные, агент иногда исследует поле. Его
$\enfPar{\varepsilon}$-жадное правило (*epsilon-greedy rule*) имеет вид

$$
\enfFun{a}=
\begin{cases}
\text{случайное действие}, & \enfVar{u}<\enfPar{\varepsilon},\\
\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a'),
& \enfVar{u}\ge\enfPar{\varepsilon}.
\end{cases}
$$

При равных максимумах случайный выбор не отдаёт постоянного предпочтения
действию с наименьшим номером.

```python
def choose_action(
    Q: np.ndarray,
    state: int,
    epsilon: float,
    rng: np.random.Generator,
) -> int:
    """Epsilon-жадное действие со случайным разрешением ничьих."""
    if rng.random() < epsilon:                             # (1)
        return int(rng.integers(4))                        # (2)
    best_value = Q[state].max()
    best_actions = np.flatnonzero(Q[state] == best_value)  # (3)
    return int(rng.choice(best_actions))                   # (4)
```

**Таблица 6. Выбор действия: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{u}\in[0,1)$ | `rng.random()` — новое равномерное число при каждом выборе |
| $\enfVar{u}<\enfPar{\varepsilon}$ | `if rng.random() < epsilon:` — ветка исследования |
| случайное $\enfFun{a}\in\{0,1,2,3\}$ | `rng.integers(4)` — верхняя граница 4 не включается |
| $\max_{a'}\enfOp{Q}(\enfVar{s},a')$ | `Q[state].max()` — лучшая оценка в строке |
| $\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `np.flatnonzero(Q[state] == best_value)` — находятся все лучшие действия |
| вся формула: $\enfFun{a}$ по $\enfPar{\varepsilon}$-жадному правилу | `action = choose_action(Q, state, epsilon, rng)` — выбирается исследование или максимум |

**Разбор.**

**(1)** Сравнение $\enfVar{u}<\enfPar{\varepsilon}$ решает, будет ли ход
исследовательским.

**(2)** `integers(4)` возвращает 0, 1, 2 или 3.

**(3)** `flatnonzero` возвращает номера всех элементов, равных максимуму.

**(4)** `choice` равновероятно выбирает одно из лучших действий.

В минимальном цикле используем постоянные $\enfPar{\alpha}=0{,}8$,
$\enfPar{\gamma}=0{,}95$ и $\enfPar{\varepsilon}=0{,}2$. Каждая итерация
внутреннего цикла делает один переход и одно обновление.

```python
Q = np.zeros((16, 4))
successes = np.zeros(5000)
trace = []
for k in range(5000):                                      # (1)
    state = START_STATE
    for _ in range(MAX_STEPS):                             # (2)
        action = choose_action(Q, state, 0.2, rng)
        next_state, reward, terminated = step(state, action)
        q_update(Q, state, action, reward, next_state,
                 terminated, alpha=0.8, gamma=0.95)         # (3)
        state = next_state
        if terminated:
            successes[k] = reward                          # (4)
            break
    if k in {0, 499, 1999, 4999}:
        trace.append((k + 1, successes[:k + 1].sum()))

print("trace =", trace)
print(f"success rate, last 500 = {successes[-500:].mean():.3f}")
```

```output
trace = [(1, 0.0), (500, 338.0), (2000, 1505.0), (5000, 3841.0)]
success rate, last 500 = 0.776
```

**Таблица 7. Трассировка обучения.**

| Эпизоды $K$ | Успешных эпизодов | Накопленная доля успехов |
|---:|---:|---:|
| 1 | `0` | `0.000` |
| 500 | `338` | `0.676` |
| 2000 | `1505` | `0.752` |
| 5000 | `3841` | `0.768` |

Трассировка показывает накопление данных, а не гарантирует монотонный рост:
при постоянном $\enfPar{\varepsilon}=0{,}2$ агент продолжает делать
случайные ходы и после того, как таблица выучила безопасный путь.

**Разбор.**

**(1)** Внешний цикл создаёт 5000 эпизодов; $k$ — их нейтральный индекс.

**(2)** Ограничение `MAX_STEPS` не позволяет ошибочной политике ходить
бесконечно.

**(3)** После каждого перехода вызывается единственная реализация формулы
обновления.

**(4)** Награда записывается как успех: в цели она равна 1, в лунке — 0.

Последние 500 обучающих эпизодов дали долю успехов `0.776`. Это не качество
жадной политики: в обучении всё ещё действует исследование с
$\enfPar{\varepsilon}=0{,}2$.

### Шаг 5. Проверяем жадную политику

После обучения случайность отключается. Политика выбирает действие

$$
\enfFun{\pi}(\enfVar{s})=
\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a').
$$

```python
state = START_STATE
path = [state]
actions = []
for _ in range(MAX_STEPS):                                  # (1)
    action = int(np.argmax(Q[state]))                        # (2)
    actions.append(ACTION_NAMES[action])
    state, reward, terminated = step(state, action)
    path.append(state)
    if terminated:                                          # (3)
        break

print("path =", path)
print("actions =", actions)
print("reward =", reward)
assert path[-1] == 15 and reward == 1.0
```

```output
path = [0, 4, 8, 9, 13, 14, 15]
actions = ['D', 'D', 'R', 'D', 'R', 'R']
reward = 1.0
```

**Таблица 8. Жадная политика: формула → код.**

| Формула | Python |
|---|---|
| $\enfOp{Q}(\enfVar{s},\cdot)$ | `Q[state]` — четыре оценки текущего состояния |
| $\max_{a'}\enfOp{Q}(\enfVar{s},a')$ | `Q[state].max()` — величина лучшей оценки |
| $\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `np.argmax(Q[state])` — номер первой максимальной оценки |
| $\enfVar{s}\leftarrow\enfVar{s}'$ | `state, reward, terminated = step(state, action)` — следующий ход начинается из новой клетки |
| вся формула: $\enfFun{\pi}(\enfVar{s})=\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `action = int(np.argmax(Q[state]))` — исследование отключено |

**Разбор.**

**(1)** Цикл строит маршрут до терминального состояния, но не более чем за
100 ходов.

**(2)** `np.argmax` реализует $\enfOp{\arg\max}$ и возвращает номер
действия жадной политики $\enfFun{\pi}$.

**(3)** После лунки или цели маршрут заканчивается.

Политика прошла `0 → 4 → 8 → 9 → 13 → 14 → 15` и получила
$\enfTgt{r}=1$. Значит, минимальное решение действительно достигло цели.

## Типичная ошибка: нет исследования

> [!warning] Нулевая таблица и чистый `argmax`
>
> ```python
> Q_zero = np.zeros((16, 4))
> action = int(np.argmax(Q_zero[0]))
> next_state, _, _ = step(0, action)
> print(ACTION_NAMES[action], next_state)
> ```
>
> ```output
> L 0
> ```
>
> Все оценки равны, поэтому `np.argmax` возвращает первый индекс — действие
> `L`. На левом краю агент остаётся в состоянии $\enfVar{s}=0$ и не видит
> награду $\enfTgt{r}=1$. Исследование с $\enfPar{\varepsilon}>0$ даёт
> шанс попробовать остальные действия.

## Упражнения

1. Рассчитайте новое значение $\enfOp{Q}(\enfVar{13},\enfFun{2})$, если
   старая оценка равна 0, $\enfTgt{r}=0$,
   $\max_{a'}\enfOp{Q}(\enfVar{14},a')=0{,}8$,
   $\enfVar{d}=0$, $\enfPar{\alpha}=0{,}5$ и
   $\enfPar{\gamma}=0{,}9$.
2. Замените $\enfPar{\varepsilon}=0{,}2$ на
   $\enfPar{\varepsilon}=0{,}05$ и снова запустите весь урок. Сравните
   обучающую долю успехов и жадный маршрут.
3. Объясните, почему в TD-цели после достижения цели множитель
   $1-\enfVar{d}$ обязан обнулить будущую оценку.

> [!example] Решение упражнения 1
>
> TD-цель и ошибка равны
> $\enfTgt{y}=\enfTgt{0}+\enfPar{0{,}9}\cdot\enfOp{0{,}8}=0{,}72$ и
> $\enfVar{\delta}=\enfTgt{0{,}72}-\enfOp{0}=0{,}72$. Поэтому
>
> $$
> \enfOp{Q}(\enfVar{13},\enfFun{2})
> \leftarrow\enfOp{0}+\enfPar{0{,}5}\cdot\enfVar{0{,}72}=0{,}36.
> $$
>
> ```python
> old_value = 0.0
> target = 0.0 + 0.9 * 0.8
> updated_value = old_value + 0.5 * (target - old_value)
> print(f"y = {target:.2f}, Q[13, R] = {updated_value:.2f}")
> ```
>
> ```output
> y = 0.72, Q[13, R] = 0.36
> ```

## Итоги

Минимальное решение состоит из четырёх частей: перехода среды, таблицы
$\enfOp{Q}$, $\enfPar{\varepsilon}$-жадного выбора и правила обновления.
На детерминированном поле этого достаточно, чтобы выучить безопасный путь.

**Таблица 9. Итоговое соответствие математики и Python.**

| Математика | Python |
|---|---|
| $\enfVar{s}=4i+j$ | `row, column = divmod(state, 4)` |
| $\enfVar{s},\enfFun{a}\mapsto(\enfVar{s}',\enfTgt{r},\enfVar{d})$ | `next_state, reward, terminated = step(state, action)` |
| $\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `target = reward + gamma * bootstrap` |
| $\enfVar{\delta}=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `td_error = target - Q[state, action]` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\,\enfVar{\delta}$ | `Q[state, action] += alpha * td_error` |
| $\enfFun{a}$ случайно при $\enfVar{u}<\enfPar{\varepsilon}$, иначе $\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `choose_action(Q, state, epsilon, rng)` |
| $\enfFun{\pi}(\enfVar{s})=\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `int(np.argmax(Q[state]))` |

## Что дальше

- [Q-Learning на табличном Frozen Lake](Q_Learning_Frozen_Lake.learning.md)
  подробно разбирает распространение ценности и расписание исследования.
- [Дисконтированная доходность](Discounted_Return.learning.md) объясняет
  смысл коэффициента $\enfPar{\gamma}$.
- [SARSA на табличном Frozen Lake](SARSA_Frozen_Lake.learning.md) заменяет
  максимум в цели на фактически выбранное следующее действие.
