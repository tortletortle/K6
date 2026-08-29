# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 10 theorems (10-1 .. 10-5) in
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
    "10-1": [
        "设 `F=∇φ`，曲线 `C` 参数方程 `r(t)`，`t∈[t0,t1]`",
        "线积分 `∫_C F·dr = ∫_{t0}^{t1} ∇φ(r(t))·r'(t) dt`",
        "由链式法则，`d/dt [φ(r(t))] = ∇φ(r(t))·r'(t)`",
        "故 `∫_C F·dr = ∫_{t0}^{t1} d/dt[φ(r(t))] dt`",
        "积分得 `φ(r(t1)) - φ(r(t0))`",
        "即 `∫_C ∇φ·dr = φ(B)-φ(A)`",
    ],
    "10-2": [
        "若 `F=∇φ`，由定理 10-1，线积分仅与端点有关，故与路径无关",
        "反之，若线积分与路径无关，固定基点 `x0`",
        "定义 `φ(x)=∫_{x0}^{x} F·dr`（任取路径）",
        "由路径无关性，`φ` 定义良好",
        "对坐标方向 `e_i`，考虑 `φ(x+he_i)-φ(x)=∫_{x}^{x+he_i} F·dr`",
        "右端为 `∫_0^h F_i(x+se_i) ds`",
        "除以 `h` 取极限得 `∂φ/∂x_i = F_i`",
        "因此 `F=∇φ`，即保守场",
    ],
    "10-3": [
        "先考虑矩形区域 `R=[a,b]×[c,d]`",
        "对边界四边分别积分并相加，可得",
        "`∮_{∂R} (P dx + Q dy) = ∫_a^b [Q(x,d)-Q(x,c)] dx + ∫_c^d [P(a,y)-P(b,y)] dy`",
        "由一元积分基本定理，右端等于",
        "`∬_R (∂Q/∂x - ∂P/∂y) dA`",
        "对一般简单区域可分割为有限矩形或简单区域并取极限",
        "内部边界方向相反而相互抵消，故结论成立",
    ],
    "10-4": [
        "先对平行六面体 `V=[a,b]×[c,d]×[e,f]` 证明",
        "对六个面计算通量并相加，得",
        "`∯_{∂V} F·n dS = ∭_V (∂P/∂x+∂Q/∂y+∂R/∂z) dV`",
        "该式由一元积分基本定理逐次积分得到",
        "对一般有界体，分割为小盒并求和",
        "内部面通量相互抵消，取极限得结论",
    ],
    "10-5": [
        "设有向曲面 `S` 边界为 `C`，对 `S` 作参数化 `r(u,v)`",
        "在参数域内将 `S` 分割为小片，曲线积分在相邻片的公共边界上相互抵消",
        "每个小片在参数平面上映射为小区域，可对其应用 Green 定理",
        "Green 定理给出该片边界积分等于该片上旋度的法向分量面积积分",
        "求和并取极限，得到 `∮_C F·dr = ∬_S (∇×F)·n dS`",
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
            if tid.startswith("10-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter10 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("10-")))


if __name__ == "__main__":
    main()
