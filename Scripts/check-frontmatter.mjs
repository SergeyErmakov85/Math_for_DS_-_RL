#!/usr/bin/env node
/**
 * check-frontmatter.mjs — проверка фронтматтера материалов.
 *
 * Правила: ENF-PUB-001 (фронтматтер есть и корректен),
 *          ENF-PUB-002 (обязательные поля заполнены),
 *          ENF-MATH-022 (enf_mode имеет допустимое значение).
 */

import { resolve } from 'node:path';
import { readText, walk, parseFrontmatter, Report, targetsFromArgv, isTemplate } from './enf-lib.mjs';

const REQUIRED = ['title', 'enf_mode', 'discipline'];
const MODES = ['learning', 'publication'];
const DISCIPLINES = [
  'calculus', 'linalg', 'probability', 'statistics',
  'ml', 'rl', 'optimization', 'meta',
];

/* Каталоги, где фронтматтер не требуется: служебная документация
   репозитория материалом не является. */
const EXEMPT = [
  /(^|\/)README\.md$/i,
  /(^|\/)CHANGELOG\.md$/i,
  /(^|\/)CONTRIBUTING\.md$/i,
  /(^|\/)CLAUDE\.md$/i,
  /(^|\/)CATALOG\.md$/i,
  /(^|\/)AGENTS\.md$/i,
  /(^|\/)DOCUMENT_CONVERSION\.md$/i,
  /(^|\/)docs\/PROGRESS\.md$/,
  /(^|\/)docs\/Codex\//,
  /(^|\/)Mermaid\//,
];

const root = resolve('.');
const report = new Report('фронтматтер', root);

for (const target of targetsFromArgv(process.argv)) {
  for (const file of walk(resolve(target), ['.md'])) {
    const rel = report.rel(file);
    if (EXEMPT.some((re) => re.test(rel))) continue;
    if (isTemplate(file)) continue;

    const text = readText(file);
    const { data } = parseFrontmatter(text);

    if (!data) {
      report.error(file, 1, 'ENF-PUB-001', 'нет фронтматтера или он не закрыт строкой ---');
      continue;
    }

    for (const key of REQUIRED) {
      if (data[key] === undefined || data[key] === null || data[key] === '') {
        report.error(file, 2, 'ENF-PUB-002', `не заполнено обязательное поле «${key}»`);
      }
    }

    if (data.enf_mode && !MODES.includes(data.enf_mode)) {
      report.error(file, 2, 'ENF-MATH-022',
        `enf_mode = «${data.enf_mode}»; допустимо только ${MODES.join(' или ')}`);
    }

    if (data.discipline && !DISCIPLINES.includes(data.discipline)) {
      report.warn(file, 2, 'ENF-PUB-002',
        `discipline = «${data.discipline}» вне списка известных: ${DISCIPLINES.join(', ')}`);
    }

    if (data.title && /^\s*$/.test(String(data.title))) {
      report.error(file, 2, 'ENF-PUB-002', 'поле title пустое');
    }
  }
}

process.exit(report.print());
