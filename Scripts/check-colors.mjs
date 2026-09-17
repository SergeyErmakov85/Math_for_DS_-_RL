#!/usr/bin/env node
/**
 * check-colors.mjs — проверка цвета в материалах, SVG и Mermaid.
 *
 * Правила: ENF-COLOR-001 (никаких HEX вне единого источника),
 *          ENF-COLOR-030 (никаких прямых команд цвета в формулах),
 *          ENF-MATH-021  (лимит тонов на формулу по режиму),
 *          ENF-COLOR-012 (в Publication Mode — только безопасная тройка).
 */

import { resolve, sep } from 'node:path';
import { readText, walk, parseFrontmatter, maskCodeBlocks, lineOf, Report, targetsFromArgv, isTemplate } from './enf-lib.mjs';

/* Файлы, которым HEX разрешён по существу: единый источник истины,
   порождённые из него файлы и документация, объясняющая палитру. */
const HEX_ALLOWED = [
  /css\/enf-tokens\.css$/,
  /snippets\//,
  /\.obsidian\/snippets\//,
  /Build\/templates\/enf-colors\.tex$/,
  /docs\/02_Color_System\.md$/,
  /mermaid\//,
  /Scripts\//,
  /docs\/reference\/PROGRESS\.md$/,
];

/* В SVG HEX допустим только как запасное значение в var(): файл обязан
   оставаться корректным вне Obsidian. Проверяется отдельным правилом. */
const MODE_LIMITS = {
  learning: { max: 4, allowed: null },
  publication: { max: 3, allowed: new Set(['enfVar', 'enfFun', 'enfPar']) },
};

/* Нейтральный макрос \enfNeu намеренно не входит в набор: нейтральный тон
   не участвует в семантике и не расходует лимит ролей (ENF-COLOR-010). */
const MACRO_RE = /\\(enfVar|enfFun|enfPar|enfOp|enfTgt)\b/g;
const NAKED_MACRO_RE = /(?<![\\\w])(enfVar|enfFun|enfPar|enfOp|enfTgt|enfNeu)\s*\{/g;
const HEX_RE = /#[0-9a-fA-F]{6}\b/g;
const RAW_COLOR_RE = /\\(textcolor|color|definecolor|colorbox|pagecolor)\b/g;

const root = resolve('.');
const report = new Report('цвета и режимы', root);

function checkMarkdown(file, rel) {
  const text = readText(file);
  const { data, body } = parseFrontmatter(text);
  const masked = maskCodeBlocks(text);

  if (!HEX_ALLOWED.some((re) => re.test(rel))) {
    for (const m of masked.matchAll(HEX_RE)) {
      report.error(file, lineOf(masked, m.index), 'ENF-COLOR-001',
        `HEX-код ${m[0]} в материале; цвет задаётся ролью, а значение живёт в css/enf-tokens.css`);
    }
  }

  for (const m of masked.matchAll(RAW_COLOR_RE)) {
    report.error(file, lineOf(masked, m.index), 'ENF-COLOR-030',
      `прямая команда цвета \\${m[1]}; используйте макросы ролей \\enfVar, \\enfFun, \\enfPar, \\enfOp, \\enfTgt`);
  }

  /* Макрос без обратной косой черты. Ошибка выглядит безобидно и глазом
     не ловится: `$enfVar{x}$` вместо `$\enfVar{x}$`. Раскраска молча не
     применяется, а в формулу попадает мусорный текст «enfVarx». */
  for (const m of masked.matchAll(NAKED_MACRO_RE)) {
    report.error(file, lineOf(masked, m.index), 'ENF-COLOR-030',
      `макрос ${m[1]} записан без обратной косой черты; нужно \\${m[1]}{…}, иначе имя макроса попадёт в формулу текстом`);
  }

  /* Документы о самом фреймворке (discipline: meta) показывают палитру
     целиком — справка по ролям обязана предъявить все пять тонов сразу.
     Применять к ним лимит режима бессмысленно: это не учебный материал,
     а описание инструмента. */
  if (data?.discipline === 'meta') return;

  const mode = data?.enf_mode;
  if (!mode || !MODE_LIMITS[mode]) return;
  const limit = MODE_LIMITS[mode];

  /* Формулы: выключные $$...$$ и строчные $...$. Ищем в теле без блоков кода. */
  const bodyMasked = maskCodeBlocks(body);
  const formulas = [
    ...bodyMasked.matchAll(/\$\$([\s\S]*?)\$\$/g),
    ...bodyMasked.matchAll(/(?<!\$)\$(?!\$)([^\n$]+?)\$(?!\$)/g),
  ];

  const offset = text.length - body.length;

  for (const f of formulas) {
    const used = new Set([...f[1].matchAll(MACRO_RE)].map((m) => m[1]));
    if (used.size === 0) continue;
    const line = lineOf(text, offset + f.index);

    if (used.size > limit.max) {
      report.error(file, line, 'ENF-MATH-021',
        `в формуле ${used.size} тонов при лимите ${limit.max} для режима «${mode}»: ${[...used].join(', ')}`);
    }

    if (limit.allowed) {
      const forbidden = [...used].filter((u) => !limit.allowed.has(u));
      if (forbidden.length) {
        report.error(file, line, 'ENF-COLOR-012',
          `в Publication Mode разрешены только \\enfVar, \\enfFun, \\enfPar; найдено: ${forbidden.map((f) => '\\' + f).join(', ')}`);
      }
    }
  }
}

function checkSvg(file) {
  const text = readText(file);

  /* HEX вне var() — нарушение: значение не будет обновлено при смене палитры. */
  const withoutFallbacks = text.replace(/var\(\s*--enf-[\w-]+\s*,\s*#[0-9a-fA-F]{6}\s*\)/g, 'var()');
  for (const m of withoutFallbacks.matchAll(HEX_RE)) {
    report.error(file, lineOf(withoutFallbacks, m.index), 'ENF-COLOR-001',
      `HEX ${m[0]} вне var(--enf-color-*, …); цвет должен приходить из палитры, HEX допустим только как запасное значение`);
  }

  for (const bad of ['black', 'white', 'red', 'blue', 'green', 'gray', 'grey']) {
    const re = new RegExp(`(fill|stroke)\\s*[:=]\\s*["']?${bad}\\b`, 'gi');
    for (const m of text.matchAll(re)) {
      report.error(file, lineOf(text, m.index), 'ENF-DIAG-010',
        `именованный цвет «${bad}» в атрибуте ${m[1]}; на тёмном фоне он исчезнет — берите тон из палитры`);
    }
  }

  const tones = new Set([...text.matchAll(/--enf-color-(variable|function|parameter|operator|target)/g)].map((m) => m[1]));
  if (tones.size > 4) {
    report.error(file, 1, 'ENF-DIAG-011',
      `на диаграмме ${tones.size} тонов при лимите 4: ${[...tones].join(', ')}`);
  }
}

for (const target of targetsFromArgv(process.argv)) {
  const base = resolve(target);
  for (const file of walk(base, ['.md'])) {
    if (isTemplate(file)) continue;
    checkMarkdown(file, report.rel(file));
  }
  for (const file of walk(base, ['.svg'])) checkSvg(file);
}

process.exit(report.print());
