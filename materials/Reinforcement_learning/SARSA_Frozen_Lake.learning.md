---
title: "SARSA на табличном Frozen Lake"
enf_mode: learning
discipline: rl
tags: [rl, sarsa, tabular-method, frozen-lake, python]
duration: 90
code_python: "3.12"
code_requires: ["numpy>=2.0"]
code_level: basic
code_seed: 17
code_runnable: true
---

# SARSA на табличном Frozen Lake

## Зачем это нужно

SARSA — табличный метод (*tabular method*) обучения с подкреплением
(*reinforcement learning*, RL). Он учит агента ходить по полю Frozen Lake:
найти путь от старта к цели по безопасному льду и не попасть в лунку. Агент
не знает ценности ходов заранее; он видит только состояние, выполненное
действие, награду и новое состояние.

Главная особенность SARSA — обучение по фактически следующему действию.
Если стратегия иногда исследует поле, то цель обновления учитывает и этот
риск. Поэтому SARSA учит ценности той стратегии, которой агент реально
пользуется, а не ценности её жадной версии.

В уроке использована компактная детерминированная версия Frozen Lake 4×4.
Она самодостаточна, запускается только с NumPy и позволяет проверить каждое
число в ручном расчёте и коде.

## Обозначения

**Таблица 1. Обозначения SARSA.**

| Символ | Значение | Роль |
|---|---|---|
| $\enfVar{s}$, $\enfVar{s'}$ | текущее и следующее состояния (*state*) | `variable` |
| $\enfVar{d}$ | индикатор терминального перехода | `variable` |
| $\enfVar{\delta}$ | TD-ошибка (*temporal-difference error*) | `variable` |
| $\enfFun{a}$, $\enfFun{a}_{t+1}$ | выполненное и фактически следующее действия (*action*) | `function` |
| $\enfFun{\pi}$ | поведенческая стратегия (*behaviour policy*) | `function` |
| $\enfTgt{r}$ | награда за переход (*reward*) | `target` |
| $\enfTgt{y}$ | TD-цель (*temporal-difference target*) | `target` |
| $\enfPar{\alpha}$ | скорость обучения (*learning rate*) | `parameter` |
| $\enfPar{\gamma}$ | коэффициент дисконтирования (*discount factor*) | `parameter` |
| $\enfPar{\varepsilon}$ | вероятность исследовательского действия | `parameter` |
| $\enfOp{Q}(s,a)$ | оценка ценности пары «состояние — действие» | `operator` |
| $a'$ | связанное действие под $\max$ или $\arg\max$ | нейтральная переменная |
| $t$, $k$, $i$, $j$ | номера шага, эпизода, строки и столбца | нейтральные индексы |

Цвет в формулах отмечает объект, действие, цель, параметр или таблицу-
агрегат. В формуле SARSA одновременно встречаются все пять ролей, поэтому
фактически следующее действие $a_{t+1}$ оставлено нейтральным: его роль
зафиксирована в таблице, а формула остаётся в лимите четырёх тонов.

## Поле и правило SARSA

На поле 4×4 `S` обозначает старт, `F` — безопасный лёд, `H` — лунку, а `G`
— цель. Награда равна $\enfTgt{r}=1$ только при входе в цель; лунка и цель
завершают эпизод. Состояние в строке $i$ и столбце $j$ имеет номер

$$
\enfVar{s} = 4i + j, \qquad i,j \in \{0,1,2,3\}.
$$

**Таблица 2. Карта Frozen Lake и действия.**

| Строка поля | Номера состояний | Действия |
|---|---|---|
| `S F F F` | `0 1 2 3` | `L=0` — влево, `D=1` — вниз |
| `F H F H` | `4 5 6 7` | `R=2` — вправо, `U=3` — вверх |
| `F F F H` | `8 9 10 11` | |
| `H F F G` | `12 13 14 15` | |

> [!intuition] Почему не максимум
> В Q-Learning будущая часть цели — максимальная оценка следующего состояния.
> SARSA вместо этого смотрит на действие, которое стратегия действительно
> выбрала следующим. Если она иногда совершает случайные рискованные ходы,
> их последствия уже учтены в обучаемой оценке.

После перехода $(\enfVar{s},\enfFun{a},\enfTgt{r},\enfVar{s}')$ стратегия
выбирает следующее действие $a_{t+1}$. TD-цель SARSA равна

$$
\enfTgt{y} = \enfTgt{r} + \enfPar{\gamma}(1-\enfVar{d})
\enfOp{Q}(\enfVar{s}',a_{t+1}).
$$

Здесь $\enfTgt{r}$ — немедленная награда, $\enfPar{\gamma}$ ослабляет
будущее, $\enfVar{d}$ выключает будущую часть после конца эпизода, а
$\enfOp{Q}(\enfVar{s}',a_{t+1})$ использует выбор текущей стратегии.

TD-ошибка и обновление одной ячейки имеют вид

$$
\enfVar{\delta} = \enfTgt{y} -
\enfOp{Q}(\enfVar{s},\enfFun{a}),
$$

$$
\enfOp{Q}(\enfVar{s},\enfFun{a}) \leftarrow
\enfOp{Q}(\enfVar{s},\enfFun{a}) +
\enfPar{\alpha}\,\enfVar{\delta}.
$$

> [!definition] Определение 1. SARSA
> SARSA (*State–Action–Reward–State–Action*) обновляет оценку
> $\enfOp{Q}(\enfVar{s},\enfFun{a})$ по пятёрке
> $(\enfVar{s},\enfFun{a},\enfTgt{r},\enfVar{s}',a_{t+1})$. Пятое значение
> — следующее действие, выбранное той же поведенческой стратегией
> $\enfFun{\pi}$. Поэтому SARSA является алгоритмом обучения в политике
> (*on-policy learning*).

### Ручной расчёт

Рассмотрим безопасный переход из состояния $\enfVar{s}=13$ вправо в
$\enfVar{s'}=14$. Награда $\enfTgt{r}=0$, переход не терминальный
($\enfVar{d}=0$), а стратегия выбрала следующее действие вправо. Пусть
$\enfOp{Q}(\enfVar{14},R)=0{,}8$,
$\enfOp{Q}(\enfVar{13},R)=0$,
$\enfPar{\alpha}=0{,}5$ и $\enfPar{\gamma}=0{,}95$.

$$
\begin{aligned}
\enfTgt{y}
  &= \enfTgt{r} + \enfPar{\gamma}(1-\enfVar{d})
     \enfOp{Q}(\enfVar{s}',a_{t+1}) \\
  &= \enfTgt{0} + \enfPar{0{,}95}(1-\enfVar{0})
     \enfOp{Q}(\enfVar{14},R) \\
  &= 0{,}76.
\end{aligned}
$$

В первой строке стоит правило SARSA, а во второй числа сохранили роли
исходных символов. Действие `R` оставлено нейтральным по объявленному
правилу лимита тонов.

$$
\begin{aligned}
\enfVar{\delta}
  &= \enfTgt{y} - \enfOp{Q}(\enfVar{s},\enfFun{a}) \\
  &= \enfTgt{0{,}76} - \enfOp{Q}(\enfVar{13},R) = 0{,}76, \\
\enfOp{Q}(\enfVar{s},\enfFun{a})
  &\leftarrow \enfOp{Q}(\enfVar{s},\enfFun{a}) +
     \enfPar{\alpha}\,\enfVar{\delta} \\
  &= \enfOp{0} + \enfPar{0{,}5}\cdot\enfVar{0{,}76} = 0{,}38.
\end{aligned}
$$

Скорость обучения $\enfPar{\alpha}=0{,}5$ сдвинула нулевую оценку ровно на
половину расстояния до цели $\enfTgt{y}=0{,}76$.

## От формулы к коду

**Таблица 3. Символы и имена в Python.**

| Символ | Смысл | В коде | Тип и форма |
|---|---|---|---|
| $\enfVar{s}$, $\enfVar{s'}$ | номера текущего и следующего состояний | `state`, `next_state` | `int` от 0 до 15 |
| $\enfVar{d}$ | терминальность перехода | `terminated` | `bool` |
| $\enfVar{\delta}$ | TD-ошибка | `td_error` | `float` |
| $\enfFun{a}$, $\enfFun{a}_{t+1}$ | текущее и следующее действия | `action`, `next_action` | `int` от 0 до 3 |
| $\enfPar{\varepsilon}$ | вероятность исследования | `epsilon` | `float` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | ячейка таблицы | `Q[state, action]` | элемент массива формы `(16, 4)` |
| $\enfTgt{r}$, $\enfTgt{y}$ | награда и TD-цель | `reward`, `target` | `float` |
| $\enfPar{\alpha}$, $\enfPar{\gamma}$ | параметры обновления | `alpha`, `gamma` | `float` |

> [!warning] У терминального перехода нет следующего действия
> Если `terminated` равно `True`, функцию выбора действия вызывать не нужно.
> Будущая часть TD-цели равна `0.0`, а `next_action` остаётся `None`.
> Иначе случайное действие после лунки или цели исказило бы логику SARSA.

### Шаг 1. Один генератор случайных чисел

Один генератор с фиксированным зерном управляет всеми исследовательскими
ходами. Его нельзя создавать заново внутри эпизода: это повторяло бы один и
тот же случайный выбор.

```python
import numpy as np

rng = np.random.default_rng(17)  # (1)
np.set_printoptions(precision=3, suppress=True, floatmode="fixed")
print("rng seed = 17")
```

```output
rng seed = 17
```

**Разбор.**

**(1)** `default_rng(17)` создаёт единственный генератор. Последующие вызовы
`rng.random`, `rng.integers` и `rng.choice` используют именно его.

### Шаг 2. Один переход на поле

Функция `step` переводит состояние $\enfVar{s}$ и действие
$\enfFun{a}$ в следующую пятёрку среды: новое состояние, награду и признак
завершения. В отличие от настоящего скользкого озера, эта учебная версия
детерминирована: одно и то же действие всегда даёт один результат.

```python
MAP = ("SFFF", "FHFH", "FFFH", "HFFG")
DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))  # (1)
ACTION_NAMES = ("L", "D", "R", "U")
START_STATE = 0
MAX_STEPS = 100


def step(state: int, action: int) -> tuple[int, float, bool]:
    """Выполняет один ход и возвращает (s', r, d)."""
    row, column = divmod(state, 4)  # (2)
    delta_row, delta_column = DELTAS[action]
    new_row = min(max(row + delta_row, 0), 3)  # (3)
    new_column = min(max(column + delta_column, 0), 3)
    next_state = 4 * new_row + new_column  # (4)
    cell = MAP[new_row][new_column]
    terminated = cell in {"H", "G"}  # (5)
    reward = float(cell == "G")  # (6)
    return next_state, reward, terminated
```

```python
next_state, reward, terminated = step(14, 2)
print(f"state = {next_state}, reward = {reward:.1f}, "
      f"terminated = {terminated}")
```

```output
state = 15, reward = 1.0, terminated = True
```

Получили $\enfVar{s'}=15$, $\enfTgt{r}=1$ и $\enfVar{d}=1$: это
терминальный переход в цель.

**Таблица 4. Переход среды: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{s}=4i+j$ | `row, column = divmod(state, 4)` — частное и остаток дают строку $i$ и столбец $j$ |
| $i+\Delta i$ в пределах $0\leq i\leq3$ | `min(max(row + delta_row, 0), 3)` — ход за границу оставляет агента на краю |
| $\enfVar{s'}=4i'+j'$ | `next_state = 4 * new_row + new_column` — номер клетки после хода |
| $\enfVar{d}=1$ для лунки или цели | `terminated = cell in {"H", "G"}` — `True` выключает будущую часть цели |
| вся функция: $(\enfVar{s},\enfFun{a})\mapsto(\enfVar{s'},\enfTgt{r},\enfVar{d})$ | `next_state, reward, terminated = step(state, action)` — результат одного перехода |

**Разбор.**

**(1)** Кортеж `DELTAS` хранит сдвиги для четырёх действий. Элемент 2 —
`(0, 1)`, то есть движение вправо.

**(2)** `divmod` возвращает сразу частное и остаток; для состояния
$\enfVar{s}=14$ получаются строка 3 и столбец 2.

**(3)** Вложенные `min` и `max` ограничивают новую координату границей поля.

**(4)** Это обратный переход от координат к номеру
$\enfVar{s'}=4i'+j'$.

**(5)** Лунка и цель завершают эпизод, поэтому `terminated` соответствует
индикатору $\enfVar{d}$.

**(6)** Только клетка `G` превращается в награду $\enfTgt{r}=1.0$.

### Шаг 3. Следующее действие стратегии

$\varepsilon$-жадная стратегия (*epsilon-greedy strategy*) исследует среду
с вероятностью $\enfPar{\varepsilon}$, а в остальных случаях выбирает
максимальную строку $\enfOp{Q}(\enfVar{s},\cdot)$. При равенстве оценок
случайно выбирается одно из лучших действий, чтобы номер 0 не получал
необоснованного преимущества.

$$
\enfFun{a}_{t+1} =
\begin{cases}
\text{случайное действие}, & \text{с вероятностью } \enfPar{\varepsilon}, \\
\arg\max_{a'}\enfOp{Q}(\enfVar{s}',a'), & \text{с вероятностью } 1-\enfPar{\varepsilon}.
\end{cases}
$$

```python
def choose_action(
    Q: np.ndarray,
    state: int,
    epsilon: float,
    rng: np.random.Generator,
) -> int:
    """Выбирает действие epsilon-жадной стратегии."""
    if rng.random() < epsilon:  # (1)
        return int(rng.integers(4))
    best_value = Q[state].max()  # (2)
    best_actions = np.flatnonzero(Q[state] == best_value)  # (3)
    return int(rng.choice(best_actions))  # (4)
```

```python
Q_demo = np.zeros((16, 4))
Q_demo[0, 1] = 0.3
Q_demo[0, 2] = 0.7
action = choose_action(Q_demo, 0, epsilon=0.0, rng=rng)
print(f"action = {ACTION_NAMES[action]}")
```

```output
action = R
```

**Таблица 5. Выбор действия: формула → код.**

| Формула | Python |
|---|---|
| $\enfPar{\varepsilon}$ | `rng.random() < epsilon` — случайное число меньше вероятности запускает исследование |
| случайное $\enfFun{a}_{t+1}$ | `rng.integers(4)` — один из номеров 0, 1, 2 или 3 |
| $\enfOp{Q}(\enfVar{s'},\cdot)$ | `Q[state]` — строка четырёх оценок текущего состояния |
| $\arg\max_{a'}\enfOp{Q}(\enfVar{s'},a')$ | `np.flatnonzero(Q[state] == best_value)` — собираются все лучшие действия, а не только первое |
| вся формула: $\enfFun{a}_{t+1}\sim\varepsilon\text{-жадной стратегии}$ | `choose_action(Q, state, epsilon, rng)` — функция возвращает одно следующее действие |

**Разбор.**

**(1)** При `epsilon=0.0` условие ложно, поэтому пример использует жадную
ветвь.

**(2)** Метод `.max()` переводит максимум из формулы в одно число.

**(3)** Сравнение создаёт булев массив, а `flatnonzero` возвращает индексы
истинных элементов. Это устраняет систематическое преимущество первого
столбца при ничьей.

**(4)** `rng.choice` выбирает один индекс из массива лучших действий.

### Шаг 4. Одно обновление SARSA

В коде терминальный переход обрабатывается до обращения к `next_action`.
Поэтому будущая оценка в точности равна нулю при $\enfVar{d}=1$.

```python
def sarsa_update(
    Q: np.ndarray,
    state: int,
    action: int,
    reward: float,
    next_state: int,
    next_action: int | None,
    terminated: bool,
    alpha: float,
    gamma: float,
) -> tuple[float, float]:
    """Обновляет Q(s,a) по SARSA и возвращает (y, delta)."""
    bootstrap = 0.0 if terminated else Q[next_state, next_action]  # (1)
    target = reward + gamma * bootstrap  # (2)
    td_error = target - Q[state, action]  # (3)
    Q[state, action] += alpha * td_error  # (4)
    return target, td_error
```

```python
Q = np.zeros((16, 4))
Q[14, 2] = 0.8
target, td_error = sarsa_update(
    Q, 13, 2, 0.0, 14, 2, False, alpha=0.5, gamma=0.95
)
print(f"y = {target:.3f}, delta = {td_error:.3f}, "
      f"Q[13, R] = {Q[13, 2]:.3f}")
assert np.isclose(Q[13, 2], 0.38)
```

```output
y = 0.760, delta = 0.760, Q[13, R] = 0.380
```

Получены $\enfTgt{y}=0{,}76$, $\enfVar{\delta}=0{,}76$ и
$\enfOp{Q}(\enfVar{13},R)=0{,}38$ — те же числа, что в ручном расчёте.

**Таблица 6. Цель и обновление SARSA: формула → код.**

| Формула | Python |
|---|---|
| $\enfOp{Q}(\enfVar{s}',a_{t+1})$ | `Q[next_state, next_action]` — оценка именно выбранного следующего действия |
| $(1-\enfVar{d})\enfOp{Q}(\enfVar{s}',a_{t+1})$ | `0.0 if terminated else Q[next_state, next_action]` — при конце эпизода будущей оценки нет |
| $\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\enfOp{Q}(\enfVar{s}',a_{t+1})$ | `target = reward + gamma * bootstrap` — TD-цель SARSA |
| $\enfVar{\delta}=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `td_error = target - Q[state, action]` — ошибка вычисляется до изменения ячейки |
| вся формула: $\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\enfVar{\delta}$ | `Q[state, action] += alpha * td_error` — меняется только посещённая пара |

**Разбор.**

**(1)** Если `terminated` истинно, Python не вычисляет правую ветвь. Это
важно: `next_action` тогда равно `None` и не является индексом массива.

**(2)** `target` — прямая запись TD-цели $\enfTgt{y}$.

**(3)** `td_error` хранит разницу новой цели и старой ячейки.

**(4)** Оператор `+=` сдвигает ячейку на долю
$\enfPar{\alpha}\enfVar{\delta}$.

### Шаг 5. Один эпизод и трассировка

SARSA сначала выбирает $\enfFun{a}$ для начального состояния, а затем в
каждом нетерминальном переходе выбирает $\enfFun{a}_{t+1}$ до обновления.
Именно этот порядок превращает пятёрку «состояние — действие — награда —
состояние — действие» в одно обновление.

```python
def run_sarsa_episode(
    Q: np.ndarray, alpha: float, gamma: float,
    epsilon: float, rng: np.random.Generator,
) -> tuple[int, int]:
    """Запускает один эпизод и возвращает (успех, число ходов)."""
    state = START_STATE
    action = choose_action(Q, state, epsilon, rng)  # (1)
    for steps in range(1, MAX_STEPS + 1):
        next_state, reward, terminated = step(state, action)  # (2)
        next_action = None
        if not terminated:
            next_action = choose_action(Q, next_state, epsilon, rng)  # (3)
        sarsa_update(Q, state, action, reward, next_state,
                     next_action, terminated, alpha, gamma)  # (4)
        if terminated:
            return int(reward), steps
        state, action = next_state, int(next_action)  # (5)
    return 0, MAX_STEPS
```

**Таблица 7. Цикл SARSA: формула → код.**

| Формула | Python |
|---|---|
| начальное $\enfFun{a}$ | `action = choose_action(Q, state, epsilon, rng)` — действие выбирается ещё до первого перехода |
| $(\enfVar{s},\enfFun{a})\mapsto(\enfVar{s'},\enfTgt{r},\enfVar{d})$ | `next_state, reward, terminated = step(state, action)` — наблюдается переход среды |
| следующее $\enfFun{a}_{t+1}$ | `choose_action(Q, next_state, epsilon, rng)` — выбор происходит до вызова `sarsa_update` |
| $\enfVar{d}=1$ | `if terminated: return ...` — после лунки или цели действие не выбирается |
| вся пятёрка: $(\enfVar{s},\enfFun{a},\enfTgt{r},\enfVar{s}',a_{t+1})$ | `sarsa_update(...)` — все значения передаются в правило обновления |

**Разбор.**

**(1)** Первое действие нужно выбрать до цикла: без него нельзя сделать
первый переход.

**(2)** Среда возвращает три наблюдаемые части перехода.

**(3)** Для нетерминального состояния стратегия выбирает действие, которое
войдёт в TD-цель. Это ключевое отличие от Q-Learning.

**(4)** Функция обновляет таблицу до перехода к следующей паре.

**(5)** После обновления новая пара становится текущей на следующей итерации.

### Шаг 6. Обучение таблицы

На ранних эпизодах $\enfPar{\varepsilon}$ велико и агент исследует поле.
Затем вероятность линейно уменьшается до 0,05. Трассировка ниже содержит
первые четыре эпизода фактического запуска и показывает, что до первой
удачи лунки встречаются чаще цели.

```python
def train_sarsa(
    Q: np.ndarray, episodes: int, alpha: float, gamma: float,
    eps_start: float, eps_end: float, rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Обучает таблицу и возвращает успехи и длины эпизодов."""
    successes = np.zeros(episodes, dtype=int)
    lengths = np.zeros(episodes, dtype=int)
    for k in range(episodes):
        fraction = k / (episodes - 1)
        epsilon = eps_start + fraction * (eps_end - eps_start)  # (1)
        successes[k], lengths[k] = run_sarsa_episode(
            Q, alpha, gamma, epsilon, rng
        )  # (2)
    return successes, lengths
```

```python
Q = np.zeros((16, 4))
successes, lengths = train_sarsa(
    Q, episodes=9000, alpha=0.8, gamma=0.95,
    eps_start=1.0, eps_end=0.05, rng=rng,
)
for k in range(4):
    print(f"episode {k + 1}: success = {successes[k]}, "
          f"steps = {lengths[k]}")
print(f"successes in last 500 = {successes[-500:].mean():.3f}")
assert Q.shape == (16, 4)
```

```output
episode 1: success = 0, steps = 8
episode 2: success = 0, steps = 2
episode 3: success = 0, steps = 3
episode 4: success = 0, steps = 2
successes in last 500 = 0.000
```

**Таблица 8. Расписание обучения: формула → код.**

| Формула | Python |
|---|---|
| $k/(K-1)$ | `fraction = k / (episodes - 1)` — положение текущего эпизода между началом и концом обучения |
| $\enfPar{\varepsilon}_k$ | `epsilon = eps_start + fraction * (eps_end - eps_start)` — линейное уменьшение исследования |
| одна пятёрка SARSA | `run_sarsa_episode(Q, alpha, gamma, epsilon, rng)` — эпизод выполняет много обновлений |
| $\enfOp{Q}$ после эпизода $k$ | тот же массив `Q` — обновления сохраняются для следующего эпизода |
| вся процедура: $\enfOp{Q}_{k+1}\leftarrow\operatorname{SARSA}(\enfOp{Q}_k)$ | `successes, lengths = train_sarsa(...)` — цикл строит одну обученную таблицу |

**Разбор.**

**(1)** `fraction` начинается с 0 и заканчивается 1, поэтому `epsilon`
принимает ровно начальное и конечное значения.

**(2)** Массив `Q` передаётся в функцию по ссылке на объект: обновления из
каждого эпизода остаются в таблице для последующих эпизодов.

Таблица 9 повторяет трассировку первых эпизодов из запуска.

**Таблица 9. Трассировка начала обучения.**

| Эпизод | Успех | Число ходов |
|---:|---:|---:|
| 1 | 0 | 8 |
| 2 | 0 | 2 |
| 3 | 0 | 3 |
| 4 | 0 | 2 |

### Шаг 7. Жадная проверка политики

После обучения отключаем исследование и выбираем максимальную строку
$\enfOp{Q}(\enfVar{s},\cdot)$. Это оценка жадного маршрута, а не поведение
во время обучения с $\enfPar{\varepsilon}>0$.

```python
def greedy_rollout(Q: np.ndarray) -> list[int]:
    """Возвращает состояния жадного прохода от старта."""
    state = START_STATE
    path = [state]
    for _ in range(MAX_STEPS):
        action = int(np.argmax(Q[state]))  # (1)
        state, reward, terminated = step(state, action)  # (2)
        path.append(state)
        if terminated:
            return path
    raise RuntimeError("Greedy policy did not terminate")


path = greedy_rollout(Q)
print("states =", path)
assert path[-1] == 15
```

```output
states = [0, 4, 8, 9, 13, 14, 15]
```

**Таблица 10. Жадная политика: формула → код.**

| Формула | Python |
|---|---|
| $\enfFun{\pi}(\enfVar{s})$ | `np.argmax(Q[state])` — номер действия с наибольшей оценкой |
| $\arg\max_{a'}\enfOp{Q}(\enfVar{s},a')$ | `np.argmax(Q[state])` — перебор $a'$ скрыт внутри NumPy |
| $\enfVar{s}_{t+1}$ | `state, reward, terminated = step(state, action)` — переход по жадному действию |
| терминальность $\enfVar{d}=1$ | `if terminated: return path` — маршрут закончен в лунке или цели |
| вся политика: $\enfFun{\pi}(\enfVar{s})=\arg\max_{a'}\enfOp{Q}(\enfVar{s},a')$ | `path = greedy_rollout(Q)` — последовательность состояний жадной политики |

**Разбор.**

**(1)** Для проверки берётся `np.argmax`, а не `choose_action`: случайное
исследование скрыло бы качество выученной таблицы.

**(2)** Траектория заканчивается в состоянии 15, то есть в цели. Она
проходит безопасный путь `0 → 4 → 8 → 9 → 13 → 14 → 15`.

**Таблица 11. Трассировка жадного маршрута.**

| Шаг | Состояние | Действие | Следующее состояние |
|---:|---:|---|---:|
| 1 | 0 | `D` | 4 |
| 2 | 4 | `D` | 8 |
| 3 | 8 | `R` | 9 |
| 4 | 9 | `D` | 13 |
| 5 | 13 | `R` | 14 |
| 6 | 14 | `R` | 15 |

## Типичная ошибка: подмена SARSA максимумом

Если в цели заменить фактическое `next_action` на `.max()`, получится
Q-Learning, а не SARSA. Ошибка не вызывает исключения, но меняет смысл
алгоритма: риск исследовательской стратегии исчезает из обновления.

> [!warning] Неверная цель для SARSA
>
> ```python
> Q_wrong = np.zeros((16, 4))
> Q_wrong[14, 2] = 0.8
> wrong_target = 0.0 + 0.95 * Q_wrong[14].max()
> print(f"wrong target = {wrong_target:.3f}")
> ```
>
> ```output
> wrong target = 0.760
> ```
>
> В этом числовом случае максимум совпал с действием `R` случайно. Если
> стратегия выбрала бы действие с оценкой 0,1, правильная цель SARSA была бы
> 0,095, а не 0,760. Для SARSA нужно индексирование
> `Q[next_state, next_action]`.

## Упражнения

1. Рассчитайте $\enfTgt{y}$ и новое значение
   $\enfOp{Q}(\enfVar{13},R)$, если $\enfOp{Q}(\enfVar{14},R)=0{,}4$,
   $\enfOp{Q}(\enfVar{13},R)=0{,}2$, $\enfTgt{r}=0$,
   $\enfVar{d}=0$, $\enfPar{\alpha}=0{,}5$ и
   $\enfPar{\gamma}=0{,}95$.
2. Объясните, почему после лунки `next_action` в функции эпизода остаётся
   `None`.
3. Установите `eps_end=0.0` и повторите обучение. Почему жадная проверка
   может стать успешнее, хотя стратегия во время обучения изменилась?
4. Замените в `sarsa_update` индексирование на `Q[next_state].max()`.
   Какой алгоритм получится и где именно исчезнет зависимость от
   $a_{t+1}$?

> [!example] Решение упражнения 1
>
> ```python
> old_value = 0.2
> next_value = 0.4
> target = 0.0 + 0.95 * next_value
> updated_value = old_value + 0.5 * (target - old_value)
> print(f"y = {target:.3f}, Q[13, R] = {updated_value:.3f}")
> ```
>
> ```output
> y = 0.380, Q[13, R] = 0.290
> ```
>
> Будущая оценка входит в TD-цель с множителем $\enfPar{\gamma}$, а
> $\enfPar{\alpha}=0{,}5$ сдвигает старую ячейку на половину ошибки.

## Итоги

1. SARSA обновляет таблицу по фактически выбранному следующему действию,
   поэтому оценивает текущую поведенческую стратегию.
2. Терминальный переход обнуляет будущую часть TD-цели и не требует выбора
   следующего действия.
3. $\varepsilon$-жадное исследование необходимо для сбора переходов, но его
   риск остаётся частью того, чему учится SARSA.
4. На детерминированном поле обученная жадная политика приходит к цели по
   маршруту `0 → 4 → 8 → 9 → 13 → 14 → 15`.

**Таблица 12. Итоговое соответствие математики и Python.**

| Математика | Python |
|---|---|
| $\enfVar{s}=4i+j$ | `row, column = divmod(state, 4)` |
| $\enfFun{a}_{t+1}\sim\varepsilon\text{-жадной стратегии}$ | `next_action = choose_action(Q, next_state, epsilon, rng)` |
| $\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\enfOp{Q}(\enfVar{s}',a_{t+1})$ | `target = reward + gamma * bootstrap` |
| $\enfVar{\delta}=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `td_error = target - Q[state, action]` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\enfVar{\delta}$ | `Q[state, action] += alpha * td_error` |
| $\enfFun{\pi}(\enfVar{s})=\arg\max_{a'}\enfOp{Q}(\enfVar{s},a')$ | `action = int(np.argmax(Q[state]))` |

## Что дальше

- [Q-Learning на табличном Frozen Lake](Q_Learning_Frozen_Lake.learning.md)
  использует максимум следующей строки таблицы и поэтому учится вне
  политики.
- [DQN: Q-обучение с нейросетевой аппроксимацией](DQN.learning.md) заменяет
  таблицу Q-функцией для сред, где число состояний слишком велико.
