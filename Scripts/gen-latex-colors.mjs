#!/usr/bin/env node
/**
 * gen-latex-colors.mjs — порождает LaTeX-определения цветов и макросов ролей.
 *
 * LaTeX не читает CSS, поэтому значения палитры обязаны попасть в преамбулу.
 * Чтобы единый источник истины не раздваивался (ENF-COLOR-001), файл
 * порождается из Build/css/enf-tokens.css, а не пишется руками.
 *
 * Источник:   Build/css/enf-tokens.css (светлая тема — печать идёт по белому)
 * Результат:  Build/templates/enf-colors.tex
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(HERE, '..', 'Build', 'css', 'enf-tokens.css');
const DST = resolve(HERE, '..', 'Build', 'templates', 'enf-colors.tex');

let css;
try {
  css = readFileSync(SRC, 'utf8');
} catch {
  console.error(`Не найден файл токенов: ${SRC}`);
  process.exit(2);
}

const block = css.match(/:root\s*\{([^}]*)\}/);
if (!block) {
  console.error('Не удалось найти блок :root в файле токенов.');
  process.exit(2);
}

const tokens = {};
for (const m of block[1].matchAll(/(--enf-[\w-]+)\s*:\s*#([0-9a-fA-F]{6})\s*;/g)) {
  tokens[m[1]] = m[2].toUpperCase();
}

const ROLES = [
  ['variable',  'enfVar', 'объект, над которым действуем'],
  ['function',  'enfFun', 'действие, преобразование'],
  ['parameter', 'enfPar', 'то, что настраивается'],
  ['operator',  'enfOp',  'агрегат, свёртка'],
  ['target',    'enfTgt', 'цель: награда, потери, оптимум'],
  ['neutral',   'enfNeu', 'служебное обозначение'],
];

const missing = ROLES.filter(([r]) => !tokens[`--enf-color-${r}`]).map(([r]) => r);
if (missing.length) {
  console.error(`В палитре нет тонов: ${missing.join(', ')}`);
  process.exit(2);
}

const lines = [
  '% =============================================================',
  '% ПОРОЖДЁННЫЙ ФАЙЛ — НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ.',
  '%',
  '% Источник:  Build/css/enf-tokens.css',
  '% Генератор: Scripts/gen-latex-colors.mjs',
  '% Пересоздать: node Scripts/gen-latex-colors.mjs',
  '%',
  '% Берётся светлая тема: печать идёт по белой бумаге.',
  '% =============================================================',
  '',
  '\\usepackage{xcolor}',
  '',
];

for (const [role, , note] of ROLES) {
  lines.push(`\\definecolor{enf${role}}{HTML}{${tokens[`--enf-color-${role}`]}}  % ${note}`);
}

lines.push('', '% Макросы ролей. Имена совпадают с макросами MathJax из хранилища,');
lines.push('% поэтому один и тот же исходник собирается и там, и здесь.');
lines.push('');

for (const [role, macro] of ROLES) {
  lines.push(`\\newcommand{\\${macro}}[1]{\\textcolor{enf${role}}{#1}}`);
}

lines.push('');

writeFileSync(DST, lines.join('\n') + '\n', 'utf8');
console.log(`Обновлён: ${DST}`);
