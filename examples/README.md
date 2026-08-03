# Examples — эталонные документы

Полностью оформленные материалы, на которые следует равняться. Каждый пример существует в двух вариантах — `.learning.md` и `.publication.md`: один и тот же материал, различающийся только плотностью раскраски и подробностью пояснений.

| Материал | Дисциплина | Файлы |
|----------|------------|-------|
| Предел функции | Математический анализ | `Limit.learning.md`, `Limit.publication.md` |
| Производная | Математический анализ | `Derivative.learning.md`, `Derivative.publication.md` |
| Определённый интеграл | Математический анализ | `Integral.learning.md`, `Integral.publication.md` |
| Линейная регрессия | Статистика, ML | `Linear_Regression.learning.md`, `Linear_Regression.publication.md` |
| Уравнение Беллмана | Reinforcement Learning | `Bellman_Equation.learning.md`, `Bellman_Equation.publication.md` |
| Q-Learning | Reinforcement Learning | `Q_Learning.learning.md`, `Q_Learning.publication.md` |
| Обратное распространение | Нейронные сети | `Backpropagation.learning.md`, `Backpropagation.publication.md` |

## Требования к примерам

Пример принимается в каталог только если он одновременно:

1. проходит все машинные проверки — `pwsh Scripts/check.ps1 examples/`;
2. собирается пайплайном во все пять форматов — `pwsh Scripts/build.ps1 -Source <файл> -All`;
3. проходит ревью по [`../docs/10_Review_Checklist.md`](../docs/10_Review_Checklist.md).

Примеры — это тесты фреймворка. Если правило Style Guide изменилось, а примеры продолжают собираться без правок, стоит проверить, действительно ли правило что-то нормирует.

## Сравнение режимов

Самый быстрый способ понять разницу между режимами — открыть рядом `Bellman_Equation.learning.md` и `Bellman_Equation.publication.md`. Один и тот же вывод: в первом почти каждая роль подсвечена и каждый шаг разобран, во втором выделены только состояние, действие и награда, а выкладки уплотнены. Оба варианта корректны — они решают разные задачи.
