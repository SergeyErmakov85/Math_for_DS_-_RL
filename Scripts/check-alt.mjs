#!/usr/bin/env node
/**
 * check-alt.mjs — доступность иллюстраций.
 *
 * Правила: ENF-DIAG-030 (alt-текст есть и описывает содержание),
 *          ENF-DIAG-031 (у каждого SVG есть <title> и <desc>).
 */

import { resolve } from 'node:path';
import { readText, walk, maskCodeBlocks, lineOf, Report, targetsFromArgv, isTemplate } from './enf-lib.mjs';

const IMG_RE = /!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;

/* Слова, которые называют тип объекта вместо его содержания. Alt-текст,
   целиком состоящий из них, формально есть, а работы своей не делает. */
const EMPTY_WORDS = [
  'схема', 'график', 'диаграмма', 'рисунок', 'картинка', 'изображение',
  'иллюстрация', 'фото', 'скриншот', 'image', 'picture', 'diagram', 'chart', 'figure',
];

const MIN_ALT_WORDS = 4;

const root = resolve('.');
const report = new Report('alt-текст', root);

for (const target of targetsFromArgv(process.argv)) {
  const base = resolve(target);

  for (const file of walk(base, ['.md'])) {
    if (isTemplate(file)) continue;
    const text = maskCodeBlocks(readText(file));

    for (const m of text.matchAll(IMG_RE)) {
      const alt = m[1].trim();
      const line = lineOf(text, m.index);

      if (!alt) {
        report.error(file, line, 'ENF-DIAG-030', `изображение ${m[2]} без alt-текста`);
        continue;
      }

      const words = alt.split(/\s+/).filter(Boolean);
      const meaningful = words.filter(
        (w) => !EMPTY_WORDS.includes(w.toLowerCase().replace(/[^\p{L}]/gu, ''))
      );

      if (meaningful.length === 0) {
        report.error(file, line, 'ENF-DIAG-030',
          `alt-текст «${alt}» называет тип объекта, а не его содержание`);
      } else if (words.length < MIN_ALT_WORDS) {
        report.warn(file, line, 'ENF-DIAG-030',
          `alt-текст «${alt}» короче ${MIN_ALT_WORDS} слов — вероятно, не описывает содержание`);
      }
    }
  }

  for (const file of walk(base, ['.svg'])) {
    const text = readText(file);

    const title = text.match(/<title[^>]*>([\s\S]*?)<\/title>/);
    const desc = text.match(/<desc[^>]*>([\s\S]*?)<\/desc>/);

    if (!title || !title[1].trim()) {
      report.error(file, 1, 'ENF-DIAG-031', 'нет элемента <title>');
    }

    if (!desc || !desc[1].trim()) {
      report.error(file, 1, 'ENF-DIAG-031', 'нет элемента <desc>');
    } else if (desc[1].trim().split(/\s+/).length < 8) {
      report.warn(file, 1, 'ENF-DIAG-031',
        '<desc> короче восьми слов; он должен сообщать, что изображено и что из этого следует');
    }

    if (!/role\s*=\s*["']img["']/.test(text)) {
      report.warn(file, 1, 'ENF-DIAG-031', 'нет атрибута role="img" у корневого <svg>');
    }

    if (!/aria-labelledby/.test(text)) {
      report.warn(file, 1, 'ENF-DIAG-031',
        'нет aria-labelledby: <title> и <desc> не будут связаны с изображением');
    }
  }
}

process.exit(report.print());
