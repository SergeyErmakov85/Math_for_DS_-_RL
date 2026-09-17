# -*- coding: utf-8 -*-
"""Генератор каркаса учебного пособия по математике ML/RL.

Источник структуры — mind map и модули хаба «Математика RL»
(rl-cuber-unity-code.com), реестр перекрёстных ссылок сайта
и математика, реализованная в средах этого репозитория.
"""
import os, re, json, io

ROOT = r"C:\unity-ml-agents-lab\math-textbook"
SITE = "https://rl-cuber-unity-code.com"

# ---------------------------------------------------------------- slug сайта
def hub_anchor(title):
    """Повторяет slugify сайта: lower, [^\\w а-яё]+ -> '-', trim '-', срез 60."""
    s = title.lower()
    s = re.sub(r"[^0-9a-z_а-яё]+", "-", s, flags=re.IGNORECASE)
    s = s.strip("-")
    return s[:60]

# Часть VI задаёт разделам явные короткие id (введение, глава-1 … глава-10).
# Компонент рендерит оба якоря, но реестр перекрёстных ссылок сайта использует короткий.
CANON = {"part-5": {
    "Введение: От интуитивного кодирования к математическому осознанию": "введение",
    **{t: f"глава-{n}" for n, t in enumerate([
        "Глава 1. Теоретико-вероятностный фундамент",
        "Глава 2. Многорукие бандиты: Исследование vs Использование",
        "Глава 3. Марковские процессы принятия решений (MDP)",
        "Глава 4. Возврат, политики и функции ценности",
        "Глава 5. Сердце RL: Уравнения Беллмана",
        "Глава 6. От динамического программирования к Model-Free RL",
        "Глава 7. Следы пригодности (Eligibility Traces)",
        "Глава 8. Аппроксимация функций и Deep RL",
        "Глава 9. Методы градиента политики (Policy Gradients)",
        "Глава 10. Мост к практике: Unity ML-Agents"], start=1)},
}}

# ---------------------------------------------------------------- структура
# (номер, заголовок как на сайте, файловый слаг, [подпараграфы], [теги])
PARTS = [
 dict(id="part-1", num="I", roman="I", title="Пределы, последовательности и ряды",
      short="Пределы и ряды", caption="Сходимость, ряды, дисконтирование",
      base="/math-rl/module-1", dir="part-1-limits-series", color="cyan",
      sections=[
   ("00","Введение","introduction",[],["convergence","rl-bridge"]),
   ("01","1. Теоретические основы: предел последовательности","sequence-limit",
     ["1.1 Предел последовательности"],["limit","convergence"]),
   ("02","2. Бесконечные ряды и их сходимость","infinite-series",
     ["Геометрический ряд","Необходимое условие сходимости","Абсолютная сходимость"],
     ["series","convergence","discounting"]),
   ("03","3. Пределы и ряды в контексте обучения с подкреплением","limits-in-rl",[],
     ["discounting","return","rl-bridge"]),
   ("04","4. Уравнения Беллмана и дисконтирование","bellman-and-discounting",
     ["Функция ценности состояния","Уравнение оптимальности Беллмана","Пример: MDP с двумя состояниями"],
     ["bellman","value-function","discounting","mdp"]),
   ("05","5. Итерация ценности: сходимость на практике","value-iteration",[],
     ["bellman","dp","convergence","value-function"]),
   ("06","6. Дисконтирование в RL и его влияние","discounting-in-rl",[],
     ["discounting","return","reward-design"]),
   ("07","7. Примеры, аналогии и задачи","examples-and-tasks",
     ["7.1 Предел последовательности: рекурсия","7.2 Сумма геометрического ряда",
      "7.3 Дисконтированные награды в RL","7.4 Конвергенция Q-обучения"],
     ["exercises","limit","series","q-learning"]),
   ("08","8. Интерактивные визуализации сходимости","convergence-visualizations",
     ["8.1 Сходимость геометрического ряда","8.2 Визуализация итерации ценности"],
     ["viz","convergence","dp"]),
   ("09","8b. Практические задачи: пределы и сходимость","practice-limits",[],
     ["exercises","limit","series"]),
   ("10","9. Источники","sources",[],["refs"]),
   ("11","Мини-глоссарий","glossary",[],["glossary"]),
      ]),
 dict(id="part-1b", num="II", roman="II", title="Производные, градиент и оптимизация",
      short="Производные и градиент", caption="Дифференцирование и оптимизация",
      base="/math-rl/calculus", dir="part-2-derivatives-gradient", color="emerald",
      sections=[
   ("01","§ 1. Производные и дифференцирование","derivatives",
     ["Определение производной","Три интуиции","Таблица основных производных","Правила дифференцирования"],
     ["derivative"]),
   ("02","§ 2. Частные производные и градиент","partial-derivatives-gradient",
     ["Функции многих переменных","Частная производная","Градиент"],
     ["gradient","derivative"]),
   ("03","§ 3. Градиентный спуск и оптимизация","gradient-descent",
     ["Варианты градиентного спуска","Проблемы и решения"],
     ["gradient-descent","optimization"]),
   ("04","§ 4. Применение в RL: Policy Gradient","policy-gradient-application",
     ["Задача оптимизации политики","Теорема о градиенте политики","TD-ошибка как стохастический градиент"],
     ["policy-gradient","gradient","td"]),
   ("05","§ 5. Весь раздел в одной картине","big-picture",[],["summary","gradient"]),
      ]),
 dict(id="part-2", num="III", roman="III", title="Линейная алгебра для RL",
      short="Линейная алгебра", caption="Векторы, матрицы, SVD",
      base="/math-rl/module-2", dir="part-3-linear-algebra", color="blue",
      sections=[
   ("01","1. Векторы","vectors",
     ["1.4. Линейная комбинация векторов","1.5. Линейная зависимость и независимость","1.6. Базис и размерность"],
     ["vector","linear-algebra"]),
   ("02","2. Матрицы","matrices",
     ["2.1. Определение и типы матриц","2.2. Операции над матрицами","2.3. Определитель матрицы",
      "2.4. Ранг матрицы","2.5. Обратная матрица"],
     ["matrix","linear-algebra"]),
   ("03","3. Скалярное произведение","dot-product",[],["vector","linear-algebra","similarity"]),
   ("04","4. Собственные значения и собственные векторы","eigenvalues",
     ["Спектральное разложение","Связь с собственными значениями"],
     ["eigen","linear-algebra","convergence"]),
   ("05","5. Сингулярное разложение (SVD)","svd",["Теорема Эккарта-Янга"],
     ["svd","eigen","linear-algebra"]),
   ("06","6. Дополнительные темы","advanced-topics",
     ["6.1. Квадратичные формы","6.2. Ортогональная проекция","6.3. Изменение базиса","6.4. Разложения LU и QR"],
     ["linear-algebra","optimization","quadratic"]),
      ]),
 dict(id="part-3", num="IV", roman="IV", title="От вероятности к алгоритмам RL",
      short="Вероятность", caption="Вероятность, статистика, MDP",
      base="/math-rl/module-3", dir="part-4-probability", color="violet",
      sections=[
   ("01","1. Теория вероятностей","probability-theory",
     ["Основные понятия","Случайные величины и распределения","Ожидаемое значение и дисперсия",
      "Условная вероятность и правило Байеса"],
     ["probability","expectation"]),
   ("02","2. Статистика","statistics",
     ["Описательная статистика","Оценка параметров","Проверка гипотез"],
     ["statistics","estimation"]),
   ("03","3. Марковские процессы","markov-processes",
     ["Цепи Маркова","MDP — Марковский процесс принятия решений"],
     ["markov","mdp"]),
   ("04","4. Функции ценности и уравнения Беллмана","value-functions-bellman",
     ["Функция ценности состояния","Функция ценности действия","Уравнения Беллмана",
      "Уравнения оптимальности Беллмана"],
     ["bellman","value-function","mdp"]),
   ("05","5. Алгоритмы RL","rl-algorithms",
     ["Методы, основанные на ценности","Методы, основанные на политике","Методы, основанные на модели"],
     ["rl-algorithms","value-based","policy-based","model-based"]),
   ("06","6. Практические примеры (Python)","python-examples",
     ["Пример 1: Симуляция бросков монеты","Пример 2: Анализ вознаграждений",
      "Пример 3: Оценка политики в MDP","Упражнения для самопроверки"],
     ["python","exercises"]),
      ]),
 dict(id="part-4", num="V", roman="V", title="Методы оптимизации политик",
      short="Оптимизация политик", caption="Вывод градиента и PPO",
      base="/math-rl/module-4", dir="part-5-policy-optimization", color="purple",
      sections=[
   ("01","Лекция 1. Основы RL и оптимизация политики","policy-optimization-basics",
     ["Целевая функция политики"],["policy-optimization","policy-gradient"]),
   ("02","Лекция 2. Вывод градиента политики","policy-gradient-derivation",
     ["Шаг 1: Дифференцирование под знаком интеграла","Шаг 2: Трюк с логарифмом","Шаг 3: Упрощение",
      "Шаг 4: Формула REINFORCE","Шаг 5: Reward-to-go","Шаг 6: Базис и Advantage"],
     ["policy-gradient","log-trick","advantage","reinforce"]),
   ("03","Лекция 3. Градиентный спуск и его варианты","gradient-descent-variants",
     ["1. Momentum","2. RMSProp","3. Adam (Adaptive Moment Estimation)"],
     ["gradient-descent","optimization","adam"]),
   ("04","Лекция 4. Proximal Policy Optimization (PPO)","ppo",
     ["Клиповый суррогат-объектив","Гиперпараметры PPO"],
     ["ppo","policy-optimization","clipping","hyperparameters"]),
      ]),
 dict(id="part-5", num="VI", roman="VI", title="Фундаментальная математика RL",
      short="Фундаментальная RL", caption="Беллман, TD, Actor-Critic",
      base="/math-rl/module-5", dir="part-6-fundamental-rl", color="pink",
      sections=[
   ("00","Введение: От интуитивного кодирования к математическому осознанию","introduction",[],
     ["rl-bridge"]),
   ("01","Глава 1. Теоретико-вероятностный фундамент","probability-foundation",
     ["Случайная величина (Random Variable)","Математическое ожидание (Expected Value)"],
     ["probability","expectation"]),
   ("02","Глава 2. Многорукие бандиты: Исследование vs Использование","multi-armed-bandits",
     ["Дилемма Exploration vs Exploitation","Ценность действия (Action-Value)",
      "ε-жадная стратегия","Верхняя доверительная граница (UCB)"],
     ["bandits","exploration"]),
   ("03","Глава 3. Марковские процессы принятия решений (MDP)","mdp",
     ["Марковское свойство"],["mdp","markov"]),
   ("04","Глава 4. Возврат, политики и функции ценности","return-policy-value",
     ["Возврат (Return)","Политика (Policy)","Функции ценности (Value Functions)"],
     ["return","policy","value-function","discounting"]),
   ("05","Глава 5. Сердце RL: Уравнения Беллмана","bellman-equations",
     ["Рекурсивное разложение возврата","Уравнение ожиданий Беллмана","Уравнение оптимальности Беллмана"],
     ["bellman","value-function","dp"]),
   ("06","Глава 6. От динамического программирования к Model-Free RL","model-free-rl",
     ["Монте-Карло vs Temporal Difference","TD-обучение: величайший прорыв","SARSA vs Q-learning"],
     ["td","monte-carlo","q-learning","sarsa","dp"]),
   ("07","Глава 7. Следы пригодности (Eligibility Traces)","eligibility-traces",
     ["Механизм кратковременной памяти","Backward View: мгновенное распространение"],
     ["td","traces"]),
   ("08","Глава 8. Аппроксимация функций и Deep RL","function-approximation",
     ["Нейросети как аппроксиматоры","DQN: Deep Q-Network"],
     ["function-approximation","dqn","deep-rl"]),
   ("09","Глава 9. Методы градиента политики (Policy Gradients)","policy-gradients",
     ["Параметризация политики","Теорема о градиенте политики","Логарифмический трюк (Log-derivative trick)",
      "Алгоритм REINFORCE","Архитектура Актор-Критик (Actor-Critic)"],
     ["policy-gradient","reinforce","actor-critic","log-trick","advantage"]),
   ("10","Глава 10. Мост к практике: Unity ML-Agents","unity-ml-agents-bridge",
     ["Связь MDP → Unity Event-функции","Гиперпараметры .yaml и их математический смысл"],
     ["unity","hyperparameters","rl-bridge"]),
   ("11","Заключение","conclusion",[],["summary"]),
   ("12","Мини-глоссарий","glossary",[],["glossary"]),
      ]),
 dict(id="part-6", num="VII", roman="VII", title="Глубокое обучение с подкреплением",
      short="Глубокое RL", caption="DQN, статистика, дифуры",
      base="/math-rl/module-6", dir="part-7-deep-rl", color="amber",
      sections=[
   ("01","1.1 Основные понятия","core-concepts",
     ["Ключевые компоненты","Особенности Deep RL"],["deep-rl","rl-bridge"]),
   ("02","1.2 Обзор алгоритмов RL","algorithms-overview",
     ["Deep Q-Network (DQN)","Улучшения DQN","Современные алгоритмы"],
     ["rl-algorithms","dqn","deep-rl"]),
   ("03","2.1 Математический анализ","calculus",
     ["Производные и правила дифференцирования","Частные производные и градиент","Экстремумы функций"],
     ["derivative","gradient","optimization"]),
   ("04","2.2 Теория вероятностей и статистика","probability-statistics",
     ["Нормальное распределение","Оценка максимального правдоподобия (MLE)","Оценка MAP"],
     ["probability","statistics","mle"]),
   ("05","2.3 Дифференциальные уравнения","differential-equations",
     ["ОДУ с разделяющимися переменными","ОДУ второго порядка"],["ode"]),
      ]),
]

# ------------------------------------------------- узлы mind map (39 листьев)
MINDMAP = {
 "part-1":[("Предел последовательности","1. Теоретические основы: предел последовательности","beginner"),
           ("Бесконечные ряды и сходимость","2. Бесконечные ряды и их сходимость","beginner"),
           ("Уравнения Беллмана","4. Уравнения Беллмана и дисконтирование","intermediate"),
           ("Итерация ценности","5. Итерация ценности: сходимость на практике","intermediate"),
           ("Дисконтирование в RL","6. Дисконтирование в RL и его влияние","intermediate"),
           ("Визуализации сходимости","8. Интерактивные визуализации сходимости","beginner")],
 "part-1b":[("Производные и дифференцирование","§ 1. Производные и дифференцирование","beginner"),
           ("Частные производные и градиент","§ 2. Частные производные и градиент","intermediate"),
           ("Градиентный спуск","§ 3. Градиентный спуск и оптимизация","intermediate"),
           ("Policy Gradient","§ 4. Применение в RL: Policy Gradient","advanced"),
           ("Весь раздел в одной картине","§ 5. Весь раздел в одной картине","beginner")],
 "part-2":[("Векторы","1. Векторы","beginner"),("Матрицы","2. Матрицы","beginner"),
           ("Скалярное произведение","3. Скалярное произведение","beginner"),
           ("Собственные значения и векторы","4. Собственные значения и собственные векторы","intermediate"),
           ("Сингулярное разложение (SVD)","5. Сингулярное разложение (SVD)","advanced"),
           ("Дополнительные темы","6. Дополнительные темы","advanced")],
 "part-3":[("Теория вероятностей","1. Теория вероятностей","beginner"),
           ("Статистика","2. Статистика","beginner"),
           ("Марковские процессы","3. Марковские процессы","intermediate"),
           ("Функции ценности и Беллман","4. Функции ценности и уравнения Беллмана","intermediate"),
           ("Алгоритмы RL","5. Алгоритмы RL","advanced"),
           ("Примеры на Python","6. Практические примеры (Python)","intermediate")],
 "part-4":[("Основы оптимизации политики","Лекция 1. Основы RL и оптимизация политики","intermediate"),
           ("Вывод градиента политики","Лекция 2. Вывод градиента политики","advanced"),
           ("Варианты градиентного спуска","Лекция 3. Градиентный спуск и его варианты","intermediate"),
           ("PPO","Лекция 4. Proximal Policy Optimization (PPO)","advanced")],
 "part-5":[("Вероятностный фундамент","Глава 1. Теоретико-вероятностный фундамент","beginner"),
           ("Многорукие бандиты","Глава 2. Многорукие бандиты: Исследование vs Использование","intermediate"),
           ("MDP","Глава 3. Марковские процессы принятия решений (MDP)","intermediate"),
           ("Уравнения Беллмана","Глава 5. Сердце RL: Уравнения Беллмана","intermediate"),
           ("Model-Free RL (TD)","Глава 6. От динамического программирования к Model-Free RL","advanced"),
           ("Policy Gradients","Глава 9. Методы градиента политики (Policy Gradients)","advanced"),
           ("Мост к Unity ML-Agents","Глава 10. Мост к практике: Unity ML-Agents","advanced")],
 "part-6":[("Основные понятия Deep RL","1.1 Основные понятия","intermediate"),
           ("Обзор алгоритмов RL","1.2 Обзор алгоритмов RL","intermediate"),
           ("Математический анализ","2.1 Математический анализ","advanced"),
           ("Вероятность и статистика","2.2 Теория вероятностей и статистика","advanced"),
           ("Дифференциальные уравнения","2.3 Дифференциальные уравнения","advanced")],
}

# ------------------------------------------------------------- 24 раздела курса
LESSONS = [
 ("1-1","Урок 1.1. Что такое обучение с подкреплением?",1,"lesson"),
 ("1-2","Урок 1.2. Установка окружения: PyTorch + Unity ML-Agents",1,"lesson"),
 ("1-3","Урок 1.3. Марковские процессы принятия решений (MDP)",1,"lesson"),
 ("1-4","Урок 1.4. Q-Learning: табличный метод",1,"lesson"),
 ("1-5","Урок 1.5. CartPole — твой первый RL-агент",1,"lesson"),
 ("1-6","Урок 1.6. DQN с нуля на PyTorch",1,"lesson"),
 ("1-7","Урок 1.7. Exploration vs Exploitation",1,"lesson"),
 ("project-1","Проект 1. «Баланс в 3D»",1,"project"),
 ("2-1","Урок 2.1. Policy Gradient и теорема градиента",2,"lesson"),
 ("2-2","Урок 2.2. PPO — реализация с нуля",2,"lesson"),
 ("2-3","Урок 2.3. Непрерывные действия и Actor-Critic",2,"lesson"),
 ("2-4","Урок 2.4. Reward Shaping",2,"lesson"),
 ("2-5","Урок 2.5. Параллельные среды",2,"lesson"),
 ("2-6","Урок 2.6. TensorBoard и W&B",2,"lesson"),
 ("project-2","Проект 2. 3D-охотник",2,"project"),
 ("project-3","Проект 3. Гоночный агент",2,"project"),
 ("3-1","Урок 3.1. SAC — Soft Actor-Critic",3,"lesson"),
 ("3-2","Урок 3.2. MA-POCA и Self-Play",3,"lesson"),
 ("3-3","Урок 3.3. Curriculum Learning и рандомизация среды",3,"lesson"),
 ("3-4","Урок 3.4. Имитационное обучение (BC и GAIL)",3,"lesson"),
 ("3-5","Урок 3.5. Деплой модели: ONNX",3,"lesson"),
 ("3-6","Урок 3.6. Оптимизация гиперпараметров: Optuna + W&B",3,"lesson"),
 ("3-7","Урок 3.7. Архитектуры нейросетей для RL-агентов",3,"lesson"),
 ("3-8","Урок 3.8. Финальный проект: игра с обученным NPC",3,"lesson"),
]
LESSON_TITLE = {i:t for i,t,l,k in LESSONS}

# связи «урок → раздел математики», уже существующие на сайте (crosslinks.ts)
SITE_LINKS = [
 ("1-1","part-5","Глава 3. Марковские процессы принятия решений (MDP)","Формальное определение MDP, V/Q функции"),
 ("1-1","part-1","4. Уравнения Беллмана и дисконтирование","Математика за γ и бесконечными суммами наград"),
 ("1-3","part-5","Глава 5. Сердце RL: Уравнения Беллмана","Рекурсивная структура функции ценности"),
 ("1-3","part-5","Глава 3. Марковские процессы принятия решений (MDP)","Формальное описание MDP-среды"),
 ("1-3","part-5","Глава 6. От динамического программирования к Model-Free RL","Переход от DP к Model-Free методам"),
 ("1-6","part-5","Глава 5. Сердце RL: Уравнения Беллмана","Математическая основа DQN — уравнение Беллмана"),
 ("1-6","part-4","Лекция 3. Градиентный спуск и его варианты","Оптимизация Q-сети через SGD / Adam"),
 ("2-1","part-4","Лекция 2. Вывод градиента политики","Стохастический градиентный подъём для политики"),
 ("2-1","part-3","1. Теория вероятностей","Логарифмические производные и REINFORCE"),
 ("2-2","part-5","Глава 9. Методы градиента политики (Policy Gradients)","Математика GAE и advantage estimation"),
 ("2-4","part-1","6. Дисконтирование в RL и его влияние","Математическое обоснование reward shaping"),
 ("3-1","part-5","Глава 9. Методы градиента политики (Policy Gradients)","Математика soft value функций"),
 ("3-4","part-4","Лекция 2. Вывод градиента политики","GAN-подобная оптимизация в GAIL"),
 ("3-6","part-4","Лекция 3. Градиентный спуск и его варианты","Математика поиска гиперпараметров"),
 ("3-7","part-2",None,"Матричные операции в свёрточных и рекуррентных сетях"),
]

# теги → уроки (предлагаемые связи, дополняют реестр сайта)
TAG_LESSONS = {
 "mdp":["1-1","1-3"], "markov":["1-3"], "bellman":["1-3","1-6"], "value-function":["1-3","1-4"],
 "q-learning":["1-4"], "sarsa":["1-4"], "td":["1-4","1-6"], "monte-carlo":["1-4"],
 "discounting":["1-1","2-4"], "return":["1-1","2-4"], "reward-design":["2-4"],
 "bandits":["1-7"], "exploration":["1-7"],
 "dqn":["1-6"], "deep-rl":["1-5","1-6"], "function-approximation":["1-5","1-6"],
 "gradient-descent":["1-6","3-6"], "adam":["3-6"], "optimization":["3-6"],
 "policy-gradient":["2-1","2-2"], "reinforce":["2-1"], "log-trick":["2-1"],
 "advantage":["2-2"], "actor-critic":["2-3"], "policy-optimization":["2-2"],
 "ppo":["2-2","project-3"], "clipping":["2-2"], "hyperparameters":["3-6","3-1"],
 "probability":["2-1"], "expectation":["2-1"], "statistics":["2-6"], "mle":["3-4"],
 "estimation":["2-6"], "linear-algebra":["3-7"], "matrix":["3-7"], "vector":["3-7"],
 "eigen":["3-7"], "svd":["3-7"], "unity":["1-2","project-1","project-2","project-3"],
 "rl-algorithms":["1-6","2-2","3-1"], "value-based":["1-4","1-6"], "policy-based":["2-1","2-2"],
 "model-based":["3-3"], "python":["1-5"], "viz":["2-6"], "ode":["3-1"],
 "derivative":["2-1"], "gradient":["2-1"], "dp":["1-3"], "traces":["2-2"],
 "similarity":["3-7"], "quadratic":["3-6"], "convergence":["2-5"], "series":["2-4"],
 "limit":["1-3"],
}

# теги → среды и файлы этого репозитория
REPO = {
 "mdp":[("GridWorld 5×5 — MDP на индексах клеток","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md")],
 "markov":[("GridWorld: детерминированные переходы, slipProbability","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs")],
 "bellman":[("GridWorld: CurrentStateIndex 0–24 для табличного Q","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldAgent.cs")],
 "q-learning":[("GridWorld: state = r·5 + c, действия N/S/E/W","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs")],
 "value-function":[("GridWorld: разметка наград по клеткам","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs")],
 "discounting":[("gamma: 0.95 в конфиге GridWorld","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/config/GridWorldQLearning.yaml"),
                ("gamma: 0.99 в конфиге RollerAgent","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml")],
 "reward-design":[("GridWorld: шаг −0.04, цель +1.0, ловушка −1.0","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md")],
 "return":[("GridWorld: доходность кратчайшего пути +0.68","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md")],
 "exploration":[("beta: 5.0e-3 — энтропийный бонус GridWorld","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/config/GridWorldQLearning.yaml")],
 "ppo":[("PPO-конфиг RollerAgent (epsilon 0.2, lambd, num_epoch)","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml"),
        ("Справочные конфиги PPO из ml-agents","config/ml-agents-reference/ppo/")],
 "clipping":[("epsilon: 0.2 — клиппинг PPO","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml")],
 "advantage":[("lambd — параметр GAE","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml")],
 "hyperparameters":[("Все trainer-конфиги проекта","config/ml-agents-reference/"),
                    ("Проверка обучаемости сред","Assets/Editor/MLAgentsTrainingValidator.cs")],
 "policy-gradient":[("RollerAgent: непрерывная политика, 2 действия","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/Scripts/RollerAgent.cs")],
 "gradient-descent":[("learning_rate 3.0e-4, learning_rate_schedule: linear","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml")],
 "vector":[("RollerAgent: вектор наблюдений из 8 чисел","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/Scripts/RollerAgent.cs")],
 "linear-algebra":[("network_settings: hidden_units, num_layers","Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/config/RollerAgent.yaml")],
 "matrix":[("GridWorld: one-hot наблюдение размера 25","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldAgent.cs")],
 "probability":[("slipProbability — модель скольжения FrozenLake","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/Scripts/GridWorldEnvironment.cs")],
 "unity":[("Обучение: scripts/train.ps1","docs/TRAINING.md"),
          ("Сборка сцен из кода","Assets/Editor/ProjectBootstrap.cs")],
 "deep-rl":[("Обучение нейросетевой политики через mlagents-learn","docs/TRAINING.md")],
 "rl-bridge":[("Обзор лаборатории сред","README.md")],
 "dp":[("GridWorld: перебор клеток 5×5 как модель для value iteration","Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/INSTRUCTIONS.md")],
 "viz":[("TensorBoard: scripts/tensorboard.ps1","docs/TRAINING.md")],
 "statistics":[("Метрики обучения в results/","docs/TRAINING.md")],
}

# ------------------------------------------------------------------ сборка
sections = []   # плоский список
for p in PARTS:
    mm = {anchor:(label,diff) for label,anchor,diff in MINDMAP[p["id"]]}
    for idx,(num,title,slug,subs,tags) in enumerate(p["sections"]):
        node = mm.get(title)
        sections.append(dict(
            part=p, num=num, title=title, slug=slug, subs=subs, tags=tags,
            file=f"{num}-{slug}.md",
            path=f"{p['dir']}/{num}-{slug}.md",
            mindmap=node[0] if node else None,
            difficulty=node[1] if node else None,
            url=f"{SITE}{p['base']}#{hub_anchor(title)}",
            canon=CANON.get(p["id"], {}).get(title),
        ))

by_path = {s["path"]:s for s in sections}
def sec_of(part_id, title):
    for s in sections:
        if s["part"]["id"]==part_id and s["title"]==title: return s
    return None

# обратный индекс: раздел -> уроки (сайт)
site_by_sec = {}
for lid, pid, title, ctx in SITE_LINKS:
    if title is None:
        for s in sections:
            if s["part"]["id"]==pid:
                site_by_sec.setdefault(s["path"],[]).append((lid,ctx)); break
    else:
        s = sec_of(pid,title)
        if s: site_by_sec.setdefault(s["path"],[]).append((lid,ctx))

def rel(frm, to):
    """относительная ссылка между файлами каркаса"""
    a = os.path.dirname(frm); b = to
    r = os.path.relpath(b, a if a else ".").replace("\\","/")
    return r

def related(s, limit=6):
    """См. также — разделы других частей с общими тегами"""
    scored=[]
    for t in sections:
        if t["path"]==s["path"] or t["part"]["id"]==s["part"]["id"]: continue
        common = set(s["tags"]) & set(t["tags"])
        if common: scored.append((len(common), sorted(common), t))
    scored.sort(key=lambda x:(-x[0], x[2]["part"]["num"], x[2]["num"]))
    return scored[:limit]

def lessons_for(s):
    site = site_by_sec.get(s["path"], [])
    site_ids = {l for l,_ in site}
    prop=[]
    for t in s["tags"]:
        for l in TAG_LESSONS.get(t,[]):
            if l not in site_ids and l not in prop: prop.append(l)
    order = [i for i,_,_,_ in LESSONS]
    prop.sort(key=lambda l: order.index(l) if l in order else 99)
    return site, prop[:5]

def repo_for(s):
    out=[]
    for t in s["tags"]:
        for item in REPO.get(t,[]):
            if item not in out: out.append(item)
    return out[:4]

def plural(n, one, few, many):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11: return f"{n} {one}"
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14: return f"{n} {few}"
    return f"{n} {many}"

def yaml_list(xs):
    return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in xs) + "]"

os.makedirs(ROOT, exist_ok=True)
written=[]
def W(path, text):
    full = os.path.join(ROOT, path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    written.append(path)

# ---------------------------------------------------------- файлы разделов
for i,s in enumerate(sections):
    p=s["part"]
    same = [x for x in sections if x["part"]["id"]==p["id"]]
    k = same.index(s)
    prev = same[k-1] if k>0 else None
    nxt  = same[k+1] if k<len(same)-1 else None
    site, prop = lessons_for(s)

    part_label = p["roman"] + " · " + p["short"]
    fm = ["---",
          f'id: {p["id"]}-{s["num"]}',
          f'title: {json.dumps(s["title"], ensure_ascii=False)}',
          f'part: {json.dumps(part_label, ensure_ascii=False)}',
          f'part_id: {p["id"]}',
          f'order: {int(s["num"])}',
          f'mindmap_node: {json.dumps(s["mindmap"], ensure_ascii=False) if s["mindmap"] else "null"}',
          f'difficulty: {s["difficulty"] or "null"}',
          f'tags: {yaml_list(s["tags"])}',
          f'hub_url: {json.dumps(s["url"], ensure_ascii=False)}',
          f'hub_anchor_canonical: {json.dumps(s["canon"], ensure_ascii=False) if s["canon"] else "null"}',
          "status: empty",
          "---",""]

    b=[]
    b.append(f'# {s["title"]}')
    b.append("")
    b.append(f'> **Заготовка.** Содержание не написано — файл держит место в структуре и перекрёстные ссылки.')
    b.append("")
    if s["mindmap"]:
        b.append(f'Узел mind map: **{s["mindmap"]}** · уровень: `{s["difficulty"]}`')
    else:
        b.append(f'Раздел модуля хаба (в mind map отдельным узлом не вынесен).')
    b.append("")
    b.append("## Параграфы")
    b.append("")
    if s["subs"]:
        for sub in s["subs"]:
            b.append(f'- [ ] {sub}')
    else:
        b.append("- [ ] _(подпараграфы не выделены — наполнить по месту)_")
    b.append("")
    b.append("## Навигация")
    b.append("")
    b.append(f'- Часть: [{p["roman"]} · {p["title"]}]({rel(s["path"], p["dir"]+"/index.md")})')
    if prev: b.append(f'- ← Предыдущий: [{prev["title"]}]({rel(s["path"], prev["path"])})')
    if nxt:  b.append(f'- → Следующий: [{nxt["title"]}]({rel(s["path"], nxt["path"])})')
    b.append(f'- Оглавление: [SUMMARY]({rel(s["path"], "SUMMARY.md")}) · [Карта]({rel(s["path"], "_meta/mindmap.md")})')
    b.append("")
    b.append("## См. также (другие части пособия)")
    b.append("")
    r = related(s)
    if r:
        for n, common, t in r:
            b.append(f'- [{t["part"]["roman"]} · {t["title"]}]({rel(s["path"], t["path"])}) — общие темы: {", ".join("`"+c+"`" for c in common)}')
    else:
        b.append("- _(пересечений по темам нет)_")
    b.append("")
    b.append("## Уроки курса")
    b.append("")
    if site:
        for lid, ctx in site:
            b.append(f'- **[{LESSON_TITLE.get(lid,lid)}]({SITE}/courses/{lid})** — {ctx} ⟵ *связь уже есть на сайте*')
    if prop:
        for lid in prop:
            b.append(f'- [{LESSON_TITLE.get(lid,lid)}]({SITE}/courses/{lid}) — *предлагаемая связь*')
    if not site and not prop:
        b.append("- _(прямых связей с уроками не выявлено)_")
    b.append("")
    b.append("## Практика в этом репозитории")
    b.append("")
    rp = repo_for(s)
    if rp:
        for label, path in rp:
            b.append(f'- {label} — `{path}`')
    else:
        b.append("- _(прямой привязки к средам нет)_")
    b.append("")
    b.append("## Источник на сайте")
    b.append("")
    b.append(f'- [{p["roman"]} · {p["title"]} → {s["title"]}]({s["url"]})')
    if s["canon"]:
        b.append(f'- Канонический якорь раздела (его использует реестр ссылок сайта): '
                 f'[`#{s["canon"]}`]({SITE}{p["base"]}#{s["canon"]})')
    b.append("")

    W(s["path"], "\n".join(fm+b))

# ------------------------------------------------------------ index частей
for pi,p in enumerate(PARTS):
    same=[x for x in sections if x["part"]["id"]==p["id"]]
    nodes = MINDMAP[p["id"]]
    part_title = "Часть " + p["roman"] + ". " + p["title"]
    fm=["---", f'id: {p["id"]}', f'title: {json.dumps(part_title, ensure_ascii=False)}',
        f'part_id: {p["id"]}', f'order: {pi+1}',
        f'hub_url: {json.dumps(SITE+p["base"], ensure_ascii=False)}',
        f'sections: {len(same)}', f'mindmap_nodes: {len(nodes)}', "status: empty", "---",""]
    b=[f'# Часть {p["roman"]}. {p["title"]}','',
       f'> **Заготовка.** {p["caption"]}.','',
       f'Ветвь mind map: **{p["roman"]} · {p["short"]}** — '
       f'{plural(len(nodes),"узел","узла","узлов")}, '
       f'{plural(len(same),"раздел","раздела","разделов")} пособия.','',
       '## Разделы','']
    for s in same:
        mark = f' · mind map: **{s["mindmap"]}** (`{s["difficulty"]}`)' if s["mindmap"] else ''
        b.append(f'- [{s["title"]}]({s["file"]}){mark}')
    b += ['','## Узлы mind map этой ветви','']
    for label, anchor, diff in nodes:
        t = sec_of(p["id"], anchor)
        b.append(f'- **{label}** (`{diff}`) → [{anchor}]({t["file"]})')
    b += ['','## Навигация','']
    if pi>0:
        q=PARTS[pi-1]; b.append(f'- ← Предыдущая часть: [Часть {q["roman"]}. {q["title"]}](../{q["dir"]}/index.md)')
    if pi<len(PARTS)-1:
        q=PARTS[pi+1]; b.append(f'- → Следующая часть: [Часть {q["roman"]}. {q["title"]}](../{q["dir"]}/index.md)')
    b += [f'- Оглавление: [SUMMARY](../SUMMARY.md) · [Карта](../_meta/mindmap.md)','',
          '## Источник на сайте','', f'- [{p["title"]}]({SITE}{p["base"]})','']
    W(f'{p["dir"]}/index.md', "\n".join(fm+b))

# ------------------------------------------------------------------- SUMMARY
NS, NN, NU = len(sections), sum(len(v) for v in MINDMAP.values()), sum(len(s["subs"]) for s in sections)
b=['# Оглавление','',
   f'Всего: **{plural(len(PARTS),"часть","части","частей")}**, '
   f'**{plural(NS,"раздел","раздела","разделов")}**, '
   f'**{plural(NN,"узел","узла","узлов")} mind map**, '
   f'**{plural(NU,"подпараграф","подпараграфа","подпараграфов")}**.','',
   '- [О пособии](README.md)','']
for p in PARTS:
    b.append(f'- [Часть {p["roman"]}. {p["title"]}]({p["dir"]}/index.md)')
    for s in [x for x in sections if x["part"]["id"]==p["id"]]:
        star = ' ★' if s["mindmap"] else ''
        b.append(f'  - [{s["title"]}]({s["path"]}){star}')
        for sub in s["subs"]:
            b.append(f'    - {sub}')
b += ['','- Служебное','  - [Карта mind map](_meta/mindmap.md)','  - [Реестр перекрёстных ссылок](_meta/crosslinks.md)',
      '  - [24 раздела курса](_meta/lessons.md)','  - [Мост в Unity-репозиторий](_meta/unity-bridge.md)',
      '  - [Соглашения по наполнению](_meta/conventions.md)','',
      '★ — раздел вынесен отдельным узлом в mind map сайта.','']
W("SUMMARY.md", "\n".join(b))

# -------------------------------------------------------------------- README
b=['# Интерактивное пособие по математике ML и RL','',
   'Каркас учебного пособия: структура повторяет [mind map хаба «Математика RL»]'
   f'({SITE}/math-rl/mindmap) — каждая ветвь стала частью, каждый узел получил отдельный файл.',
   'Файлы пустые по содержанию: в них только метаданные, список подпараграфов и перекрёстные ссылки.','',
   '## Части','',
   '| # | Часть | Разделов | Узлов mind map | Модуль хаба |','|---|---|---|---|---|']
for p in PARTS:
    n=len([x for x in sections if x["part"]["id"]==p["id"]])
    b.append(f'| {p["roman"]} | [{p["title"]}]({p["dir"]}/index.md) | {n} | {len(MINDMAP[p["id"]])} | [{p["base"]}]({SITE}{p["base"]}) |')
b += ['',f'**Итого:** {plural(NS,"раздел","раздела","разделов")}, '
      f'{plural(NN,"узел","узла","узлов")} mind map, '
      f'{plural(NU,"подпараграф","подпараграфа","подпараграфов")}.','',
      '## Как устроен файл раздела','',
      '```','---','id, title, part, part_id, order      # положение в структуре',
      'mindmap_node, difficulty             # соответствие узлу mind map (null — если узла нет)',
      'tags                                 # темы; по ним построен блок «См. также»',
      'hub_url                              # якорь на живой раздел сайта','status: empty','---','',
      '# Заголовок','## Параграфы            — чек-лист того, что предстоит написать',
      '## Навигация            — часть, предыдущий/следующий раздел',
      '## См. также            — разделы других частей с общими темами',
      '## Уроки курса          — из 24 разделов курса',
      '## Практика в этом репозитории — среды и конфиги Unity ML-Agents',
      '## Источник на сайте    — ссылка на живой раздел','```','',
      '## Связи','',
      f'- **Вертикальные** — часть ⇄ раздел ⇄ подпараграф (иерархия mind map).',
      '- **Горизонтальные** — «См. также» между частями по общим темам (`bellman`, `gradient`, `mdp`, …).',
      f'- **Наружу, в курс** — {len(SITE_LINKS)} связей взяты из реестра сайта (помечены *связь уже есть на сайте*), '
      'остальные помечены как *предлагаемая связь*.',
      '- **Наружу, в код** — привязка к средам `Assets/ML-ENVIRONMENTS` и trainer-конфигам.','',
      '## Дальше','',
      '1. Наполнять разделы по одному, снимая галочки в блоке «Параграфы».',
      '2. Менять `status: empty` → `draft` → `ready`.',
      '3. Подтверждённые связи «раздел ⇄ урок» переносить в реестр сайта (`crosslinks`).','',
      '## Навигация','',
      '- [Полное оглавление](SUMMARY.md)','- [Карта mind map](_meta/mindmap.md)',
      '- [Реестр перекрёстных ссылок](_meta/crosslinks.md)','- [24 раздела курса](_meta/lessons.md)',
      '- [Мост в Unity-репозиторий](_meta/unity-bridge.md)','- [Соглашения по наполнению](_meta/conventions.md)','',
      '---','',
      'Каркас собран скриптом [`_meta/generate.py`](_meta/generate.py) из структуры mind map,',
      'модулей хаба и реестра перекрёстных ссылок сайта. Повторный запуск перезаписывает',
      'служебные файлы и заготовки — запускать только пока разделы не наполнены текстом.','']
W("README.md", "\n".join(b))

# ------------------------------------------------------------ _meta/mindmap
b=['# Карта mind map → файлы пособия','',
   f'Источник: [{SITE}/math-rl/mindmap]({SITE}/math-rl/mindmap) — 7 ветвей, '
   f'{sum(len(v) for v in MINDMAP.values())} узлов.','',
   'Каждый узел mind map получил отдельный файл. Разделы модулей, которые в mind map',
   'не вынесены отдельным узлом, тоже присутствуют — они помечены «—» в колонке «Узел».','',
   '| Ветвь | Узел mind map | Уровень | Файл пособия |','|---|---|---|---|']
for p in PARTS:
    for s in [x for x in sections if x["part"]["id"]==p["id"]]:
        node = f'**{s["mindmap"]}**' if s["mindmap"] else '—'
        diff = f'`{s["difficulty"]}`' if s["difficulty"] else ''
        b.append(f'| {p["roman"]} · {p["short"]} | {node} | {diff} | [{s["title"]}](../{s["path"]}) |')
b += ['','## Ветви','','| # | Ветвь | Узлов | Разделов | Файл |','|---|---|---|---|---|']
for p in PARTS:
    n=len([x for x in sections if x["part"]["id"]==p["id"]])
    b.append(f'| {p["roman"]} | {p["short"]} | {len(MINDMAP[p["id"]])} | {n} | [index](../{p["dir"]}/index.md) |')
b.append('')
W("_meta/mindmap.md", "\n".join(b))

# --------------------------------------------------------- _meta/crosslinks
b=['# Реестр перекрёстных ссылок','',
   '## 1. Связи «урок → раздел математики», уже существующие на сайте','',
   f'Взято из реестра crosslinks сайта — {len(SITE_LINKS)} связей, ведущих в `/math-rl/*`.','',
   '| Урок | Раздел пособия | Контекст |','|---|---|---|']
for lid,pid,title,ctx in SITE_LINKS:
    s = sec_of(pid,title) if title else next(x for x in sections if x["part"]["id"]==pid)
    b.append(f'| [{LESSON_TITLE.get(lid,lid)}]({SITE}/courses/{lid}) | [{s["title"]}](../{s["path"]}) | {ctx} |')
b += ['','## 2. Горизонтальные связи между частями','',
      'Строятся по общим тегам. Ниже — темы, которые проходят более чем через одну часть.','',
      '| Тема | Разделы |','|---|---|']
tag_index={}
for s in sections:
    for t in s["tags"]: tag_index.setdefault(t,[]).append(s)
for t in sorted(tag_index):
    ss=tag_index[t]
    if len({x["part"]["id"] for x in ss})<2: continue
    b.append(f'| `{t}` | ' + " · ".join(f'[{x["part"]["roman"]}·{x["num"]}](../{x["path"]})' for x in ss) + ' |')
b += ['','## 3. Раздел → уроки (сводка)','','| Раздел пособия | Уроки |','|---|---|']
for s in sections:
    site, prop = lessons_for(s)
    cells=[f'**[{l}]({SITE}/courses/{l})**' for l,_ in site]+[f'[{l}]({SITE}/courses/{l})' for l in prop]
    b.append(f'| [{s["part"]["roman"]} · {s["title"]}](../{s["path"]}) | ' + (", ".join(cells) if cells else "—") + ' |')
b += ['','**Жирным** — связь уже есть в реестре сайта; обычным — предлагаемая.','']
W("_meta/crosslinks.md", "\n".join(b))

# ------------------------------------------------------------ _meta/lessons
b=['# 24 учебных раздела курса и математика под ними','',
   f'Источник: [{SITE}/courses]({SITE}/courses) — 3 уровня, 21 урок и 3 проекта.','']
inv={}
for s in sections:
    site, prop = lessons_for(s)
    for l,_ in site: inv.setdefault(l,{"site":[],"prop":[]})["site"].append(s)
    for l in prop:   inv.setdefault(l,{"site":[],"prop":[]})["prop"].append(s)
lvl=None
for lid,title,level,kind in LESSONS:
    if level!=lvl:
        lvl=level
        b += ['', f'## Уровень {level}', '']
    b.append(f'### [{title}]({SITE}/courses/{lid})')
    b.append("")
    d=inv.get(lid,{"site":[],"prop":[]})
    if d["site"]:
        b.append("Связи с сайта:")
        for s in d["site"]: b.append(f'- **[{s["part"]["roman"]} · {s["title"]}](../{s["path"]})**')
    if d["prop"]:
        b.append("Предлагаемые связи:")
        for s in d["prop"][:8]: b.append(f'- [{s["part"]["roman"]} · {s["title"]}](../{s["path"]})')
    if not d["site"] and not d["prop"]:
        b.append("- _(математический раздел не привязан — кандидат на новую связь)_")
    b.append("")
W("_meta/lessons.md", "\n".join(b))

# ------------------------------------------------------- _meta/unity-bridge
b=['# Мост: математика → среды этого репозитория','',
   'Где абстракция становится кодом. Пути — от корня репозитория.','',
   '| Тема | Что смотреть | Путь |','|---|---|---|']
seen=set()
for t in sorted(REPO):
    for label,path in REPO[t]:
        if (t,path) in seen: continue
        seen.add((t,path))
        b.append(f'| `{t}` | {label} | `{path}` |')
b += ['','## Среды','',
      '### GridWorld 5×5 — `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/`','',
      'Дискретный MDP по ТЗ TS-001: 25 состояний (`state = r·5 + c`), 4 действия (N/S/E/W),',
      'награды −0.04 / +1.0 / −1.0, `gamma: 0.95`, необязательное скольжение `slipProbability`.',
      'Опорная среда для частей IV, VI (MDP, Беллман, TD, Q-learning).','',
      '### Hit_the_ball / RollerAgent — `Assets/ML-ENVIRONMENTS/01-Basics/Hit_the_ball/`','',
      'Непрерывное управление: 8 наблюдений, 2 непрерывных действия, PPO',
      '(`epsilon: 0.2`, `lambd: 0.99`, `gamma: 0.99`, `learning_rate: 3.0e-4`).',
      'Опорная среда для частей II, V (градиент политики, PPO, оптимизация).','',
      '### Справочные конфиги — `config/ml-agents-reference/`','',
      'PPO / SAC / POCA / imitation — материал для разбора гиперпараметров',
      'в части V (Лекция 4) и части VI (Глава 10).','']
W("_meta/unity-bridge.md", "\n".join(b))

# -------------------------------------------------------- _meta/conventions
b=['# Соглашения по наполнению','',
   '## Статус файла','',
   '`status` во frontmatter: `empty` → `draft` → `ready`.','',
   '## Формулы','',
   'KaTeX, как на сайте: `$...$` внутри строки, `$$...$$` блоком.',
   'Обозначения держим едиными по всему пособию:','',
   '| Символ | Значение |','|---|---|',
   '| $s, s\'$ | состояние, следующее состояние |',
   '| $a$ | действие |',
   '| $r$ | награда за шаг |',
   '| $\\gamma$ | коэффициент дисконтирования |',
   '| $\\pi(a\\mid s)$ | политика |',
   '| $V^{\\pi}(s),\\; Q^{\\pi}(s,a)$ | функции ценности |',
   '| $G_t$ | возврат (return) |',
   '| $\\theta$ | параметры политики |',
   '| $\\alpha$ | скорость обучения |','',
   '## Перекрёстные ссылки','',
   '- Внутри пособия — относительные пути (`../part-6-fundamental-rl/05-bellman-equations.md`).',
   '- На сайт — абсолютные, с якорем раздела (`hub_url` во frontmatter уже посчитан).',
   '  Якорь получается из заголовка тем же slugify, что и на сайте:',
   '  `lower → [^\\w а-яё]+ → "-" → trim("-") → срез 60`.',
   '  Часть VI дополнительно задаёт короткие id (`#глава-5`) — они в `hub_anchor_canonical`',
   '  и именно их использует реестр ссылок сайта; оба якоря рабочие.',
   '- На код — путь от корня репозитория в обратных кавычках, без ссылки.','',
   '## Что должно быть в готовом разделе','',
   '- [ ] интуиция до формул;','- [ ] формальное определение;',
   '- [ ] пример на числах из среды репозитория;','- [ ] фрагмент кода (Python или C#);',
   '- [ ] интерактивная демонстрация или её ТЗ;','- [ ] 2–4 задачи с ответами;',
   '- [ ] проверенные перекрёстные ссылки.','']
W("_meta/conventions.md", "\n".join(b))

print(f"файлов: {len(written)}")
print(f"разделов: {len(sections)}, узлов mind map: {sum(len(v) for v in MINDMAP.values())}, "
      f"подпараграфов: {sum(len(s['subs']) for s in sections)}")
