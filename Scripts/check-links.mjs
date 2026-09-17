#!/usr/bin/env node
/**
 * check-links.mjs — проверка внутренних ссылок.
 *
 * Правило ENF-TYPO-051: ссылки внутри репозитория — относительными путями;
 * wiki-ссылки Obsidian допустимы только в служебных заметках хранилища
 * (Obsidian/) и в Templater-шаблонах (templates/templater/), потому что
 * Pandoc их не понимает и материал развалится при сборке.
 */

import { existsSync, statSync } from 'node:fs';
import { resolve, dirname, join, sep } from 'node:path';
import { readText, walk, maskCodeBlocks, lineOf, Report, targetsFromArgv } from './enf-lib.mjs';

const LINK_RE = /\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;
const WIKI_RE = /(?<!!)\[\[([^\]]+)\]\]/g;
const EXTERNAL_RE = /^(https?:|mailto:|tel:|#|data:)/i;

const root = resolve('.');
const report = new Report('ссылки', root);

/** Якоря заголовков файла — для проверки ссылок вида file.md#раздел. */
function anchorsOf(file) {
  const text = maskCodeBlocks(readText(file));
  const out = new Set();
  for (const m of text.matchAll(/^#{1,6}\s+(.+?)\s*$/gm)) {
    out.add(
      m[1]
        .toLowerCase()
        .replace(/[`*_~]/g, '')
        .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
        .trim()
        .replace(/\s+/g, '-')
        .replace(/[^\p{L}\p{N}-]/gu, '')
    );
  }
  return out;
}

const anchorCache = new Map();
const anchorsCached = (file) => {
  if (!anchorCache.has(file)) anchorCache.set(file, anchorsOf(file));
  return anchorCache.get(file);
};

for (const target of targetsFromArgv(process.argv)) {
  for (const file of walk(resolve(target), ['.md'])) {
    const rel = report.rel(file);
    const wikiAllowed = rel.startsWith('Obsidian/') || rel.startsWith('templates/templater/');
    const raw = readText(file);
    const text = maskCodeBlocks(raw);

    for (const m of text.matchAll(WIKI_RE)) {
      if (wikiAllowed) continue;
      report.error(file, lineOf(text, m.index), 'ENF-TYPO-051',
        `wiki-ссылка [[${m[1]}]] в материале; Pandoc её не понимает — используйте относительный путь`);
    }

    for (const m of text.matchAll(LINK_RE)) {
      const href = m[2];
      if (EXTERNAL_RE.test(href)) continue;

      const [pathPart, anchor] = href.split('#');
      const line = lineOf(text, m.index);

      if (pathPart === '') {
        if (anchor && !anchorsCached(file).has(decodeURIComponent(anchor).toLowerCase())) {
          report.warn(file, line, 'ENF-TYPO-051',
            `якорь #${anchor} не найден среди заголовков этого файла`);
        }
        continue;
      }

      const decoded = decodeURIComponent(pathPart);
      const abs = join(dirname(file), decoded);

      if (!existsSync(abs)) {
        report.error(file, line, 'ENF-TYPO-051', `битая ссылка: ${href}`);
        continue;
      }

      if (anchor && statSync(abs).isFile() && abs.endsWith('.md')) {
        if (!anchorsCached(abs).has(decodeURIComponent(anchor).toLowerCase())) {
          report.warn(file, line, 'ENF-TYPO-051',
            `файл найден, но якоря #${anchor} в нём нет`);
        }
      }

      if (/\\/.test(pathPart)) {
        report.error(file, line, 'ENF-TYPO-051',
          `в пути использован обратный слэш: ${href}; путь должен работать и вне Windows`);
      }
    }

    for (const m of text.matchAll(/\[([^\]]*)\]\(/g)) {
      const label = m[1].trim().toLowerCase();
      if (['здесь', 'тут', 'по ссылке', 'сюда', 'here', 'link', 'ссылка'].includes(label)) {
        report.warn(file, lineOf(text, m.index), 'ENF-TYPO-050',
          `неинформативный текст ссылки «${m[1].trim()}»`);
      }
    }
  }
}

process.exit(report.print());
