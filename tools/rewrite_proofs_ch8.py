# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 8 theorems (8-1 .. 8-9) in
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
    "8-1": [
        "设 `lim_{x→a} f(x)=A` 且 `lim_{x→a} f(x)=B`",
        "任取 `ε>0`",
        "由极限定义，存在 `δ1` 使 `0<||x-a||<δ1 ⇒ |f(x)-A|<ε/2`",
        "同理存在 `δ2` 使 `0<||x-a||<δ2 ⇒ |f(x)-B|<ε/2`",
        "取 `δ=min(δ1,δ2)`",
        "当 `0<||x-a||<δ` 时，`|A-B|≤|A-f(x)|+|f(x)-B|<ε`",
        "由 `ε` 任意得 `A=B`",
    ],
    "8-2": [
        "设 `f` 在点 `a` 可微",
        "则存在线性映射 `L(h)` 使 `f(a+h)-f(a)=L(h)+o(||h||)`",
        "当 `h→0`，`L(h)→0` 且 `o(||h||)→0`",
        "于是 `f(a+h)→f(a)`",
        "故 `f` 在 `a` 连续",
    ],
    "8-3": [
        "设 `f` 在 `(x0,y0)` 邻域内有偏导且 `f_x,f_y` 在该点连续",
        "记 `Δx=x-x0`，`Δy=y-y0`",
        "分解增量：`Δf=f(x0+Δx,y0+Δy)-f(x0,y0)`",
        "`= [f(x0+Δx,y0+Δy)-f(x0,y0+Δy)] + [f(x0,y0+Δy)-f(x0,y0)]`",
        "对第一项按 `x` 变量用一元中值定理，得 `= f_x(x0+θΔx,y0+Δy)Δx`",
        "对第二项按 `y` 变量用一元中值定理，得 `= f_y(x0,y0+ηΔy)Δy`",
        "于是 `Δf = f_x(x0,y0)Δx + f_y(x0,y0)Δy + o(√(Δx^2+Δy^2))`",
        "满足可微定义，故 `f` 可微",
    ],
    "8-4": [
        "设 `f` 在点 `a` 可微，`u` 为单位向量",
        "由可微性：`f(a+h)=f(a)+∇f(a)·h+o(||h||)`",
        "令 `h=t u`，则 `f(a+tu)-f(a)=t∇f(a)·u+o(|t|)`",
        "两边除以 `t`，取极限 `t→0` 得 `D_u f(a)=∇f(a)·u`",
        "由 Cauchy-Schwarz，不等式 `|∇f·u|≤||∇f||·||u||=||∇f||`",
        "当 `u` 取 `∇f` 方向时取等号，故最大方向导数为 `||∇f||`",
    ],
    "8-5": [
        "设 `z=f(u,v)`，`u=u(x,y)`，`v=v(x,y)`，均可微",
        "全微分：`dz = f_u du + f_v dv`",
        "且 `du = u_x dx + u_y dy`，`dv = v_x dx + v_y dy`",
        "代入得 `dz = (f_u u_x + f_v v_x) dx + (f_u u_y + f_v v_y) dy`",
        "因此 `∂z/∂x = f_u u_x + f_v v_x`，`∂z/∂y = f_u u_y + f_v v_y`",
    ],
    "8-6": [
        "设 `F(x,y)` 在 `(x0,y0)` 可微且 `F(x0,y0)=0`、`F_y(x0,y0)≠0`",
        "存在隐函数 `y=y(x)` 使 `F(x,y(x))=0`",
        "记 `Δx=x-x0`，`Δy=y(x)-y0`",
        "可微性给出 `F(x0+Δx,y0+Δy)-F(x0,y0)=F_xΔx+F_yΔy+o(√(Δx^2+Δy^2))`",
        "左端恒为 0，故 `F_x+F_y(Δy/Δx)+o(1)=0`",
        "取极限得 `F_x+F_y y'(x0)=0`",
        "从而 `y'(x0)=-F_x(x0,y0)/F_y(x0,y0)`",
    ],
    "8-7": [
        "设 `f` 在内点 `a` 可微并取局部极值",
        "对任意单位向量 `u`，函数 `φ(t)=f(a+tu)` 在 `t=0` 取极值",
        "由一元 Fermat 定理，`φ'(0)=0`",
        "而 `φ'(0)=D_u f(a)=∇f(a)·u`",
        "对任意 `u` 均有 `∇f(a)·u=0`，故 `∇f(a)=0`",
        "即所有一阶偏导为 0",
    ],
    "8-8": [
        "设 `(x0,y0)` 为临界点，`f_x=f_y=0`",
        "记 `h=x-x0`，`k=y-y0`，二阶 Taylor 展开：",
        "`f(x0+h,y0+k)=f(x0,y0)+1/2 (f_xx h^2 + 2f_xy hk + f_yy k^2) + o(h^2+k^2)`",
        "二次型记为 `Q(h,k)=f_xx h^2 + 2f_xy hk + f_yy k^2`",
        "判别式 `D=f_xx f_yy - f_xy^2`",
        "若 `D>0` 且 `f_xx>0`，则 `Q>0`，得局部极小",
        "若 `D>0` 且 `f_xx<0`，则 `Q<0`，得局部极大",
        "若 `D<0`，则 `Q` 不定号，得鞍点",
    ],
    "8-9": [
        "设在约束 `g(x)=0` 上 `f` 取极值，且 `∇g(a)≠0`",
        "任取满足 `∇g(a)·v=0` 的切向量 `v`",
        "沿曲线 `a+tv` 方向，`g` 一阶不变，而 `f` 在 `t=0` 取极值",
        "故 `D_v f(a)=∇f(a)·v=0` 对所有切向量 `v` 成立",
        "于是 `∇f(a)` 与所有切向量正交",
        "法向量由 `∇g(a)` 张成，故存在 `λ` 使 `∇f(a)=λ∇g(a)`",
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
            if tid.startswith("8-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter8 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("8-")))


if __name__ == "__main__":
    main()
