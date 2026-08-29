# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 6 theorems (6-1 .. 6-4) in
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
    "6-1": [
        "设 `0≤f(x)≤g(x)` 于 `[a,∞)`（或邻域内）",
        "对任意 `A>a`，有 `0≤∫_a^A f(x)dx ≤ ∫_a^A g(x)dx`",
        "若 `∫_a^∞ g` 收敛且其值为 `G`，则 `∫_a^A f` 单调递增且有上界 `G`",
        "由单调有界收敛，`∫_a^∞ f` 收敛",
        "若 `∫_a^∞ f` 发散到 `∞`，则因 `∫_a^A g ≥ ∫_a^A f`，`∫_a^∞ g` 亦发散",
    ],
    "6-2": [
        "设 `f,g≥0` 且 `lim_{x→∞} f(x)/g(x)=L`，其中 `0<L<∞`",
        "取 `ε=L/2`，则存在 `X` 使 `x≥X` 时 `|f/g-L|<ε`",
        "于是对 `x≥X` 有 `(L/2)g(x) ≤ f(x) ≤ (3L/2)g(x)`",
        "由比较判别，`∫_X^∞ f` 与 `∫_X^∞ g` 同敛散",
        "故 `∫_a^∞ f` 与 `∫_a^∞ g` 同敛散",
    ],
    "6-3": [
        "设 `f` 在 `[-a,a]` 可积且为偶函数，则 `f(x)=f(-x)`",
        "有 `∫_{-a}^a f(x)dx = ∫_{-a}^0 f(x)dx + ∫_0^a f(x)dx`",
        "令 `x=-t`，得 `∫_{-a}^0 f(x)dx = ∫_0^a f(t)dt`",
        "故 `∫_{-a}^a f = 2∫_0^a f`",
        "若 `f` 为奇函数，则 `f(-x)=-f(x)`，同样变换得 `∫_{-a}^a f = 0`",
        "若积分为瑕积分，定义主值 `PV∫_{-a}^a f = lim_{b→a-} ∫_{-b}^b f`",
        "对奇函数，上述对称性仍给出 `PV∫_{-a}^a f = 0`",
    ],
    "6-4": [
        "设 `F(x)=∫_a^x f(t)dt` 有界，且 `g(x)` 单调趋于 0",
        "对任意 `A>a`，分部积分：`∫_a^A f(x)g(x)dx = F(A)g(A)-F(a)g(a)-∫_a^A F(x)g'(x)dx`",
        "由 `g(A)→0` 且 `F` 有界，`F(A)g(A)→0`",
        "因 `g` 单调，`g'` 可作负号，且 `∫_a^A |g'(x)|dx = g(a)-g(A) ≤ g(a)`",
        "设 `|F(x)|≤M`，则 `|∫_a^A F(x)g'(x)dx| ≤ M∫_a^A |g'(x)|dx ≤ Mg(a)`",
        "故右端在 `A→∞` 时有极限，`∫_a^∞ f(x)g(x)dx` 收敛",
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
            if tid.startswith("6-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter6 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("6-")))


if __name__ == "__main__":
    main()
