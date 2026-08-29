# -*- coding: utf-8 -*-
"""
Further split proof/solution numbered steps into finer-grained steps.
This pass splits on:
  - Chinese period '。' (outside backticks)
  - Chinese comma/semicolon '，' '；' (outside backticks)
  - Logical connectors (因此/所以/于是/从而/故/因而/则/即...) outside backticks

Targets:
  - **证明（逐行）** ... **例题**
  - **解题（逐行）** ... (to end of theorem block)
"""

from __future__ import annotations

import re
from pathlib import Path


MD_PATH = Path(r"D:\spot\K6\tongji-calculus-notes.md")

PROOF_MARK = "**证明（逐行）**"
EX_MARK = "**例题**"
SOL_MARK = "**解题（逐行）**"

# Order matters: longer first to avoid partial matches.
CONNECTORS = [
    "因此可得",
    "因此得到",
    "从而可得",
    "从而得到",
    "于是可得",
    "于是得到",
    "因此有",
    "从而有",
    "于是有",
    "故有",
    "可得",
    "因此",
    "所以",
    "于是",
    "从而",
    "因而",
    "故",
    "则",
    "即",
]


def ensure_period(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    if s.endswith(("。", "；", "：", "？", "！")):
        return s
    return s + "。"


def split_by_char_outside_backticks(s: str, ch: str) -> list[str]:
    segs: list[str] = []
    buf: list[str] = []
    in_code = False
    for c in s:
        if c == "`":
            in_code = not in_code
            buf.append(c)
            continue
        if not in_code and c == ch:
            seg = "".join(buf).strip()
            if seg:
                segs.append(seg)
            buf = []
            continue
        buf.append(c)
    last = "".join(buf).strip()
    if last:
        segs.append(last)
    return segs


def split_outside_backticks_by_chars(s: str, chars: set[str]) -> list[str]:
    segs: list[str] = []
    buf: list[str] = []
    in_code = False
    for c in s:
        if c == "`":
            in_code = not in_code
            buf.append(c)
            continue
        if not in_code and c in chars:
            seg = "".join(buf).strip()
            if seg:
                segs.append(seg)
            buf = []
            continue
        buf.append(c)
    last = "".join(buf).strip()
    if last:
        segs.append(last)
    return segs


def find_connector_pos(s: str) -> tuple[int, str] | None:
    in_code = False
    i = 0
    while i < len(s):
        if s[i] == "`":
            in_code = not in_code
            i += 1
            continue
        if not in_code:
            for conn in CONNECTORS:
                if s.startswith(conn, i):
                    return i, conn
        i += 1
    return None


def split_by_connectors(s: str) -> list[str]:
    parts = [s]
    changed = True
    while changed:
        changed = False
        new_parts: list[str] = []
        for seg in parts:
            pos = find_connector_pos(seg)
            if pos is None:
                new_parts.append(seg)
                continue
            idx, conn = pos
            # only split if connector is not at start or end
            if idx == 0 or idx + len(conn) >= len(seg):
                new_parts.append(seg)
                continue
            left = seg[:idx].strip()
            right = seg[idx:].strip()
            if left and right:
                new_parts.append(left)
                new_parts.append(right)
                changed = True
            else:
                new_parts.append(seg)
        parts = new_parts
    return parts


def expand_numbered_line(line: str) -> list[str]:
    m = re.match(r"^\d+\.\s*(.*)$", line)
    if not m:
        return [line]
    content = m.group(1).strip()
    if not content:
        return []

    # 1) split by Chinese period first (outside backticks)
    segs = split_by_char_outside_backticks(content, "。")

    # 2) split each by comma/semicolon
    fine: list[str] = []
    for seg in segs:
        fine.extend(split_outside_backticks_by_chars(seg, {"，", "；"}))

    # 3) split by logical connectors
    refined: list[str] = []
    for seg in fine:
        refined.extend(split_by_connectors(seg))

    refined = [ensure_period(s) for s in refined if s.strip()]
    return refined


def rewrite_proof_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    step = 1
    for line in lines:
        if not line.strip():
            continue
        if re.match(r"^\d+\.\s*", line):
            parts = expand_numbered_line(line)
            for p in parts:
                out.append(f"{step}. {p}")
                step += 1
        else:
            out.append(line)
    return out


def rewrite_solution_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    step = 1
    for line in lines:
        if not line.strip():
            continue
        if re.match(r"^例题\d+解：", line):
            out.append(line)
            step = 1
            continue
        if re.match(r"^\d+\.\s*", line):
            parts = expand_numbered_line(line)
            for p in parts:
                out.append(f"{step}. {p}")
                step += 1
        else:
            out.append(line)
    return out


def process_block(block: list[str]) -> list[str]:
    if PROOF_MARK in block and EX_MARK in block:
        p = block.index(PROOF_MARK)
        e = block.index(EX_MARK)
        proof_lines = block[p + 1 : e]
        new_proof = rewrite_proof_lines(proof_lines)
        block = block[: p + 1] + new_proof + block[e:]

    if SOL_MARK in block:
        s = block.index(SOL_MARK)
        sol_lines = block[s + 1 :]
        new_sol = rewrite_solution_lines(sol_lines)
        block = block[: s + 1] + new_sol
    return block


def main() -> None:
    lines = MD_PATH.read_text(encoding="utf-8").splitlines()
    thm_re = re.compile(r"^### 定理(\d+-\d+)")
    starts = [i for i, l in enumerate(lines) if thm_re.match(l)]
    start_set = set(starts)
    idx_to_id = {i: thm_re.match(lines[i]).group(1) for i in starts}  # type: ignore[union-attr]

    out: list[str] = []
    i = 0
    while i < len(lines):
        if i in start_set:
            _ = idx_to_id[i]
            j = i + 1
            while j < len(lines) and j not in start_set:
                j += 1
            block = lines[i:j]
            block = process_block(block)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("refined blocks:", len(starts))


if __name__ == "__main__":
    main()
