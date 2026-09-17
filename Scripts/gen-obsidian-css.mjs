#!/usr/bin/env node
/**
 * gen-obsidian-css.mjs — переносит CSS-сниппеты в хранилище Obsidian.
 *
 * Зачем это нужно. Obsidian не умеет подключать CSS из-за пределов хранилища:
 * @import на файл вне vault не работает. Значит, сниппеты обязаны физически
 * лежать внутри хранилища. Копировать их руками нельзя — это нарушило бы
 * ENF-COLOR-001 (единый источник истины), поэтому копии порождаются
 * скриптом и помечены как порождённые.
 *
 * Источники: css/enf-tokens.css, snippets/enf-math.css, snippets/enf-callouts.css,
 *            snippets/enf-code.css
 * Результат:  .obsidian/snippets/ — корень репозитория и есть хранилище
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const VAULT = resolve(HERE, '..', '.obsidian', 'snippets');

/* Токены живут в css/ вместе с остальной конфигурацией сборки: их читают
   и Pandoc, и генератор LaTeX-цветов. Остальные сниппеты специфичны для
   Obsidian и живут в snippets/. */
const SOURCES = [
  { src: resolve(HERE, '..', 'css', 'enf-tokens.css'), from: 'css/enf-tokens.css', name: 'enf-tokens.css' },
  { src: resolve(HERE, '..', 'snippets', 'enf-math.css'), from: 'snippets/enf-math.css', name: 'enf-math.css' },
  { src: resolve(HERE, '..', 'snippets', 'enf-callouts.css'), from: 'snippets/enf-callouts.css', name: 'enf-callouts.css' },
  { src: resolve(HERE, '..', 'snippets', 'enf-code.css'), from: 'snippets/enf-code.css', name: 'enf-code.css' },
];

mkdirSync(VAULT, { recursive: true });

const header = (from) => `/* =============================================================
   ПОРОЖДЁННЫЙ ФАЙЛ — НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ.

   Источник: ${from}
   Генератор: Scripts/gen-obsidian-css.mjs
   Пересоздать: node Scripts/gen-obsidian-css.mjs

   Правки, внесённые сюда напрямую, будут потеряны при следующей
   генерации. Меняйте значения в источнике — там же лежит и
   обоснование выбора цветов.
   ============================================================= */

`;

for (const { src, from, name } of SOURCES) {
  let text;
  try {
    text = readFileSync(src, 'utf8');
  } catch {
    console.error(`Не найден источник: ${src}`);
    process.exit(2);
  }
  const dst = resolve(VAULT, name);
  writeFileSync(dst, header(from) + text, 'utf8');
  console.log(`Сниппет обновлён: ${dst}`);
}
