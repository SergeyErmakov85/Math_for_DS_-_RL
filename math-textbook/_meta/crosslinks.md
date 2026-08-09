---
title: "Реестр перекрёстных ссылок"
enf_mode: publication
discipline: meta
date: 2026-08-09
status: ready
---
# Реестр перекрёстных ссылок

## 1. Связи «урок → раздел математики», уже существующие на сайте

Взято из реестра crosslinks сайта — 15 связей, ведущих в `/math-rl/*`.

| Урок | Раздел пособия | Контекст |
|---|---|---|
| [Урок 1.1. Что такое обучение с подкреплением?](https://rl-cuber-unity-code.com/courses/1-1) | [Глава 3. Марковские процессы принятия решений (MDP)](../part-6-fundamental-rl/03-mdp.md) | Формальное определение MDP, V/Q функции |
| [Урок 1.1. Что такое обучение с подкреплением?](https://rl-cuber-unity-code.com/courses/1-1) | [4. Уравнения Беллмана и дисконтирование](../part-1-limits-series/04-bellman-and-discounting.md) | Математика за γ и бесконечными суммами наград |
| [Урок 1.3. Марковские процессы принятия решений (MDP)](https://rl-cuber-unity-code.com/courses/1-3) | [Глава 5. Сердце RL: Уравнения Беллмана](../part-6-fundamental-rl/05-bellman-equations.md) | Рекурсивная структура функции ценности |
| [Урок 1.3. Марковские процессы принятия решений (MDP)](https://rl-cuber-unity-code.com/courses/1-3) | [Глава 3. Марковские процессы принятия решений (MDP)](../part-6-fundamental-rl/03-mdp.md) | Формальное описание MDP-среды |
| [Урок 1.3. Марковские процессы принятия решений (MDP)](https://rl-cuber-unity-code.com/courses/1-3) | [Глава 6. От динамического программирования к Model-Free RL](../part-6-fundamental-rl/06-model-free-rl.md) | Переход от DP к Model-Free методам |
| [Урок 1.6. DQN с нуля на PyTorch](https://rl-cuber-unity-code.com/courses/1-6) | [Глава 5. Сердце RL: Уравнения Беллмана](../part-6-fundamental-rl/05-bellman-equations.md) | Математическая основа DQN — уравнение Беллмана |
| [Урок 1.6. DQN с нуля на PyTorch](https://rl-cuber-unity-code.com/courses/1-6) | [Лекция 3. Градиентный спуск и его варианты](../part-5-policy-optimization/03-gradient-descent-variants.md) | Оптимизация Q-сети через SGD / Adam |
| [Урок 2.1. Policy Gradient и теорема градиента](https://rl-cuber-unity-code.com/courses/2-1) | [Лекция 2. Вывод градиента политики](../part-5-policy-optimization/02-policy-gradient-derivation.md) | Стохастический градиентный подъём для политики |
| [Урок 2.1. Policy Gradient и теорема градиента](https://rl-cuber-unity-code.com/courses/2-1) | [1. Теория вероятностей](../part-4-probability/01-probability-theory.md) | Логарифмические производные и REINFORCE |
| [Урок 2.2. PPO — реализация с нуля](https://rl-cuber-unity-code.com/courses/2-2) | [Глава 9. Методы градиента политики (Policy Gradients)](../part-6-fundamental-rl/09-policy-gradients.md) | Математика GAE и advantage estimation |
| [Урок 2.4. Reward Shaping](https://rl-cuber-unity-code.com/courses/2-4) | [6. Дисконтирование в RL и его влияние](../part-1-limits-series/06-discounting-in-rl.md) | Математическое обоснование reward shaping |
| [Урок 3.1. SAC — Soft Actor-Critic](https://rl-cuber-unity-code.com/courses/3-1) | [Глава 9. Методы градиента политики (Policy Gradients)](../part-6-fundamental-rl/09-policy-gradients.md) | Математика soft value функций |
| [Урок 3.4. Имитационное обучение (BC и GAIL)](https://rl-cuber-unity-code.com/courses/3-4) | [Лекция 2. Вывод градиента политики](../part-5-policy-optimization/02-policy-gradient-derivation.md) | GAN-подобная оптимизация в GAIL |
| [Урок 3.6. Оптимизация гиперпараметров: Optuna + W&B](https://rl-cuber-unity-code.com/courses/3-6) | [Лекция 3. Градиентный спуск и его варианты](../part-5-policy-optimization/03-gradient-descent-variants.md) | Математика поиска гиперпараметров |
| [Урок 3.7. Архитектуры нейросетей для RL-агентов](https://rl-cuber-unity-code.com/courses/3-7) | [1. Векторы](../part-3-linear-algebra/01-vectors.md) | Матричные операции в свёрточных и рекуррентных сетях |

## 2. Горизонтальные связи между частями

Строятся по общим тегам. Ниже — темы, которые проходят более чем через одну часть.

| Тема | Разделы |
|---|---|
| `advantage` | [V·02](../part-5-policy-optimization/02-policy-gradient-derivation.md) · [VI·09](../part-6-fundamental-rl/09-policy-gradients.md) |
| `bellman` | [I·04](../part-1-limits-series/04-bellman-and-discounting.md) · [I·05](../part-1-limits-series/05-value-iteration.md) · [IV·04](../part-4-probability/04-value-functions-bellman.md) · [VI·05](../part-6-fundamental-rl/05-bellman-equations.md) |
| `convergence` | [I·00](../part-1-limits-series/00-introduction.md) · [I·01](../part-1-limits-series/01-sequence-limit.md) · [I·02](../part-1-limits-series/02-infinite-series.md) · [I·05](../part-1-limits-series/05-value-iteration.md) · [I·08](../part-1-limits-series/08-convergence-visualizations.md) · [III·04](../part-3-linear-algebra/04-eigenvalues.md) |
| `deep-rl` | [VI·08](../part-6-fundamental-rl/08-function-approximation.md) · [VII·01](../part-7-deep-rl/01-core-concepts.md) · [VII·02](../part-7-deep-rl/02-algorithms-overview.md) |
| `derivative` | [II·01](../part-2-derivatives-gradient/01-derivatives.md) · [II·02](../part-2-derivatives-gradient/02-partial-derivatives-gradient.md) · [VII·03](../part-7-deep-rl/03-calculus.md) |
| `discounting` | [I·02](../part-1-limits-series/02-infinite-series.md) · [I·03](../part-1-limits-series/03-limits-in-rl.md) · [I·04](../part-1-limits-series/04-bellman-and-discounting.md) · [I·06](../part-1-limits-series/06-discounting-in-rl.md) · [VI·04](../part-6-fundamental-rl/04-return-policy-value.md) |
| `dp` | [I·05](../part-1-limits-series/05-value-iteration.md) · [I·08](../part-1-limits-series/08-convergence-visualizations.md) · [VI·05](../part-6-fundamental-rl/05-bellman-equations.md) · [VI·06](../part-6-fundamental-rl/06-model-free-rl.md) |
| `dqn` | [VI·08](../part-6-fundamental-rl/08-function-approximation.md) · [VII·02](../part-7-deep-rl/02-algorithms-overview.md) |
| `exercises` | [I·07](../part-1-limits-series/07-examples-and-tasks.md) · [I·09](../part-1-limits-series/09-practice-limits.md) · [IV·06](../part-4-probability/06-python-examples.md) |
| `expectation` | [IV·01](../part-4-probability/01-probability-theory.md) · [VI·01](../part-6-fundamental-rl/01-probability-foundation.md) |
| `glossary` | [I·11](../part-1-limits-series/11-glossary.md) · [VI·12](../part-6-fundamental-rl/12-glossary.md) |
| `gradient` | [II·02](../part-2-derivatives-gradient/02-partial-derivatives-gradient.md) · [II·04](../part-2-derivatives-gradient/04-policy-gradient-application.md) · [II·05](../part-2-derivatives-gradient/05-big-picture.md) · [VII·03](../part-7-deep-rl/03-calculus.md) |
| `gradient-descent` | [II·03](../part-2-derivatives-gradient/03-gradient-descent.md) · [V·03](../part-5-policy-optimization/03-gradient-descent-variants.md) |
| `hyperparameters` | [V·04](../part-5-policy-optimization/04-ppo.md) · [VI·10](../part-6-fundamental-rl/10-unity-ml-agents-bridge.md) |
| `log-trick` | [V·02](../part-5-policy-optimization/02-policy-gradient-derivation.md) · [VI·09](../part-6-fundamental-rl/09-policy-gradients.md) |
| `markov` | [IV·03](../part-4-probability/03-markov-processes.md) · [VI·03](../part-6-fundamental-rl/03-mdp.md) |
| `mdp` | [I·04](../part-1-limits-series/04-bellman-and-discounting.md) · [IV·03](../part-4-probability/03-markov-processes.md) · [IV·04](../part-4-probability/04-value-functions-bellman.md) · [VI·03](../part-6-fundamental-rl/03-mdp.md) |
| `optimization` | [II·03](../part-2-derivatives-gradient/03-gradient-descent.md) · [III·06](../part-3-linear-algebra/06-advanced-topics.md) · [V·03](../part-5-policy-optimization/03-gradient-descent-variants.md) · [VII·03](../part-7-deep-rl/03-calculus.md) |
| `policy-gradient` | [II·04](../part-2-derivatives-gradient/04-policy-gradient-application.md) · [V·01](../part-5-policy-optimization/01-policy-optimization-basics.md) · [V·02](../part-5-policy-optimization/02-policy-gradient-derivation.md) · [VI·09](../part-6-fundamental-rl/09-policy-gradients.md) |
| `probability` | [IV·01](../part-4-probability/01-probability-theory.md) · [VI·01](../part-6-fundamental-rl/01-probability-foundation.md) · [VII·04](../part-7-deep-rl/04-probability-statistics.md) |
| `q-learning` | [I·07](../part-1-limits-series/07-examples-and-tasks.md) · [VI·06](../part-6-fundamental-rl/06-model-free-rl.md) |
| `reinforce` | [V·02](../part-5-policy-optimization/02-policy-gradient-derivation.md) · [VI·09](../part-6-fundamental-rl/09-policy-gradients.md) |
| `return` | [I·03](../part-1-limits-series/03-limits-in-rl.md) · [I·06](../part-1-limits-series/06-discounting-in-rl.md) · [VI·04](../part-6-fundamental-rl/04-return-policy-value.md) |
| `rl-algorithms` | [IV·05](../part-4-probability/05-rl-algorithms.md) · [VII·02](../part-7-deep-rl/02-algorithms-overview.md) |
| `rl-bridge` | [I·00](../part-1-limits-series/00-introduction.md) · [I·03](../part-1-limits-series/03-limits-in-rl.md) · [VI·00](../part-6-fundamental-rl/00-introduction.md) · [VI·10](../part-6-fundamental-rl/10-unity-ml-agents-bridge.md) · [VII·01](../part-7-deep-rl/01-core-concepts.md) |
| `statistics` | [IV·02](../part-4-probability/02-statistics.md) · [VII·04](../part-7-deep-rl/04-probability-statistics.md) |
| `summary` | [II·05](../part-2-derivatives-gradient/05-big-picture.md) · [VI·11](../part-6-fundamental-rl/11-conclusion.md) |
| `td` | [II·04](../part-2-derivatives-gradient/04-policy-gradient-application.md) · [VI·06](../part-6-fundamental-rl/06-model-free-rl.md) · [VI·07](../part-6-fundamental-rl/07-eligibility-traces.md) |
| `value-function` | [I·04](../part-1-limits-series/04-bellman-and-discounting.md) · [I·05](../part-1-limits-series/05-value-iteration.md) · [IV·04](../part-4-probability/04-value-functions-bellman.md) · [VI·04](../part-6-fundamental-rl/04-return-policy-value.md) · [VI·05](../part-6-fundamental-rl/05-bellman-equations.md) |

## 3. Раздел → уроки (сводка)

| Раздел пособия | Уроки |
|---|---|
| [I · Введение](../part-1-limits-series/00-introduction.md) | [2-5](https://rl-cuber-unity-code.com/courses/2-5) |
| [I · 1. Теоретические основы: предел последовательности](../part-1-limits-series/01-sequence-limit.md) | [1-3](https://rl-cuber-unity-code.com/courses/1-3), [2-5](https://rl-cuber-unity-code.com/courses/2-5) |
| [I · 2. Бесконечные ряды и их сходимость](../part-1-limits-series/02-infinite-series.md) | [1-1](https://rl-cuber-unity-code.com/courses/1-1), [2-4](https://rl-cuber-unity-code.com/courses/2-4), [2-5](https://rl-cuber-unity-code.com/courses/2-5) |
| [I · 3. Пределы и ряды в контексте обучения с подкреплением](../part-1-limits-series/03-limits-in-rl.md) | [1-1](https://rl-cuber-unity-code.com/courses/1-1), [2-4](https://rl-cuber-unity-code.com/courses/2-4) |
| [I · 4. Уравнения Беллмана и дисконтирование](../part-1-limits-series/04-bellman-and-discounting.md) | **[1-1](https://rl-cuber-unity-code.com/courses/1-1)**, [1-3](https://rl-cuber-unity-code.com/courses/1-3), [1-4](https://rl-cuber-unity-code.com/courses/1-4), [1-6](https://rl-cuber-unity-code.com/courses/1-6), [2-4](https://rl-cuber-unity-code.com/courses/2-4) |
| [I · 5. Итерация ценности: сходимость на практике](../part-1-limits-series/05-value-iteration.md) | [1-3](https://rl-cuber-unity-code.com/courses/1-3), [1-4](https://rl-cuber-unity-code.com/courses/1-4), [1-6](https://rl-cuber-unity-code.com/courses/1-6), [2-5](https://rl-cuber-unity-code.com/courses/2-5) |
| [I · 6. Дисконтирование в RL и его влияние](../part-1-limits-series/06-discounting-in-rl.md) | **[2-4](https://rl-cuber-unity-code.com/courses/2-4)**, [1-1](https://rl-cuber-unity-code.com/courses/1-1) |
| [I · 7. Примеры, аналогии и задачи](../part-1-limits-series/07-examples-and-tasks.md) | [1-3](https://rl-cuber-unity-code.com/courses/1-3), [1-4](https://rl-cuber-unity-code.com/courses/1-4), [2-4](https://rl-cuber-unity-code.com/courses/2-4) |
| [I · 8. Интерактивные визуализации сходимости](../part-1-limits-series/08-convergence-visualizations.md) | [1-3](https://rl-cuber-unity-code.com/courses/1-3), [2-5](https://rl-cuber-unity-code.com/courses/2-5), [2-6](https://rl-cuber-unity-code.com/courses/2-6) |
| [I · 8b. Практические задачи: пределы и сходимость](../part-1-limits-series/09-practice-limits.md) | [1-3](https://rl-cuber-unity-code.com/courses/1-3), [2-4](https://rl-cuber-unity-code.com/courses/2-4) |
| [I · 9. Источники](../part-1-limits-series/10-sources.md) | — |
| [I · Мини-глоссарий](../part-1-limits-series/11-glossary.md) | — |
| [II · § 1. Производные и дифференцирование](../part-2-derivatives-gradient/01-derivatives.md) | [2-1](https://rl-cuber-unity-code.com/courses/2-1) |
| [II · § 2. Частные производные и градиент](../part-2-derivatives-gradient/02-partial-derivatives-gradient.md) | [2-1](https://rl-cuber-unity-code.com/courses/2-1) |
| [II · § 3. Градиентный спуск и оптимизация](../part-2-derivatives-gradient/03-gradient-descent.md) | [1-6](https://rl-cuber-unity-code.com/courses/1-6), [3-6](https://rl-cuber-unity-code.com/courses/3-6) |
| [II · § 4. Применение в RL: Policy Gradient](../part-2-derivatives-gradient/04-policy-gradient-application.md) | [1-4](https://rl-cuber-unity-code.com/courses/1-4), [1-6](https://rl-cuber-unity-code.com/courses/1-6), [2-1](https://rl-cuber-unity-code.com/courses/2-1), [2-2](https://rl-cuber-unity-code.com/courses/2-2) |
| [II · § 5. Весь раздел в одной картине](../part-2-derivatives-gradient/05-big-picture.md) | [2-1](https://rl-cuber-unity-code.com/courses/2-1) |
| [III · 1. Векторы](../part-3-linear-algebra/01-vectors.md) | **[3-7](https://rl-cuber-unity-code.com/courses/3-7)** |
| [III · 2. Матрицы](../part-3-linear-algebra/02-matrices.md) | [3-7](https://rl-cuber-unity-code.com/courses/3-7) |
| [III · 3. Скалярное произведение](../part-3-linear-algebra/03-dot-product.md) | [3-7](https://rl-cuber-unity-code.com/courses/3-7) |
| [III · 4. Собственные значения и собственные векторы](../part-3-linear-algebra/04-eigenvalues.md) | [2-5](https://rl-cuber-unity-code.com/courses/2-5), [3-7](https://rl-cuber-unity-code.com/courses/3-7) |
| [III · 5. Сингулярное разложение (SVD)](../part-3-linear-algebra/05-svd.md) | [3-7](https://rl-cuber-unity-code.com/courses/3-7) |
| [III · 6. Дополнительные темы](../part-3-linear-algebra/06-advanced-topics.md) | [3-6](https://rl-cuber-unity-code.com/courses/3-6), [3-7](https://rl-cuber-unity-code.com/courses/3-7) |
| [IV · 1. Теория вероятностей](../part-4-probability/01-probability-theory.md) | **[2-1](https://rl-cuber-unity-code.com/courses/2-1)** |
| [IV · 2. Статистика](../part-4-probability/02-statistics.md) | [2-6](https://rl-cuber-unity-code.com/courses/2-6) |
| [IV · 3. Марковские процессы](../part-4-probability/03-markov-processes.md) | [1-1](https://rl-cuber-unity-code.com/courses/1-1), [1-3](https://rl-cuber-unity-code.com/courses/1-3) |
| [IV · 4. Функции ценности и уравнения Беллмана](../part-4-probability/04-value-functions-bellman.md) | [1-1](https://rl-cuber-unity-code.com/courses/1-1), [1-3](https://rl-cuber-unity-code.com/courses/1-3), [1-4](https://rl-cuber-unity-code.com/courses/1-4), [1-6](https://rl-cuber-unity-code.com/courses/1-6) |
| [IV · 5. Алгоритмы RL](../part-4-probability/05-rl-algorithms.md) | [1-4](https://rl-cuber-unity-code.com/courses/1-4), [1-6](https://rl-cuber-unity-code.com/courses/1-6), [2-1](https://rl-cuber-unity-code.com/courses/2-1), [2-2](https://rl-cuber-unity-code.com/courses/2-2), [3-1](https://rl-cuber-unity-code.com/courses/3-1) |
| [IV · 6. Практические примеры (Python)](../part-4-probability/06-python-examples.md) | [1-5](https://rl-cuber-unity-code.com/courses/1-5) |
| [V · Лекция 1. Основы RL и оптимизация политики](../part-5-policy-optimization/01-policy-optimization-basics.md) | [2-1](https://rl-cuber-unity-code.com/courses/2-1), [2-2](https://rl-cuber-unity-code.com/courses/2-2) |
| [V · Лекция 2. Вывод градиента политики](../part-5-policy-optimization/02-policy-gradient-derivation.md) | **[2-1](https://rl-cuber-unity-code.com/courses/2-1)**, **[3-4](https://rl-cuber-unity-code.com/courses/3-4)**, [2-2](https://rl-cuber-unity-code.com/courses/2-2) |
| [V · Лекция 3. Градиентный спуск и его варианты](../part-5-policy-optimization/03-gradient-descent-variants.md) | **[1-6](https://rl-cuber-unity-code.com/courses/1-6)**, **[3-6](https://rl-cuber-unity-code.com/courses/3-6)** |
| [V · Лекция 4. Proximal Policy Optimization (PPO)](../part-5-policy-optimization/04-ppo.md) | [2-2](https://rl-cuber-unity-code.com/courses/2-2), [project-3](https://rl-cuber-unity-code.com/courses/project-3), [3-1](https://rl-cuber-unity-code.com/courses/3-1), [3-6](https://rl-cuber-unity-code.com/courses/3-6) |
| [VI · Введение: От интуитивного кодирования к математическому осознанию](../part-6-fundamental-rl/00-introduction.md) | — |
| [VI · Глава 1. Теоретико-вероятностный фундамент](../part-6-fundamental-rl/01-probability-foundation.md) | [2-1](https://rl-cuber-unity-code.com/courses/2-1) |
| [VI · Глава 2. Многорукие бандиты: Исследование vs Использование](../part-6-fundamental-rl/02-multi-armed-bandits.md) | [1-7](https://rl-cuber-unity-code.com/courses/1-7) |
| [VI · Глава 3. Марковские процессы принятия решений (MDP)](../part-6-fundamental-rl/03-mdp.md) | **[1-1](https://rl-cuber-unity-code.com/courses/1-1)**, **[1-3](https://rl-cuber-unity-code.com/courses/1-3)** |
| [VI · Глава 4. Возврат, политики и функции ценности](../part-6-fundamental-rl/04-return-policy-value.md) | [1-1](https://rl-cuber-unity-code.com/courses/1-1), [1-3](https://rl-cuber-unity-code.com/courses/1-3), [1-4](https://rl-cuber-unity-code.com/courses/1-4), [2-4](https://rl-cuber-unity-code.com/courses/2-4) |
| [VI · Глава 5. Сердце RL: Уравнения Беллмана](../part-6-fundamental-rl/05-bellman-equations.md) | **[1-3](https://rl-cuber-unity-code.com/courses/1-3)**, **[1-6](https://rl-cuber-unity-code.com/courses/1-6)**, [1-4](https://rl-cuber-unity-code.com/courses/1-4) |
| [VI · Глава 6. От динамического программирования к Model-Free RL](../part-6-fundamental-rl/06-model-free-rl.md) | **[1-3](https://rl-cuber-unity-code.com/courses/1-3)**, [1-4](https://rl-cuber-unity-code.com/courses/1-4), [1-6](https://rl-cuber-unity-code.com/courses/1-6) |
| [VI · Глава 7. Следы пригодности (Eligibility Traces)](../part-6-fundamental-rl/07-eligibility-traces.md) | [1-4](https://rl-cuber-unity-code.com/courses/1-4), [1-6](https://rl-cuber-unity-code.com/courses/1-6), [2-2](https://rl-cuber-unity-code.com/courses/2-2) |
| [VI · Глава 8. Аппроксимация функций и Deep RL](../part-6-fundamental-rl/08-function-approximation.md) | [1-5](https://rl-cuber-unity-code.com/courses/1-5), [1-6](https://rl-cuber-unity-code.com/courses/1-6) |
| [VI · Глава 9. Методы градиента политики (Policy Gradients)](../part-6-fundamental-rl/09-policy-gradients.md) | **[2-2](https://rl-cuber-unity-code.com/courses/2-2)**, **[3-1](https://rl-cuber-unity-code.com/courses/3-1)**, [2-1](https://rl-cuber-unity-code.com/courses/2-1), [2-3](https://rl-cuber-unity-code.com/courses/2-3) |
| [VI · Глава 10. Мост к практике: Unity ML-Agents](../part-6-fundamental-rl/10-unity-ml-agents-bridge.md) | [1-2](https://rl-cuber-unity-code.com/courses/1-2), [project-1](https://rl-cuber-unity-code.com/courses/project-1), [project-2](https://rl-cuber-unity-code.com/courses/project-2), [project-3](https://rl-cuber-unity-code.com/courses/project-3), [3-1](https://rl-cuber-unity-code.com/courses/3-1) |
| [VI · Заключение](../part-6-fundamental-rl/11-conclusion.md) | — |
| [VI · Мини-глоссарий](../part-6-fundamental-rl/12-glossary.md) | — |
| [VII · 1.1 Основные понятия](../part-7-deep-rl/01-core-concepts.md) | [1-5](https://rl-cuber-unity-code.com/courses/1-5), [1-6](https://rl-cuber-unity-code.com/courses/1-6) |
| [VII · 1.2 Обзор алгоритмов RL](../part-7-deep-rl/02-algorithms-overview.md) | [1-5](https://rl-cuber-unity-code.com/courses/1-5), [1-6](https://rl-cuber-unity-code.com/courses/1-6), [2-2](https://rl-cuber-unity-code.com/courses/2-2), [3-1](https://rl-cuber-unity-code.com/courses/3-1) |
| [VII · 2.1 Математический анализ](../part-7-deep-rl/03-calculus.md) | [2-1](https://rl-cuber-unity-code.com/courses/2-1), [3-6](https://rl-cuber-unity-code.com/courses/3-6) |
| [VII · 2.2 Теория вероятностей и статистика](../part-7-deep-rl/04-probability-statistics.md) | [2-1](https://rl-cuber-unity-code.com/courses/2-1), [2-6](https://rl-cuber-unity-code.com/courses/2-6), [3-4](https://rl-cuber-unity-code.com/courses/3-4) |
| [VII · 2.3 Дифференциальные уравнения](../part-7-deep-rl/05-differential-equations.md) | [3-1](https://rl-cuber-unity-code.com/courses/3-1) |

**Жирным** — связь уже есть в реестре сайта; обычным — предлагаемая.
