---
id: part-1-10
title: "9. Источники"
part: "I · Пределы и ряды"
part_id: part-1
order: 10
mindmap_node: null
difficulty: null
tags: ["refs"]
hub_url: "https://rl-cuber-unity-code.com/math-rl/module-1#9-источники"
hub_anchor_canonical: null
enf_mode: learning
discipline: meta
duration: 40
date: 2026-08-09
status: ready
---

# 9. Источники

Литература, на которую опирается Часть I. Список разделён по назначению: одни книги нужны, чтобы восполнить пробел в анализе, другие — чтобы увидеть, откуда взялись формулы RL, третьи содержат первоисточники конкретных теорем, упомянутых в разделах.

## Математический анализ: пределы и ряды

- **Зорич В. А.** Математический анализ. Часть I. — 10-е изд. — М.: МЦНМО, 2019. Строгое изложение теории пределов; главы 3 и 5 покрывают материал [раздела 1](01-sequence-limit.md) и [раздела 2](02-infinite-series.md).
- **Фихтенгольц Г. М.** Курс дифференциального и интегрального исчисления. Том I. — М.: Физматлит. Подробнее и медленнее Зорича, с большим числом разобранных примеров; полезен как задачник по технике вычисления пределов.
- **Rudin W.** Principles of Mathematical Analysis. 3rd ed. — McGraw-Hill, 1976. Глава 3 — последовательности и ряды, глава 9 содержит принцип сжимающих отображений в той форме, в которой он применён в [разделе 5](05-value-iteration.md).

## Обучение с подкреплением: базовые книги

- **Sutton R. S., Barto A. G.** Reinforcement Learning: An Introduction. 2nd ed. — MIT Press, 2018. Основной учебник области. Главы 3–4 соответствуют разделам [4](04-bellman-and-discounting.md) и [5](05-value-iteration.md) этой части: определения возврата, уравнения Беллмана, итерация ценности.
- **Puterman M. L.** Markov Decision Processes: Discrete Stochastic Dynamic Programming. — Wiley, 1994. Наиболее полное изложение теории MDP: условия существования оптимальной политики, сходимость итерационных методов, оценки скорости.
- **Bertsekas D. P.** Dynamic Programming and Optimal Control. — Athena Scientific. Акцент на сжимающих отображениях и оценках погрешности; отсюда взята форма критерия остановки, приведённая в [разделе 5](05-value-iteration.md).

## Первоисточники теорем, упомянутых в части

- **Bellman R.** Dynamic Programming. — Princeton University Press, 1957. Работа, в которой введено уравнение, носящее имя автора.
- **Robbins H., Monro S.** A Stochastic Approximation Method // Annals of Mathematical Statistics. — 1951. — Vol. 22, № 3. — P. 400–407. Источник условий на скорость обучения, разобранных в [разделе 7](07-examples-and-tasks.md).
- **Watkins C. J. C. H., Dayan P.** Q-learning // Machine Learning. — 1992. — Vol. 8, № 3–4. — P. 279–292. Доказательство сходимости табличного Q-обучения.
- **Jaakkola T., Jordan M. I., Singh S. P.** On the Convergence of Stochastic Iterative Dynamic Programming Algorithms // Neural Computation. — 1994. — Vol. 6, № 6. — P. 1185–1201. Более общая формулировка условий сходимости, охватывающая и TD-обучение.
- **Ng A. Y., Harada D., Russell S.** Policy Invariance Under Reward Transformations: Theory and Application to Reward Shaping // Proceedings of ICML. — 1999. — P. 278–287. Теорема о потенциальном формировании награды из [раздела 6](06-discounting-in-rl.md).

## Практика и инструменты

- **Unity Technologies.** ML-Agents Toolkit Documentation. Описание гиперпараметров конфигурации, включая `gamma`, и рекомендаций по масштабу наград.
- **Mnih V. et al.** Human-level control through deep reinforcement learning // Nature. — 2015. — Vol. 518. — P. 529–533. Статья о DQN; полезна как иллюстрация того, что происходит с оценками сходимости при переходе к аппроксимации функции ценности нейросетью.

## Как пользоваться списком

Порядок чтения зависит от того, чего не хватает.

- Если непонятны рассуждения с $\varepsilon$ и $N$ — Зорич, глава 3, затем задачи из Фихтенгольца.
- Если понятна математика, но неясно её место в RL — Sutton & Barto, главы 3–4, параллельно с разделами 3–6 этой части.
- Если нужны точные условия и оценки для реализации — Puterman и Bertsekas.
- Если интересует, что ломается при переходе к нейросетям — Mnih et al. и [Часть VII](../part-7-deep-rl/index.md).

## Навигация

- Часть: [I · Пределы, последовательности и ряды](index.md)
- ← Предыдущий: [8b. Практические задачи: пределы и сходимость](09-practice-limits.md)
- → Следующий: [Мини-глоссарий](11-glossary.md)
- Оглавление: [SUMMARY](../SUMMARY.md) · [Карта](../_meta/mindmap.md)

## См. также (другие части пособия)

- _(пересечений по темам нет)_

## Уроки курса

- _(прямых связей с уроками не выявлено)_

## Практика в этом репозитории

- _(прямой привязки к средам нет)_

## Источник на сайте

- [I · Пределы, последовательности и ряды → 9. Источники](https://rl-cuber-unity-code.com/math-rl/module-1#9-источники)
