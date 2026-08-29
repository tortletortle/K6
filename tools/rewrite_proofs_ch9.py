# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 9 theorems (9-1 .. 9-2) in
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
    "9-1": [
        "设 `f` 在矩形 `R=[a,b]×[c,d]` 上连续",
        "对每个 `x`，`y↦f(x,y)` 连续，可积，定义 `Φ(x)=∫_c^d f(x,y)dy`",
        "由连续性与一致连续性可证 `Φ` 在 `[a,b]` 连续",
        "因此 `∫_a^b Φ(x)dx` 存在",
        "取分割 `P` 与 `Q`，双重 Riemann 和为 `∑_{i,j} f(ξ_{ij},η_{ij}) Δx_i Δy_j`",
        "对固定 `i`，内层和 `∑_j f(ξ_{ij},η_{ij}) Δy_j` 逼近 `∫_c^d f(ξ_{ij},y)dy`",
        "于是双重和逼近 `∑_i Φ(ξ_i) Δx_i`",
        "当分割细化时，上述和收敛到 `∫_a^b Φ(x)dx`",
        "由双重积分定义，`∬_R f = ∫_a^b (∫_c^d f(x,y)dy) dx`",
    ],
    "9-2": [
        "设变换 `T:(u,v)↦(x,y)` 可微、单射，Jacobian `J=∂(x,y)/∂(u,v)` 非零",
        "对小矩形 `ΔuΔv`，用线性近似 `Δx ≈ x_u Δu + x_v Δv`，`Δy ≈ y_u Δu + y_v Δv`",
        "对应平行四边形面积近似为 `|J| ΔuΔv`",
        "取对 `D'` 的分割，双重和 `∑ f(x_{ij},y_{ij}) |J(u_{ij},v_{ij})| Δu_i Δv_j`",
        "在变换下对应 `D` 的分割面积和 `∑ f(x_{ij},y_{ij}) Δx_i Δy_j`",
        "令网格趋于 0，得到 `∬_D f(x,y)dxdy = ∬_{D'} f(T(u,v)) |J| dudv`",
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
            if tid.startswith("9-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter9 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("9-")))


if __name__ == "__main__":
    main()
