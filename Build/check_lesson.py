#!/usr/bin/env python3
"""Автопроверка учебного .md-файла с кодом на Python.

Что делает:
  1. Находит все огороженные блоки кода (``` и ~~~), в том числе внутри
     выносок Obsidian (строки, начинающиеся с «>»).
  2. Выполняет блоки ```python сверху вниз в общем пространстве имён —
     так, как их выполнит ученик. Блоки внутри выносок (решения,
     типичные ошибки) выполняются в копии пространства имён и не меняют
     основной поток.
  3. Сверяет напечатанное с блоком ```output, который идёт сразу за кодом.
     Если код падает с исключением, последней строкой фактического вывода
     считается «ТипОшибки: сообщение».
  4. Проверяет оформление: тег языка у каждого блока, длину строк,
     табуляции, приглашения «>>>», не-ASCII имена, устаревшие API.

Запуск:
  python check_lesson.py lesson.md            # проверка с выполнением кода
  python check_lesson.py lesson.md --no-exec  # только оформление

Код из файла выполняется на вашем компьютере: запускайте проверку
только для своих материалов.
"""
from __future__ import annotations

import argparse
import contextlib
import difflib
import io
import os
import re
import sys
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

MAX_CODE_LINE = 79      # PEP 8: строки кода
MAX_COMMENT_LINE = 72   # PEP 8: комментарии и докстринги
MAX_BLOCK_LINES = 25    # мягкий предел длины одного блока
ALLOWED_TAGS = {
    "python", "output", "bash", "text", "diff",
    "yaml", "toml", "json", "markdown", "mermaid",
}
DEPRECATED = [
    (re.compile(r"\bnp\.random\.seed\("),
     "np.random.seed(...) → rng = np.random.default_rng(seed)"),
    (re.compile(r"^\s*import\s+gym\b|^\s*from\s+gym\b"),
     "gym устарел → gymnasium (reset/step с terminated и truncated)"),
    (re.compile(r"\bnp\.(float|int|bool|object)\b(?!\d|_)"),
     "псевдонимы np.float/np.int удалены из NumPy → float, int"),
]
WILDCARD = {"...", "…"}

FENCE_RE = re.compile(
    r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})(?P<info>.*)$"
)
QUOTE_RE = re.compile(r"^ {0,3}((?:>[ ]?)+)")


@dataclass
class Block:
    lang: str
    info: str
    start: int                  # номер строки открывающего ограждения
    depth: int                  # вложенность выносок, 0 — основной поток
    lines: list[str] = field(default_factory=list)
    gap_before: bool = True     # есть ли текст между этим и предыдущим блоком

    @property
    def code(self) -> str:
        return "\n".join(self.lines) + "\n"


@dataclass
class Report:
    errors: list[tuple[int, str]] = field(default_factory=list)
    warnings: list[tuple[int, str]] = field(default_factory=list)
    ok: list[tuple[int, str]] = field(default_factory=list)

    def error(self, line: int, msg: str) -> None:
        self.errors.append((line, msg))

    def warn(self, line: int, msg: str) -> None:
        self.warnings.append((line, msg))

    def success(self, line: int, msg: str) -> None:
        self.ok.append((line, msg))

    @staticmethod
    def lines(items: list[tuple[int, str]]) -> list[str]:
        return [f"  строка {no}: {msg}" for no, msg in sorted(items)]


def split_quote(line: str) -> tuple[int, str]:
    """Возвращает (глубина цитаты, строка без маркеров «>»)."""
    m = QUOTE_RE.match(line)
    if not m:
        return 0, line
    return m.group(1).count(">"), line[m.end():]


def strip_levels(line: str, levels: int) -> str | None:
    """Снимает ровно `levels` маркеров «>»; None, если маркеров меньше."""
    for _ in range(levels):
        m = re.match(r"^ {0,3}>[ ]?", line)
        if not m:
            return None
        line = line[m.end():]
    return line


def parse_blocks(text: str) -> list[Block]:
    blocks: list[Block] = []
    current: Block | None = None
    fence = ""
    had_text = True             # был ли текст после предыдущего блока
    for no, raw in enumerate(text.splitlines(), start=1):
        if current is not None:
            inner = strip_levels(raw, current.depth)
            if inner is not None:
                if re.match(rf"^ {{0,3}}{re.escape(fence[0])}"
                            rf"{{{len(fence)},}}\s*$", inner):
                    blocks.append(current)  # закрывающее ограждение
                    current = None
                    had_text = False
                else:
                    current.lines.append(inner)
                continue
            blocks.append(current)          # выноска закончилась раньше блока
            current = None
            had_text = False
        depth, line = split_quote(raw)
        m = FENCE_RE.match(line)
        if m:
            fence = m.group("fence")
            info = m.group("info").strip()
            lang = info.split()[0].lower() if info else ""
            current = Block(lang=lang, info=info, start=no, depth=depth,
                            gap_before=had_text)
            continue
        if line.strip():
            had_text = True
    if current is not None:
        blocks.append(current)
    return blocks


def lint_block(b: Block, rep: Report) -> None:
    if not b.info:
        rep.error(b.start, "у блока нет тега языка (```python, ```output …)")
        return
    if b.info.startswith("{") or len(b.info.split()) > 1:
        rep.error(b.start, f"в строке-ограждении лишнее: «{b.info}» — "
                           "допустим только тег языка")
    elif b.lang not in ALLOWED_TAGS:
        rep.warn(b.start, f"нестандартный тег «{b.lang}»")
    if b.lang == "output" and not any(s.strip() for s in b.lines):
        rep.error(b.start, "пустой блок output")
    if b.lang != "python":
        return
    body = [s for s in b.lines if s.strip()]
    if len(body) > MAX_BLOCK_LINES:
        rep.warn(b.start, f"блок из {len(body)} строк — разбейте на шаги "
                          f"(предел {MAX_BLOCK_LINES})")
    for off, s in enumerate(b.lines, start=1):
        where = b.start + off
        if "\t" in s:
            rep.error(where, "табуляция — используйте 4 пробела")
        if s.lstrip().startswith(">>>"):
            rep.error(where, "приглашение «>>>» ломает копирование кода")
        is_comment = s.lstrip().startswith("#")
        limit = MAX_COMMENT_LINE if is_comment else MAX_CODE_LINE
        if len(s) > limit:
            rep.warn(where, f"строка длиннее {limit} символов ({len(s)})")
        for rx, hint in DEPRECATED:
            if rx.search(s):
                rep.warn(where, f"устаревший API: {hint}")
    try:
        toks = tokenize.generate_tokens(io.StringIO(b.code).readline)
        for tok in toks:
            if tok.type == tokenize.NAME and not tok.string.isascii():
                rep.warn(b.start + tok.start[0],
                         f"не-ASCII имя «{tok.string}» — его трудно набрать")
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass  # синтаксис проверит выполнение


def run_code(code: str, env: dict, label: str) -> tuple[list[str], str | None]:
    buf = io.StringIO()
    exc_line = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(compile(code, label, "exec"), env)
        except Exception as exc:  # noqa: BLE001 — ошибка и есть результат
            exc_line = f"{type(exc).__name__}: {exc}"
    lines = buf.getvalue().splitlines()
    if exc_line:
        lines.append(exc_line)
    return [s.rstrip() for s in lines], exc_line


def normalize(lines: list[str]) -> list[str]:
    out = [s.rstrip() for s in lines]
    while out and not out[-1]:
        out.pop()
    while out and not out[0]:
        out.pop(0)
    return out


def matches(expected: list[str], actual: list[str]) -> bool:
    if not any(s.strip() in WILDCARD for s in expected):
        return expected == actual
    chunks: list[list[str]] = [[]]
    for s in expected:
        if s.strip() in WILDCARD:
            chunks.append([])
        else:
            chunks[-1].append(s)
    head, tail = chunks[0], chunks[-1]
    if actual[:len(head)] != head:
        return False
    end = len(actual) - len(tail)
    if tail and actual[end:] != tail:
        return False
    pos = len(head)
    for chunk in chunks[1:-1]:
        for i in range(pos, end - len(chunk) + 1):
            if actual[i:i + len(chunk)] == chunk:
                pos = i + len(chunk)
                break
        else:
            return False
    return pos <= end


def check(path: Path, execute: bool) -> Report:
    rep = Report()
    blocks = parse_blocks(path.read_text(encoding="utf-8"))
    for b in blocks:
        lint_block(b, rep)
    if not execute:
        return rep

    os.environ.setdefault("MPLBACKEND", "Agg")
    try:
        import matplotlib.pyplot as plt
        plt.show = lambda *a, **k: None
    except ImportError:
        pass

    main_env: dict = {"__name__": "__lesson__"}
    old_cwd = Path.cwd()
    os.chdir(path.parent)
    try:
        for i, b in enumerate(blocks):
            if b.lang != "python":
                if b.lang == "output" and (
                    i == 0 or blocks[i - 1].lang != "python"
                    or b.gap_before or blocks[i - 1].depth != b.depth
                ):
                    rep.error(b.start, "блок output не прикреплён к коду: "
                                       "он должен идти сразу за ```python")
                continue
            env = main_env if b.depth == 0 else dict(main_env)
            actual, exc = run_code(b.code, env, f"<{path.name}:{b.start}>")
            nxt = blocks[i + 1] if i + 1 < len(blocks) else None
            has_out = (nxt is not None and nxt.lang == "output"
                       and not nxt.gap_before and nxt.depth == b.depth)
            if not has_out:
                if exc:
                    rep.error(b.start, f"код падает: {exc}")
                elif actual:
                    rep.warn(b.start, "код печатает, но блока output нет")
                else:
                    rep.success(b.start, "выполнено")
                continue
            expected = normalize(nxt.lines)
            actual = normalize(actual)
            if matches(expected, actual):
                rep.success(b.start, "вывод совпадает")
            else:
                diff = "\n".join(
                    "      " + d for d in difflib.unified_diff(
                        expected, actual, "в файле", "фактически", lineterm="")
                )
                rep.error(nxt.start, f"вывод не совпадает:\n{diff}")
    finally:
        os.chdir(old_cwd)
    return rep


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("lesson", type=Path, help="путь к .md-файлу")
    parser.add_argument("--no-exec", action="store_true",
                        help="не выполнять код, проверить только оформление")
    args = parser.parse_args()

    rep = check(args.lesson.resolve(), execute=not args.no_exec)
    print(f"Проверка: {args.lesson}")
    for title, items in (("✓ Успешно", rep.ok),
                         ("⚠ Предупреждения", rep.warnings),
                         ("✗ Ошибки", rep.errors)):
        if items:
            print(f"\n{title} ({len(items)}):", *rep.lines(items), sep="\n")
    print("\nИтог:", "есть ошибки" if rep.errors else "замечаний, мешающих "
          "публикации, нет")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
