---
title: "<% tp.file.title %>"
enf_mode: learning
discipline: <% await tp.system.suggester(["calculus","linalg","probability","statistics","ml","rl","optimization"], ["calculus","linalg","probability","statistics","ml","rl","optimization"]) %>
tags: []
duration: <% await tp.system.prompt("Длительность в минутах", "90") %>
date: <% tp.date.now("YYYY-MM-DD") %>
---

# <% tp.file.title %>

## Зачем это нужно

## Обозначения

| Символ | Значение | Роль |
|--------|----------|------|
| $\enfVar{x}$ | | `variable` |
| $\enfFun{f}$ | | `function` |

## Раздел 1

### Постановка

### Вывод

$$
\begin{aligned}
  a &= b \\
    &= c
\end{aligned}
$$

### Пример

## Что стоит запомнить

1.
2.
3.

## Проверка себя

1.
2.
3.

## Что дальше

- [[ ]]
