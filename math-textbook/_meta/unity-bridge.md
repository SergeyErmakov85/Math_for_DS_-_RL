---
title: "Мост в Unity-репозиторий"
enf_mode: publication
discipline: meta
date: 2026-08-09
status: ready
---
# Мост: математика → среды этого репозитория

Где абстракция становится кодом. Пути — от корня репозитория.

| Тема | Что смотреть | Путь |
|---|---|---|
| `advantage` | lambd — параметр GAE | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml` |
| `bellman` | GridWorld: CurrentStateIndex 0–24 для табличного Q | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldAgent.cs` |
| `clipping` | epsilon: 0.2 — клиппинг PPO | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml` |
| `deep-rl` | Обучение нейросетевой политики через mlagents-learn | `docs/TRAINING.md` |
| `discounting` | gamma: 0.95 в конфиге GridWorld | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/config/GridWorldQLearning.yaml` |
| `discounting` | gamma: 0.99 в конфиге RollerAgent | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml` |
| `dp` | GridWorld: перебор клеток 5×5 как модель для value iteration | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md` |
| `exploration` | beta: 5.0e-3 — энтропийный бонус GridWorld | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/config/GridWorldQLearning.yaml` |
| `gradient-descent` | learning_rate 3.0e-4, learning_rate_schedule: linear | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml` |
| `hyperparameters` | Все trainer-конфиги проекта | `config/ml-agents-reference/` |
| `hyperparameters` | Проверка обучаемости сред | `Assets/Editor/MLAgentsTrainingValidator.cs` |
| `linear-algebra` | network_settings: hidden_units, num_layers | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml` |
| `markov` | GridWorld: детерминированные переходы, slipProbability | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs` |
| `matrix` | GridWorld: one-hot наблюдение размера 25 | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldAgent.cs` |
| `mdp` | GridWorld 5×5 — MDP на индексах клеток | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md` |
| `policy-gradient` | RollerAgent: непрерывная политика, 2 действия | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/Scripts/RollerAgent.cs` |
| `ppo` | PPO-конфиг RollerAgent (epsilon 0.2, lambd, num_epoch) | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml` |
| `ppo` | Справочные конфиги PPO из ml-agents | `config/ml-agents-reference/ppo/` |
| `probability` | slipProbability — модель скольжения FrozenLake | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs` |
| `q-learning` | GridWorld: state = r·5 + c, действия N/S/E/W | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs` |
| `return` | GridWorld: доходность кратчайшего пути +0.68 | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md` |
| `reward-design` | GridWorld: шаг −0.04, цель +1.0, ловушка −1.0 | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md` |
| `rl-bridge` | Обзор лаборатории сред | `README.md` |
| `statistics` | Метрики обучения в results/ | `docs/TRAINING.md` |
| `unity` | Обучение: scripts/train.ps1 | `docs/TRAINING.md` |
| `unity` | Сборка сцен из кода | `Assets/Editor/ProjectBootstrap.cs` |
| `value-function` | GridWorld: разметка наград по клеткам | `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs` |
| `vector` | RollerAgent: вектор наблюдений из 8 чисел | `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/Scripts/RollerAgent.cs` |
| `viz` | TensorBoard: scripts/tensorboard.ps1 | `docs/TRAINING.md` |

## Среды

### GridWorld 5×5 — `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/`

Дискретный MDP по ТЗ TS-001: 25 состояний (`state = r·5 + c`), 4 действия (N/S/E/W),
награды −0.04 / +1.0 / −1.0, `gamma: 0.95`, необязательное скольжение `slipProbability`.
Опорная среда для частей IV, VI (MDP, Беллман, TD, Q-learning).

### Hit_the_ball / RollerAgent — `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/`

Непрерывное управление: 8 наблюдений, 2 непрерывных действия, PPO
(`epsilon: 0.2`, `lambd: 0.99`, `gamma: 0.99`, `learning_rate: 3.0e-4`).
Опорная среда для частей II, V (градиент политики, PPO, оптимизация).

### Справочные конфиги — `config/ml-agents-reference/`

PPO / SAC / POCA / imitation — материал для разбора гиперпараметров
в части V (Лекция 4) и части VI (Глава 10).
