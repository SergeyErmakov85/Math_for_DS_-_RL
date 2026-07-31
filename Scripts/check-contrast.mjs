#!/usr/bin/env node
/**
 * check-contrast.mjs — проверка палитры ENF.
 *
 * Три проверки:
 *   1. Контраст каждого тона к фону своей темы — WCAG 2.1, порог 4.5:1
 *      (обычный текст; формулы набираются основным кеглем).
 *   2. Попарная различимость тонов внутри темы при нормальном зрении.
 *   3. Попарная различимость при дейтеранопии и протанопии — цвета
 *      прогоняются через модель Виено — Брет — Моллона, затем сравниваются
 *      по CIEDE2000.
 *
 * Источник данных — Build/css/enf-tokens.css. Другого источника нет
 * и быть не должно (ENF-COLOR-001).
 *
 * Коды возврата: 0 — нарушений нет, 1 — есть, 2 — ошибка запуска.
 */

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const TOKENS = resolve(HERE, '..', 'Build', 'css', 'enf-tokens.css');

/* Пороги. Меняются только вместе с правилами ENF-COLOR-*.
 *
 * Два уровня по различимости при дальтонизме — это не послабление,
 * а следствие устройства зрения. Дихромат различает светлоту и ось
 * «синее — жёлтое»; пять тонов в это пространство укладываются, шесть
 * и более — уже нет. Отсюда:
 *   · ядро из пяти тонов  → порог CVD 9, обязателен дублирующий
 *     нецветовой признак (ENF-COLOR-010);
 *   · безопасная тройка   → порог CVD 12; только она разрешена в
 *     Publication Mode, где больше трёх цветов и не нужно.
 */
const MIN_CONTRAST_TEXT = 4.5;   // WCAG AA, обычный текст
const MIN_DELTA_NORMAL  = 18;    // CIEDE2000 между тонами, нормальное зрение
const MIN_DELTA_CVD     = 9;     // CIEDE2000 после симуляции дальтонизма, ядро
const MIN_DELTA_CVD_SAFE = 12;   // то же для безопасной тройки
const MAX_NEUTRAL_CHROMA = 14;   // нейтральный тон обязан читаться как серый

/* ---------- разбор CSS ---------- */

function parseBlock(css, selectorRe) {
  const m = css.match(selectorRe);
  if (!m) return null;
  const body = m[1];
  const out = {};
  for (const decl of body.matchAll(/(--enf-[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;/g)) {
    out[decl[1]] = decl[2].toUpperCase();
  }
  return out;
}

function loadThemes() {
  let css;
  try {
    css = readFileSync(TOKENS, 'utf8');
  } catch {
    console.error(`Не найден файл токенов: ${TOKENS}`);
    process.exit(2);
  }
  const light = parseBlock(css, /:root\s*\{([^}]*)\}/);
  const dark = parseBlock(css, /\[data-enf-theme="dark"\][^{]*\{([^}]*)\}/);
  if (!light || !dark) {
    console.error('Не удалось разобрать блоки :root и [data-enf-theme="dark"].');
    process.exit(2);
  }
  return { light, dark };
}

/* ---------- цветовые преобразования ---------- */

const hexToRgb = (hex) => [
  parseInt(hex.slice(1, 3), 16),
  parseInt(hex.slice(3, 5), 16),
  parseInt(hex.slice(5, 7), 16),
];

const srgbToLinear = (c) => {
  const s = c / 255;
  return s <= 0.04045 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
};

const linearToSrgb = (c) => {
  const v = c <= 0.0031308 ? c * 12.92 : 1.055 * c ** (1 / 2.4) - 0.055;
  return Math.min(255, Math.max(0, Math.round(v * 255)));
};

function relativeLuminance(hex) {
  const [r, g, b] = hexToRgb(hex).map(srgbToLinear);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrastRatio(a, b) {
  const la = relativeLuminance(a);
  const lb = relativeLuminance(b);
  const [hi, lo] = la > lb ? [la, lb] : [lb, la];
  return (hi + 0.05) / (lo + 0.05);
}

/* sRGB → CIE XYZ (D65) → CIE Lab */
function hexToXyz(hex) {
  const [r, g, b] = hexToRgb(hex).map(srgbToLinear);
  return [
    r * 0.4124564 + g * 0.3575761 + b * 0.1804375,
    r * 0.2126729 + g * 0.7151522 + b * 0.0721750,
    r * 0.0193339 + g * 0.1191920 + b * 0.9503041,
  ];
}

function xyzToLab([x, y, z]) {
  const wx = 0.95047, wy = 1.0, wz = 1.08883;
  const f = (t) => (t > 216 / 24389 ? Math.cbrt(t) : (841 / 108) * t + 4 / 29);
  const fx = f(x / wx), fy = f(y / wy), fz = f(z / wz);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}

const hexToLab = (hex) => xyzToLab(hexToXyz(hex));

/** CIEDE2000 — воспринимаемое различие двух цветов. */
function deltaE2000(lab1, lab2) {
  const [L1, a1, b1] = lab1;
  const [L2, a2, b2] = lab2;
  const kL = 1, kC = 1, kH = 1;
  const deg = (r) => (r * 180) / Math.PI;
  const rad = (d) => (d * Math.PI) / 180;

  const C1 = Math.hypot(a1, b1);
  const C2 = Math.hypot(a2, b2);
  const Cbar = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Cbar ** 7 / (Cbar ** 7 + 25 ** 7)));
  const a1p = (1 + G) * a1;
  const a2p = (1 + G) * a2;
  const C1p = Math.hypot(a1p, b1);
  const C2p = Math.hypot(a2p, b2);
  let h1p = deg(Math.atan2(b1, a1p)); if (h1p < 0) h1p += 360;
  let h2p = deg(Math.atan2(b2, a2p)); if (h2p < 0) h2p += 360;

  const dLp = L2 - L1;
  const dCp = C2p - C1p;
  let dhp = 0;
  if (C1p * C2p !== 0) {
    dhp = h2p - h1p;
    if (dhp > 180) dhp -= 360;
    else if (dhp < -180) dhp += 360;
  }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(rad(dhp) / 2);

  const Lbp = (L1 + L2) / 2;
  const Cbp = (C1p + C2p) / 2;
  let hbp;
  if (C1p * C2p === 0) hbp = h1p + h2p;
  else if (Math.abs(h1p - h2p) <= 180) hbp = (h1p + h2p) / 2;
  else hbp = h1p + h2p < 360 ? (h1p + h2p + 360) / 2 : (h1p + h2p - 360) / 2;

  const T = 1
    - 0.17 * Math.cos(rad(hbp - 30))
    + 0.24 * Math.cos(rad(2 * hbp))
    + 0.32 * Math.cos(rad(3 * hbp + 6))
    - 0.20 * Math.cos(rad(4 * hbp - 63));

  const dTheta = 30 * Math.exp(-(((hbp - 275) / 25) ** 2));
  const Rc = 2 * Math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7));
  const Sl = 1 + (0.015 * (Lbp - 50) ** 2) / Math.sqrt(20 + (Lbp - 50) ** 2);
  const Sc = 1 + 0.045 * Cbp;
  const Sh = 1 + 0.015 * Cbp * T;
  const Rt = -Math.sin(rad(2 * dTheta)) * Rc;

  return Math.sqrt(
    (dLp / (kL * Sl)) ** 2 +
    (dCp / (kC * Sc)) ** 2 +
    (dHp / (kH * Sh)) ** 2 +
    Rt * (dCp / (kC * Sc)) * (dHp / (kH * Sh))
  );
}

/* ---------- симуляция дальтонизма ----------
   Модель Виено, Брета и Моллона (1999): проекция в пространстве LMS
   на плоскость, доступную дихромату. */

const RGB_TO_LMS = [
  [0.31399022, 0.63951294, 0.04649755],
  [0.15537241, 0.75789446, 0.08670142],
  [0.01775239, 0.10944209, 0.87256922],
];
const LMS_TO_RGB = [
  [ 5.47221206, -4.64196010,  0.16963708],
  [-1.12524190,  2.29317094, -0.16789520],
  [ 0.02980165, -0.19318073,  1.16364789],
];

const mul = (m, v) => m.map((row) => row[0] * v[0] + row[1] * v[1] + row[2] * v[2]);

/** type: 'protan' | 'deutan' */
function simulateCvd(hex, type) {
  const lin = hexToRgb(hex).map(srgbToLinear);
  const [l, m, s] = mul(RGB_TO_LMS, lin);
  let lms;
  if (type === 'protan') {
    lms = [(2.02344 * m) - (2.52581 * s), m, s];
  } else {
    lms = [l, (0.494207 * l) + (1.24827 * s), s];
  }
  const rgb = mul(LMS_TO_RGB, lms).map(linearToSrgb);
  return '#' + rgb.map((c) => c.toString(16).padStart(2, '0').toUpperCase()).join('');
}

/* ---------- проверки ---------- */

/** Пять семантических тонов — полное ядро палитры. */
const CORE_ROLES = ['variable', 'function', 'parameter', 'operator', 'target'];

/** Безопасная тройка «объект — действие — настройка»: различима при
 *  дихроматии с уверенным запасом. Только она разрешена в Publication
 *  Mode, где лимит и так три цвета (ENF-COLOR-021). */
const SAFE_ROLES = ['variable', 'function', 'parameter'];

const problems = [];
const rows = [];

function pairwise(hues, simulate, min, label, theme, group) {
  const labs = hues.map((h) => ({ role: h.role, lab: hexToLab(simulate(h.hex)) }));
  let worst = { d: Infinity, pair: '' };
  const fails = [];
  for (let i = 0; i < labs.length; i++) {
    for (let j = i + 1; j < labs.length; j++) {
      const d = deltaE2000(labs[i].lab, labs[j].lab);
      const pair = `${labs[i].role} ↔ ${labs[j].role}`;
      if (d < worst.d) worst = { d, pair };
      if (d < min) fails.push(`${pair} = ${d.toFixed(1)}`);
    }
  }
  const status = fails.length ? 'FAIL' : 'OK  ';
  console.log(`  ${status} ${group}, ${label}: порог ΔE00 ${min}, худшая пара ${worst.pair} = ${worst.d.toFixed(1)}`);
  for (const f of fails) {
    console.log(`       · ${f}`);
    problems.push(`[${theme}/${group}/${label}] неразличимая пара ${f} (порог ${min})`);
  }
  return worst.d;
}

function checkTheme(name, tokens) {
  const bg = tokens['--enf-bg'];
  const get = (r) => ({ role: r, hex: tokens[`--enf-color-${r}`] });
  const core = CORE_ROLES.map(get);
  const safe = SAFE_ROLES.map(get);

  const missing = [...core, get('neutral')].filter((h) => !h.hex);
  if (missing.length) {
    problems.push(`[${name}] в палитре нет тонов: ${missing.map((m) => m.role).join(', ')}`);
    return;
  }

  console.log(`\n=== Тема: ${name} (фон ${bg}) ===`);

  console.log('Контраст к фону (порог 4.5:1):');
  for (const { role, hex } of [...core, get('neutral')]) {
    const cr = contrastRatio(hex, bg);
    const ok = cr >= MIN_CONTRAST_TEXT;
    rows.push({ theme: name, role, hex, contrast: cr.toFixed(2) });
    console.log(`  ${ok ? 'OK  ' : 'FAIL'} ${role.padEnd(10)} ${hex}  ${cr.toFixed(2)}:1`);
    if (!ok) problems.push(`[${name}] ${role} ${hex}: контраст ${cr.toFixed(2)}:1 < ${MIN_CONTRAST_TEXT}:1`);
  }

  // Нейтральный тон обязан читаться как серый, иначе он вступит
  // в семантическую конкуренцию с ролевыми тонами.
  const nLab = hexToLab(tokens['--enf-color-neutral']);
  const nChroma = Math.hypot(nLab[1], nLab[2]);
  const nOk = nChroma <= MAX_NEUTRAL_CHROMA;
  console.log(`  ${nOk ? 'OK  ' : 'FAIL'} neutral: насыщенность C* = ${nChroma.toFixed(1)} (порог ${MAX_NEUTRAL_CHROMA})`);
  if (!nOk) problems.push(`[${name}] нейтральный тон слишком насыщен: C* = ${nChroma.toFixed(1)}`);

  console.log('Различимость тонов:');
  const id = (h) => h;
  const deu = (h) => simulateCvd(h, 'deutan');
  const pro = (h) => simulateCvd(h, 'protan');

  pairwise(core, id,  MIN_DELTA_NORMAL,   'нормальное зрение', name, 'ядро (5)');
  pairwise(core, deu, MIN_DELTA_CVD,      'дейтеранопия',      name, 'ядро (5)');
  pairwise(core, pro, MIN_DELTA_CVD,      'протанопия',        name, 'ядро (5)');
  pairwise(safe, deu, MIN_DELTA_CVD_SAFE, 'дейтеранопия',      name, 'безопасная (3)');
  pairwise(safe, pro, MIN_DELTA_CVD_SAFE, 'протанопия',        name, 'безопасная (3)');
}

const { light, dark } = loadThemes();
checkTheme('светлая', light);
checkTheme('тёмная', dark);

if (process.argv.includes('--markdown')) {
  console.log('\n--- таблица для документации ---\n');
  console.log('| Тема | Роль | HEX | Контраст к фону |');
  console.log('|------|------|-----|-----------------|');
  for (const r of rows) console.log(`| ${r.theme} | ${r.role} | \`${r.hex}\` | ${r.contrast}:1 |`);
}

console.log('');
if (problems.length) {
  console.log(`Нарушений: ${problems.length}`);
  for (const p of problems) console.log(`  · ${p}`);
  process.exit(1);
}
console.log('Палитра проверена: контраст и различимость в норме.');
process.exit(0);
