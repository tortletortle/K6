# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 5 theorems (5-1 .. 5-5) in
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
    "5-1": [
        "设 `f` 在 `[a,b]` 有界，记上和 `U(P)`、下和 `L(P)`",
        "定义上积分 `I^* = inf_P U(P)`，下积分 `I_* = sup_P L(P)`",
        "若 `f` 可积，则 `I^* = I_* =: I`",
        "给定 `ε>0`，取分划 `P1,P2` 使 `U(P1)<I+ε/2` 且 `L(P2)>I-ε/2`",
        "取共同细化 `P=P1∪P2`，有 `U(P)≤U(P1)` 且 `L(P)≥L(P2)`",
        "于是 `U(P)-L(P) < ε`",
        "反之，若对任意 `ε>0` 存在 `P` 使 `U(P)-L(P)<ε`",
        "则 `I^* - I_* ≤ U(P)-L(P) < ε`",
        "令 `ε→0` 得 `I^* = I_*`，故 `f` Riemann 可积",
    ],
    "5-2": [
        "设 `f` 在 `[a,b]` 连续，则 `f` 一致连续",
        "给定 `ε>0`，存在 `δ>0` 使 `|x-y|<δ ⇒ |f(x)-f(y)|<ε/(b-a)`",
        "取分划 `P` 使网格 `||P||<δ`",
        "对任意小区间 `[x_{i-1},x_i]`，有振幅 `ω_i < ε/(b-a)`",
        "故 `U(P)-L(P)=∑ ω_i Δx_i < (ε/(b-a))·∑ Δx_i = ε`",
        "由可积判别知 `f` 可积",
    ],
    "5-3": [
        "设 `f` 在 `[a,b]` 连续，记 `m=min f`，`M=max f`",
        "则对任意 `x∈[a,b]` 有 `m ≤ f(x) ≤ M`",
        "两边积分得 `m(b-a) ≤ ∫_a^b f(x)dx ≤ M(b-a)`",
        "令 `A = (1/(b-a))∫_a^b f(x)dx`，则 `m ≤ A ≤ M`",
        "由连续性与介值性，存在 `ξ∈[a,b]` 使 `f(ξ)=A`",
        "于是 `∫_a^b f(x)dx = f(ξ)(b-a)`",
    ],
    "5-4": [
        "设 `F(x)=∫_a^x f(t)dt`，且 `f` 在 `[a,b]` 连续",
        "对 `h→0`，差商 ` [F(x+h)-F(x)]/h = (1/h)∫_x^{x+h} f(t)dt`",
        "由积分中值定理，存在 `ξ` 介于 `x` 与 `x+h` 使 `∫_x^{x+h} f(t)dt=f(ξ)h`",
        "故差商等于 `f(ξ)`",
        "当 `h→0` 时 `ξ→x`，由连续性得 `f(ξ)→f(x)`",
        "因此 `F'(x)=f(x)`",
    ],
    "5-5": [
        "设 `F' = f` 于 `[a,b]`，令 `G(x)=∫_a^x f(t)dt`",
        "由变上限积分求导，`G'(x)=f(x)`",
        "于是 `(F-G)'=0`，故 `F(x)-G(x)=C` 为常数",
        "取 `x=a` 得 `C=F(a)-G(a)=F(a)`",
        "故 `F(b)-G(b)=F(a)`，即 `G(b)=F(b)-F(a)`",
        "从而 `∫_a^b f(x)dx = F(b)-F(a)`",
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
            if tid.startswith("5-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter5 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("5-")))


if __name__ == "__main__":
    main()
