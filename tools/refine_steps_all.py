# -*- coding: utf-8 -*-
"""
Further refine proof/solution steps by splitting long lines into smaller,
formula-level steps across the whole merged notes file.

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

CONNECTORS = {
    "则",
    "故",
    "因此",
    "所以",
    "于是",
    "从而",
    "因而",
    "故而",
    "并且",
    "并",
    "且",
    "同时",
    "即",
    "因此：",
    "所以：",
    "于是：",
    "从而：",
    "故：",
}


def ensure_period(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    if s.endswith(("。", "；", "：", "？", "！")):
        return s
    return s + "。"


def split_outside_backticks(s: str) -> list[str]:
    segs: list[str] = []
    buf: list[str] = []
    in_code = False
    for ch in s:
        if ch == "`":
            in_code = not in_code
            buf.append(ch)
            continue
        if not in_code and ch in ("，", "；"):
            seg = "".join(buf).strip()
            if seg:
                segs.append(seg)
            buf = []
            continue
        buf.append(ch)
    last = "".join(buf).strip()
    if last:
        segs.append(last)
    return segs


def merge_connectors(segs: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(segs):
        seg = segs[i].strip()
        if seg in CONNECTORS and i + 1 < len(segs):
            merged = seg + segs[i + 1].strip()
            out.append(merged)
            i += 2
            continue
        out.append(seg)
        i += 1
    return out


def expand_numbered_line(line: str) -> list[str]:
    m = re.match(r"^\d+\.\s*(.*)$", line)
    if not m:
        return [line]
    content = m.group(1).strip()
    if not content:
        return []
    parts = split_outside_backticks(content)
    parts = merge_connectors(parts)
    parts = [ensure_period(p) for p in parts if p.strip()]
    return parts


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
            # preserve non-numbered lines (rare)
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
    # proof
    if PROOF_MARK in block and EX_MARK in block:
        p = block.index(PROOF_MARK)
        e = block.index(EX_MARK)
        proof_lines = block[p + 1 : e]
        new_proof = rewrite_proof_lines(proof_lines)
        block = block[: p + 1] + new_proof + block[e:]

    # solution
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
            tid = idx_to_id[i]
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
