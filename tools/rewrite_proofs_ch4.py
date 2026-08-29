# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 4 theorems (4-1 .. 4-4) in
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
    "4-1": [
        "设 `f` 在区间 `I` 上连续，取固定点 `x0∈I`",
        "定义 `F(x)=∫_{x0}^{x} f(t) dt`",
        "取 `h→0`，差商 ` [F(x+h)-F(x)]/h = (1/h)∫_{x}^{x+h} f(t) dt`",
        "由积分中值定理，存在 `ξ` 介于 `x` 与 `x+h` 使 `∫_{x}^{x+h} f(t) dt = f(ξ)h`",
        "故差商等于 `f(ξ)`",
        "当 `h→0` 时 `ξ→x`，由连续性 `f(ξ)→f(x)`",
        "因此 `F'(x)=f(x)`，即 `F` 为 `f` 的原函数",
    ],
    "4-2": [
        "设 `u=φ(x)` 可导，且 `F' = f`",
        "由链式法则，`d/dx [F(φ(x))]=F'(φ(x))·φ'(x)=f(φ(x))·φ'(x)`",
        "因此 `f(φ(x))·φ'(x)` 是 `F(φ(x))` 的导数",
        "两边积分得 `∫ f(φ(x))·φ'(x) dx = F(φ(x)) + C`",
        "若记 `u=φ(x)`，则右端即 `∫ f(u) du`",
    ],
    "4-3": [
        "由乘积法则：`(u v)' = u'v + u v'`",
        "两边积分：`∫ (u v)' dx = ∫ u'v dx + ∫ u v' dx`",
        "由基本定理，左端为 `uv + C`",
        "移项：`∫ u v' dx = uv + C - ∫ u' v dx`",
        "将常数并入积分常数，得 `∫ u v' dx = u v - ∫ u' v dx`",
    ],
    "4-4": [
        "设有理函数 `R(x)=P(x)/Q(x)`，先做多项式除法",
        "得 `R(x)=S(x)+R0(x)/Q(x)`，其中 `deg R0 < deg Q`",
        "故仅需分解真分式 `R0/Q`",
        "将 `Q(x)` 分解为实因子：`Q=∏(x-a_i)^{k_i}·∏(x^2+b_j x+c_j)^{m_j}`",
        "设部分分式形式：`∑_{i,r} A_{ir}/(x-a_i)^r + ∑_{j,r} (B_{jr}x+C_{jr})/(x^2+b_j x+c_j)^r`",
        "两边同乘 `Q(x)` 得到多项式恒等式",
        "比较同次幂系数，得到线性方程组",
        "该方程组解存在且唯一，故分解存在且唯一",
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
            if tid.startswith("4-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter4 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("4-")))


if __name__ == "__main__":
    main()
