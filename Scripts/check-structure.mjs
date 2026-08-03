#!/usr/bin/env node
/**
 * check-structure.mjs — структура документа и разметка.
 *
 * Правила: ENF-TYPO-010 (ровно один заголовок первого уровня),
 *          ENF-TYPO-011 (уровни заголовков не пропущены),
 *          ENF-TYPO-012 (глубина не больше четырёх),
 *          ENF-TYPO-014 (в заголовках нет формул),
 *          ENF-TYPO-040 (у блока кода указан язык),
 *          ENF-MATH-002 (только разрешённые окружения LaTeX),
 *          ENF-MATH-041 (доказательство завершается символом),
 *          ENF-DIAG-040 (только разрешённые типы диаграмм Mermaid),
 *          ENF-PUB-005 (в готовом материале нет служебных комментариев).
 */

import { resolve } from 'node:path';
import { readText, walk, maskCodeBlocks, findCodeFences, lineOf, Report, targetsFromArgv, isTemplate } from './enf-lib.mjs';

const FORBIDDEN_ENV = ['align', 'equation', 'eqnarray', 'tikzpicture', 'tabular', 'figure', 'table'];
const ALLOWED_MERMAID = [
  'flowchart', 'graph', 'stateDiagram-v2', 'sequenceDiagram',
  'classDiagram', 'pie', 'gitGraph',
];

const EXEMPT_STRUCTURE = [/(^|\/)CHANGELOG\.md$/i, /(^|\/)docs\/reference\/PROGRESS\.md$/];

const root = resolve('.');
const report = new Report('структура', root);

for (const target of targetsFromArgv(process.argv)) {
  for (const file of walk(resolve(target), ['.md'])) {
    const rel = report.rel(file);
    const template = isTemplate(file);
    const raw = readText(file);
    const text = maskCodeBlocks(raw);

    /* ---------- заголовки ---------- */
    if (!EXEMPT_STRUCTURE.some((re) => re.test(rel))) {
      const heads = [...text.matchAll(/^(#{1,6})\s+(.*)$/gm)].map((m) => ({
        level: m[1].length,
        title: m[2],
        line: lineOf(text, m.index),
      }));

      const h1 = heads.filter((h) => h.level === 1);
      if (h1.length === 0) {
        report.error(file, 1, 'ENF-TYPO-010', 'нет заголовка первого уровня');
      } else if (h1.length > 1) {
        report.error(file, h1[1].line, 'ENF-TYPO-010',
          `заголовков первого уровня ${h1.length}, должен быть ровно один`);
      }

      let prev = 0;
      for (const h of heads) {
        if (prev && h.level > prev + 1) {
          report.error(file, h.line, 'ENF-TYPO-011',
            `пропущен уровень заголовка: после h${prev} идёт h${h.level}`);
        }
        if (h.level > 4) {
          report.warn(file, h.line, 'ENF-TYPO-012',
            `глубина заголовка h${h.level}; вероятно, документ пора разделить`);
        }
        if (/\$[^$]+\$/.test(h.title)) {
          report.error(file, h.line, 'ENF-TYPO-014',
            'формула в заголовке: она не попадёт в оглавление PDF и закладки EPUB');
        }
        prev = h.level;
      }
    }

    /* ---------- блоки кода ---------- */
    for (const b of findCodeFences(raw)) {
      if (b.unterminated) {
        report.error(file, b.line, 'ENF-TYPO-040', 'блок кода не закрыт');
      } else if (b.info === '') {
        report.error(file, b.line, 'ENF-TYPO-040', 'у блока кода не указан язык');
      }
    }

    /* ---------- LaTeX ---------- */
    for (const env of FORBIDDEN_ENV) {
      const re = new RegExp(`\\\\begin\\{${env}\\*?\\}`, 'g');
      for (const m of text.matchAll(re)) {
        report.error(file, lineOf(text, m.index), 'ENF-MATH-002',
          `окружение \\begin{${env}} запрещено: оно ведёт себя по-разному в MathJax и LaTeX`);
      }
    }

    /* ---------- доказательства ---------- */
    for (const m of text.matchAll(/^>\s*\[!proof\]/gmi)) {
      const start = m.index;
      const rest = text.slice(start, start + 4000);
      const end = rest.search(/\n(?!>)/);
      const block = end === -1 ? rest : rest.slice(0, end);
      if (!/\\blacksquare|\\square|∎/.test(block)) {
        report.error(file, lineOf(text, start), 'ENF-MATH-041',
          'доказательство не завершается символом $\\blacksquare$');
      }
    }

    /* ---------- Mermaid ---------- */
    for (const m of raw.matchAll(/```mermaid\s*\n([\s\S]*?)```/g)) {
      const body = m[1].replace(/^%%\{[\s\S]*?\}%%\s*/m, '').trim();
      const kind = body.split(/[\s\n]/)[0];
      if (kind && !ALLOWED_MERMAID.includes(kind)) {
        report.error(file, lineOf(raw, m.index), 'ENF-DIAG-040',
          `тип диаграммы «${kind}» не поддержан одновременно Obsidian и Pandoc; разрешено: ${ALLOWED_MERMAID.join(', ')}`);
      }
    }

    /* ---------- служебные комментарии ----------
       Ищем в тексте без блоков кода: в промтах и чек-листе такой комментарий
       показан как образец, и это не нарушение. */
    if (!template) {
      for (const m of text.matchAll(/<!--\s*ENF:/g)) {
        report.error(file, lineOf(text, m.index), 'ENF-PUB-005',
          'служебный комментарий <!-- ENF: … --> остался в готовом материале');
      }
    }
  }
}

process.exit(report.print());
