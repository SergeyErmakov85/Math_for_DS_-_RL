#!/usr/bin/env node
/**
 * gen-mermaid-init.mjs — порождает init-блоки Mermaid из палитры ENF.
 *
 * Зачем. Mermaid не умеет подключать внешние темы: цвета обязаны находиться
 * в тексте самой диаграммы, в директиве %%{init: ...}%%. Единственный способ
 * сохранить при этом единый источник истины (ENF-COLOR-001) — порождать эти
 * директивы из css/enf-tokens.css, а не писать руками.
 *
 * Почему берётся светлая палитра. Директива одна на диаграмму, а тем две.
 * Разрешается это тем, что диаграмма задаёт собственный фон и не наследует
 * фон страницы: светлые заливки с тёмным текстом читаются одинаково в обеих
 * темах. Так требование ENF-COLOR-032 выполняется по построению, а не
 * подстройкой под тему.
 *
 * Что делает:
 *   1. переписывает mermaid/init-config.md;
 *   2. заменяет строки вида %%{init: ...}%% во всех остальных файлах mermaid/.
 */

import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const TOKENS = resolve(HERE, '..', 'css', 'enf-tokens.css');
const MERMAID_DIR = resolve(HERE, '..', 'mermaid');

/* ---------- чтение палитры ---------- */

function readLightTokens() {
  let css;
  try {
    css = readFileSync(TOKENS, 'utf8');
  } catch {
    console.error(`Не найден файл токенов: ${TOKENS}`);
    process.exit(2);
  }
  const block = css.match(/:root\s*\{([^}]*)\}/);
  if (!block) {
    console.error('Не удалось найти блок :root в файле токенов.');
    process.exit(2);
  }
  const out = {};
  for (const m of block[1].matchAll(/(--enf-[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;/g)) {
    out[m[1]] = m[2].toUpperCase();
  }
  return out;
}

const t = readLightTokens();
const need = [
  '--enf-fg', '--enf-bg', '--enf-border',
  '--enf-color-variable', '--enf-color-function', '--enf-color-parameter',
  '--enf-color-operator', '--enf-color-target', '--enf-color-neutral',
  '--enf-fill-variable', '--enf-fill-function', '--enf-fill-parameter',
  '--enf-fill-operator', '--enf-fill-target', '--enf-fill-neutral',
];
const missing = need.filter((k) => !t[k]);
if (missing.length) {
  console.error(`В палитре не хватает токенов: ${missing.join(', ')}`);
  process.exit(2);
}

/* ---------- сборка директивы ---------- */

const themeVars = {
  fontFamily: "Inter, 'PT Sans', system-ui, sans-serif",
  fontSize: '15px',

  background: t['--enf-bg'],
  primaryColor: t['--enf-fill-variable'],
  primaryTextColor: t['--enf-fg'],
  primaryBorderColor: t['--enf-color-variable'],

  secondaryColor: t['--enf-fill-function'],
  secondaryTextColor: t['--enf-fg'],
  secondaryBorderColor: t['--enf-color-function'],

  tertiaryColor: t['--enf-fill-parameter'],
  tertiaryTextColor: t['--enf-fg'],
  tertiaryBorderColor: t['--enf-color-parameter'],

  lineColor: t['--enf-color-neutral'],
  textColor: t['--enf-fg'],

  mainBkg: t['--enf-fill-variable'],
  nodeBorder: t['--enf-color-variable'],
  nodeTextColor: t['--enf-fg'],
  clusterBkg: t['--enf-bg'],
  clusterBorder: t['--enf-border'],
  edgeLabelBackground: t['--enf-bg'],
  titleColor: t['--enf-fg'],
};

const INIT_LINE =
  `%%{init: {'theme':'base','themeVariables':${JSON.stringify(themeVars)}}}%%`;

/* Классы ролей, которые диаграммы применяют через classDef.
   Имена совпадают с ролями палитры — так их значение очевидно из текста. */
const CLASSDEFS = [
  ['variable',  '--enf-fill-variable',  '--enf-color-variable'],
  ['function',  '--enf-fill-function',  '--enf-color-function'],
  ['parameter', '--enf-fill-parameter', '--enf-color-parameter'],
  ['operator',  '--enf-fill-operator',  '--enf-color-operator'],
  ['target',    '--enf-fill-target',    '--enf-color-target'],
  ['neutral',   '--enf-fill-neutral',   '--enf-color-neutral'],
]
  .map(([name, fill, stroke]) =>
    `    classDef ${name} fill:${t[fill]},stroke:${t[stroke]},stroke-width:2px,color:${t['--enf-fg']};`)
  .join('\n');

/* ---------- запись init-config.md ---------- */

const configDoc = `<!-- ПОРОЖДЁННЫЙ ФАЙЛ — НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ.
     Источник: css/enf-tokens.css
     Генератор: Scripts/gen-mermaid-init.mjs
     Пересоздать: node Scripts/gen-mermaid-init.mjs -->

# Единый init-блок Mermaid

Директива ниже подключает палитру ENF. Она вставляется **первой строкой** каждой диаграммы фреймворка.

Mermaid не поддерживает внешние файлы тем: цвета обязаны находиться в тексте диаграммы. Поэтому директива порождается из единого источника, а не пишется руками — правка цвета прямо в диаграмме потеряется при следующей генерации (\`ENF-DIAG-041\`).

## Директива

\`\`\`text
${INIT_LINE}
\`\`\`

## Классы ролей

Узлы окрашиваются не литералами, а классами, имена которых совпадают с ролями палитры. Добавьте нужные строки в конец диаграммы и примените классы через \`class\`:

\`\`\`text
${CLASSDEFS}
\`\`\`

Применение:

\`\`\`text
    class A,B variable;
    class C function;
\`\`\`

## Почему используется светлая палитра

Директива одна на диаграмму, а тем две. Разрешается это тем, что диаграмма задаёт собственный фон и не наследует фон страницы: светлые заливки с тёмным текстом читаются одинаково в светлой и тёмной теме. Требование \`ENF-COLOR-032\` выполняется по построению — диаграмма не зависит от темы, а не подстраивается под неё.

## Проверка

\`\`\`powershell
node Scripts/gen-mermaid-init.mjs      # пересоздать директивы
node Scripts/check-colors.mjs mermaid/ # цвета вне палитры
\`\`\`
`;

writeFileSync(join(MERMAID_DIR, 'init-config.md'), configDoc, 'utf8');
console.log('Обновлён: mermaid/init-config.md');

/* ---------- обновление init-строк в шаблонах ---------- */

let touched = 0;
for (const name of readdirSync(MERMAID_DIR)) {
  if (!name.endsWith('.md') || name === 'init-config.md' || name === 'README.md') continue;
  const path = join(MERMAID_DIR, name);
  const src = readFileSync(path, 'utf8');
  const out = src.replace(/^%%\{init:.*\}%%$/gm, INIT_LINE);
  if (out !== src) {
    writeFileSync(path, out, 'utf8');
    touched++;
    console.log(`Обновлён: mermaid/${name}`);
  }
}

console.log(`Готово. Файлов с обновлённой директивой: ${touched}.`);
