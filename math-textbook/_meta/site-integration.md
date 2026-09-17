---
title: "Перенос пособия на сайт: инструкция по интеграции"
enf_mode: publication
discipline: meta
date: 2026-08-09
status: ready
---

# Перенос пособия на сайт rl-cuber-unity-code.com

Инструкция для исполнителя (человека или агента), который переносит `math-textbook/`
из репозитория `Math_for_DS_&_RL` в репозиторий сайта `cyber-unity-learn`.

Читать целиком до начала работ: решения в разделах 2 и 5 определяют всё остальное.

---

## 0. Исходные данные

### 0.1 Что переносим

`math-textbook/` — 51 лекция в 7 частях + 7 `index.md` частей + 6 служебных файлов `_meta/`.
Всё написано по правилам Ermakov Notes Framework:

| Элемент | Как выглядит в `.md` | Сколько |
|---|---|---|
| Формулы | KaTeX-совместимый LaTeX, `$…$` и `$$…$$` | во всех разделах |
| Цветные формулы | макросы `\enfVar \enfFun \enfPar \enfOp \enfTgt \enfNeu` | во всех разделах |
| Коллауты | `> [!definition]`, `> [!theorem]`, `> [!proof]`, `> [!intuition]`, `> [!example]`, `> [!remark]`, `> [!warning]` | 215 блоков |
| Код | ` ```python ` (14), ` ```powershell ` (1), без языка (24) | 39 блоков |
| Диаграммы | ` ```mermaid ` | 9 блоков |
| Растровые изображения | — | 0 |
| Таблицы | GFM | много |
| Внутренние ссылки | относительные, `../part-6-fundamental-rl/05-bellman-equations.md` | много |
| Ссылки на сайт | абсолютные, `https://rl-cuber-unity-code.com/...` | много |

Frontmatter лекции (пример — `part-6-fundamental-rl/05-bellman-equations.md`):

```yaml
id: part-5-05
title: "Глава 5. Сердце RL: Уравнения Беллмана"
part: "VI · Фундаментальная RL"
part_id: part-5                  # ВНИМАНИЕ: это id ЧАСТИ НА САЙТЕ, не номер каталога
order: 5
mindmap_node: "Уравнения Беллмана"
difficulty: intermediate         # beginner | intermediate | advanced
tags: ["bellman", "value-function", "dp"]
hub_url: "https://rl-cuber-unity-code.com/math-rl/module-5#глава-5-…"
hub_anchor_canonical: "глава-5"
enf_mode: learning
discipline: rl
duration: 90                     # минут
date: 2026-08-09
status: ready
```

Служебные реестры (использовать как источник данных, не переписывать вручную):

| Файл | Что содержит |
|---|---|
| `_meta/mindmap.md` | соответствие «узел mind map → файл пособия», все 39 узлов + разделы без узлов |
| `_meta/crosslinks.md` | §1 — 15 связей «урок → раздел», уже существующих в реестре сайта; §2 — горизонтальные связи по тегам; §3 — полная таблица «раздел → уроки» (51 строка) |
| `_meta/lessons.md` | 24 урока курса и математика под каждым |
| `_meta/unity-bridge.md` | соответствие «тема → файл в репозитории `unity-ml-agents-lab`» |
| `_meta/conventions.md` | соглашения по формулам, ссылкам, обозначениям |
| `SUMMARY.md`, `README.md` | оглавление и точка входа пособия |

### 0.2 Куда переносим

Репозиторий `cyber-unity-learn`: Vite 5 + React 18 + TypeScript + React Router 6 + Tailwind +
shadcn/ui + Supabase. SPA, деплой на Vercel, тема одна — тёмная («киберпанк»).

Ключевые точки, которых касается интеграция:

| Что | Файл | Роль |
|---|---|---|
| Рендер формул | `src/components/Math.tsx` | KaTeX, `throwOnError: false`, `strict: false`, **без макросов и без `trust`** |
| Хаб математики | `src/pages/MathRL.tsx` | одна страница, 7 частей-аккордеонов, боковое оглавление, `slugify` (строка 223) |
| Контент хаба | `src/components/math-rl/parts/*.tsx`, `src/components/math-rl/module1/*.tsx` | краткая версия того же материала, захардкожена в TSX |
| Секции хаба | `src/components/math-rl/module1/Section.tsx` | `id = short id` + алиас `id = slugify(title)` |
| Маршруты | `src/App.tsx` | `/math-rl`, `/math-rl/mindmap`, `/math-rl/calculus`, `/math-rl/module-1…6` |
| Mind map №1 | `src/pages/MathMindMap.tsx` + `src/content/mathMindMap.ts` | 7 ветвей, 39 узлов, deep-link `base#slugify(anchor)` |
| Mind map №2 | `src/pages/KnowledgeMap.tsx` + `src/content/knowledgeMap.ts` | карта всего сайта: ветви → уроки |
| Отрисовка карт | `src/components/knowledge-map/MindMapCanvas.tsx` | общий канвас для обеих карт |
| Реестр связей | `src/config/crosslinks.ts` | 15 связей «урок ↔ хаб математики», типизировано |
| Урок → хаб | `src/components/math-rl/HubLink.tsx` | навигация с `?from=&fromAnchor=&fromLabel=` |
| Хаб → урок | `src/components/math-rl/ReturnToLessonChip.tsx` | sticky-чип «← Вернуться к уроку» |
| Аудит ссылок | `scripts/link-audit.mjs` | проверяет, что каждый якорь существует |
| Токены темы | `src/index.css` | `--background: 230 25% 8%`, `--primary: 180 100% 50%` и т. д. |

Важный факт: `hub_url` и `hub_anchor_canonical` во frontmatter пособия **уже посчитаны под эти маршруты
и под эту `slugify`**. Ничего пересчитывать не нужно — нужно не сломать.

---

## 1. Что должно получиться (критерии приёмки)

- [ ] 51 лекция и 7 обзоров частей доступны на сайте как самостоятельные страницы.
- [ ] Формулы отрисованы KaTeX **с сохранением ролевой раскраски** (пять тонов ENF); цвет приходит
      из CSS-переменных, а не хардкодится в LaTeX.
- [ ] Все относительные ссылки между лекциями работают как внутренняя SPA-навигация.
- [ ] Все ссылки «лекция → урок сайта» и «урок сайта → лекция» двусторонние: с лекции виден
      возврат в урок (`ReturnToLessonChip`), из урока — переход в лекцию (`HubLink`).
- [ ] Каждый раздел хаба `/math-rl` имеет ссылку «Полная лекция →» на соответствующую лекцию.
- [ ] Обе mind map ведут в лекции; у узлов сохранена вторая ссылка — на обзорный раздел хаба.
- [ ] Ни один существующий якорь и ни одна из 15 связей в `crosslinks.ts` не сломаны.
- [ ] `node scripts/link-audit.mjs` и новый `node scripts/textbook-audit.mjs` — без ошибок.
- [ ] `npm run build` проходит; вес страницы лекции — не более чем +150 KB gzip к текущему хабу.
- [ ] Единственный источник истины по содержанию — `.md`-файлы; TSX-контент не дублирует лекции.

---

## 2. Принятые решения

**Модель интеграции — «новый слой глубины».** Хаб `/math-rl` остаётся кратким обзором в текущем виде
(аккордеоны, TSX). Лекции пособия — новый уровень детализации на собственных маршрутах.
Существующие якоря, deep-link'и карт и 15 связей `crosslinks.ts` продолжают работать без правок.

```text
/math-rl                                    обзор (как сейчас)
  └ § «Глава 5. Уравнения Беллмана»          ← якорь #глава-5 остаётся
      └ [Полная лекция →]  /math-rl/textbook/part-6/05-bellman-equations

/math-rl/textbook                           оглавление пособия (7 частей, 51 раздел)
/math-rl/textbook/part-6                    обзор части VI (из index.md)
/math-rl/textbook/part-6/05-bellman-equations   лекция
```

**Mind map — узел ведёт в лекцию, вторая ссылка ведёт в обзор.** Основной клик по узлу открывает
полную лекцию; в карточке/тултипе узла остаётся ссылка «в обзоре» на прежний `base#anchor`.

**Сегмент URL части = номер каталога пособия** (`part-1` … `part-7`, то есть римские I…VII).
Не путать с `part_id` во frontmatter: там id части **на сайте** (`part-1`, `part-1b`, `part-2`, …).
Единственная таблица соответствия — раздел 3.2, все остальные места берут значения из неё.

---

## 3. Шаг 1. Перенос файлов

### 3.1 Что и куда копировать

```text
math-textbook/**/*.md            →  cyber-unity-learn/src/content/math-textbook/**/*.md
math-textbook/_meta/*.md         →  туда же (реестры нужны как данные и как документация)
Math_for_DS_&_RL/css/enf-tokens.css → основа для src/styles/enf-math.css (см. раздел 5.4)
```

Ничего не переименовывать: имена файлов уже нормализованы (`kebab-case`, английские).
`_meta/generate.py` не переносить — генератор каркаса остаётся в исходном репозитории.

Пособие остаётся в исходном репозитории тоже: сайт получает **копию**, а правки делаются в
`Math_for_DS_&_RL` и синхронизируются (раздел 11).

### 3.2 Каноническая таблица частей

Создать `src/content/textbook/parts.ts` — единственный источник соответствий:

```ts
export interface TextbookPart {
  /** Сегмент URL: /math-rl/textbook/<segment> */
  segment: string;
  /** Каталог с .md внутри src/content/math-textbook */
  dir: string;
  /** id части НА САЙТЕ (совпадает с part_id во frontmatter и с parts[] в MathRL.tsx) */
  sitePartId: string;
  /** Обзорный маршрут хаба */
  hubRoute: string;
  roman: string;
  title: string;
  sections: number;
}

export const TEXTBOOK_PARTS: TextbookPart[] = [
  { segment: "part-1", dir: "part-1-limits-series",       sitePartId: "part-1",  hubRoute: "/math-rl/module-1",  roman: "I",   title: "Пределы, последовательности и ряды",   sections: 12 },
  { segment: "part-2", dir: "part-2-derivatives-gradient", sitePartId: "part-1b", hubRoute: "/math-rl/calculus",  roman: "II",  title: "Производные, градиент и оптимизация",  sections: 5  },
  { segment: "part-3", dir: "part-3-linear-algebra",       sitePartId: "part-2",  hubRoute: "/math-rl/module-2",  roman: "III", title: "Линейная алгебра для RL",              sections: 6  },
  { segment: "part-4", dir: "part-4-probability",          sitePartId: "part-3",  hubRoute: "/math-rl/module-3",  roman: "IV",  title: "От вероятности к алгоритмам RL",       sections: 6  },
  { segment: "part-5", dir: "part-5-policy-optimization",  sitePartId: "part-4",  hubRoute: "/math-rl/module-4",  roman: "V",   title: "Методы оптимизации политик",           sections: 4  },
  { segment: "part-6", dir: "part-6-fundamental-rl",       sitePartId: "part-5",  hubRoute: "/math-rl/module-5",  roman: "VI",  title: "Фундаментальная математика RL",        sections: 13 },
  { segment: "part-7", dir: "part-7-deep-rl",              sitePartId: "part-6",  hubRoute: "/math-rl/module-6",  roman: "VII", title: "Глубокое обучение с подкреплением",    sections: 5  },
];
```

Проверка при сборке индекса: `part_id` из frontmatter обязан совпасть с `sitePartId` каталога,
иначе — ошибка сборки. Это ловит расхождение двух нумераций.

---

## 4. Шаг 2. Пайплайн рендера Markdown

### 4.1 Зависимости

```bash
npm i react-markdown@^9 remark-gfm@^4 remark-math@^6 rehype-katex@^7 unist-util-visit@^5
npm i -D gray-matter@^4        # только для build-time скрипта, в бандл не попадает
npm i mermaid@^11              # 9 диаграмм; загружается лениво, см. 4.6
```

`katex@^0.16.28` уже стоит.

### 4.2 Метаданные — на этапе сборки, не в браузере

YAML в браузере не парсим. Скрипт `scripts/build-textbook-index.mjs` читает все `.md`,
достаёт frontmatter через `gray-matter` и пишет `src/content/textbook/index.generated.ts`:

```ts
export interface LectureMeta {
  id: string;            // part-5-05
  partSegment: string;   // part-6
  slug: string;          // 05-bellman-equations
  route: string;         // /math-rl/textbook/part-6/05-bellman-equations
  title: string;
  order: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  duration: number;
  tags: string[];
  mindmapNode: string | null;
  hubRoute: string;      // /math-rl/module-5
  hubAnchor: string;     // глава-5   (hub_anchor_canonical или slugify(title))
  status: "empty" | "draft" | "ready";
}
export const LECTURES: LectureMeta[] = [ /* … 51 запись … */ ];
export const PART_INDEX: Record<string, LectureMeta[]> = { /* … */ };
```

Скрипт обязан падать с ненулевым кодом, если: `part_id` не совпал с таблицей частей;
дублируется `id`; `status !== "ready"`; относительная ссылка ведёт в несуществующий файл.

Подключить в `package.json`:

```json
"scripts": {
  "textbook:index": "node scripts/build-textbook-index.mjs",
  "prebuild": "npm run textbook:index",
  "predev": "npm run textbook:index"
}
```

### 4.3 Тело лекции — ленивый raw-импорт

```ts
// src/content/textbook/loader.ts
const files = import.meta.glob("/src/content/math-textbook/**/*.md", {
  query: "?raw",
  import: "default",
});

/** Отрезает frontmatter — метаданные уже пришли из index.generated.ts. */
const stripFrontmatter = (src: string) => src.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "");

export async function loadLecture(partDir: string, slug: string): Promise<string> {
  const key = `/src/content/math-textbook/${partDir}/${slug}.md`;
  const load = files[key];
  if (!load) throw new Error(`Lecture not found: ${key}`);
  return stripFrontmatter((await load()) as string);
}
```

Каждая лекция становится отдельным чанком — страница грузит только свой файл.

### 4.4 Компонент рендера

`src/components/textbook/MarkdownLecture.tsx`:

```tsx
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { KATEX_OPTIONS } from "@/lib/katex-options";
import { remarkEnfCallouts } from "@/lib/remark-enf-callouts";
import { slugify } from "@/lib/slug";
import Callout from "./Callout";
import LectureLink from "./LectureLink";
import MermaidDiagram from "./MermaidDiagram";
import CyberCodeBlock from "@/components/CyberCodeBlock";

const heading = (Tag: "h2" | "h3" | "h4") =>
  ({ children }: { children?: React.ReactNode }) => {
    const text = String(children);
    return <Tag id={slugify(text)} className="scroll-mt-28 …">{children}</Tag>;
  };

export default function MarkdownLecture({ source }: { source: string }) {
  return (
    <div className="prose-cyber max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath, remarkEnfCallouts]}
        rehypePlugins={[[rehypeKatex, KATEX_OPTIONS]]}
        components={{
          h2: heading("h2"), h3: heading("h3"), h4: heading("h4"),
          a: LectureLink,
          callout: Callout,          // узел из remarkEnfCallouts
          code: ({ className, children }) => {
            const lang = /language-(\w+)/.exec(className ?? "")?.[1];
            if (lang === "mermaid") return <MermaidDiagram chart={String(children)} />;
            if (lang) return <CyberCodeBlock language={lang === "csharp" ? "csharp" : "python"}>{String(children)}</CyberCodeBlock>;
            return <code className="…">{children}</code>;
          },
        }}
      >
        {source}
      </ReactMarkdown>
    </div>
  );
}
```

`slugify` вынести в `src/lib/slug.ts` **одной копией** и переиспользовать в `MathRL.tsx`,
`mathMindMap.ts`, `Section.tsx`, `scripts/link-audit.mjs`:

```ts
export const slugify = (text: string) =>
  text.toLowerCase().replace(/[^\wа-яё]+/gi, "-").replace(/^-|-$/g, "").slice(0, 60);
```

Менять её нельзя ни на символ: от неё зависят все существующие якоря сайта.

### 4.5 Коллауты

`src/lib/remark-enf-callouts.ts` — плагин, превращающий `blockquote`, первая строка которого
`[!type] Заголовок`, в `<div class="enf-callout" data-callout="type">` с первым потомком
`<div class="enf-callout-title">`. Оформление — CSS по `data-callout`, отдельный React-компонент
не нужен.

Заголовок обязан остаться деревом inline-узлов, а не строкой: в нём встречается математика
(«Почему $\gamma < 1$ появляется так часто»), и `remark-math` должен её увидеть. Плагин режет
первый абзац по первому переводу строки, а не по тексту.

Соответствие типов и оформления:

| Тип ENF | Подпись | Акцент |
|---|---|---|
| `definition` | Определение | `primary` (cyan) |
| `theorem` | Теорема | `secondary` (purple) |
| `lemma`, `corollary` | Лемма / Следствие | `secondary` |
| `proof` | Доказательство | нейтральная рамка, моноширинный заголовок, `▢` в конце |
| `intuition` | Интуиция | `accent` (pink) |
| `example` | Пример | `primary`, приглушённый фон |
| `remark` | Замечание | `muted` |
| `warning` | Осторожно | `--destructive` |

Визуально держаться `InfoBox` из `src/components/math-rl/module1/Section.tsx` — новые блоки не должны
выглядеть чужеродно рядом с существующим хабом.

### 4.6 Mermaid

`src/components/textbook/MermaidDiagram.tsx` — динамический `import("mermaid")`,
инициализация `theme: "dark"` с цветами из токенов сайта, рендер в `useEffect`.

Перед рендером обязателен `await document.fonts.ready`: ширину узлов mermaid считает по метрикам
шрифта, и если рисовать до загрузки Inter, ширина берётся по запасному шрифту — подписи в блоках
обрезаются. Симптом характерный: «Уравнения Беллман», «Дисконтировани».
Библиотека не должна попадать в основной бандл: `manualChunks` в `vite.config.ts` — отдельный чанк
`mermaid`. Если вес окажется неприемлемым, запасной путь — прогнать 9 диаграмм через
`Scripts/convert-svg.ps1` исходного репозитория и положить готовые SVG в `public/textbook/`.

---

## 5. Шаг 3. Цветные формулы — главное требование

### 5.1 Как это устроено в пособии

В `.md` роль сущности задаётся макросом, а не цветом:

```latex
\enfOp{V}^{\pi}(\enfVar{s}) = \sum_a \pi(a\mid \enfVar{s})\sum_{\enfVar{s}'}
  P(\enfVar{s}'\mid \enfVar{s},a)\left[\enfTgt{r} + \enfPar{\gamma}\,\enfOp{V}^{\pi}(\enfVar{s}')\right]
```

| Макрос | Роль | CSS-класс |
|---|---|---|
| `\enfVar` | переменная, объект действия | `enf-variable` |
| `\enfFun` | функция, преобразование | `enf-function` |
| `\enfPar` | параметр, то что настраивается | `enf-parameter` |
| `\enfOp` | оператор, агрегат | `enf-operator` |
| `\enfTgt` | целевая величина, награда, потери | `enf-target` |
| `\enfNeu` | служебное, нейтральное | `enf-neutral` |

В Obsidian макросы разворачиваются в `\class{enf-variable}{…}` (расширение `html` MathJax).
**KaTeX команду `\class` не знает** — её аналог `\htmlClass`. Это единственное место, где
пайплайн сайта отличается от исходного, и оно закрывается одной строкой в определении макросов.

### 5.2 Опции KaTeX (единая точка)

Создать `src/lib/katex-options.ts`:

```ts
import type { KatexOptions } from "katex";

/** Роли ENF → CSS-классы. Цвет приходит из src/styles/enf-math.css. */
export const ENF_MACROS = {
  "\\enfVar": "\\htmlClass{enf-variable}{#1}",
  "\\enfFun": "\\htmlClass{enf-function}{#1}",
  "\\enfPar": "\\htmlClass{enf-parameter}{#1}",
  "\\enfOp":  "\\htmlClass{enf-operator}{#1}",
  "\\enfTgt": "\\htmlClass{enf-target}{#1}",
  "\\enfNeu": "\\htmlClass{enf-neutral}{#1}",
} as const;

export const KATEX_OPTIONS: KatexOptions = {
  throwOnError: false,
  strict: false,
  macros: { ...ENF_MACROS },
  // \htmlClass — часть htmlExtension: без trust KaTeX его игнорирует и цвет пропадёт.
  trust: (ctx) => ctx.command === "\\htmlClass",
};
```

Три условия, при нарушении любого из которых раскраска молча исчезает:
`macros` заданы; `trust` разрешает `\htmlClass`; `strict: false`.

### 5.3 Правка существующего компонента

`src/components/Math.tsx` — добавить опции, не меняя сигнатуру:

```diff
+import { KATEX_OPTIONS } from "@/lib/katex-options";
 …
       katex.render(children, ref.current, {
+        ...KATEX_OPTIONS,
         displayMode: display,
-        throwOnError: false,
-        strict: false,
       });
```

Существующие формулы в TSX макросов не используют — они не изменятся. Зато после этой правки
цветные формулы можно писать и в TSX-частях хаба, если понадобится.

### 5.4 Палитра и CSS

Создать `src/styles/enf-math.css`, импортировать в `src/index.css` **после** `katex.min.css`.
Сайт тёмный всегда — берём тёмную половину палитры из `css/enf-tokens.css` пособия:

```css
:root {
  --enf-color-variable:  #9BA3D2;  /* переменная  */
  --enf-color-function:  #E89157;  /* функция     */
  --enf-color-parameter: #A6E768;  /* параметр    */
  --enf-color-operator:  #FFD6FF;  /* оператор    */
  --enf-color-target:    #D6768B;  /* цель        */
  --enf-color-neutral:   #B9C2CC;  /* нейтральное */
}

/* Внутри .katex цвет наследуется вложенными span'ами (KaTeX не задаёт color сам),
   поэтому достаточно покрасить обёртку, созданную \htmlClass.
   ВАЖНО: KaTeX добавляет к обёртке свои классы — в DOM это выглядит как
   class="enclosing enf-variable" или "enclosing enf-variable mtight".
   Селектор [class^="enf-"] по такой обёртке НЕ сработает: перечисляем классы явно. */
.katex .enf-variable  { color: var(--enf-color-variable); }
.katex .enf-function  { color: var(--enf-color-function); }
.katex .enf-parameter { color: var(--enf-color-parameter); }
.katex .enf-operator  { color: var(--enf-color-operator); }
.katex .enf-target    { color: var(--enf-color-target); }
.katex .enf-neutral   { color: var(--enf-color-neutral); }

/* Те же классы вне формул: таблица «Обозначения», легенда ролей. */
.enf-variable { color: var(--enf-color-variable); }
/* … остальные пять — так же … */
```

Правила:

- HEX'ы правятся **только здесь**. Появление `\textcolor{...}` или `\color{...}` в `.md` — ошибка:
  это ломает единый источник истины и не переживает смену темы.
- Значения подобраны под фон `#1B1E22`. Фон сайта — `hsl(230 25% 8%)` ≈ `#0F111A`; контраст
  измерен и составляет от 6.1:1 (`target`) до 14.6:1 (`operator`), на фоне карточки — от 5.6:1.
  Требование ENF — не ниже 4.5:1, запас есть у всех шести тонов.
- Тон закреплён за ролью, а не за символом. Не «сделать γ зелёной», а «параметры — зелёные».

### 5.5 Легенда ролей

На странице лекции — свёрнутый блок «Что означают цвета» с шестью образцами и подписями
(тексты взять из `docs/02_Color_System.md` исходного репозитория). Без легенды раскраска читается
как украшение; с ней — как часть нотации.

Опционально: переключатель «цвет вкл/выкл» — снимает класс с контейнера страницы,
`.enf-mono .katex [class^="enf-"] { color: inherit; }`. Полезно для печати и для читателей
с цветовой слепотой (роли продублированы начертанием — `\mathbf`, `\mathcal`, `\mathrm`, — так что
без цвета текст остаётся однозначным).

### 5.6 Контрольный тест

Первая же собранная страница обязана показать пять разных цветов в формуле

```latex
\enfOp{\mathbb{E}}\left[ \enfTgt{r} + \enfPar{\gamma}\, \enfFun{f}(\enfVar{x}) \right]
```

Роли слева направо: оператор, цель, параметр, функция, переменная. Если всё серое — смотреть 5.2
(скорее всего не передан `trust`). Если видно `\enfVar` текстом — не переданы `macros`.

---

## 6. Шаг 4. Маршруты и страницы

### 6.1 Маршруты

```tsx
// src/App.tsx
const TextbookIndex   = lazy(() => import("./pages/textbook/TextbookIndex"));
const TextbookPart    = lazy(() => import("./pages/textbook/TextbookPart"));
const TextbookLecture = lazy(() => import("./pages/textbook/TextbookLecture"));

<Route path="/math-rl/textbook" element={<TextbookIndex />} />
<Route path="/math-rl/textbook/:part" element={<TextbookPart />} />
<Route path="/math-rl/textbook/:part/:slug" element={<TextbookLecture />} />
```

Неизвестный `:part` или `:slug` — редирект на `/math-rl/textbook`, а не 404-страница сайта.

### 6.2 Страница лекции

Собирается из уже существующих кирпичей сайта:

| Элемент | Откуда |
|---|---|
| Шапка, футер | `Navbar`, `FooterSection` |
| SEO | `SEOHead` — `title` из frontmatter + « — Математика RL», `description` — первый абзац, `path` — маршрут, `type="article"`, `jsonLd` типа `LearningResource` |
| Прогресс чтения | `ScrollProgressBar` |
| Возврат в урок | `ReturnToLessonChip` — **обязательно**, иначе двусторонность связей рвётся |
| Хлебные крошки | Главная → Математика RL → Учебник → Часть N → лекция |
| Оглавление | `LessonSidebarTOC` или свой, по `h2`/`h3` из markdown (те же `slugify`-якоря) |
| Метаданные | `difficulty`, `duration` — бейджами; палитра из `DIFFICULTY_META` (`knowledgeMap.ts`) |
| Prev / next | `NextPrevLesson` по `order` внутри части, с переходом между частями |
| Тело | `MarkdownLecture` |
| «Где это применяется» | список уроков из реестра связей (раздел 8) |
| «Смежные темы» | лекции с общими `tags` — данные из `_meta/crosslinks.md` §2 |

### 6.3 Страницы части и оглавления

`TextbookPart` — рендер `index.md` части через тот же `MarkdownLecture` + карточки её разделов
(`PART_INDEX[segment]`) + ссылка «Обзорная версия в хабе →» на `hubRoute`.

`TextbookIndex` — рендер `math-textbook/README.md` + сетка из 7 частей с числом разделов и
суммарной длительностью. Кнопка «Открыть карту» → `/math-rl/mindmap`.

---

## 7. Шаг 5. Связи внутри пособия

Компонент `LectureLink` (подставляется как `components.a`) разбирает `href`:

| Что во входе | Что на выходе |
|---|---|
| `04-return-policy-value.md` | `<Link to="/math-rl/textbook/{текущая часть}/04-return-policy-value">` |
| `../part-1-limits-series/05-value-iteration.md` | `<Link to="/math-rl/textbook/part-1/05-value-iteration">` |
| `…/05-bellman-equations.md#обозначения` | тот же маршрут + `#обозначения` (якорь уже в `slugify`-форме) |
| `index.md` | маршрут части |
| `https://rl-cuber-unity-code.com/courses/1-3` | внутренний `<Link to="/courses/1-3">` — без перезагрузки SPA |
| `https://rl-cuber-unity-code.com/math-rl/module-5#глава-5` | внутренний `<Link>` с якорем |
| любой другой `https://…` | `<a target="_blank" rel="noopener noreferrer">` + иконка внешней ссылки |
| `../docs/…`, `Assets/…` и прочие пути репозиториев | не ссылка, а `<code>` — путь к файлу, как и задумано в `_meta/conventions.md` |

Преобразование делать **на этапе сборки индекса тоже**: скрипт проверяет, что каждая относительная
ссылка разрешается в существующий файл, и падает, если нет. Ссылка, которая не резолвится в рантайме,
— тихая ошибка; в сборке — громкая.

---

## 8. Шаг 6. Связи «сайт ↔ пособие»

### 8.1 Расширить реестр связей

В `src/config/crosslinks.ts` тип `CrossLink` дополняется одним необязательным полем:

```ts
  /** Полная лекция пособия, если она есть для этой связи. */
  textbookRoute?: string;
```

Затем:

1. **15 существующих связей** (`_meta/crosslinks.md` §1, отмечены **жирным**) — проставить
   `textbookRoute` рядом с уже имеющимся `hubPath`/`hubAnchor`. Существующие поля **не трогать**.
2. **Предлагаемые связи** из `_meta/crosslinks.md` §3 — добавить новыми записями. Это доводит
   покрытие до всех 24 уроков и почти всех 51 раздела. Не добавлять связь, если контекст
   в лекции не проговорён: реестр — навигация, а не таблица тегов.
3. Обновить `getLinksForHub` — фильтр по `textbookRoute` для обратного направления.

### 8.2 В уроках курса

В каждом уроке из `_meta/lessons.md`, где указана связь, поставить `HubLink` с обратным якорем:

```tsx
<HubLink
  to="/math-rl/textbook/part-6/05-bellman-equations"
  fromPath="/courses/1-3" fromAnchor="bellman-intro" fromLabel="Урок 1.3. MDP"
>
  Полный вывод уравнения Беллмана
</HubLink>
```

`fromPath`/`fromAnchor`/`fromLabel` обязательны — на них держится `ReturnToLessonChip` на лекции.

### 8.3 В хабе `/math-rl`

В `Section.tsx` добавить необязательный проп `lecture?: string` — маршрут полной лекции; при его
наличии в шапке секции рисуется чип «Полная лекция →». Значения расставить по таблице
`_meta/mindmap.md` (там для каждого узла указан файл пособия) — 39 узлов + разделы без узлов.
Обратное направление на лекции — строка «Краткая версия в хабе →» на `hubRoute#hubAnchor`.

### 8.4 Мост в Unity-репозиторий

`_meta/unity-bridge.md` даёт соответствие «тема → файл в `unity-ml-agents-lab`». На лекциях с
соответствующими тегами — блок «Где это в коде» со ссылками на GitHub (внешние, `target="_blank"`).
Пути в `unity-bridge.md` даны от корня того репозитория; базовый URL задать одной константой.

---

## 9. Шаг 7. Две mind map

### 9.1 `/math-rl/mindmap` — карта математики

Файл `src/content/mathMindMap.ts`. Правки:

```diff
 interface RawLeaf {
   label: string;
   anchor?: string;
   difficulty: MapNode["difficulty"];
+  /** Маршрут полной лекции пособия. */
+  textbook?: string;
 }
```

- Заполнить `textbook` для всех 39 листьев — соответствие «узел → файл» готово в `_meta/mindmap.md`.
- `leafLink` возвращает `textbook ?? base#slugify(anchor)`; прежний `base#anchor` кладётся в новое
  поле узла `secondaryLink` с подписью «в обзоре».
- В `MapNode` (`knowledgeMap.ts`) добавить необязательные `secondaryLink?: string` и
  `secondaryLabel?: string`; в `MindMapCanvas.tsx` — вторую строку-ссылку в карточке/тултипе узла.
  Оба типа карт используют один канвас, поле необязательное — вторая карта не ломается.
- Разделы, которых нет среди 39 узлов (введения, задачники, глоссарии, источники — отмечены «—»
  в `_meta/mindmap.md`), добавить листьями с `difficulty: "beginner"` там, где это осмысленно.
  Ветвь не должна разрастись вдвое: глоссарии и источники лучше оставить только на странице части.
- `getMathCoverage()` — пересчитать: число узлов, число лекций, процент покрытия пособием.
  Значение выводится в шапке страницы карты, оно не должно разойтись с реальностью.

### 9.2 `/knowledge-map` — карта всего сайта

Файл `src/content/knowledgeMap.ts`. Здесь листья — уроки, и математика должна выглядеть как
опора под ними, а не как отдельная вселенная:

1. Существующим узлам-урокам добавить `secondaryLink` на профильную лекцию пособия
   (по `_meta/crosslinks.md` §1 и §3): у «MDP» — `…/part-6/03-mdp`, у «Q-Learning» —
   `…/part-6/06-model-free-rl`, и так далее.
2. Добавить ветвь `math-textbook`:
   ```ts
   {
     id: "math-textbook",
     label: "Математика: учебник",
     caption: "51 раздел: от предела последовательности до PPO",
     icon: Sigma,
     color: "emerald",
     link: "/math-rl/textbook",
     nodes: [ /* 7 узлов — по одному на часть, link = /math-rl/textbook/part-N */ ],
   }
   ```
   Именно 7 узлов, а не 51: карта сайта отвечает на вопрос «куда идти», детализация — на
   `/math-rl/mindmap`. У каждого узла части `blurb` — из `index.md` («Что будет уметь читатель»).
3. `link` ветви `fundamentals` (сейчас `/hub/math-rl`) оставить как есть — он разрешается
   через `HubLink`.

### 9.3 Требование к обеим картам

Единственный источник данных карт — `mathMindMap.ts` и `knowledgeMap.ts`; маршруты лекций в них
берутся из `index.generated.ts`, а не пишутся строками руками. Опечатка в маршруте на карте —
самая незаметная поломка из всех: узел просто ведёт в пустоту.

---

## 10. Шаг 8. Обнаружимость

- `src/content/hubs.ts` — в описание хаба `math-rl` добавить упоминание учебника;
  при желании — отдельный `SupportHub` c `slug: "math-rl/textbook"`.
- `MathRL.tsx` — рядом с кнопкой «Mathematics Mind Map» кнопка «Учебник · 51 раздел»
  на `/math-rl/textbook`. В боковом оглавлении хаба — ссылка на учебник первой строкой.
- `GlobalSearch.tsx` — подключить `LECTURES` из `index.generated.ts` (title + tags + part).
  Поиск по телу лекций не делать: это отдельная задача с индексом.
- `Navbar` — пункт «Математика» ведёт на `/math-rl`; учебник — вложенным пунктом.
- SEO: страницы лекций попадают в `sitemap.xml` (если он генерируется — добавить источник
  `LECTURES`); `canonical` ставит `SEOHead`.

---

## 11. Шаг 9. Проверки

Новый скрипт `scripts/textbook-audit.mjs` (запускать в CI вместе с существующим `link-audit.mjs`):

1. Каждая лекция из `index.generated.ts` имеет маршрут в `App.tsx`-схеме и файл на диске.
2. Каждая относительная `.md`-ссылка разрешается в существующий файл.
3. Каждый `#якорь` во внутренней ссылке существует среди `slugify(h2|h3|h4)` целевой лекции.
4. Каждый `textbookRoute` в `crosslinks.ts` есть среди `LECTURES`.
5. Каждый `textbook` и `secondaryLink` в обеих картах есть среди `LECTURES` / маршрутов сайта.
6. Каждый `hub_anchor_canonical` по-прежнему находится среди `id` в `src/**` (это уже делает
   `link-audit.mjs` — не сломать его расширением на `.md`).
7. Ни в одном `.md` нет `\class{`, `\textcolor{`, `\color{`, а также юникодных `∑ ∫ θ γ`
   внутри `$…$` (правило `ENF-MATH-001`).

Ручная проверка перед сдачей:

- [ ] Пять цветов в контрольной формуле (5.6).
- [ ] Переход «урок 1.3 → лекция → чип возврата → урок 1.3» отрабатывает и скроллит к якорю.
- [ ] Клик по узлу «Уравнения Беллмана» на `/math-rl/mindmap` открывает лекцию;
      вторая ссылка ведёт в `/math-rl/module-5#глава-5` и раскрывает аккордеон.
- [ ] На мобильном: формулы скроллятся горизонтально, не режутся (`overflow-x: auto`
      у контейнера формулы — уже есть в `Math.tsx` и `.prose-cyber`).
- [ ] Длинная лекция (part-6/05) не тормозит: KaTeX рендерит один раз, mermaid — лениво.
- [ ] `npm run build` без предупреждений о размере чанков сверх текущих.

---

## 12. Шаг 10. Синхронизация в будущем

Источник истины по содержанию — `.md` в `Math_for_DS_&_RL/math-textbook/`. Сайт получает копию.
Чтобы копии не разошлись:

- Обновление одной командой: `npm run textbook:sync` — скрипт копирует `math-textbook/**/*.md`
  из настроенного пути и перегенерирует индекс. Альтернатива — `git subtree` для каталога.
- Правки контента в репозитории сайта запрещены: там только рендер. Если правка сделана на сайте,
  её нужно вернуть в исходный репозиторий и прогнать `pwsh Scripts/check.ps1 <путь>`.
- Проверки ENF (`check-colors`, `check-frontmatter`, `check-structure`, `check-links`) остаются
  в исходном репозитории и запускаются там; сайт проверяет только интеграционный слой.
- При добавлении новой лекции достаточно: положить `.md` → `npm run textbook:index` →
  добавить узел в mind map, если тема того заслуживает. Маршрут появится сам.

---

## 13. Порядок работ

| Этап | Содержание | Результат, который видно |
|---|---|---|
| 1 | Разделы 3–4: копирование, `parts.ts`, скрипт индекса, `loader.ts` | `index.generated.ts` с 58 записями |
| 2 | Раздел 5: KaTeX-макросы, `enf-math.css`, правка `Math.tsx` | контрольная формула в пяти цветах |
| 3 | Раздел 4.4–4.6 + 6: `MarkdownLecture`, коллауты, код, mermaid, три страницы, маршруты | одна лекция целиком, вживую |
| 4 | Раздел 7: `LectureLink`, проверка относительных ссылок | связность внутри пособия |
| 5 | Раздел 8: `crosslinks.ts`, `HubLink` в уроках, чипы «Полная лекция →» | двусторонние связи с сайтом |
| 6 | Раздел 9: обе mind map | узлы ведут в лекции |
| 7 | Разделы 10–11: обнаружимость, аудиты, приёмка | зелёный CI и чек-лист раздела 1 |

Этапы 1–3 — критический путь: пока не работает раздел 5, всё остальное собирать бессмысленно,
потому что раскраска — не оформление, а часть нотации пособия.

---

## 14. Состояние реализации на 9 августа 2026

Ветка `feat/math-textbook-integration` в репозитории сайта. Пройдены этапы 1–6; типизация,
линтер, сборка и оба аудита проходят, страницы проверены в браузере.

**Сделано**

| Что | Где |
|---|---|
| 58 `.md` перенесены | `src/content/math-textbook/**` |
| Таблица частей | `src/content/textbook/parts.ts` |
| Генератор индекса + проверки целостности | `scripts/build-textbook-index.mjs` → `index.generated.ts` (51 лекция, 7 частей) |
| Ленивая загрузка тела | `src/content/textbook/loader.ts` |
| Раскраска формул | `src/lib/katex-options.ts`, `src/styles/enf-math.css`, правка `Math.tsx` |
| Рендер markdown | `src/components/textbook/MarkdownLecture.tsx` |
| Коллауты | `src/lib/remark-enf-callouts.ts` + `src/styles/textbook.css` |
| Ссылки | `src/lib/textbook-links.ts`, `LectureLink.tsx` |
| Диаграммы | `src/components/textbook/MermaidDiagram.tsx` |
| Легенда ролей | `src/components/textbook/ColorLegend.tsx` |
| Три страницы и маршруты | `src/pages/textbook/*`, `App.tsx` |
| Связь с уроками | `crosslinks.ts` (+`textbookRoute` у 15 связей), `LectureCrossLinks.tsx` |
| Мост из хаба | `src/components/math-rl/TextbookStrip.tsx` + кнопка в `MathRL.tsx` |
| Обе mind map | `mathMindMap.ts`, `knowledgeMap.ts`, `MindMapCanvas.tsx` |
| Аудит | `scripts/textbook-audit.mjs`, `npm run textbook:audit` |
| Реестр связей целиком | 89 связей «урок → лекция» из §3 добавлено к 15 прежним, итого 162 записи |
| Ссылки в самих уроках | `LessonLayout.tsx` (12 уроков, чип «Полная лекция →» в блоке «Углубись в тему») и `LessonTextbookLinks.tsx` (8 уроков со своей вёрсткой) |
| Поиск | `GlobalSearch.tsx` — группа «Учебник» из сгенерированного индекса |
| sitemap | генерируется тем же скриптом в блоке `<!-- textbook:start -->…<!-- textbook:end -->` |
| Синхронизация | `scripts/sync-textbook.mjs`, `npm run textbook:sync` и `npm run textbook:check` |
| Мост в код | пути из `_meta/unity-bridge.md` в разделах «Практика в этом репозитории» стали ссылками на GitHub |

**Отличия от первоначального плана** (осознанные, менять обратно не нужно)

- Коллауты — remark-плагин плюс CSS вместо React-компонента: меньше кода, заголовок с математикой
  остаётся деревом узлов.
- Мост «хаб → учебник» сделан полосой `TextbookStrip` на уровне части (одна правка `MathRL.tsx`
  покрывает все 51 лекцию), а не чипом в каждой секции: части I–V и VII свёрстаны большими TSX-файлами
  без общего компонента секции, и 51 точечная правка не окупалась.
- Маршруты лекций в `mathMindMap.ts` не пишутся руками: ищутся по паре «часть + `mindmap_node`»
  в сгенерированном индексе. В `knowledgeMap.ts` соответствие задано явно (`TEXTBOOK_UNDER`)
  и проверяется аудитом.
- Мост в код сделан не отдельным блоком, а ссылками на самих путях: раздел «Практика в этом
  репозитории» уже есть во всех 51 лекции, и второй список тех же путей был бы копией.
  Ссылку получают только пути из `_meta/unity-bridge.md` — обычный `код` в тексте ею не становится.
  Адреса вида `.../blob/HEAD/<путь>`: GitHub разрешает `HEAD` в ветку по умолчанию, поэтому
  её переименование ссылки не ломает.

**Как теперь обновлять содержание**

```powershell
# 1. правка .md в исходном репозитории + проверки ENF
pwsh Scripts/check.ps1 math-textbook/part-6/05-bellman-equations.md

# 2. в репозитории сайта
npm run textbook:sync     # копирует .md и пересобирает индекс со sitemap
npm run textbook:audit    # ссылки, маршруты, карты, раскраска
npm run audit:links       # якоря внутри сайта
```

`npm run textbook:check` ничего не копирует, а только сообщает о расхождении копий и выходит
с ненулевым кодом — годится для CI, чтобы правка, сделанная на стороне сайта, не осталась незамеченной.

**Осталось**

- Пять путей из `_meta/unity-bridge.md` лежат в репозитории сред на невлитой ветке
  `mlagents-training-setup` и до её слияния с `main` дадут 404: `docs/TRAINING.md`,
  `Assets/Editor/MLAgentsTrainingValidator.cs`, `config/ml-agents-reference/`,
  `config/ml-agents-reference/ppo/`,
  `Assets/ML-ENVIRONMENTS/02-Examples/Greed_world/config/GridWorldQLearning.yaml`.
  `npm run textbook:audit` печатает этот список, если репозиторий сред есть локально
  (путь берётся из `UNITY_LAB_SRC`, по умолчанию `C:/unity-ml-agents-lab`).
- Уроки 3.2, 3.3, 3.5, 3.8 связей с пособием не получили: в `_meta/crosslinks.md` §3 для них
  нет пар, и придумывать их без разбора содержания урока не нужно.

---

## Приложение. Частые ошибки

| Симптом | Причина | Где чинить |
|---|---|---|
| Формулы серые, ошибок нет | не передан `trust` — KaTeX игнорирует `\htmlClass` | 5.2 |
| В формуле виден текст `\enfVar` | не переданы `macros` | 5.2 |
| «Undefined control sequence» | в `.md` попал `\class` вместо макроса | 5.1 |
| Цвет есть, но не меняется с темой | HEX прописан в LaTeX | 5.4 |
| Якорь из урока не находит цель | `slugify` продублирована и разошлась | 4.4 |
| Ссылка `../part-…md` открывает 404 | `LectureLink` не разобрал путь | 7 |
| Узел карты ведёт в пустоту | маршрут в карте написан строкой руками | 9.3 |
| `part_id` не совпал с каталогом | путаница двух нумераций (сайт vs пособие) | 3.2 |
