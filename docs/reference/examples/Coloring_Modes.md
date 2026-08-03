---
title: "Learning Mode и Publication Mode на одной формуле"
enf_mode: publication
discipline: meta
tags: [пример, раскраска]
date: 2026-07-31
---

# Learning Mode и Publication Mode на одной формуле

Мини-пример к правилам `ENF-MATH-020` и `ENF-MATH-021`. Одна и та же формула — уравнение Беллмана — в трёх вариантах раскраски.

## Так нельзя ни в одном режиме

Раскрашено всё, включая индексы, скобки, знаки суммирования и условной черты:

```latex
\enfOp{V^\pi}(\enfVar{s}) = \enfOp{\sum_{\enfFun{a}}} \enfPar{\pi}(\enfFun{a} \enfNeu{\mid} \enfVar{s})
  \enfOp{\sum_{\enfVar{s'}}} \enfFun{P}(\enfVar{s'} \enfNeu{\mid} \enfVar{s}, \enfFun{a})
  \enfNeu{\bigl[}\enfTgt{r} \enfNeu{+} \enfPar{\gamma}\enfOp{V^\pi}(\enfVar{s'})\enfNeu{\bigr]}
```

Формула перестала читаться как формула и превратилась в мозаику. Запрещено правилом `ENF-MATH-020` — оно действует в обоих режимах.

## Learning Mode: четыре тона

```latex
\enfOp{V^\pi}(\enfVar{s}) = \sum_{a} \enfPar{\pi}(a \mid \enfVar{s})
  \sum_{\enfVar{s'}} P(\enfVar{s'} \mid \enfVar{s}, a)
  \bigl[\enfTgt{r} + \enfPar{\gamma}\,\enfOp{V^\pi}(\enfVar{s'})\bigr]
```

Выделены: состояние (`variable`), политика и коэффициент дисконтирования (`parameter`), награда (`target`), функция ценности (`operator`). Действие и вероятность перехода оставлены нейтральными — четыре тона, лимит соблюдён.

Выбор, что именно оставить нейтральным, делается по содержанию: в этом фрагменте разбирается структура усреднения, а не механика выбора действия.

## Publication Mode: три тона из безопасной тройки

```latex
V^\pi(\enfVar{s}) = \sum_{\enfFun{a}} \enfPar{\pi}(\enfFun{a} \mid \enfVar{s})
  \sum_{s'} P(s' \mid \enfVar{s}, \enfFun{a})\bigl[r + \gamma V^\pi(s')\bigr]
```

Выделены только `variable`, `function` и `parameter` — тона, различимые при дихроматии с уверенным запасом (`ENF-COLOR-012`). Награда, дисконтирование и функция ценности набраны нейтрально: в книге они уже введены ранее и не нуждаются в подсветке.

## Сводка

| | Learning | Publication |
|---|---|---|
| Тонов в формуле | до 4 | до 3 |
| Разрешённые тона | все пять ролей | `variable`, `function`, `parameter` |
| Доля окрашенного | до ≈ 40 % | до ≈ 15 % |
| Что окрашивается | все встречающиеся роли | только разбираемые рядом |

Проверяется командой `node Scripts/check-colors.mjs`: скрипт считает число различных макросов в каждой формуле и сверяет с режимом документа.
