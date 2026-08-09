---
id: part-4
title: "Часть V. Методы оптимизации политик"
part_id: part-4
order: 5
hub_url: "https://rl-cuber-unity-code.com/math-rl/module-4"
sections: 4
mindmap_nodes: 4
enf_mode: learning
discipline: meta
duration: 20
date: 2026-08-09
status: ready
---

# Часть V. Методы оптимизации политик

Часть доводит одну линию до конца: от постановки задачи «оптимизировать политику напрямую» до формул PPO, применяемого в Unity ML-Agents по умолчанию. Каждый гиперпараметр конфигурации к концу части оказывается не настройкой из документации, а членом выведенной формулы.

Ветвь mind map: **V · Оптимизация политик** — 4 узла, 4 раздела пособия.

**Что нужно знать заранее.** Градиент и градиентный спуск из [Части II](../part-2-derivatives-gradient/03-gradient-descent.md); математическое ожидание и дисперсия из [Части IV](../part-4-probability/01-probability-theory.md); функции ценности из [Части IV](../part-4-probability/04-value-functions-bellman.md).

**Что будет уметь читатель.** Ставить задачу оптимизации политики и объяснять, почему прямое дифференцирование невозможно; проводить вывод градиента политики все шесть шагов; доказывать инвариантность к базису и понимать, почему базис не может зависеть от действия; выбирать между Momentum, RMSProp и Adam по свойствам задачи; читать формулу PPO и связывать каждое слагаемое с параметром конфигурации; диагностировать обучение по логам.

**Порядок чтения.** Лекции 1–2 читаются подряд и составляют теоретическое ядро. Лекция 3 независима и полезна сама по себе — её можно читать сразу после [Части II](../part-2-derivatives-gradient/03-gradient-descent.md). Лекция 4 опирается на все предыдущие.

## Разделы

- [Лекция 1. Основы RL и оптимизация политики](01-policy-optimization-basics.md) · mind map: **Основы оптимизации политики** (`intermediate`)
- [Лекция 2. Вывод градиента политики](02-policy-gradient-derivation.md) · mind map: **Вывод градиента политики** (`advanced`)
- [Лекция 3. Градиентный спуск и его варианты](03-gradient-descent-variants.md) · mind map: **Варианты градиентного спуска** (`intermediate`)
- [Лекция 4. Proximal Policy Optimization (PPO)](04-ppo.md) · mind map: **PPO** (`advanced`)

## Узлы mind map этой ветви

- **Основы оптимизации политики** (`intermediate`) → [Лекция 1. Основы RL и оптимизация политики](01-policy-optimization-basics.md)
- **Вывод градиента политики** (`advanced`) → [Лекция 2. Вывод градиента политики](02-policy-gradient-derivation.md)
- **Варианты градиентного спуска** (`intermediate`) → [Лекция 3. Градиентный спуск и его варианты](03-gradient-descent-variants.md)
- **PPO** (`advanced`) → [Лекция 4. Proximal Policy Optimization (PPO)](04-ppo.md)

## Навигация

- ← Предыдущая часть: [Часть IV. От вероятности к алгоритмам RL](../part-4-probability/index.md)
- → Следующая часть: [Часть VI. Фундаментальная математика RL](../part-6-fundamental-rl/index.md)
- Оглавление: [SUMMARY](../SUMMARY.md) · [Карта](../_meta/mindmap.md)

## Источник на сайте

- [Методы оптимизации политик](https://rl-cuber-unity-code.com/math-rl/module-4)
