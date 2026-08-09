# Интерактивное пособие по математике ML и RL

Полный курс математики, необходимой для обучения с подкреплением: от предела последовательности до формул PPO и конфигурации Unity ML-Agents. **51 раздел, 7 частей**, все написаны как самостоятельные лекции по правилам [Ermakov Notes Framework](../docs/00_Project_Charter.md).

Эта страница — точка входа. С неё можно перейти в любой раздел; внутри разделов расставлены перекрёстные ссылки: всякий раз, когда для разбора одного понятия нужно другое, стоит ссылка на раздел, где оно вводится.

## Как читать

**Подряд.** Части I–V строят математический аппарат, часть VI собирает из него алгоритмы RL, часть VII разбирает специфику глубокого обучения. Порядок частей — порядок зависимостей.

**По необходимости.** Если известно, чего не хватает, идите прямо в нужный раздел: недостающие предпосылки указаны ссылками в начале каждой части.

**От практики.** Если перед глазами конфигурация обучения, начните с [главы 10 части VI](part-6-fundamental-rl/10-unity-ml-agents-bridge.md) — она сопоставляет поля `.yaml` с математическими объектами и ведёт ссылками к разбору каждого.

## Части

| # | Часть | Разделов | О чём |
|---|---|---|---|
| I | [Пределы, последовательности и ряды](part-1-limits-series/index.md) | 12 | почему бесконечная сумма наград — число и когда итерации можно остановить |
| II | [Производные, градиент и оптимизация](part-2-derivatives-gradient/index.md) | 5 | в какую сторону двигать параметры и насколько |
| III | [Линейная алгебра для RL](part-3-linear-algebra/index.md) | 6 | язык векторов и матриц; почему обучение идёт быстро или медленно |
| IV | [От вероятности к алгоритмам RL](part-4-probability/index.md) | 6 | ожидание, дисперсия, марковские процессы, четыре уравнения Беллмана |
| V | [Методы оптимизации политик](part-5-policy-optimization/index.md) | 4 | вывод градиента политики и устройство PPO |
| VI | [Фундаментальная математика RL](part-6-fundamental-rl/index.md) | 13 | ядро: от бандитов до актор-критика и моста в Unity |
| VII | [Глубокое обучение с подкреплением](part-7-deep-rl/index.md) | 5 | что меняется при замене таблицы нейросетью |

## Все разделы

### I. Пределы, последовательности и ряды

- [Введение](part-1-limits-series/00-introduction.md) · [1. Предел последовательности](part-1-limits-series/01-sequence-limit.md) · [2. Бесконечные ряды](part-1-limits-series/02-infinite-series.md)
- [3. Пределы и ряды в RL](part-1-limits-series/03-limits-in-rl.md) · [4. Уравнения Беллмана и дисконтирование](part-1-limits-series/04-bellman-and-discounting.md) · [5. Итерация ценности](part-1-limits-series/05-value-iteration.md)
- [6. Дисконтирование в RL](part-1-limits-series/06-discounting-in-rl.md) · [7. Примеры и задачи](part-1-limits-series/07-examples-and-tasks.md) · [8. Визуализации сходимости](part-1-limits-series/08-convergence-visualizations.md)
- [8b. Практические задачи](part-1-limits-series/09-practice-limits.md) · [9. Источники](part-1-limits-series/10-sources.md) · [Мини-глоссарий](part-1-limits-series/11-glossary.md)

### II. Производные, градиент и оптимизация

- [§ 1. Производные и дифференцирование](part-2-derivatives-gradient/01-derivatives.md) · [§ 2. Частные производные и градиент](part-2-derivatives-gradient/02-partial-derivatives-gradient.md)
- [§ 3. Градиентный спуск](part-2-derivatives-gradient/03-gradient-descent.md) · [§ 4. Применение в RL: Policy Gradient](part-2-derivatives-gradient/04-policy-gradient-application.md) · [§ 5. Весь раздел в одной картине](part-2-derivatives-gradient/05-big-picture.md)

### III. Линейная алгебра для RL

- [1. Векторы](part-3-linear-algebra/01-vectors.md) · [2. Матрицы](part-3-linear-algebra/02-matrices.md) · [3. Скалярное произведение](part-3-linear-algebra/03-dot-product.md)
- [4. Собственные значения и векторы](part-3-linear-algebra/04-eigenvalues.md) · [5. Сингулярное разложение](part-3-linear-algebra/05-svd.md) · [6. Дополнительные темы](part-3-linear-algebra/06-advanced-topics.md)

### IV. От вероятности к алгоритмам RL

- [1. Теория вероятностей](part-4-probability/01-probability-theory.md) · [2. Статистика](part-4-probability/02-statistics.md) · [3. Марковские процессы](part-4-probability/03-markov-processes.md)
- [4. Функции ценности и уравнения Беллмана](part-4-probability/04-value-functions-bellman.md) · [5. Алгоритмы RL](part-4-probability/05-rl-algorithms.md) · [6. Практические примеры на Python](part-4-probability/06-python-examples.md)

### V. Методы оптимизации политик

- [Лекция 1. Основы оптимизации политики](part-5-policy-optimization/01-policy-optimization-basics.md) · [Лекция 2. Вывод градиента политики](part-5-policy-optimization/02-policy-gradient-derivation.md)
- [Лекция 3. Варианты градиентного спуска](part-5-policy-optimization/03-gradient-descent-variants.md) · [Лекция 4. Proximal Policy Optimization](part-5-policy-optimization/04-ppo.md)

### VI. Фундаментальная математика RL

- [Введение](part-6-fundamental-rl/00-introduction.md) · [Гл. 1. Вероятностный фундамент](part-6-fundamental-rl/01-probability-foundation.md) · [Гл. 2. Многорукие бандиты](part-6-fundamental-rl/02-multi-armed-bandits.md)
- [Гл. 3. MDP](part-6-fundamental-rl/03-mdp.md) · [Гл. 4. Возврат, политики, ценность](part-6-fundamental-rl/04-return-policy-value.md) · [Гл. 5. Уравнения Беллмана](part-6-fundamental-rl/05-bellman-equations.md)
- [Гл. 6. Model-Free RL](part-6-fundamental-rl/06-model-free-rl.md) · [Гл. 7. Следы пригодности](part-6-fundamental-rl/07-eligibility-traces.md) · [Гл. 8. Аппроксимация и Deep RL](part-6-fundamental-rl/08-function-approximation.md)
- [Гл. 9. Градиент политики](part-6-fundamental-rl/09-policy-gradients.md) · [Гл. 10. Мост к Unity ML-Agents](part-6-fundamental-rl/10-unity-ml-agents-bridge.md) · [Заключение](part-6-fundamental-rl/11-conclusion.md) · [Мини-глоссарий](part-6-fundamental-rl/12-glossary.md)

### VII. Глубокое обучение с подкреплением

- [1.1 Основные понятия](part-7-deep-rl/01-core-concepts.md) · [1.2 Обзор алгоритмов RL](part-7-deep-rl/02-algorithms-overview.md) · [2.1 Математический анализ](part-7-deep-rl/03-calculus.md)
- [2.2 Вероятность и статистика](part-7-deep-rl/04-probability-statistics.md) · [2.3 Дифференциальные уравнения](part-7-deep-rl/05-differential-equations.md)

## Ответы на частые вопросы — где искать

| Вопрос | Раздел |
|---|---|
| Какое `gamma` поставить? | [I · 6. Дисконтирование в RL](part-1-limits-series/06-discounting-in-rl.md) |
| Почему обучение расходится? | [II · § 3. Градиентный спуск](part-2-derivatives-gradient/03-gradient-descent.md), [VI · гл. 8](part-6-fundamental-rl/08-function-approximation.md) |
| Почему обучение идёт медленно? | [III · 4. Собственные значения](part-3-linear-algebra/04-eigenvalues.md) |
| Агент лучше или это шум? | [IV · 2. Статистика](part-4-probability/02-statistics.md) |
| Агент колеблется и дёргается | [IV · 3. Марковские процессы](part-4-probability/03-markov-processes.md), [VI · гл. 3](part-6-fundamental-rl/03-mdp.md) |
| Откуда взялась формула PPO? | [V · Лекция 4. PPO](part-5-policy-optimization/04-ppo.md) |
| SARSA или Q-обучение? | [VI · гл. 6. Model-Free RL](part-6-fundamental-rl/06-model-free-rl.md) |
| Что означает поле в `.yaml`? | [VI · гл. 10. Мост к Unity](part-6-fundamental-rl/10-unity-ml-agents-bridge.md) |
| Какой алгоритм выбрать? | [IV · 5. Алгоритмы RL](part-4-probability/05-rl-algorithms.md), [VII · 1.2](part-7-deep-rl/02-algorithms-overview.md) |

## Как устроен раздел

Каждый файл — лекция по правилам ENF в режиме Learning Mode:

- **Зачем это нужно** — задача, которую тема решает, до всякого формализма;
- **Обозначения** — таблица символов с ролями, заполненная до первой формулы;
- **содержательные разделы** — постановка, вывод с названным основанием каждого шага, разобранный числовой пример;
- **Что стоит запомнить** — 4–5 пунктов, остающихся через полгода;
- **Проверка себя** — вопросы по нарастанию сложности;
- **Навигация, См. также, Уроки курса, Практика в репозитории, Источник на сайте** — связи наружу и внутрь пособия.

## Связи

- **Вертикальные** — часть ⇄ раздел ⇄ подпараграф.
- **Горизонтальные** — блок «См. также» связывает разделы разных частей по общим темам (`bellman`, `gradient`, `mdp`, …); полный реестр — [`_meta/crosslinks.md`](_meta/crosslinks.md).
- **Наружу, в курс** — 15 связей взяты из реестра сайта, остальные помечены как предлагаемые.
- **Наружу, в код** — привязка к средам `Assets/ML-ENVIRONMENTS` и trainer-конфигам, сводка в [`_meta/unity-bridge.md`](_meta/unity-bridge.md).

## Навигация

- [Полное оглавление](SUMMARY.md)
- [Карта mind map](_meta/mindmap.md)
- [Реестр перекрёстных ссылок](_meta/crosslinks.md)
- [24 раздела курса](_meta/lessons.md)
- [Мост в Unity-репозиторий](_meta/unity-bridge.md)
- [Соглашения по наполнению](_meta/conventions.md)
- [Перенос пособия на сайт](_meta/site-integration.md)

## Проверка

Все разделы проходят машинные проверки уровня 1 фреймворка:

```powershell
pwsh Scripts/check.ps1 math-textbook
```

---

Каркас структуры собран скриптом [`_meta/generate.py`](_meta/generate.py) из mind map сайта; содержание разделов написано поверх него и повторным запуском генератора будет затёрто — запускать его больше не следует.
