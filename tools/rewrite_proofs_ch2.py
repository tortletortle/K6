# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 2 theorems (2-1 .. 2-10) in
D:\\spot\\K6\\tongji-calculus-notes.md to a more formula-level, step-by-step style.

This script is deterministic (no AI calls). It replaces only the numbered lines
under "**证明（逐行）**" and stops at "**例题**".
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
    "2-1": [
        "设函数 `f` 在 `x0` 可导，记 `f'(x0)=lim_{x→x0} (f(x)-f(x0))/(x-x0)`",
        "对 `x≠x0`，恒等式 `f(x)-f(x0)=[(f(x)-f(x0))/(x-x0)]·(x-x0)`",
        "令 `x→x0`，上式右端为两个因子乘积的极限",
        "由可导性，第一因子 `[(f(x)-f(x0))/(x-x0)]→f'(x0)`",
        "显然 `x-x0→0`",
        "乘积极限存在且等于 `f'(x0)·0=0`",
        "因此 `lim_{x→x0} (f(x)-f(x0))=0`",
        "等价于 `lim_{x→x0} f(x)=f(x0)`",
        "故 `f` 在 `x0` 连续",
    ],
    "2-2": [
        "设 `h(x)=αf(x)+βg(x)`，且 `f,g` 在 `x0` 可导",
        "由导数定义：`h'(x0)=lim_{x→x0} [h(x)-h(x0)]/(x-x0)`",
        "展开分子：`h(x)-h(x0)=α(f(x)-f(x0))+β(g(x)-g(x0))`",
        "据极限线性性：`h'(x0)=α·lim (f(x)-f(x0))/(x-x0)+β·lim (g(x)-g(x0))/(x-x0)`",
        "即 `h'(x0)=αf'(x0)+βg'(x0)`",
    ],
    "2-3": [
        "设 `h(x)=f(x)g(x)`，且 `f,g` 在 `x0` 可导",
        "由导数定义：`h'(x0)=lim_{x→x0} [f(x)g(x)-f(x0)g(x0)]/(x-x0)`",
        "加减同项：`f(x)g(x)-f(x0)g(x0)=[f(x)-f(x0)]g(x)+f(x0)[g(x)-g(x0)]`",
        "除以 `x-x0`：`h'(x0)=lim [f(x)-f(x0)]/(x-x0)·g(x) + f(x0)·lim [g(x)-g(x0)]/(x-x0)`",
        "由“可导必连续”，`g(x)→g(x0)`",
        "因此 `h'(x0)=f'(x0)g(x0)+f(x0)g'(x0)`",
    ],
    "2-4": [
        "设 `h(x)=f(x)/g(x)`，且 `f,g` 在 `x0` 可导、`g(x0)≠0`",
        "由可导必连续，存在邻域使 `g(x)≠0`",
        "先求倒数函数导数：令 `q(x)=1/g(x)`",
        "`q'(x0)=lim_{x→x0} [1/g(x)-1/g(x0)]/(x-x0)`",
        "化简分子：`1/g(x)-1/g(x0)=(g(x0)-g(x))/(g(x)g(x0))`",
        "故 `q'(x0)=lim [-(g(x)-g(x0))/(x-x0)]·1/(g(x)g(x0))`",
        "其中 `-(g(x)-g(x0))/(x-x0)→-g'(x0)`，且 `1/(g(x)g(x0))→1/g(x0)^2`",
        "故 `q'(x0)=-g'(x0)/g(x0)^2`",
        "再用乘积法则：`h=f·q`，所以 `h'(x0)=f'(x0)q(x0)+f(x0)q'(x0)`",
        "代入 `q=1/g` 与 `q'` 得 `h'(x0)=(f'(x0)g(x0)-f(x0)g'(x0))/g(x0)^2`",
    ],
    "2-5": [
        "设 `y=f(u)` 且 `u=g(x)`，`g` 在 `x0` 可导，`f` 在 `u0=g(x0)` 可导",
        "令 `Δx=x-x0`，`Δu=g(x)-g(x0)`，则 `Δx→0 ⇒ Δu→0`",
        "当 `Δu≠0` 时，有恒等式",
        "`[f(g(x))-f(g(x0))]/(x-x0) = [f(u0+Δu)-f(u0)]/Δu · (Δu/Δx)`",
        "由 `f` 可导，第一因子 `→ f'(u0)`",
        "由 `g` 可导，第二因子 `Δu/Δx → g'(x0)`",
        "因此 `lim_{x→x0} [f(g(x))-f(g(x0))]/(x-x0)=f'(u0)g'(x0)`",
        "即 `(f∘g)'(x0)=f'(g(x0))·g'(x0)`",
    ],
    "2-6": [
        "设 `y0=f(x0)`，`f` 在 `x0` 可导且 `f'(x0)≠0`，并在邻域内可逆，逆函数为 `φ`",
        "对 `y` 近 `y0`，令 `x=φ(y)`，则 `y=f(x)`",
        "差商：`[φ(y)-φ(y0)]/(y-y0) = (x-x0)/(f(x)-f(x0))`",
        "当 `y→y0` 时，由逆函数连续性得 `x→x0`",
        "于是 `[(f(x)-f(x0))/(x-x0)] → f'(x0)`",
        "取倒数得 `lim_{y→y0} [φ(y)-φ(y0)]/(y-y0) = 1/f'(x0)`",
        "故 `φ'(y0)=1/f'(x0)`",
    ],
    "2-7": [
        "设 `F` 在 `(x0,y0)` 可微且 `F(x0,y0)=0`、`F_y(x0,y0)≠0`",
        "令隐函数 `y=y(x)` 满足 `F(x,y(x))≡0`，设 `Δx=x-x0`，`Δy=y(x)-y0`",
        "可微性给出增量公式：`F(x0+Δx,y0+Δy)-F(x0,y0)=F_xΔx+F_yΔy+o(√(Δx^2+Δy^2))`",
        "左端恒为 `0-0=0`，故 `F_xΔx+F_yΔy+o(√(Δx^2+Δy^2))=0`",
        "两边除以 `Δx`：`F_x+F_y(Δy/Δx)+o(1)=0`",
        "当 `Δx→0` 时，`o(1)→0`，得 `F_x+F_y y'(x0)=0`",
        "解得 `y'(x0)=-F_x(x0,y0)/F_y(x0,y0)`",
    ],
    "2-8": [
        "设 `x=x(t)`、`y=y(t)` 在 `t0` 可导且 `x'(t0)≠0`",
        "当 `t≠t0` 时，有 `dy/dx = [y(t)-y(t0)]/[x(t)-x(t0)]`",
        "将分子分母同除以 `t-t0`：`dy/dx = ([y(t)-y(t0)]/(t-t0)) / ([x(t)-x(t0)]/(t-t0))`",
        "令 `t→t0`，分子趋于 `y'(t0)`，分母趋于 `x'(t0)`",
        "故 `dy/dx|_{t0}=y'(t0)/x'(t0)`",
    ],
    "2-9": [
        "对 `n=1`，乘积法则给出 `(fg)'=f'g+fg'`，公式成立",
        "假设对某 `n` 成立：`(fg)^{(n)}=∑_{k=0}^n C(n,k) f^{(k)} g^{(n-k)}`",
        "两边再求导：`(fg)^{(n+1)}=∑_{k=0}^n C(n,k)[f^{(k+1)} g^{(n-k)} + f^{(k)} g^{(n-k+1)}]`",
        "将第一项和第二项分别成两组求和并改换指标",
        "得到 `∑_{k=1}^{n+1} C(n,k-1) f^{(k)} g^{(n+1-k)} + ∑_{k=0}^{n} C(n,k) f^{(k)} g^{(n+1-k)}`",
        "利用恒等式 `C(n,k-1)+C(n,k)=C(n+1,k)` 合并同类项",
        "于是 `(fg)^{(n+1)}=∑_{k=0}^{n+1} C(n+1,k) f^{(k)} g^{(n+1-k)}`",
        "由归纳法，公式对一切 `n` 成立",
    ],
    "2-10": [
        "设 `f` 在 `x0` 可导，记 `f'(x0)=lim_{x→x0} (f(x)-f(x0))/(x-x0)`",
        "等价地，`[(f(x)-f(x0))/(x-x0)]-f'(x0) → 0`",
        "记 `ε(x)=[(f(x)-f(x0))/(x-x0)]-f'(x0)`，则 `ε(x)→0`",
        "于是 `f(x)-f(x0)=f'(x0)(x-x0)+ε(x)(x-x0)`",
        "令 `r(x)=ε(x)(x-x0)`，则 `r(x)/(x-x0)→0`",
        "故 `f(x)=f(x0)+f'(x0)(x-x0)+o(x-x0)`",
        "这给出在 `x0` 的线性近似",
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
            if tid.startswith("2-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter2 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("2-")))


if __name__ == "__main__":
    main()
