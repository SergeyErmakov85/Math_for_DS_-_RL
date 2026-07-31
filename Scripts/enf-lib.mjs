/**
 * enf-lib.mjs — общие функции проверок ENF.
 *
 * Здесь живёт всё, что нужно больше чем одному скрипту: обход файлов,
 * разбор фронтматтера, вырезание блоков кода, формат отчёта.
 */

import { readdirSync, statSync, readFileSync } from 'node:fs';
import { join, extname, relative, sep } from 'node:path';

/**
 * Чтение файла с нормализацией переводов строк.
 *
 * Все проверки обязаны читать файлы только через эту функцию. В рабочем
 * каталоге на Windows переводы строк смешанные, а в регулярных выражениях
 * JavaScript точка не совпадает с \r: строка «discipline: meta\r» не
 * распозналась бы как поле, а «```markdown\r» — как ограждение блока кода.
 * Ошибка при этом выглядит как отсутствующее поле, а не как проблема
 * с кодировкой, и ищется долго.
 */
export function readText(file) {
  return readFileSync(file, 'utf8').replace(/\r\n?/g, '\n');
}

/** Каталоги, которые не проверяются никогда. */
export const IGNORED_DIRS = new Set([
  '.git', 'node_modules', 'out', 'build-output', '.obsidian', '.trash', '.vscode', '.idea',
]);

/**
 * Файлы-шаблоны: в них служебные комментарии, заглушки и синтаксис Templater
 * (`<% … %>`) — норма, а не нарушение.
 */
export function isTemplate(path) {
  const p = path.split(sep).join('/');
  if (p.includes('/Vault/_templates/')) return true;
  return p.includes('/Templates/') && !p.includes('/Templates/examples/');
}

/** Рекурсивный обход с фильтром по расширению. */
export function walk(root, exts = ['.md']) {
  const out = [];
  const visit = (dir) => {
    let entries;
    try {
      entries = readdirSync(dir);
    } catch {
      return;
    }
    for (const name of entries) {
      if (IGNORED_DIRS.has(name)) continue;
      const full = join(dir, name);
      let st;
      try {
        st = statSync(full);
      } catch {
        continue;
      }
      if (st.isDirectory()) visit(full);
      else if (exts.includes(extname(name).toLowerCase())) out.push(full);
    }
  };
  const st = statSync(root);
  if (st.isDirectory()) visit(root);
  else if (exts.includes(extname(root).toLowerCase())) out.push(root);
  return out;
}

/**
 * Разбор фронтматтера. Намеренно минимальный: поддерживаются скаляры,
 * плоские списки в квадратных скобках и списки дефисами. Полный YAML
 * не нужен, а зависимость ради него — лишняя.
 */
export function parseFrontmatter(text) {
  if (!text.startsWith('---')) return { data: null, body: text, endLine: 0 };
  const end = text.indexOf('\n---', 3);
  if (end === -1) return { data: null, body: text, endLine: 0 };

  const raw = text.slice(4, end);
  const body = text.slice(text.indexOf('\n', end + 1) + 1);
  const data = {};
  let currentKey = null;

  for (const line of raw.split('\n')) {
    if (!line.trim() || line.trim().startsWith('#')) continue;

    const item = line.match(/^\s+-\s+(.*)$/);
    if (item && currentKey) {
      if (!Array.isArray(data[currentKey])) data[currentKey] = [];
      data[currentKey].push(unquote(item[1].trim()));
      continue;
    }

    const kv = line.match(/^([A-Za-z_][\w-]*)\s*:\s*(.*)$/);
    if (!kv) continue;
    const [, key, valRaw] = kv;
    currentKey = key;
    const val = valRaw.trim();

    if (val === '') data[key] = null;
    else if (val.startsWith('[') && val.endsWith(']')) {
      const inner = val.slice(1, -1).trim();
      data[key] = inner ? inner.split(',').map((s) => unquote(s.trim())) : [];
    } else data[key] = unquote(val);
  }

  return { data, body, endLine: raw.split('\n').length + 2 };
}

const unquote = (s) => s.replace(/^["'](.*)["']$/, '$1');

/**
 * Разбор ограждённых блоков кода.
 *
 * Реализован конечным автоматом, а не регулярным выражением: во фреймворке
 * сплошь встречаются вложенные ограждения — блок ````markdown, внутри
 * которого показан ```mermaid. Регулярное выражение закрывает внешний блок
 * на первом же внутреннем ограждении и разъезжается на всём остальном файле.
 *
 * Возвращает список блоков: номер строки открытия, информационная строка,
 * смещения начала и конца.
 */
export function findCodeFences(text) {
  const lines = text.split('\n');
  const blocks = [];
  let open = null;
  let offset = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    /* Возврат каретки снимается перед разбором: в рабочем каталоге на Windows
       переводы строк смешанные, а в JS точка не совпадает с \r, из-за чего
       строка «```markdown\r» перестала бы распознаваться как ограждение.
       Смещения при этом считаются по исходной длине строки. */
    const m = line.replace(/\r$/, '').match(/^([ \t]*)(`{3,}|~{3,})(.*)$/);

    if (m) {
      const [, indent, fence, info] = m;
      const char = fence[0];

      if (!open) {
        open = {
          line: i + 1, indent, char, len: fence.length,
          info: info.trim(), start: offset, contentStart: offset + line.length + 1,
        };
      } else if (char === open.char && fence.length >= open.len && info.trim() === '') {
        blocks.push({ ...open, end: offset + line.length, contentEnd: offset });
        open = null;
      }
    }

    offset += line.length + 1;
  }

  if (open) blocks.push({ ...open, end: text.length, contentEnd: text.length, unterminated: true });
  return blocks;
}

/**
 * Замена содержимого блоков кода и строчного кода пробелами с сохранением
 * длины и номеров строк. Нужно всюду, где проверка не должна срабатывать
 * на примерах: в главах Style Guide блоки кода намеренно содержат образцы
 * того, как делать не следует.
 */
export function maskCodeBlocks(text) {
  /* Массив строится через split(''), а не через [...text]: смещения блоков
     считаются в кодовых единицах UTF-16, как и String.length. Разбор по
     кодовым точкам рассинхронизировал бы индексы на любом символе вне
     базовой плоскости — например, на эмодзи в пометках сложности задач. */
  const chars = text.split('');
  for (const b of findCodeFences(text)) {
    for (let i = b.start; i < b.end && i < chars.length; i++) {
      if (chars[i] !== '\n') chars[i] = ' ';
    }
  }
  return chars.join('').replace(/`[^`\n]*`/g, (m) => ' '.repeat(m.length));
}

/** Строка по смещению в тексте — для указания места нарушения. */
export function lineOf(text, index) {
  return text.slice(0, index).split('\n').length;
}

/* ---------- отчёт ---------- */

export class Report {
  constructor(name, root) {
    this.name = name;
    this.root = root;
    this.errors = [];
    this.warnings = [];
  }

  error(file, line, rule, message) {
    this.errors.push({ file: this.rel(file), line, rule, message });
  }

  warn(file, line, rule, message) {
    this.warnings.push({ file: this.rel(file), line, rule, message });
  }

  rel(file) {
    try {
      return relative(this.root, file).split(sep).join('/') || file;
    } catch {
      return file;
    }
  }

  print() {
    const line = (e, mark) =>
      `  ${mark} ${e.file}:${e.line}  [${e.rule}] ${e.message}`;

    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log(`${this.name.padEnd(24)} OK`);
      return 0;
    }

    console.log(`${this.name.padEnd(24)} ${this.errors.length} нарушений, ${this.warnings.length} предупреждений`);
    for (const e of this.errors) console.log(line(e, '·'));
    for (const w of this.warnings) console.log(line(w, '~'));
    return this.errors.length ? 1 : 0;
  }
}

/** Разбор аргументов: пути для проверки, по умолчанию текущий каталог. */
export function targetsFromArgv(argv) {
  const paths = argv.slice(2).filter((a) => !a.startsWith('-'));
  return paths.length ? paths : ['.'];
}
