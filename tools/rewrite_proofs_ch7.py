# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 7 theorems (7-1 .. 7-3) in
D:\\spot\\K6\\tongji-calculus-notes.md to a more formula-level, step-by-step style.
"""

from __future__ import annotations

import re
from pathlib import Path


MD_PATH = Path(r"D:\spot\K6\tongji-calculus-notes.md")

PROOF_MARK = "**证明（逐行）**"
EX_MARK = "**例题**"


def ensure_period(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    if s.endswith(("。", "；", "：", "？", "！")):
        return s
    return s + "。"


PROOFS: dict[str, list[str]] = {
    "7-1": [
        "设方程 `y' = g(x)h(y)`，且 `h(y)≠0`",
        "将变量分离：`dy/h(y) = g(x) dx`",
        "两边积分：`∫ dy/h(y) = ∫ g(x) dx + C`",
        "若记 `H(y)=∫ dy/h(y)` 与 `G(x)=∫ g(x) dx`，则 `H(y)=G(x)+C`",
        "对该隐式关系两边求导可回到 `y'=g(x)h(y)`",
        "因此分离变量积分式给出方程的通解",
    ],
    "7-2": [
        "设一阶线性方程 `y' + p(x)y = q(x)`",
        "取积分因子 `μ(x)=exp(∫ p(x)dx)`",
        "则 `μ'(x)=p(x)μ(x)`",
        "将原方程乘以 `μ`：`μ y' + μ p y = μ q`",
        "左端为 ` (μ y)'`，故 ` (μ y)' = μ q`",
        "积分得 `μ(x) y(x) = ∫ μ(x) q(x) dx + C`",
        "于是 `y(x)= μ(x)^{-1} (∫ μ q dx + C)`",
    ],
    "7-3": [
        "设二阶齐次线性方程 `y''+p(x)y'+q(x)y=0`",
        "若 `y1,y2` 为两解，则对任意常数 `C1,C2`，`C1 y1 + C2 y2` 仍为解（线性叠加）",
        "若 `y1,y2` 线性无关，记 Wronskian `W=y1 y2' - y1' y2`，则 `W(x0)≠0`",
        "给定任意初值 `y(x0)=A`、`y'(x0)=B`，解系数方程组",
        "`C1 y1(x0)+C2 y2(x0)=A`，`C1 y1'(x0)+C2 y2'(x0)=B`",
        "因 `W(x0)≠0`，该线性方程组有唯一解 `C1,C2`",
        "由初值问题解的唯一性，任意解必与该线性组合一致",
        "故通解为 `y=C1 y1 + C2 y2`",
    ],
}


def rewrite_proof_block(block: list[str], tid: str) -> list[str]:
    if tid not in PROOFS:
        return block

    try:
        p = block.index(PROOF_MARK)
        e = block.index(EX_MARK)
    except ValueError:
        return block

    head = block[: p + 1]
    tail = block[e:]

    steps = [ensure_period(s) for s in PROOFS[tid] if s.strip()]
    proof_lines = [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    return head + proof_lines + tail


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
            if tid.startswith("7-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter7 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("7-")))


if __name__ == "__main__":
    main()
