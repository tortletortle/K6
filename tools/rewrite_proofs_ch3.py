# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 3 theorems (3-1 .. 3-10) in
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
    "3-1": [
        "设 `f` 在 `x0` 处取局部最大值（最小值同理），且在 `x0` 可导",
        "存在 `δ>0` 使 `|x-x0|<δ` 时 `f(x)≤f(x0)`",
        "取 `x>x0`，则 `f(x)-f(x0)≤0` 且 `x-x0>0`",
        "故右差商 `[(f(x)-f(x0))/(x-x0)]≤0`",
        "取 `x<x0`，则 `f(x)-f(x0)≤0` 且 `x-x0<0`",
        "故左差商 `[(f(x)-f(x0))/(x-x0)]≥0`",
        "导数存在意味着左右极限相等",
        "于是只能是 `f'(x0)=0`",
    ],
    "3-2": [
        "设 `f` 在 `[a,b]` 连续、在 `(a,b)` 可导，且 `f(a)=f(b)`",
        "由闭区间连续，`f` 在 `[a,b]` 取到最大值 `M` 与最小值 `m`",
        "若 `M=m`，则 `f` 为常数函数，任取 `c∈(a,b)` 有 `f'(c)=0`",
        "若 `M>m`，则至少有一个极值点位于 `(a,b)`（因 `f(a)=f(b)`）",
        "设 `c` 为内部极值点，由 Fermat 定理得 `f'(c)=0`",
    ],
    "3-3": [
        "设 `f` 在 `[a,b]` 连续、在 `(a,b)` 可导",
        "构造辅助函数 `φ(x)=f(x)-[(f(b)-f(a))/(b-a)](x-a)`",
        "计算：`φ(a)=f(a)`，`φ(b)=f(b)-[(f(b)-f(a))/(b-a)](b-a)=f(a)`",
        "故 `φ(a)=φ(b)`，满足 Rolle 定理条件",
        "由 Rolle 定理，存在 `c∈(a,b)` 使 `φ'(c)=0`",
        "而 `φ'(x)=f'(x)-[(f(b)-f(a))/(b-a)]`",
        "故 `f'(c)=(f(b)-f(a))/(b-a)`",
    ],
    "3-4": [
        "设 `f,g` 在 `[a,b]` 连续、在 `(a,b)` 可导，且 `g(b)≠g(a)`",
        "构造 `φ(x)=(f(b)-f(a))g(x)-(g(b)-g(a))f(x)`",
        "代入端点：`φ(a)=(f(b)-f(a))g(a)-(g(b)-g(a))f(a)`",
        "`φ(b)=(f(b)-f(a))g(b)-(g(b)-g(a))f(b)`",
        "直接化简得 `φ(a)=φ(b)`",
        "由 Rolle 定理，存在 `c∈(a,b)` 使 `φ'(c)=0`",
        "计算 `φ'(x)=(f(b)-f(a))g'(x)-(g(b)-g(a))f'(x)`",
        "故在 `c` 有 `(f(b)-f(a))g'(c)=(g(b)-g(a))f'(c)`",
        "整理得 `f'(c)/g'(c)=(f(b)-f(a))/(g(b)-g(a))`",
    ],
    "3-5": [
        "以 `x→a+` 且 `f(a)=g(a)=0` 的 `0/0` 型为例",
        "对任意 `x∈(a,a+δ)`，由 Cauchy 中值定理，存在 `ξ∈(a,x)` 使",
        "`[f(x)-f(a)]/[g(x)-g(a)]=f'(ξ)/g'(ξ)`",
        "因 `f(a)=g(a)=0`，得 `f(x)/g(x)=f'(ξ)/g'(ξ)`",
        "当 `x→a+` 时，`ξ→a+`",
        "若 `lim_{x→a+} f'(x)/g'(x)=L` 存在，则 `f'(ξ)/g'(ξ)→L`",
        "故 `lim_{x→a+} f(x)/g(x)=L`",
        "其余情形（`∞/∞` 或 `x→a-`）同理处理",
    ],
    "3-6": [
        "设 `f` 在 `x0` 的邻域内具有 `n+1` 阶导数",
        "记 `P_n(x)=∑_{k=0}^n f^{(k)}(x0)/k! · (x-x0)^k`",
        "令 `R` 为待定常数，构造 `Φ(t)=f(t)-P_n(t)-R(t-x0)^{n+1}`",
        "令 `t=x`，并取 `R` 使 `Φ(x)=0`，显然 `Φ(x0)=0`",
        "于是 `Φ` 在 `[x0,x]` 上满足 Rolle 条件",
        "对 `Φ` 连续求导 `n+1` 次，可得 `Φ^{(n+1)}(t)=f^{(n+1)}(t)-(n+1)!R`",
        "由 Rolle 定理反复应用，存在 `ξ` 介于 `x0` 与 `x` 使 `Φ^{(n+1)}(ξ)=0`",
        "从而 `R=f^{(n+1)}(ξ)/(n+1)!`",
        "代回得到 `f(x)=P_n(x)+f^{(n+1)}(ξ)/(n+1)!·(x-x0)^{n+1}`",
    ],
    "3-7": [
        "设 `f` 在 `(a,b)` 可导且 `f'(x)≥0`",
        "任取 `x1<x2`，由 Lagrange 中值定理，存在 `c∈(x1,x2)` 使",
        "`f(x2)-f(x1)=f'(c)(x2-x1)`",
        "因 `f'(c)≥0` 且 `x2-x1>0`，得 `f(x2)≥f(x1)`",
        "故 `f` 在 `(a,b)` 单调不减",
        "若处处 `f'(x)>0`，则对任意 `x1<x2` 有 `f(x2)>f(x1)`，故严格递增",
    ],
    "3-8": [
        "设存在 `δ>0` 使 `x<x0` 时 `f'(x)>0`，`x>x0` 时 `f'(x)<0`",
        "由单调性判别，`f` 在 `(x0-δ,x0)` 上递增，在 `(x0,x0+δ)` 上递减",
        "因此 `f(x0)` 不小于两侧邻点函数值",
        "故 `x0` 为局部最大值点",
        "若符号相反（左负右正），同理得 `x0` 为局部最小值点",
    ],
    "3-9": [
        "设 `f` 二阶可导且 `f''(x)≥0` 于 `(a,b)`",
        "则 `f'` 在 `(a,b)` 上单调不减",
        "任取 `x1<x2`，由中值定理存在 `c1∈(x1,x2)` 使",
        "`f(x2)-f(x1)=f'(c1)(x2-x1)`",
        "若再取 `x2<x3`，存在 `c2∈(x2,x3)` 使 `f(x3)-f(x2)=f'(c2)(x3-x2)`",
        "因 `c1<c2` 且 `f'` 单调不减，得 `f'(c1)≤f'(c2)`",
        "于是 `(f(x2)-f(x1))/(x2-x1) ≤ (f(x3)-f(x2))/(x3-x2)`",
        "弦斜率随 `x` 增大不减，等价于 `f` 凸",
        "若 `f''(x)≤0`，同理得 `f` 凹",
    ],
    "3-10": [
        "设 `f''` 在 `x0` 邻域内存在并在 `x0` 两侧异号",
        "若 `f''>0` 于 `x0` 左侧、`f''<0` 于右侧，则左侧凸、右侧凹",
        "凸凹性发生改变，曲线的弯曲方向改变",
        "因此 `x0` 为拐点",
        "若符号反向，结论同理成立",
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
            if tid.startswith("3-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter3 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("3-")))


if __name__ == "__main__":
    main()
