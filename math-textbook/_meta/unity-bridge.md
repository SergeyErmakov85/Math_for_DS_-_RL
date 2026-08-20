---
title: "Мост в Unity-репозиторий"
enf_mode: publication
discipline: meta
date: 2026-08-20
status: ready
---
# Мост: математика → среды лаборатории

Где абстракция становится кодом. Все пути — от корня репозитория
[unity-ml-agents-lab](https://github.com/SergeyErmakov85/unity-ml-agents-lab):
двенадцать сред `E00`–`E11` в одном Unity-проекте плюс собственное ядро
обучения на PyTorch (`python/labrl`).

Важная особенность лаборатории: алгоритмы там написаны **своим кодом**, а не
взяты из библиотеки. Поэтому ссылка на файл в `python/labrl/algos/` — это
ссылка на ту же формулу, что стоит в лекции, только записанную на Python.

| Тема | Что смотреть | Путь |
|---|---|---|
| `advantage` | GAE: преимущество как усечённая сумма TD-ошибок | `python/labrl/algos/ppo.py` |
| `advantage` | gae_lambda: 0.95 — компромисс смещения и дисперсии | `configs/E06_Hunter3D__ppo.yaml` |
| `attention` | Внимание над переменным числом агентов (RSA) | `python/labrl/nets/attention.py` |
| `bandits` | ε-greedy, UCB1 и Thompson — три стратегии одним кодом | `python/labrl/algos/bandits.py` |
| `bandits` | Пять рук с вероятностями 0.80 / 0.65 / … | `unity/MLAgentsLab/Assets/Envs/E00_Bandit/Scripts/BanditArea.cs` |
| `bandits` | ucb_c: 1.414 — ширина доверительного интервала | `configs/E00_Bandit__ucb.yaml` |
| `bellman` | Value Iteration: стягивающее отображение на 25 состояниях | `python/labrl/algos/tabular/value_iteration.py` |
| `bellman` | Табличное обновление Q по TD-ошибке | `python/labrl/algos/tabular/q_learning.py` |
| `bellman` | GridWorld: индекс состояния 0–24 для табличного Q | `unity/MLAgentsLab/Assets/Envs/E01_GridWorld/Scripts/GridWorldAgent.cs` |
| `clipping` | clip_range: 0.2 — клиппинг отношения вероятностей | `configs/E06_Hunter3D__ppo.yaml` |
| `concept-lattice` | Формальный анализ понятий: алгоритм Close-by-One | `python/labrl/utils/fca.py` |
| `concept-lattice` | Слой понятий внутри графа политики | `python/labrl/nets/fca.py` |
| `concept-lattice` | Среда «ключ и дверь»: устройство и признаки | `unity/MLAgentsLab/Assets/Envs/E11_Research/Scripts/KeyDoorArea.cs` |
| `curriculum` | Расписание сложности и рандомизация домена | `python/labrl/train/curriculum.py` |
| `curriculum` | Лабиринт 5→11 клеток: генерация и проверка разрешимости | `unity/MLAgentsLab/Assets/Envs/E09_CurriculumMaze/Scripts/MazeArea.cs` |
| `deep-rl` | Карточки всех тринадцати алгоритмов лаборатории | `docs/algos/` |
| `deep-rl` | Карточка на каждую из двенадцати сред | `docs/envs/` |
| `discounting` | gamma: 0.99 — горизонт дисконтирования GridWorld | `configs/E01_GridWorld__qlearning.yaml` |
| `discounting` | gamma обязана совпадать с shapingGamma агента в Unity | `configs/E06_Hunter3D__ppo.yaml` |
| `dp` | Value Iteration против Q-learning на одной модели | `python/labrl/envs/gridworld_mdp.py` |
| `dqn` | Double DQN: буфер, целевая сеть, функция Хубера | `python/labrl/algos/dqn.py` |
| `dqn` | double_dqn: true, target_update_interval: 500 | `configs/E03_RollerBall__dqn.yaml` |
| `entropy` | Энтропийный бонус и автоподстройка α | `python/labrl/algos/sac.py` |
| `exploration` | Спад ε с 1.0 до 0.05 как расписание | `python/labrl/utils/schedules.py` |
| `exploration` | Три стратегии разведки на одной задаче | `docs/envs/E00_Bandit.md` |
| `fca` | Ключ и дверь: семь бинарных признаков = формальный контекст | `unity/MLAgentsLab/Assets/Envs/E11_Research/Scripts/KeyDoorAgent.cs` |
| `fca` | Решётка понятий как слой признаков политики | `docs/algos/fca_ppo.md` |
| `gradient-descent` | learning_rate линейным расписанием до нуля | `configs/E06_Hunter3D__ppo.yaml` |
| `hyperparameters` | HPO: случайный поиск и последовательное деление пополам | `python/labrl/eval/hpo.py` |
| `hyperparameters` | Все восемнадцать конфигов лаборатории | `configs/` |
| `hyperparameters` | Эталонные конфиги штатного тренера ML-Agents | `configs/mlagents/` |
| `imitation` | Поведенческое клонирование: обучение с учителем на записях | `python/labrl/algos/bc.py` |
| `imitation` | GAIL: награда −log(1−D) от дискриминатора | `python/labrl/algos/gail.py` |
| `imitation` | Коридор-змейка, где чистый RL буксует, а BC решает | `unity/MLAgentsLab/Assets/Envs/E10_Imitation/Scripts/CorridorArea.cs` |
| `imitation` | Запись демонстраций эксперта и чтение их обратно | `python/labrl/envs/demos.py` |
| `imitation` | Измерено: BC решает коридор, чистый RL — нет | `docs/envs/E10_Imitation.md` |
| `linear-algebra` | Полносвязная сеть: слои, ширина, активации | `python/labrl/nets/mlp.py` |
| `markov` | GridWorld: переходы и необязательное скольжение | `unity/MLAgentsLab/Assets/Envs/E01_GridWorld/Scripts/GridWorldEnvironment.cs` |
| `matrix` | Матрица Q 25×4 и её экспорт линейным слоем | `python/labrl/nets/tabular.py` |
| `mdp` | GridWorld 5×5 — MDP на индексах клеток | `unity/MLAgentsLab/Assets/Envs/E01_GridWorld/ENV_SPEC.md` |
| `mdp` | Явная модель переходов и наград на стороне Python | `python/labrl/envs/gridworld_mdp.py` |
| `multi-agent` | MA-POCA: централизованный критик и контрфактный базис | `python/labrl/algos/mapoca.py` |
| `multi-agent` | Футбол 2×2: зеркальный порядок тегов у двух команд | `unity/MLAgentsLab/Assets/Envs/E08_SoccerArena/Scripts/SoccerArea.cs` |
| `multi-agent` | Буфер для групп агентов переменного размера | `python/labrl/buffers/group_rollout.py` |
| `onnx` | Контракт экспорта: имена входов, выходов, opset | `docs/04_ONNX_CONTRACT.md` |
| `onnx` | Сборка графа политики под Unity Inference Engine | `python/labrl/export/onnx_export.py` |
| `policy-gradient` | REINFORCE с базисом | `python/labrl/algos/reinforce.py` |
| `policy-gradient` | Сборщик еды: гибридные действия и GridSensor | `unity/MLAgentsLab/Assets/Envs/E05_FoodCollector/Scripts/FoodCollectorAgent.cs` |
| `policy-gradient` | Гауссова политика: среднее и обучаемое log σ | `python/labrl/nets/gaussian_policy.py` |
| `policy-gradient` | Категориальная политика с маской действий | `python/labrl/nets/categorical_policy.py` |
| `ppo` | PPO целиком: отношение, клиппинг, GAE, несколько эпох | `python/labrl/algos/ppo.py` |
| `ppo` | A2C — тот же actor-critic без клиппинга, для сравнения | `python/labrl/algos/a2c.py` |
| `ppo` | Платформа с шаром: два непрерывных действия | `unity/MLAgentsLab/Assets/Envs/E04_BallBalance/Scripts/BallBalanceAgent.cs` |
| `probability` | Скольжение как стохастика переходов | `unity/MLAgentsLab/Assets/Envs/E01_GridWorld/Scripts/GridWorldEnvironment.cs` |
| `probability` | Сжатая гауссиана: tanh и поправка к логарифму плотности | `python/labrl/nets/squashed_gaussian.py` |
| `q-learning` | Табличный Q-learning: одна строка обновления | `python/labrl/algos/tabular/q_learning.py` |
| `q-learning` | Дискретизация непрерывного состояния под таблицу | `python/labrl/nets/discretized.py` |
| `q-learning` | CartPole в Unity: непрерывное состояние из четырёх чисел | `unity/MLAgentsLab/Assets/Envs/E02_CartPoleUnity/Scripts/CartPoleAgent.cs` |
| `return` | GridWorld: доходность кратчайшего пути ровно +0.68 | `configs/E01_GridWorld__qlearning.yaml` |
| `reward-design` | Потенциальное формирование награды (теорема Ына) | `docs/algos/ppo.md` |
| `reward-design` | Формирование награды по расстоянию до цели | `unity/MLAgentsLab/Assets/Envs/E06_Hunter3D/Scripts/HunterAgent.cs` |
| `reward-design` | Почему без формирования награды футбол необучаем | `docs/envs/E08_SoccerArena.md` |
| `rl-bridge` | Обзор лаборатории: двенадцать сред и своё ядро | `README.md` |
| `rl-bridge` | Карта «урок курса → среда → алгоритм → статус» | `docs/02_LESSON_MAP.md` |
| `sac` | SAC: два критика, max-entropy цель, автоподстройка α | `python/labrl/algos/sac.py` |
| `sac` | tau: 0.005, autotune_alpha: true | `configs/E07_RacingCar__sac.yaml` |
| `sac` | Гоночная машина: лучи как наблюдение, руль и газ как действие | `unity/MLAgentsLab/Assets/Envs/E07_RacingCar/Scripts/RacingAgent.cs` |
| `self-play` | Пул снимков соперников и рейтинг ELO | `python/labrl/train/selfplay.py` |
| `statistics` | IQM и доверительные интервалы по трём сидам | `python/labrl/eval/aggregate.py` |
| `statistics` | Базовая линия случайной политики по четырём уровням сложности | `docs/envs/E09_CurriculumMaze.md` |
| `statistics` | Сводка результатов всех примеров | `docs/RESULTS.md` |
| `unity` | Связь Python ↔ Unity через ML-Agents | `python/labrl/envs/unity_env.py` |
| `unity` | Векторизация: N арен как N параллельных сред | `python/labrl/envs/vec_unity_env.py` |
| `unity` | Сцена собирается кодом, а не руками | `unity/MLAgentsLab/Assets/Envs/E01_GridWorld/Editor/GridWorldSetup.cs` |
| `value-function` | Разметка наград по клеткам | `unity/MLAgentsLab/Assets/Envs/E01_GridWorld/Scripts/GridWorldEnvironment.cs` |
| `value-function` | Целевое значение: terminated против truncated | `python/labrl/buffers/rollout.py` |
| `vector` | RollerBall: вектор наблюдений из восьми чисел | `unity/MLAgentsLab/Assets/Envs/E03_RollerBall/Scripts/RollerAgent.cs` |
| `vector` | Склейка нескольких сенсоров в один вход политики | `python/labrl/envs/vec_unity_env.py` |
| `viz` | Обязательная схема тегов TensorBoard | `docs/05_TENSORBOARD.md` |
| `viz` | Запись метрик по ходу обучения | `python/labrl/logging/tb_logger.py` |

## Двенадцать сред

Статусы: **DONE** — обучено и проверено инференсом ONNX в Unity;
**READY** — сцена, сборка, конфиг и ноутбук готовы, обучение за читателем.
Карточка каждой среды лежит в `docs/envs/`.

| Среда | Задача | Действия | Алгоритмы | Части пособия |
|---|---|---|---|---|
| `E00_Bandit` | многорукий бандит | Discrete 1×5 | ε-greedy, UCB1, Thompson | VI (гл. 2) |
| `E01_GridWorld` | дойти до цели в сетке 5×5 | Discrete 1×4 | Value Iteration, табличный Q | I, IV, VI |
| `E02_CartPoleUnity` | удержать шест на тележке | Discrete 1×2 | Q-learning с дискретизацией | VI (гл. 6, 8) |
| `E03_RollerBall` | докатиться шаром до цели | Discrete 1×4 | Double DQN | III, VI (гл. 8) |
| `E04_BallBalance` | удержать шар на платформе | Continuous 2 | A2C, PPO | V |
| `E05_FoodCollector` | собрать еду, обходя вредную | гибридные | REINFORCE с базисом | V, VI (гл. 9) |
| `E06_Hunter3D` | догнать цель, обходя препятствия | Continuous 2 | PPO + GAE + PBRS | I (гл. 6), V |
| `E07_RacingCar` | проехать круг по трассе | Continuous 2 | SAC, подбор гиперпараметров | IV, VII |
| `E08_SoccerArena` | футбол 2 × 2 | Discrete 3×3×3 | MA-POCA, Self-Play | III, VII |
| `E09_CurriculumMaze` | лабиринт растущей сложности | Discrete 1×4 | PPO + Curriculum + DR | IV, VII |
| `E10_Imitation` | коридор, где RL буксует | Discrete 1×4 | BC, GAIL | IV (гл. 1), VII |
| `E11_Research` | ключ и дверь | Discrete 1×4 | PPO + слой понятий FCA | III, VII |

### Три опорные среды пособия

**`E01_GridWorld`** — дискретный MDP: 25 состояний (`s = r·5 + c`), четыре
действия (N/S/E/W), награды −0.04 за шаг, +1.0 за цель, −1.0 за ловушку.
Оптимум посчитан точно: кратчайший путь — восемь шагов, доходность
1.0 − 8 · 0.04 = 0.68. Именно поэтому среда годится и для части I (ряды
и дисконтирование), и для части IV (марковские процессы), и для части VI
(Беллман, TD, Q-learning): ответ известен заранее, и с ним можно сверяться.

**`E06_Hunter3D`** — непрерывное управление с формированием награды: PPO,
`gae_lambda: 0.95`, `clip_range: 0.2`, линейно затухающий шаг обучения.
Опорная среда для части V (градиент политики, PPO, оптимизация).

**`E11_Research`** — авторская архитектура: наблюдение из семи бинарных
признаков читается как формальный контекст, над ним строится решётка понятий,
и понятия становятся признаками политики. Метод самостоятельно обнаружил
эквивалентность «есть ключ ≡ дверь открыта». Опорная среда для части III
(решётки и линейные структуры) и части VII.

### Ядро обучения на PyTorch

`python/labrl/` — алгоритмы, сети, буферы, экспорт и оценка, написанные
для этого пособия своим кодом. Читать вместе с формулами:

* `python/labrl/algos/` — тринадцать алгоритмов, по файлу на метод;
* `python/labrl/nets/` — политики: категориальная, гауссова, сжатая гауссова,
  гибридная, табличная, внимание, слой понятий;
* `python/labrl/buffers/` — накопление переходов, включая группы агентов;
* `python/labrl/eval/` — оценка, агрегирование по сидам, подбор гиперпараметров;
* `python/labrl/export/` — экспорт в ONNX по контракту Unity.
