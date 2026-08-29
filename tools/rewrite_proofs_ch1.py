# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 1 theorems (1-1 .. 1-23) in
D:\spot\K6\tongji-calculus-notes.md to a more formula-level, step-by-step style.

This script is intentionally deterministic (no AI calls). It replaces only the
numbered lines under "**证明（逐行）**" and stops at "**例题**".
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
    if s.endswith(("。", "？", "！", "：")):
        return s
    return s + "。"


PROOFS: dict[str, list[str]] = {
    "1-1": [
        "设数列 `{a_n}` 同时满足 `a_n→A` 与 `a_n→B`",
        "取任意 `ε>0`",
        "由 `a_n→A`，存在 `N1∈ℕ`，使 `n≥N1 ⇒ |a_n-A|<ε/2`",
        "由 `a_n→B`，存在 `N2∈ℕ`，使 `n≥N2 ⇒ |a_n-B|<ε/2`",
        "令 `N=max(N1,N2)`，则 `n≥N ⇒ |a_n-A|<ε/2` 且 `|a_n-B|<ε/2`",
        "恒等变形：`A-B=(A-a_n)+(a_n-B)`",
        "取绝对值：`|A-B|=|(A-a_n)+(a_n-B)|`",
        "由三角不等式：`|A-B|≤|A-a_n|+|a_n-B|`",
        "当 `n≥N` 时：`|A-B|<ε/2+ε/2`",
        "计算：`ε/2+ε/2=ε`，故 `|A-B|<ε`",
        "`ε` 任意，推出 `|A-B|=0`",
        "因此 `A=B`",
    ],
    "1-2": [
        "设 `a_n→A`",
        "取 `ε=1`",
        "由收敛定义：存在 `N∈ℕ`，使 `n≥N ⇒ |a_n-A|<1`",
        "对 `n≥N`：`|a_n|=| (a_n-A)+A |`",
        "由三角不等式：`|a_n|≤|a_n-A|+|A|<1+|A|`",
        "记 `M0=|A|+1`，则 `n≥N ⇒ |a_n|≤M0`",
        "前 `N-1` 项为有限个数，记 `M1=max{|a_1|,|a_2|,...,|a_{N-1}|}`",
        "令 `M=max(M0,M1)`",
        "则对任意 `n`，均有 `|a_n|≤M`",
        "故 `{a_n}` 有界",
    ],
    "1-3": [
        "设存在 `N0` 使 `n≥N0 ⇒ a_n≤b_n`，且 `a_n→A`、`b_n→B`",
        "反设 `A>B`",
        "取 `ε=(A-B)/3`，则 `ε>0`",
        "由 `a_n→A`：存在 `N1` 使 `n≥N1 ⇒ |a_n-A|<ε`，从而 `a_n>A-ε`",
        "由 `b_n→B`：存在 `N2` 使 `n≥N2 ⇒ |b_n-B|<ε`，从而 `b_n<B+ε`",
        "令 `N=max(N0,N1,N2)`，则 `n≥N` 时同时有 `a_n>A-ε` 与 `b_n<B+ε`",
        "计算：`A-ε=A-(A-B)/3=(2A+B)/3`",
        "计算：`B+ε=B+(A-B)/3=(A+2B)/3`",
        "由 `A>B` 得 `(2A+B)/3>(A+2B)/3`，即 `A-ε>B+ε`",
        "于是 `n≥N ⇒ a_n>A-ε>B+ε>b_n`",
        "这与 `n≥N0 ⇒ a_n≤b_n` 矛盾",
        "故反设不成立，从而 `A≤B`",
    ],
    "1-4": [
        "设 `a_n→A`、`b_n→B`",
        "证明加法：`(a_n+b_n)-(A+B)=(a_n-A)+(b_n-B)`",
        "因此 `|a_n+b_n-(A+B)|≤|a_n-A|+|b_n-B|`",
        "给定 `ε>0`，取 `N1` 使 `n≥N1 ⇒ |a_n-A|<ε/2`",
        "取 `N2` 使 `n≥N2 ⇒ |b_n-B|<ε/2`",
        "令 `N=max(N1,N2)`，则 `n≥N ⇒ |a_n+b_n-(A+B)|<ε`",
        "故 `a_n+b_n→A+B`（减法同理）",
        "证明乘法：`a_nb_n-AB=(a_n-A)b_n + A(b_n-B)`",
        "由 `b_n→B` 知 `{b_n}` 有界，存在 `M>0` 使 `n` 充分大时 `|b_n|≤M`",
        "给定 `ε>0`，取 `N3` 使 `n≥N3 ⇒ |a_n-A|<ε/(2M)`",
        "取 `N4` 使 `n≥N4 ⇒ |b_n-B|<ε/(2(|A|+1))`",
        "令 `N=max(N, N3, N4)`，则 `n≥N` 时",
        "有 `|a_nb_n-AB|≤|b_n||a_n-A|+|A||b_n-B|`",
        "进一步有 `|a_nb_n-AB|< M*ε/(2M) + |A|*ε/(2(|A|+1)) ≤ ε/2+ε/2=ε`",
        "故 `a_nb_n→AB`",
        "证明除法（`B≠0`）：先证 `b_n` 终究不为 0",
        "取 `ε0=|B|/2`，由 `b_n→B` 存在 `N5` 使 `n≥N5 ⇒ |b_n-B|<ε0`",
        "则 `n≥N5 ⇒ |b_n|≥|B|-|b_n-B|>|B|/2>0`",
        "于是 `1/b_n` 在尾部有定义，且",
        "`|1/b_n-1/B|=|B-b_n|/(|b_n||B|) ≤ (2/|B|^2)|b_n-B|`（对 `n≥N5`）",
        "由 `|b_n-B|→0` 得 `1/b_n→1/B`",
        "再由乘法极限得 `a_n/b_n = a_n*(1/b_n) → A*(1/B)=A/B`",
    ],
    "1-5": [
        "设存在 `N0` 使 `n≥N0 ⇒ a_n≤b_n≤c_n`，且 `a_n→L`、`c_n→L`",
        "取任意 `ε>0`",
        "由 `a_n→L`：存在 `N1` 使 `n≥N1 ⇒ |a_n-L|<ε`",
        "由此 `n≥N1 ⇒ L-ε<a_n<L+ε`",
        "由 `c_n→L`：存在 `N2` 使 `n≥N2 ⇒ |c_n-L|<ε`",
        "由此 `n≥N2 ⇒ L-ε<c_n<L+ε`",
        "令 `N=max(N0,N1,N2)`",
        "则 `n≥N ⇒ L-ε<a_n≤b_n≤c_n<L+ε`",
        "于是 `n≥N ⇒ |b_n-L|<ε`",
        "因 `ε` 任意，故 `b_n→L`",
    ],
    "1-6": [
        "设 `{a_n}` 单调递增且有上界",
        "令 `A=sup{a_n | n∈ℕ}`，则 `A` 存在且对任意 `n` 有 `a_n≤A`",
        "取任意 `ε>0`",
        "`A-ε` 不是上界（否则 `A-ε` 也是上确界，矛盾）",
        "故存在 `N` 使 `a_N>A-ε`",
        "由单调递增：`n≥N ⇒ a_n≥a_N`",
        "于是 `n≥N ⇒ A-ε<a_N≤a_n≤A`",
        "两边同减 `A`：`n≥N ⇒ -ε < a_n-A ≤ 0`",
        "取绝对值：`n≥N ⇒ |a_n-A|<ε`",
        "因 `ε` 任意，故 `a_n→A`",
        "单调递减且有下界情形类似（取下确界 `inf{a_n}`）",
    ],
    "1-7": [
        "先证：若 `a_n→A`，则 `{a_n}` 为 Cauchy 列",
        "取任意 `ε>0`",
        "由 `a_n→A`，存在 `N` 使 `n≥N ⇒ |a_n-A|<ε/2`",
        "若 `m,n≥N`，则 `|a_n-a_m|=|(a_n-A)-(a_m-A)|`",
        "由三角不等式：`|a_n-a_m|≤|a_n-A|+|a_m-A|<ε/2+ε/2=ε`",
        "故满足 Cauchy 条件",
        "再证：若 `{a_n}` 为 Cauchy 列，则 `{a_n}` 收敛（用实数完备性）",
        "取 `ε=1`，存在 `N0` 使 `m,n≥N0 ⇒ |a_n-a_m|<1`",
        "固定 `n=N0`，得 `m≥N0 ⇒ |a_m|≤|a_{N0}|+1`，故尾部有界",
        "前 `N0-1` 项有限，故全列有界",
        "由 Bolzano–Weierstrass 定理，存在子列 `a_{n_k}→A`",
        "取任意 `ε>0`，由 Cauchy 性存在 `N1` 使 `m,n≥N1 ⇒ |a_n-a_m|<ε/2`",
        "取 `k` 足够大使 `n_k≥N1` 且 `|a_{n_k}-A|<ε/2`",
        "对任意 `n≥N1`：`|a_n-A|≤|a_n-a_{n_k}|+|a_{n_k}-A|<ε/2+ε/2=ε`",
        "故 `a_n→A`，即原列收敛",
    ],
    "1-8": [
        "设 `a_n→A`，取任意子列 `{a_{n_k}}`",
        "取任意 `ε>0`",
        "由 `a_n→A`，存在 `N` 使 `n≥N ⇒ |a_n-A|<ε`",
        "因 `n_k→+∞`，存在 `K` 使 `k≥K ⇒ n_k≥N`",
        "于是 `k≥K ⇒ |a_{n_k}-A|<ε`",
        "故 `a_{n_k}→A`",
    ],
    "1-9": [
        "设 `{a_n}` 有界，存在 `m<M` 使 `a_n∈[m,M]`",
        "令 `I0=[m,M]`，把 `I0` 二分为 `I0^1=[m,(m+M)/2]` 与 `I0^2=[(m+M)/2,M]`",
        "至少有一个子区间包含无穷多个项，取该区间记为 `I1`",
        "对 `Ik` 继续二分，取含无穷多项的半区间记为 `I_{k+1}`",
        "得到嵌套闭区间 `I0⊇I1⊇I2⊇...`，且 `|Ik|=(M-m)/2^k→0`",
        "在每个 `Ik` 中选取一项 `a_{n_k}∈Ik` 且令 `n_{k+1}>n_k`（保证是子列）",
        "由闭区间套定理，存在唯一 `c∈⋂_{k=0}^∞ Ik`",
        "对任意 `ε>0`，取 `K` 使 `|IK|<(ε)`",
        "则 `k≥K ⇒ a_{n_k}∈Ik⊆IK`，从而 `|a_{n_k}-c|≤|IK|<ε`",
        "故存在收敛子列 `a_{n_k}→c`",
    ],
    "1-10": [
        "令 `a_n=(1+1/n)^n`，取对数：`\\ln a_n = n\\ln(1+1/n)`",
        "对 `t>0` 有积分表示：`\\ln(1+t)=\\int_0^t \\frac{1}{1+u}\\,du`",
        "当 `0≤u≤t` 时有 `1/(1+t)≤1/(1+u)≤1`",
        "对不等式积分得：`t/(1+t)≤\\ln(1+t)≤t`",
        "令 `t=1/n`，得 `\\frac{1/n}{1+1/n} ≤ \\ln(1+1/n) ≤ 1/n`",
        "两边同乘 `n`：`\\frac{n}{n+1} ≤ n\\ln(1+1/n) ≤ 1`",
        "由夹逼：`n\\ln(1+1/n)→1`",
        "即 `\\ln a_n → 1`",
        "指数函数连续，故 `a_n = e^{\\ln a_n} → e^1 = e`",
    ],
    "1-11": [
        "令 `b_n=n^{1/n}`（`n≥1`）",
        "取对数：`\\ln b_n = \\frac{\\ln n}{n}`",
        "考察函数极限 `\\lim_{x→+\\infty} \\frac{\\ln x}{x}`",
        "这是 `∞/∞` 型，洛必达：`\\lim_{x→+\\infty} \\frac{\\ln x}{x} = \\lim_{x→+\\infty} \\frac{1/x}{1}=0`",
        "故 `\\ln b_n = (\\ln n)/n → 0`",
        "指数函数连续：`b_n = e^{\\ln b_n} → e^0 = 1`",
    ],
    "1-12": [
        "设 `\\lim_{x→a} f(x)=A` 且 `\\lim_{x→a} f(x)=B`",
        "取任意 `ε>0`",
        "由 `\\lim f = A`，存在 `δ1>0` 使 `0<|x-a|<δ1 ⇒ |f(x)-A|<ε/2`",
        "由 `\\lim f = B`，存在 `δ2>0` 使 `0<|x-a|<δ2 ⇒ |f(x)-B|<ε/2`",
        "令 `δ=min(δ1,δ2)`，则 `0<|x-a|<δ` 时两不等式同时成立",
        "恒等变形：`A-B=(A-f(x))+(f(x)-B)`",
        "取绝对值并用三角不等式：`|A-B|≤|A-f(x)|+|f(x)-B|`",
        "当 `0<|x-a|<δ`：`|A-B|<ε/2+ε/2=ε`",
        "`ε` 任意，故 `|A-B|=0`",
        "因此 `A=B`",
    ],
    "1-13": [
        "设 `\\lim_{x→a} f(x)=A`，`\\lim_{x→a} g(x)=B`",
        "证明加法：`(f+g)-(A+B)=(f-A)+(g-B)`",
        "因此 `|(f+g)-(A+B)|≤|f-A|+|g-B|`",
        "给定 `ε>0`，取 `δ1` 使 `0<|x-a|<δ1 ⇒ |f(x)-A|<ε/2`",
        "取 `δ2` 使 `0<|x-a|<δ2 ⇒ |g(x)-B|<ε/2`",
        "令 `δ=min(δ1,δ2)`，则 `0<|x-a|<δ ⇒ |(f+g)-(A+B)|<ε`",
        "故 `\\lim(f+g)=A+B`（减法同理）",
        "证明乘法：`f g-AB=(f-A)g + A(g-B)`",
        "由 `g(x)→B` 知 `g` 在去心邻域内有界：存在 `M` 与 `δ0` 使 `0<|x-a|<δ0 ⇒ |g(x)|≤M`",
        "给定 `ε>0`，取 `δ3` 使 `0<|x-a|<δ3 ⇒ |f(x)-A|<ε/(2M)`",
        "取 `δ4` 使 `0<|x-a|<δ4 ⇒ |g(x)-B|<ε/(2(|A|+1))`",
        "令 `δ=min(δ0,δ3,δ4)`，则 `0<|x-a|<δ` 时",
        "`|fg-AB|≤|g||f-A|+|A||g-B|< M*ε/(2M)+|A|*ε/(2(|A|+1))≤ε`",
        "故 `\\lim fg = AB`",
        "证明除法（`B≠0`）：取 `ε0=|B|/2`",
        "存在 `δ5` 使 `0<|x-a|<δ5 ⇒ |g(x)-B|<ε0`",
        "于是 `0<|x-a|<δ5 ⇒ |g(x)|≥|B|-|g(x)-B|>|B|/2>0`",
        "从而 `1/g(x)` 有定义，且",
        "`|1/g(x)-1/B|=|B-g(x)|/(|g(x)||B|) ≤ (2/|B|^2)|g(x)-B|`",
        "由 `g(x)→B` 得 `1/g(x)→1/B`",
        "再由乘法法则：`f(x)/g(x)=f(x)*(1/g(x))→A*(1/B)=A/B`",
    ],
    "1-14": [
        "设存在 `δ0>0` 使 `0<|x-a|<δ0 ⇒ φ(x)≤f(x)≤ψ(x)`",
        "且 `\\lim_{x→a} φ(x)=\\lim_{x→a} ψ(x)=L`",
        "取任意 `ε>0`",
        "由 `\\lim φ=L`，存在 `δ1>0` 使 `0<|x-a|<δ1 ⇒ |φ(x)-L|<ε`",
        "由此 `0<|x-a|<δ1 ⇒ L-ε<φ(x)<L+ε`",
        "由 `\\lim ψ=L`，存在 `δ2>0` 使 `0<|x-a|<δ2 ⇒ |ψ(x)-L|<ε`",
        "由此 `0<|x-a|<δ2 ⇒ L-ε<ψ(x)<L+ε`",
        "令 `δ=min(δ0,δ1,δ2)`",
        "则 `0<|x-a|<δ ⇒ L-ε<φ(x)≤f(x)≤ψ(x)<L+ε`",
        "于是 `0<|x-a|<δ ⇒ |f(x)-L|<ε`",
        "因 `ε` 任意，故 `\\lim_{x→a} f(x)=L`",
    ],
    "1-15": [
        "先证必要性：设 `\\lim_{x→a} f(x)=L`",
        "任取数列 `x_n→a` 且 `x_n≠a`",
        "取任意 `ε>0`，存在 `δ>0` 使 `0<|x-a|<δ ⇒ |f(x)-L|<ε`",
        "因 `x_n→a`，存在 `N` 使 `n≥N ⇒ |x_n-a|<δ`",
        "对 `n≥N`，有 `0<|x_n-a|<δ`，从而 `|f(x_n)-L|<ε`",
        "因此 `f(x_n)→L`",
        "再证充分性：假设对任意 `x_n→a`（`x_n≠a`）都有 `f(x_n)→L`",
        "反设 `\\lim_{x→a} f(x)≠L`",
        "则存在 `ε0>0`，使得对任意 `δ>0`，都可取 `x` 满足 `0<|x-a|<δ` 且 `|f(x)-L|≥ε0`",
        "令 `δ=1/n`，对每个 `n` 取 `x_n` 使 `0<|x_n-a|<1/n` 且 `|f(x_n)-L|≥ε0`",
        "则 `x_n→a`，但 `f(x_n)` 不可能收敛到 `L`",
        "与假设矛盾",
        "故反设不成立，从而 `\\lim_{x→a} f(x)=L`",
    ],
    "1-16": [
        "先在 `0<x<\\pi/2` 情形证明",
        "在单位圆中取弧度为 `x` 的扇形",
        "由几何比较（弦、弧、切线）：`\\sin x < x < \\tan x`",
        "两边同除以 `\\sin x`（`\\sin x>0`）：`1 < x/\\sin x < 1/\\cos x`",
        "对正数取倒数（不等号反向）：`\\cos x < \\sin x/x < 1`",
        "令 `x→0^+`，有 `\\cos x→1`",
        "由夹逼定理：`\\lim_{x→0^+} \\sin x/x = 1`",
        "注意 `\\sin x/x` 为偶函数：`\\sin(-x)/(-x)=\\sin x/x`",
        "故 `\\lim_{x→0^-} \\sin x/x = 1`",
        "综合得 `\\lim_{x→0} \\sin x/x = 1`",
    ],
    "1-17": [
        "定义 `y(x)=(1+x)^{1/x}`（取 `x>-1` 且 `x≠0`）",
        "取对数：`\\ln y(x)=\\frac{\\ln(1+x)}{x}`",
        "考察极限 `\\lim_{x→0} \\frac{\\ln(1+x)}{x}`（为 `0/0` 型）",
        "用洛必达：`\\lim_{x→0} \\frac{\\ln(1+x)}{x} = \\lim_{x→0} \\frac{1/(1+x)}{1} = 1`",
        "因此 `\\lim_{x→0} \\ln y(x)=1`",
        "指数函数连续：`\\lim_{x→0} y(x)=\\lim_{x→0} e^{\\ln y(x)} = e^{1}=e`",
    ],
    "1-18": [
        "必要性：设 `\\lim_{x→a} f(x)=L`",
        "取任意 `ε>0`",
        "存在 `δ>0` 使 `0<|x-a|<δ ⇒ |f(x)-L|<ε/2`",
        "若 `0<|x-a|<δ` 且 `0<|y-a|<δ`，则",
        "`|f(x)-f(y)|=|(f(x)-L)-(f(y)-L)|`",
        "由三角不等式：`|f(x)-f(y)|≤|f(x)-L|+|f(y)-L|<ε`",
        "充分性：设满足 Cauchy 条件：对任意 `ε>0`，存在 `δ>0` 使上述不等式成立",
        "任取数列 `x_n→a` 且 `x_n≠a`",
        "由 Cauchy 条件：对任意 `ε>0`，存在 `N` 使 `m,n≥N ⇒ |f(x_n)-f(x_m)|<ε`",
        "故数列 `{f(x_n)}` 为 Cauchy 数列",
        "由实数完备性，存在 `L` 使 `f(x_n)→L`",
        "再取任意另一数列 `y_n→a`（`y_n≠a`），同理得 `f(y_n)→L'`",
        "用 Cauchy 条件取同一 `δ`，令 `x_n,y_n` 足够靠近 `a`，可得 `|f(x_n)-f(y_n)|→0`",
        "于是 `L=L'`（所有趋于 `a` 的序列像都趋于同一极限）",
        "由 Heine 定理知 `\\lim_{x→a} f(x)=L` 存在",
    ],
    "1-19": [
        "设 `f,g` 在点 `a` 连续",
        "由连续定义：`\\lim_{x→a} f(x)=f(a)`，`\\lim_{x→a} g(x)=g(a)`",
        "由极限四则运算：`\\lim_{x→a} (f(x)±g(x))=f(a)±g(a)`",
        "而 `(f±g)(a)=f(a)±g(a)`",
        "故 `f±g` 在 `a` 连续",
        "同理：`\\lim_{x→a} (f(x)g(x))=f(a)g(a)=(fg)(a)`",
        "故 `fg` 在 `a` 连续",
        "若 `g(a)≠0`，由极限商法则：`\\lim_{x→a} f(x)/g(x)=f(a)/g(a)=(f/g)(a)`",
        "故 `f/g` 在 `a` 连续（当 `g(a)≠0`）",
        "复合：若 `g` 在 `a` 连续且 `f` 在 `g(a)` 连续，则",
        "`\\lim_{x→a} f(g(x)) = f(\\lim_{x→a} g(x)) = f(g(a))`",
        "即 `f∘g` 在 `a` 连续",
    ],
    "1-20": [
        "设 `f` 在 `[a,b]` 连续，且 `f(a)≠f(b)`",
        "不妨设 `f(a)<f(b)`，取任意 `y` 满足 `f(a)<y<f(b)`",
        "定义集合 `S={x∈[a,b] | f(x)≤y}`",
        "有 `a∈S`，故 `S` 非空",
        "又 `S` 有上界 `b`，令 `c=sup S`",
        "由上确界性质，存在序列 `x_n∈S` 使 `x_n→c` 且 `x_n<c`",
        "由 `x_n∈S` 得 `f(x_n)≤y`，由连续性得 `f(c)=\\lim f(x_n)≤y`",
        "反设 `f(c)<y`",
        "取 `ε=y-f(c)>0`，由连续性存在 `δ>0` 使 `|x-c|<δ ⇒ |f(x)-f(c)|<ε`",
        "则 `x∈(c,c+δ)∩[a,b]` 时 `f(x)<f(c)+ε=y`，从而 `x∈S`",
        "这与 `c` 为 `S` 上确界矛盾（因为出现了 `>c` 的元素）",
        "故 `f(c)≥y`",
        "综上 `f(c)≤y` 且 `f(c)≥y`，得 `f(c)=y`",
    ],
    "1-21": [
        "设 `f` 在闭区间 `[a,b]` 连续",
        "先证有界：若不有界，则可取 `x_n` 使 `|f(x_n)|≥n`",
        "`[a,b]` 紧致，存在子列 `x_{n_k}→c∈[a,b]`",
        "由连续性 `f(x_{n_k})→f(c)` 为有限值",
        "但 `|f(x_{n_k})|≥n_k→∞`，矛盾",
        "故 `f([a,b])` 有界，令 `M=sup f([a,b])`",
        "由上确界定义，存在序列 `x_n∈[a,b]` 使 `f(x_n)→M`",
        "由紧致性，存在子列 `x_{n_k}→c∈[a,b]`",
        "由连续性：`f(x_{n_k})→f(c)`",
        "又因 `f(x_{n_k})→M`，故 `f(c)=M`",
        "于是最大值在 `c` 处取得",
        "同理令 `m=inf f([a,b])`，可得存在 `d` 使 `f(d)=m`",
        "故最小值也能取得",
    ],
    "1-22": [
        "设 `f` 在闭区间 `[a,b]` 连续，反设 `f` 不一致连续",
        "则存在 `ε0>0`，使得对任意 `δ>0`，都存在 `x,y∈[a,b]` 满足",
        "`|x-y|<δ` 且 `|f(x)-f(y)|≥ε0`",
        "令 `δ=1/n`，可取数列 `x_n,y_n∈[a,b]` 使 `|x_n-y_n|<1/n` 且 `|f(x_n)-f(y_n)|≥ε0`",
        "`[a,b]` 紧致，`{x_n}` 存在收敛子列 `x_{n_k}→c∈[a,b]`",
        "由 `|x_{n_k}-y_{n_k}|<1/n_k→0` 得 `y_{n_k}→c`",
        "由连续性：`f(x_{n_k})→f(c)` 且 `f(y_{n_k})→f(c)`",
        "于是 `|f(x_{n_k})-f(y_{n_k})|→0`",
        "这与 `|f(x_{n_k})-f(y_{n_k})|≥ε0` 矛盾",
        "故反设不成立，`f` 一致连续",
    ],
    "1-23": [
        "设 `f` 在区间 `I` 上单调递增（递减情形同理）",
        "对任意 `x0∈I`，定义左极限：`f(x0-)=sup_{x<x0} f(x)`",
        "定义右极限：`f(x0+)=inf_{x>x0} f(x)`",
        "由单调性知上确界与下确界均存在，故左右极限存在",
        "并有 `f(x0-)≤f(x0)≤f(x0+)`",
        "若 `f` 在 `x0` 不连续，则 `f(x0+)-f(x0-)=:J(x0)>0`（跳跃间断）",
        "对每个间断点 `x0`，在开区间 `(f(x0-), f(x0+))` 中选取一个有理数 `q(x0)`",
        "因为 `J(x0)>0`，该区间非空，必含有理数",
        "若 `x1<x2` 为两个不同间断点，由单调性可得",
        "`f(x1+)≤f(x2-)`，从而 `(f(x1-),f(x1+))` 与 `(f(x2-),f(x2+))` 不相交",
        "因此 `q(x1)≠q(x2)`，映射 `x0↦q(x0)` 是单射",
        "有理数集合 `ℚ` 可数",
        "故间断点集合至多可数",
        "又由上述讨论，间断只能为跳跃间断",
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

    # Keep everything up to PROOF_MARK (inclusive), then insert new proof steps,
    # then keep from EX_MARK onward.
    head = block[: p + 1]
    tail = block[e:]

    steps = [ensure_period(s) for s in PROOFS[tid] if s.strip()]
    proof_lines = [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    return head + proof_lines + tail


def main() -> None:
    lines = MD_PATH.read_text(encoding="utf-8").splitlines()

    thm_re = re.compile(r"^### 定理(\\d+-\\d+)")
    starts = [i for i, l in enumerate(lines) if thm_re.match(l)]
    start_set = set(starts)
    idx_to_id = {i: thm_re.match(lines[i]).group(1) for i in starts}  # type: ignore[union-attr]

    out: list[str] = []
    i = 0
    while i < len(lines):
        if i in start_set:
            tid = idx_to_id[i]
            # find end of theorem block
            j = i + 1
            while j < len(lines) and j not in start_set:
                j += 1
            block = lines[i:j]
            # rewrite only chapter 1 ids
            if tid.startswith("1-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter1 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("1-")))


if __name__ == "__main__":
    main()

