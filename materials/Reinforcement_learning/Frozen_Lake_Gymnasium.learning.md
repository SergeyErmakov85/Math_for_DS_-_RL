---
title: "Q-Learning в Gymnasium: разбор минимальной тетради Frozen Lake"
enf_mode: learning
discipline: rl
tags: [rl, q-learning, frozen-lake, gymnasium, python, minimal-example]
duration: 60
date: 2026-10-05
source: "тетрадь автора 09.10.26_Frosen_Lake_minimal.ipynb"
notebook: "Frozen_Lake_Gymnasium.ipynb"
code_python: "3.12"
code_requires: ["numpy>=2.0", "gymnasium>=1.0"]
code_level: basic
code_seed: 23
code_runnable: true
---

# Q-Learning в Gymnasium: разбор минимальной тетради Frozen Lake

## Зачем это нужно

Это описание к короткой тетради из трёх ячеек. Тетрадь обучает агента на поле Frozen Lake 4×4 из библиотеки Gymnasium, печатает таблицу оценок и проверяет жадную политику. Весь алгоритм умещается в пятнадцать строк, и почти каждая из них реализует часть одной формулы. Урок разбирает тетрадь построчно: что означает каждая строка, к какому символу формулы она относится и почему после 20 000 эпизодов в таблице появляются степени числа $\enfPar{0{,}99}$.

В отличие от урока [«Минимальное решение Frozen Lake»](Minimal_Frozen_Lake.learning.md), где среда написана вручную, здесь поле, награды и конец эпизода берутся из Gymnasium. Поэтому урок заодно показывает интерфейс `reset` и `step`, на котором держатся все задачи Gymnasium.

> [!info] Что изменено по сравнению с исходной тетрадью
>
> Алгоритм и все гиперпараметры прежние. Изменения нужны для того, чтобы вывод был воспроизводимым и проходил проверки репозитория:
>
> - зерно `23` задано генератору `rng`, пространству действий и первому `env.reset`; `np.random.rand()` заменён на `rng.random()`;
> - имена `eps` и `s2` заменены на `epsilon` и `s_next` по правилу «имена повторяют обозначения»;
> - однострочный выбор действия разбит на `if`/`else`, длинная строка обновления перенесена;
> - в цикл добавлена трассировка, а вывод таблицы $\enfOp{Q}$ получил подписи действий `0 ←`, `1 ↓`, `2 →`, `3 ↑` — это задание из второй ячейки тетради.
>
> Исполнимая версия урока — тетрадь [`Frozen_Lake_Gymnasium.ipynb`](Frozen_Lake_Gymnasium.ipynb).

> [!info]- Подготовка окружения
>
> ```bash
> pip install "numpy>=2.0" "gymnasium>=1.0"
> ```

## Обозначения

**Таблица 1. Обозначения урока.**

| Символ | Значение | Роль |
|---|---|---|
| $\enfVar{s}$, $\enfVar{s}'$ | текущее и следующее состояния (*state*): номер клетки от 0 до 15 | `variable` |
| $\enfVar{d}$ | индикатор конца эпизода (*terminated*): 1 в лунке и в цели | `variable` |
| $\enfVar{\delta}$ | TD-ошибка (*temporal-difference error*) | `variable` |
| $\enfVar{u}$ | случайное число из $[0,1)$ | `variable` |
| $\enfFun{a}$ | действие агента (*action*): 0, 1, 2 или 3 | `function` |
| $\enfFun{\pi}$ | жадная политика: состояние → действие | `function` |
| $\enfPar{\alpha}$ | скорость обучения (*learning rate*) | `parameter` |
| $\enfPar{\gamma}$ | коэффициент дисконтирования (*discount factor*) | `parameter` |
| $\enfPar{\varepsilon}$, $\enfPar{\varepsilon}_k$ | вероятность случайного действия; её значение в эпизоде $k$ | `parameter` |
| $\enfPar{\varepsilon}_{\min}$ | нижняя граница $\enfPar{\varepsilon}$ | `parameter` |
| $\enfPar{\rho}$ | коэффициент затухания $\enfPar{\varepsilon}$ за эпизод | `parameter` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | оценка действия в состоянии (*action value*) | `operator` |
| $\enfOp{\sum}$ | суммирование по эпизодам проверки | `operator` |
| $\enfTgt{r}$ | награда за переход (*reward*) | `target` |
| $\enfTgt{y}$ | TD-цель (*temporal-difference target*) | `target` |
| $\enfTgt{\hat p}$ | доля успешных эпизодов жадной политики | `target` |
| $a'$ | действие под $\max$ или $\arg\max$ | нейтральная связанная переменная |
| $k$, $K$, $n$, $N$, $m$ | номер и число эпизодов обучения, номер и число эпизодов проверки, номер обновления | нейтральные индексы |
| $i$, $j$ | строка и столбец клетки | нейтральные индексы |

Связанная переменная $a'$ только перебирает действия под $\max$ или $\arg\max$, поэтому нейтральна. Индексы и числа эпизодов тоже нейтральны. Остальные символы окрашены при каждом появлении.

## Поле, действия и награды

Gymnasium хранит карту поля в атрибуте `env.unwrapped.desc`:

```text
S F F F
F H F H
F F F H
H F F G
```

Агент стартует в `S`, идёт по льду `F`, проваливается в лунку `H` или доходит до цели `G`. Клетки нумеруются по строкам, поэтому клетка в строке $i$ и столбце $j$ — это состояние

$$
\enfVar{s}=4i+j, \qquad i,j\in\{0,1,2,3\}.
$$

Действия Gymnasium кодирует числами: `0 ←` влево, `1 ↓` вниз, `2 →` вправо, `3 ↑` вверх. За вход в цель среда даёт $\enfTgt{r}=1$, за любой другой ход $\enfTgt{r}=0$. Лунка и цель завершают эпизод: $\enfVar{d}=1$. Параметр `is_slippery=False` делает лёд нескользким: действие всегда переводит агента туда, куда указывает стрелка.

Кроме настоящего конца эпизода есть обрезание (*truncation*): Gymnasium прерывает эпизод через 100 ходов, даже если агент стоит на льду. Это не лунка и не цель, а ограничение времени. Разница между двумя видами конца понадобится в формуле обновления.

> [!intuition] Что хранит таблица
>
> Таблица $\enfOp{Q}$ имеет 16 строк — по одной на состояние $\enfVar{s}$ — и 4 столбца — по одному на действие $\enfFun{a}$. Ячейка $\enfOp{Q}(\enfVar{s},\enfFun{a})$ отвечает на вопрос: какую дисконтированную награду получит агент, если сделает $\enfFun{a}$ в $\enfVar{s}$, а дальше будет действовать наилучшим образом. Сначала все ячейки равны нулю; награда $\enfTgt{r}=1$ в цели постепенно растекается по таблице назад к старту.

## Формулы Q-Learning

### Выбор действия

Агент выбирает действие $\enfPar{\varepsilon}$-жадно (*epsilon-greedy*): с вероятностью $\enfPar{\varepsilon}$ — случайно, иначе — лучшее по таблице:

$$
\enfFun{a}=
\begin{cases}
\text{случайное действие}, & \enfVar{u}<\enfPar{\varepsilon},\\
\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a'), & \enfVar{u}\ge\enfPar{\varepsilon}.
\end{cases}
$$

В начале $\enfPar{\varepsilon}=1$: таблица пуста, и агенту нечего использовать, кроме случайных ходов. После каждого эпизода $\enfPar{\varepsilon}$ умножается на $\enfPar{\rho}$, но не опускается ниже $\enfPar{\varepsilon}_{\min}$:

$$
\enfPar{\varepsilon}_{k+1}=\max\bigl(\enfPar{\varepsilon}_{\min},\ \enfPar{\rho}\,\enfPar{\varepsilon}_k\bigr),
\qquad \enfPar{\varepsilon}_0=1.
$$

Раскрыв рекурсию, получаем явную формулу $\enfPar{\varepsilon}_k=\max\bigl(\enfPar{\varepsilon}_{\min},\ \enfPar{\rho}^{\,k}\bigr)$. В тетради $\enfPar{\rho}=0{,}9995$ и $\enfPar{\varepsilon}_{\min}=0{,}01$. Граница достигается, когда $\enfPar{\rho}^{\,k}\le\enfPar{\varepsilon}_{\min}$, то есть при

$$
k\ge\frac{\ln\enfPar{\varepsilon}_{\min}}{\ln\enfPar{\rho}}
=\frac{\ln\enfPar{0{,}01}}{\ln\enfPar{0{,}9995}}\approx9208{,}1 .
$$

Значит, первые примерно 9200 эпизодов агент постепенно переходит от случайного блуждания к жадным ходам, а оставшиеся 10 800 эпизодов ошибается случайно лишь в 1 % ходов.

### Обновление таблицы

После хода из $\enfVar{s}$ действием $\enfFun{a}$ в $\enfVar{s}'$ строится TD-цель — немедленная награда плюс дисконтированная лучшая оценка продолжения:

$$
\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a').
$$

Множитель $1-\enfVar{d}$ обнуляет продолжение после лунки или цели: там эпизод закончился, и будущих наград нет. Расхождение цели и старой оценки — TD-ошибка:

$$
\enfVar{\delta}=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a}).
$$

Ячейка сдвигается к цели на долю $\enfPar{\alpha}$ ошибки:

$$
\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\,\enfVar{\delta}.
$$

> [!definition] Определение 1. Табличный Q-Learning
>
> Q-Learning после каждого хода сдвигает оценку $\enfOp{Q}(\enfVar{s},\enfFun{a})$ к TD-цели $\enfTgt{y}$ на долю $\enfPar{\alpha}$ TD-ошибки $\enfVar{\delta}$. В цели стоит $\max_{a'}$, а не фактически выбранное следующее действие, поэтому метод оценивает жадную политику, даже когда агент ходит $\enfPar{\varepsilon}$-жадно.

В тетради все три формулы записаны одной строкой кода. В формуле пять ролей, а лимит учебного режима — четыре тона, поэтому в тексте она разбита на $\enfTgt{y}$, $\enfVar{\delta}$ и обновление.

### Ручной расчёт: первые два попадания в цель

Возьмём последний ход к цели: $\enfVar{s}=14$, $\enfFun{a}=2$ (`→`), $\enfVar{s}'=15$, $\enfTgt{r}=1$, $\enfVar{d}=1$. Таблица пока нулевая, $\enfPar{\alpha}=0{,}1$, $\enfPar{\gamma}=0{,}99$. Подставленные числа наследуют тон символов:

$$
\begin{aligned}
\enfTgt{y}
&=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')\\
&=\enfTgt{1}+\enfPar{0{,}99}(1-\enfVar{1})\max_{a'}\enfOp{Q}(\enfVar{15},a')=1.
\end{aligned}
$$

Будущее не учитывается, потому что $1-\enfVar{d}=0$. Ошибка и обновление:

$$
\begin{aligned}
\enfVar{\delta}
&=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})\\
&=\enfTgt{1}-\enfOp{Q}(\enfVar{14},\enfFun{2})=1-0=1,
\end{aligned}
$$

$$
\begin{aligned}
\enfOp{Q}(\enfVar{s},\enfFun{a})
&\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\,\enfVar{\delta}\\
&=\enfOp{0}+\enfPar{0{,}1}\cdot\enfVar{1}=0{,}1.
\end{aligned}
$$

При втором попадании в цель цель снова равна 1, а ошибка уже меньше: $\enfVar{\delta}=1-0{,}1=0{,}9$, поэтому $\enfOp{Q}(\enfVar{14},\enfFun{2})=0{,}1+\enfPar{0{,}1}\cdot\enfVar{0{,}9}=0{,}19$. Каждое обновление сокращает расстояние до единицы в $1-\enfPar{\alpha}$ раз, так что после $m$ обновлений

$$
\enfOp{Q}_m(\enfVar{14},\enfFun{2})=1-(1-\enfPar{\alpha})^{m}.
$$

### Ручной расчёт: к чему сходится таблица

Обучение останавливается, когда ошибка $\enfVar{\delta}$ всюду равна нулю, то есть $\enfOp{Q}(\enfVar{s},\enfFun{a})=\enfTgt{y}$. Поле нескользкое, и на кратчайшем пути все награды, кроме последней, нулевые. Пойдём от цели назад:

$$
\enfOp{Q}(\enfVar{14},\enfFun{2})=\enfTgt{r}=\enfTgt{1},
$$

$$
\enfOp{Q}(\enfVar{13},\enfFun{2})=\enfPar{\gamma}\max_{a'}\enfOp{Q}(\enfVar{14},a')=\enfPar{0{,}99}\cdot1=0{,}99.
$$

Каждый шаг назад добавляет множитель $\enfPar{\gamma}$. Если после действия $\enfFun{a}$ до цели остаётся $n$ ходов, считая этот, то

$$
\enfOp{Q}(\enfVar{s},\enfFun{a})=\enfPar{\gamma}^{\,n-1}.
$$

Со старта кратчайший путь занимает 6 ходов, поэтому $\enfOp{Q}(\enfVar{0},\enfFun{1})=\enfPar{0{,}99}^{5}\approx0{,}9510$. Именно это число стоит в первой строке таблицы, которую печатает тетрадь.

## От формулы к коду

**Таблица 2. Символы и имена в Python.**

| Символ | Смысл | В коде | Тип и форма |
|---|---|---|---|
| $\enfVar{s}$, $\enfVar{s}'$ | номера клеток | `s`, `s_next` (в тетради `s2`) | `int` от 0 до 15 |
| $\enfVar{d}$ | конец эпизода в лунке или цели | `term` | `bool` |
| — | обрезание по лимиту 100 ходов | `trunc` | `bool` |
| $\enfVar{u}$ | случайное число | `rng.random()` | `float` из $[0,1)$ |
| $\enfFun{a}$ | номер действия | `a` | `int` от 0 до 3 |
| $\enfFun{\pi}(\enfVar{s})$ | жадное действие | `np.argmax(Q[s])` | `int` от 0 до 3 |
| $\enfPar{\alpha}$ | скорость обучения | `alpha` | `float`, 0.1 |
| $\enfPar{\gamma}$ | дисконт | `gamma` | `float`, 0.99 |
| $\enfPar{\varepsilon}$ | вероятность исследования | `epsilon` (в тетради `eps`) | `float` |
| $\enfPar{\varepsilon}_{\min}$ | нижняя граница | `epsilon_min` | `float`, 0.01 |
| $\enfPar{\rho}$ | затухание за эпизод | `decay` | `float`, 0.9995 |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | одна оценка | `Q[s, a]` | элемент массива `(16, 4)` |
| $\enfTgt{r}$ | награда | `r` | `int`, 0 или 1 |
| $\enfTgt{\hat p}$ | доля успехов | `wins_eval / n_eval` | `float` |
| $K$, $N$ | число эпизодов обучения и проверки | `n_episodes`, `n_eval` | `int` |

> [!info] Запятая и точка
>
> В формулах пишем $\enfPar{0{,}99}$, а в Python и выводе — `0.99`.

### Шаг 1. Создаём среду

Первый блок подключает библиотеки, фиксирует случайность и создаёт среду. Здесь же собраны все гиперпараметры тетради: $\enfPar{\alpha}$, $\enfPar{\gamma}$, $\enfPar{\varepsilon}_{\min}$ и $\enfPar{\rho}$.

```python
import gymnasium as gym
import numpy as np

SEED = 23
rng = np.random.default_rng(SEED)                        # (1)
np.set_printoptions(precision=4, suppress=True, floatmode="fixed")

env = gym.make("FrozenLake-v1", is_slippery=False)       # (2)
env.action_space.seed(SEED)                              # (3)
env.reset(seed=SEED)
n_states = env.observation_space.n
n_actions = env.action_space.n
cells = "".join(b"".join(row).decode() for row in env.unwrapped.desc)
ARROWS = "←↓→↑"                                          # (4)

alpha, gamma = 0.1, 0.99
epsilon_min, decay = 0.01, 0.9995
n_episodes, n_eval = 20000, 1000
print(f"states = {n_states}, actions = {n_actions}")
print("map =", "/".join(cells[i:i + 4] for i in range(0, 16, 4)))
```

```output
states = 16, actions = 4
map = SFFF/FHFH/FFFH/HFFG
```

**Разбор.**

**(1)** `default_rng(23)` создаёт генератор, из которого берутся числа $\enfVar{u}$. В исходной тетради вместо него стоял `np.random.rand()` без зерна, поэтому числа в таблице менялись от запуска к запуску.

**(2)** `gym.make` создаёт среду по имени. `is_slippery=False` выключает скольжение: переход $\enfVar{s},\enfFun{a}\mapsto\enfVar{s}'$ становится детерминированным.

**(3)** У пространства действий свой генератор: им пользуется `env.action_space.sample()`. Без отдельного зерна случайные ходы не воспроизводятся, даже если зафиксирован `rng`.

**(4)** Строка из четырёх стрелок: `ARROWS[a]` даёт подпись действия $\enfFun{a}$. Индексы строки совпадают с кодами действий Gymnasium.

При другом зерне изменятся случайные ходы и, значит, числа трассировки в шаге 5. Карта, предельные значения $\enfOp{Q}$ на кратчайшем пути и итоговая политика от зерна не зависят.

### Шаг 2. Делаем один эпизод вручную

Прежде чем учить агента, пройдём кратчайший путь сами. Метод `env.step(a)` выполняет действие $\enfFun{a}$ и возвращает пять значений: $\enfVar{s}'$, $\enfTgt{r}$, признак конца $\enfVar{d}$, признак обрезания и служебный словарь.

```python
s, _ = env.reset()
for a in (1, 1, 2, 1, 2, 2):                             # (1)
    s_next, r, term, trunc, _ = env.step(a)              # (2)
    print(f"s = {s:2d}  a = {a}{ARROWS[a]}  s' = {s_next:2d}  "
          f"r = {r}  term = {term}  trunc = {trunc}")
    s = s_next                                           # (3)
```

```output
s =  0  a = 1↓  s' =  4  r = 0  term = False  trunc = False
s =  4  a = 1↓  s' =  8  r = 0  term = False  trunc = False
s =  8  a = 2→  s' =  9  r = 0  term = False  trunc = False
s =  9  a = 1↓  s' = 13  r = 0  term = False  trunc = False
s = 13  a = 2→  s' = 14  r = 0  term = False  trunc = False
s = 14  a = 2→  s' = 15  r = 1  term = True  trunc = False
```

**Таблица 3. Интерфейс среды: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{s}$ в начале эпизода | `s, _ = env.reset()` — `reset` возвращает стартовое состояние и словарь, словарь не нужен |
| $\enfVar{s},\enfFun{a}\mapsto\enfVar{s}'$ | `s_next = env.step(a)[0]` — следующая клетка, $\enfVar{s}'=4i'+j'$ |
| $\enfTgt{r}$ | `r` — `1` только при входе в `G` |
| $\enfVar{d}=1$ в `H` и `G` | `term` — настоящий конец эпизода |
| конец по лимиту времени | `trunc` — `True` после 100 ходов; к $\enfVar{d}$ не относится |
| вся формула: $\enfVar{s},\enfFun{a}\mapsto(\enfVar{s}',\enfTgt{r},\enfVar{d})$ | `s_next, r, term, trunc, _ = env.step(a)` |

**Разбор.**

**(1)** `for` перебирает кортеж действий: вниз, вниз, вправо, вниз, вправо, вправо.

**(2)** Распаковка: пять значений, которые вернула `step`, раскладываются по пяти именам. Подчёркивание `_` — имя для значения, которое не используется.

**(3)** Следующий ход начинается из новой клетки: $\enfVar{s}\leftarrow\enfVar{s}'$.

Последняя строка вывода — тот самый переход из ручного расчёта: $\enfVar{s}=14$, $\enfFun{a}=2$, $\enfVar{s}'=15$, $\enfTgt{r}=1$, $\enfVar{d}=1$. Путь занял 6 ходов, как и предполагалось.

### Шаг 3. Проверяем ручной расчёт

Строка обновления из тетради реализует $\enfTgt{y}$, $\enfVar{\delta}$ и сдвиг $\enfOp{Q}(\enfVar{s},\enfFun{a})$ одной записью. Применим её дважды к переходу из шага 2 на нулевой таблице.

```python
Q_demo = np.zeros((n_states, n_actions))
s, a, s_next, r, term = 14, 2, 15, 1, True              # (1)
for m in (1, 2):
    Q_demo[s, a] += alpha * (
        r + gamma * np.max(Q_demo[s_next]) * (not term) - Q_demo[s, a]
    )                                                    # (2)
    print(f"update {m}: Q[14, 2] = {Q_demo[s, a]:.4f}")
assert np.isclose(Q_demo[14, 2], 0.19)
```

```output
update 1: Q[14, 2] = 0.1000
update 2: Q[14, 2] = 0.1900
```

**Таблица 4. Строка обновления: формула → код.**

| Формула | Python |
|---|---|
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `Q[s, a]` — меняется ровно одна ячейка массива `(16, 4)` |
| $\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `np.max(Q[s_next])` — перебор $a'$ спрятан внутри `np.max` |
| $1-\enfVar{d}$ | `(not term)` — `True` при умножении становится 1, `False` — 0 |
| $\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `gamma * np.max(Q[s_next]) * (not term)` — максимум считается и в лунке, но затем умножается на 0 |
| $\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `r + gamma * np.max(Q[s_next]) * (not term)` — TD-цель, отдельного имени у неё нет |
| $\enfVar{\delta}=\enfTgt{y}-\enfOp{Q}(\enfVar{s},\enfFun{a})$ | `(... - Q[s, a])` — содержимое скобок; берётся старое значение ячейки |
| $\leftarrow\ \ldots+\enfPar{\alpha}\,\enfVar{\delta}$ | `Q[s, a] += alpha * (...)` — `+=` прибавляет сдвиг к той же ячейке |
| вся формула: $\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\,\enfVar{\delta}$ | `Q[s, a] += alpha * (r + gamma * np.max(Q[s_next]) * (not term) - Q[s, a])` |

**Разбор.**

**(1)** Множественное присваивание задаёт переход из ручного расчёта одной строкой.

**(2)** Это строка из тетради, перенесённая внутри скобок, чтобы уложиться в 79 символов. Python продолжает выражение на следующей строке, пока не закрыта скобка.

Код дал $\enfOp{Q}(\enfVar{14},\enfFun{2})=0{,}1$ после первого обновления и $0{,}19$ после второго — ровно числа ручного расчёта, $1-(1-\enfPar{0{,}1})^{2}=0{,}19$.

### Шаг 4. Расписание исследования

В тетради $\enfPar{\varepsilon}$ меняется одной строкой в конце эпизода. Проверим, что эта строка реализует формулу $\enfPar{\varepsilon}_k=\max\bigl(\enfPar{\varepsilon}_{\min},\ \enfPar{\rho}^{\,k}\bigr)$ и когда достигается граница.

```python
epsilon = 1.0
history = []
for k in range(n_episodes):                              # (1)
    history.append(epsilon)
    epsilon = max(epsilon_min, epsilon * decay)          # (2)
history = np.array(history)
closed_form = np.maximum(epsilon_min, decay ** np.arange(n_episodes))
assert np.allclose(history, closed_form)                 # (3)
k_floor = int(np.argmax(history == epsilon_min))         # (4)
print(f"epsilon_0 = {history[0]:.4f}, epsilon_999 = {history[999]:.4f}")
print(f"first k with epsilon = epsilon_min: {k_floor}")
```

```output
epsilon_0 = 1.0000, epsilon_999 = 0.6068
first k with epsilon = epsilon_min: 9209
```

**Таблица 5. Расписание $\enfPar{\varepsilon}$: формула → код.**

| Формула | Python |
|---|---|
| $\enfPar{\varepsilon}_0=1$ | `epsilon = 1.0` — в первом эпизоде все ходы случайны |
| $\enfPar{\rho}\,\enfPar{\varepsilon}_k$ | `epsilon * decay` — умножение раз в эпизод, а не раз в ход |
| $\max\bigl(\enfPar{\varepsilon}_{\min},\ \ldots\bigr)$ | `max(epsilon_min, ...)` — встроенная `max` двух чисел, не `np.max` |
| $\enfPar{\varepsilon}_k=\max\bigl(\enfPar{\varepsilon}_{\min},\ \enfPar{\rho}^{\,k}\bigr)$ | `np.maximum(epsilon_min, decay ** np.arange(n_episodes))` — явная формула сразу для всех $k$ |
| вся формула: $\enfPar{\varepsilon}_{k+1}=\max\bigl(\enfPar{\varepsilon}_{\min},\ \enfPar{\rho}\,\enfPar{\varepsilon}_k\bigr)$ | `epsilon = max(epsilon_min, epsilon * decay)` |

**Разбор.**

**(1)** Цикл повторяет только расписание из тетради, без обучения; `history[k]` хранит $\enfPar{\varepsilon}_k$ — значение, действующее в эпизоде $k$.

**(2)** Строка из тетради без изменений, кроме имени `epsilon`.

**(3)** `np.allclose` сверяет рекуррентную и явную формулы для всех 20 000 эпизодов. Сравнивать дробные числа через `==` нельзя: умножение в цикле и возведение в степень дают разные последние знаки.

**(4)** `history == epsilon_min` даёт массив из `True` и `False`; `np.argmax` возвращает номер первого `True`. Здесь `==` допустимо: после границы в массив попадает ровно число `epsilon_min`.

Явная формула предсказала $k\approx9208{,}1$, код нашёл первый эпизод с границей $k=9209$. Значение $\enfPar{\varepsilon}_{999}=\enfPar{0{,}9995}^{999}\approx0{,}6068$ повторится в трассировке шага 5.

### Шаг 5. Обучаем агента

Это первая ячейка тетради. Внешний цикл перебирает эпизоды, внутренний делает ходы до конца эпизода. Каждый ход — выбор действия по $\enfPar{\varepsilon}$-жадному правилу и одно обновление таблицы. Для трассировки в контрольных эпизодах запоминаются $\enfPar{\varepsilon}_k$, число успехов и две ячейки таблицы.

```python
CHECKPOINTS = {1, 100, 1000, 5000, 10000, 20000}
Q = np.zeros((n_states, n_actions))                      # (1)
epsilon, wins, trace = 1.0, 0, []
for k in range(n_episodes):                              # (2)
    s, _ = env.reset()
    done = False
    while not done:                                      # (3)
        if rng.random() < epsilon:                       # (4)
            a = int(env.action_space.sample())
        else:
            a = int(np.argmax(Q[s]))
        s_next, r, term, trunc, _ = env.step(a)
        Q[s, a] += alpha * (
            r + gamma * np.max(Q[s_next]) * (not term) - Q[s, a]
        )                                                # (5)
        s, done = s_next, term or trunc                  # (6)
    wins += r                                            # (7)
    if k + 1 in CHECKPOINTS:
        trace.append((k + 1, epsilon, wins, Q[14, 2], Q[0, 1]))
    epsilon = max(epsilon_min, epsilon * decay)
```

**Таблица 6. Выбор действия: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{u}\in[0,1)$ | `rng.random()` — новое число при каждом ходе |
| $\enfVar{u}<\enfPar{\varepsilon}$ | `if rng.random() < epsilon:` — ветка исследования |
| случайное $\enfFun{a}\in\{0,1,2,3\}$ | `env.action_space.sample()` — равновероятный выбор из пространства действий |
| $\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `np.argmax(Q[s])` — при равных оценках возвращает **меньший** номер действия |
| вся формула: $\enfFun{a}$ по $\enfPar{\varepsilon}$-жадному правилу | `a = env.action_space.sample() if rng.random() < epsilon else np.argmax(Q[s])` — запись исходной тетради |

**Разбор.**

**(1)** `np.zeros((16, 4))` создаёт нулевую таблицу $\enfOp{Q}$: строка — состояние, столбец — действие.

**(2)** `range(20000)` даёт номера эпизодов $k=0,\dots,19999$. В исходной тетради эта переменная называлась `episodes` и нигде не использовалась.

**(3)** `while not done` повторяет ходы, пока эпизод не кончился: агент упал в лунку, дошёл до цели или исчерпал 100 ходов.

**(4)** Ветвление $\enfVar{u}<\enfPar{\varepsilon}$. `int(...)` превращает номер действия из типа NumPy в обычное целое; `env.step` принимает и тот и другой.

**(5)** Строка обновления, разобранная в таблице 4. Важно, что в ней стоит `(not term)`, а не `(not done)`: при обрезании по лимиту 100 ходов $\enfVar{d}=0$, и продолжение $\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ учитывается. Агент не провалился — у него просто кончилось время.

**(6)** Две операции одной строкой: переход $\enfVar{s}\leftarrow\enfVar{s}'$ и признак конца эпизода. Для остановки цикла обрезание учитывается, для формулы — нет.

**(7)** После конца эпизода `r` хранит награду последнего хода: 1, если агент дошёл до цели, и 0 иначе. Счётчик `wins` добавлен для трассировки, в тетради его не было.

Вывести трассировку:

```python
print("episode  epsilon   wins  Q[14,R]  Q[0,D]")
for k, eps_k, wins_k, q_goal, q_start in trace:          # (1)
    print(f"{k:7d}  {eps_k:7.4f}  {wins_k:5d}  "
          f"{q_goal:7.4f}  {q_start:6.4f}")
```

```output
episode  epsilon   wins  Q[14,R]  Q[0,D]
      1   1.0000      0   0.0000  0.0000
    100   0.9517      2   0.1900  0.0003
   1000   0.6068    112   1.0000  0.9506
   5000   0.0821   2933   1.0000  0.9510
  10000   0.0100   7778   1.0000  0.9510
  20000   0.0100  17675   1.0000  0.9510
```

**Разбор.**

**(1)** Каждый элемент `trace` — кортеж из пяти чисел; `for` сразу раскладывает его по пяти именам, как `env.step` в шаге 2.

**Таблица 7. Трассировка обучения.**

| Эпизод | $\enfPar{\varepsilon}_k$ | Успехов с начала | $\enfOp{Q}(\enfVar{14},\enfFun{2})$ | $\enfOp{Q}(\enfVar{0},\enfFun{1})$ |
|---:|---:|---:|---:|---:|
| 1 | `1.0000` | `0` | `0.0000` | `0.0000` |
| 100 | `0.9517` | `2` | `0.1900` | `0.0003` |
| 1000 | `0.6068` | `112` | `1.0000` | `0.9506` |
| 5000 | `0.0821` | `2933` | `1.0000` | `0.9510` |
| 10000 | `0.0100` | `7778` | `1.0000` | `0.9510` |
| 20000 | `0.0100` | `17675` | `1.0000` | `0.9510` |

Трассировка подтверждает оба ручных расчёта. К сотому эпизоду агент дошёл до цели дважды, и $\enfOp{Q}(\enfVar{14},\enfFun{2})=0{,}19$ — то самое значение после двух обновлений. К пятитысячному эпизоду стартовая оценка $\enfOp{Q}(\enfVar{0},\enfFun{1})$ достигла $\enfPar{0{,}99}^{5}\approx0{,}9510$. Случайные блуждания первых эпизодов редко доходят до цели: за первые 1000 эпизодов успешных всего 112. Зато после выхода $\enfPar{\varepsilon}$ на границу агент доходит до цели почти всегда: с 10 000-го по 20 000-й эпизод успешных $17675-7778=9897$ из 10 000.

### Шаг 6. Печатаем таблицу с подписями действий

Во второй ячейке тетради стоит задание: вывести $\enfOp{Q}$ так, чтобы были видны действия `0 ←`, `1 ↓`, `2 →`, `3 ↑`. Голый `print(Q)` печатает массив `(16, 4)` без заголовков, и читатель вынужден помнить порядок столбцов. Добавим заголовок со стрелками, номер состояния $\enfVar{s}$ и тип клетки.

```python
header = "".join(f"{a:>6d} {ARROWS[a]}" for a in range(n_actions))
print(f" s cell{header}")                                # (1)
for s in range(n_states):
    values = "".join(f"{q:8.4f}" for q in Q[s])          # (2)
    print(f"{s:2d}    {cells[s]}{values}")
```

```output
 s cell     0 ←     1 ↓     2 →     3 ↑
 0    S  0.9415  0.9510  0.9321  0.9415
 1    F  0.9415  0.0000  0.9189  0.9312
 2    F  0.9312  0.7344  0.3604  0.6157
 3    F  0.6654  0.0000  0.1005  0.1097
 4    F  0.9510  0.9606  0.0000  0.9415
 5    H  0.0000  0.0000  0.0000  0.0000
 6    F  0.0000  0.9750  0.0000  0.3117
 7    H  0.0000  0.0000  0.0000  0.0000
 8    F  0.9606  0.0000  0.9703  0.9510
 9    F  0.9606  0.9801  0.9801  0.0000
10    F  0.9677  0.9900  0.0000  0.9330
11    H  0.0000  0.0000  0.0000  0.0000
12    H  0.0000  0.0000  0.0000  0.0000
13    F  0.0000  0.9801  0.9900  0.9703
14    F  0.9801  0.9900  1.0000  0.9801
15    G  0.0000  0.0000  0.0000  0.0000
```

**Разбор.**

**(1)** Выражение-генератор внутри `"".join(...)` собирает заголовок из четырёх подписей. Формат `{a:>6d}` выравнивает номер действия по правому краю поля шириной 6, чтобы подписи стояли над столбцами чисел.

**(2)** Тот же приём для строки таблицы: `{q:8.4f}` печатает оценку с четырьмя знаками в поле шириной 8. `cells[s]` добавляет тип клетки: видно, что строки `H` и `G` нулевые.

Как читать таблицу. Строки лунок 5, 7, 11, 12 и цели 15 нулевые: из терминального состояния не делается ни одного хода, и эти строки ни разу не обновлялись. Нули в строках льда означают ход в лунку: например, $\enfOp{Q}(\enfVar{1},\enfFun{1})=0$, потому что вниз от клетки 1 — лунка 5. Наконец, строки 2 и 3 вдали от кратчайшего пути обучены хуже: после того как $\enfPar{\varepsilon}$ упало до $\enfPar{0{,}01}$, агент туда почти не заходит.

Сравним ячейки кратчайшего пути с предсказанием $\enfOp{Q}(\enfVar{s},\enfFun{a})=\enfPar{\gamma}^{\,n-1}$:

```python
path = [0, 4, 8, 9, 13, 14]                              # (1)
actions = [1, 1, 2, 1, 2, 2]
learned = Q[path, actions]                               # (2)
exact = gamma ** np.arange(5, -1, -1)                    # (3)
print("Q(s, a) on path =", learned)
print("gamma powers    =", exact)
assert np.allclose(learned, exact)
```

```output
Q(s, a) on path = [0.9510 0.9606 0.9703 0.9801 0.9900 1.0000]
gamma powers    = [0.9510 0.9606 0.9703 0.9801 0.9900 1.0000]
```

**Таблица 8. Предел на кратчайшем пути: формула → код.**

| Формула | Python |
|---|---|
| $\enfVar{s}$ на пути | `path` — клетки из шага 2 |
| $\enfFun{a}$ на пути | `actions` — действия из шага 2 |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})$ для всех пар сразу | `Q[path, actions]` — пары берутся поэлементно, а не все сочетания |
| $n-1=5,4,\dots,0$ | `np.arange(5, -1, -1)` — правая граница `-1` не включается |
| вся формула: $\enfOp{Q}(\enfVar{s},\enfFun{a})=\enfPar{\gamma}^{\,n-1}$ | `gamma ** np.arange(5, -1, -1)` |

**Разбор.**

**(1)** Путь и действия переписаны из вывода шага 2.

**(2)** Индексация двумя списками: NumPy берёт `Q[0, 1]`, `Q[4, 1]`, `Q[8, 2]` и так далее — шесть чисел, а не таблицу $6\times6$.

**(3)** `**` возводит $\enfPar{\gamma}$ в каждую степень массива: от 5 у старта до 0 у последнего хода.

Все шесть ячеек совпали с $\enfPar{\gamma}^{\,n-1}$, в том числе $\enfOp{Q}(\enfVar{0},\enfFun{1})=0{,}9510$ из ручного расчёта.

### Шаг 7. Проверяем жадную политику

Третья ячейка тетради отключает исследование и играет жадной политикой

$$
\enfFun{\pi}(\enfVar{s})=\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a').
$$

Качество политики — доля эпизодов, закончившихся в цели:

$$
\enfTgt{\hat p}=\frac{1}{N}\enfOp{\sum}_{n=1}^{N}\enfTgt{r}_n,
$$

где $\enfTgt{r}_n$ — награда последнего хода эпизода $n$.

```python
wins_eval = 0
for _ in range(n_eval):                                  # (1)
    s, _ = env.reset()
    done = False
    while not done:
        a = int(np.argmax(Q[s]))                         # (2)
        s, r, term, trunc, _ = env.step(a)
        done = term or trunc
    wins_eval += r                                       # (3)
print(f"success rate = {wins_eval / n_eval:.3f}")
```

```output
success rate = 1.000
```

**Таблица 9. Жадная политика и доля успехов: формула → код.**

| Формула | Python |
|---|---|
| $\enfFun{\pi}(\enfVar{s})=\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `a = int(np.argmax(Q[s]))` — ветки со случайным ходом больше нет |
| $\enfTgt{r}_n$ | `r` после выхода из `while` — награда последнего хода эпизода |
| $\enfOp{\sum}_{n=1}^{N}\enfTgt{r}_n$ | `wins_eval += r` внутри `for` — накопление суммы |
| $\frac{1}{N}$ | `/ n_eval` — деление на число эпизодов проверки |
| вся формула: $\enfTgt{\hat p}=\frac{1}{N}\enfOp{\sum}_{n=1}^{N}\enfTgt{r}_n$ | `wins_eval / n_eval` |

**Разбор.**

**(1)** Имя `_` вместо счётчика: номер эпизода проверки в теле цикла не нужен.

**(2)** Жадный выбор $\enfFun{\pi}(\enfVar{s})$. Вызов `env.step` сразу перезаписывает `s`, так что отдельное имя для $\enfVar{s}'$ здесь не нужно.

**(3)** Награда прибавляется один раз за эпизод, после `while`. Так считать можно только потому, что в Frozen Lake награда бывает лишь на последнем ходу.

Доля успехов $\enfTgt{\hat p}=1$. На нескользком поле и политика, и среда детерминированы, поэтому все 1000 эпизодов одинаковы; хватило бы одного. Тысяча эпизодов понадобится, когда лёд станет скользким (упражнение 2).

Покажем политику на карте поля. В клетках лунок и цели вместо стрелки печатается буква клетки:

```python
policy = np.argmax(Q, axis=1)                            # (1)
for i in range(4):
    row = []
    for j in range(4):
        s = 4 * i + j                                    # (2)
        terminal = cells[s] in "HG"
        symbol = cells[s] if terminal else ARROWS[policy[s]]
        row.append(symbol)                               # (3)
    print(" ".join(row))
```

```output
↓ ← ← ←
↓ H ↓ H
→ ↓ ↓ H
H → → G
```

**Разбор.**

**(1)** `axis=1` ищет максимум в каждой строке: результат — массив `(16,)` с действием $\enfFun{\pi}(\enfVar{s})$ для каждого состояния.

**(2)** Формула $\enfVar{s}=4i+j$ переводит строку и столбец карты в номер состояния.

**(3)** Условное выражение `x if условие else y` выбирает букву для терминальной клетки и стрелку для остальных.

От старта стрелки ведут ↓ ↓ → ↓ → → — тот же путь, что в шаге 2. Стрелки в клетках 1, 2, 3 ведут влево, к старту: оценки там ниже, чем у пути через клетку 4.

## Типичная ошибка: цифры вместо карты политики

> [!warning] Типичная ошибка: `argmax` по нулевым строкам
>
> Третья ячейка исходной тетради печатает политику так:
>
> ```python
> print(np.argmax(Q, axis=1).reshape(4, 4))
> ```
>
> ```output
> [[1 0 0 0]
>  [1 0 1 0]
>  [2 1 1 0]
>  [0 2 2 0]]
> ```
>
> В клетках лунок 5, 7, 11, 12 и цели 15 стоит `0`, будто политика велит идти влево. На самом деле строки этих состояний нулевые, а `np.argmax` при равных значениях возвращает первый индекс. Из терминальной клетки ходов нет, поэтому действия там не определены. Карта из шага 7 печатает в этих клетках `H` и `G`, и ошибиться при чтении нельзя.

## Упражнения

1. Сотый эпизод трассировки показал $\enfOp{Q}(\enfVar{14},\enfFun{2})=0{,}19$. Пусть следующим обновляется $\enfOp{Q}(\enfVar{13},\enfFun{2})$, старая оценка равна нулю, $\enfTgt{r}=0$, $\enfVar{d}=0$, а $\max_{a'}\enfOp{Q}(\enfVar{14},a')=0{,}19$. Найдите $\enfTgt{y}$ и новое $\enfOp{Q}(\enfVar{13},\enfFun{2})$ при $\enfPar{\alpha}=0{,}1$, $\enfPar{\gamma}=0{,}99$.
2. Поставьте `is_slippery=True` и запустите урок заново. Каким стало $\enfTgt{\hat p}$? Почему теперь 1000 эпизодов проверки нужны, а $\enfOp{Q}(\enfVar{0},\enfFun{1})$ уже не равно $\enfPar{0{,}99}^{5}$?
3. Замените в строке обновления `(not term)` на `(not done)`, где `done = term or trunc`. Какие переходы будут обновляться неверно? Почему на нескользком поле после обучения разница почти не заметна?
4. Уменьшите $\enfPar{\rho}$ до $\enfPar{0{,}99}$. Через сколько эпизодов $\enfPar{\varepsilon}$ достигнет $\enfPar{\varepsilon}_{\min}$? Сначала посчитайте по формуле из раздела «Выбор действия», затем проверьте кодом шага 4.

> [!example] Решение упражнения 1
>
> TD-цель: $\enfTgt{y}=\enfTgt{0}+\enfPar{0{,}99}(1-\enfVar{0})\cdot0{,}19=0{,}1881$. Ошибка $\enfVar{\delta}=\enfTgt{0{,}1881}-\enfOp{0}=0{,}1881$. Обновление:
>
> $$
> \enfOp{Q}(\enfVar{13},\enfFun{2})\leftarrow\enfOp{0}+\enfPar{0{,}1}\cdot\enfVar{0{,}1881}\approx0{,}0188.
> $$
>
> ```python
> q_old, r, d, q_next_max = 0.0, 0, 0, 0.19
> target = r + gamma * (1 - d) * q_next_max
> q_new = q_old + alpha * (target - q_old)
> print(f"y = {target:.4f}, Q[13, R] = {q_new:.4f}")
> ```
>
> ```output
> y = 0.1881, Q[13, R] = 0.0188
> ```
>
> Награда из цели продвинулась на одну клетку назад, но ослабла: ячейка получила лишь десятую долю от $\enfPar{\gamma}\cdot0{,}19$.

## Итоги

Тетрадь из трёх ячеек содержит весь табличный Q-Learning: среду Gymnasium, $\enfPar{\varepsilon}$-жадный выбор с затуханием и одну строку обновления. На нескользком поле таблица сходится к степеням $\enfPar{\gamma}$ на кратчайшем пути, а жадная политика доходит до цели в каждом эпизоде. Для чтения результата нужна таблица с подписями действий и карта политики, в которой терминальные клетки не выдают себя за ход влево.

**Таблица 10. Итоговое соответствие математики и Python.**

| Математика | Python |
|---|---|
| $\enfVar{s},\enfFun{a}\mapsto(\enfVar{s}',\enfTgt{r},\enfVar{d})$ | `s_next, r, term, trunc, _ = env.step(a)` |
| $\enfFun{a}$ случайно при $\enfVar{u}<\enfPar{\varepsilon}$, иначе $\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `a = env.action_space.sample() if rng.random() < epsilon else np.argmax(Q[s])` |
| $\enfPar{\varepsilon}_{k+1}=\max\bigl(\enfPar{\varepsilon}_{\min},\ \enfPar{\rho}\,\enfPar{\varepsilon}_k\bigr)$ | `epsilon = max(epsilon_min, epsilon * decay)` |
| $\enfTgt{y}=\enfTgt{r}+\enfPar{\gamma}(1-\enfVar{d})\max_{a'}\enfOp{Q}(\enfVar{s}',a')$ | `r + gamma * np.max(Q[s_next]) * (not term)` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})\leftarrow\enfOp{Q}(\enfVar{s},\enfFun{a})+\enfPar{\alpha}\,\enfVar{\delta}$ | `Q[s, a] += alpha * (r + gamma * np.max(Q[s_next]) * (not term) - Q[s, a])` |
| $\enfOp{Q}(\enfVar{s},\enfFun{a})=\enfPar{\gamma}^{\,n-1}$ на кратчайшем пути | `Q[path, actions]` ≈ `gamma ** np.arange(5, -1, -1)` |
| $\enfFun{\pi}(\enfVar{s})=\enfOp{\arg\max}_{a'}\enfOp{Q}(\enfVar{s},a')$ | `np.argmax(Q, axis=1)` |
| $\enfTgt{\hat p}=\frac{1}{N}\enfOp{\sum}_{n=1}^{N}\enfTgt{r}_n$ | `wins_eval / n_eval` |

## Что дальше

- [Минимальное решение Frozen Lake методом Q-Learning](Minimal_Frozen_Lake.learning.md) — та же задача со средой, написанной вручную на NumPy.
- [Q-Learning на табличном Frozen Lake](Q_Learning_Frozen_Lake.learning.md) — подробный разбор распространения ценности и расписаний исследования.
- [SARSA на табличном Frozen Lake](SARSA_Frozen_Lake.learning.md) — цель строится по фактически выбранному следующему действию, а не по максимуму.
- [Дисконтированная доходность](Discounted_Return.learning.md) — откуда берутся степени $\enfPar{\gamma}$ в таблице.
