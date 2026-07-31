#!/usr/bin/env node
/**
 * gen-obsidian-css.mjs — генерирует CSS-сниппет токенов для хранилища Obsidian.
 *
 * Зачем это нужно. Obsidian не умеет подключать CSS из-за пределов хранилища:
 * @import на файл вне vault не работает. Значит, значения цветов обязаны
 * физически лежать внутри хранилища. Копировать их руками нельзя — это
 * нарушило бы ENF-COLOR-001 (единый источник истины), поэтому копия
 * порождается скриптом и помечена как порождённая.
 *
 * Источник: Build/css/enf-tokens.css
 * Результат: Obsidian/Vault/.obsidian/snippets/enf-tokens.css
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(HERE, '..', 'Build', 'css', 'enf-tokens.css');
const DST = resolve(HERE, '..', 'Obsidian', 'Vault', '.obsidian', 'snippets', 'enf-tokens.css');

let src;
try {
  src = readFileSync(SRC, 'utf8');
} catch {
  console.error(`Не найден источник токенов: ${SRC}`);
  process.exit(2);
}

const header = `/* =============================================================
   ПОРОЖДЁННЫЙ ФАЙЛ — НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ.

   Источник: Build/css/enf-tokens.css
   Генератор: Scripts/gen-obsidian-css.mjs
   Пересоздать: node Scripts/gen-obsidian-css.mjs

   Правки, внесённые сюда напрямую, будут потеряны при следующей
   генерации. Меняйте значения в источнике — там же лежит и
   обоснование выбора цветов.
   ============================================================= */

`;

writeFileSync(DST, header + src, 'utf8');
console.log(`Сниппет обновлён: ${DST}`);
