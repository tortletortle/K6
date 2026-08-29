# -*- coding: utf-8 -*-
"""
Rewrite proof sections for Chapter 11 theorems (11-1 .. 11-9) in
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
    "11-1": [
        "设级数 `∑ a_n` 收敛，记部分和 `S_n=∑_{k=1}^n a_k`",
        "则 `S_n→S`",
        "有 `a_n = S_n - S_{n-1}`",
        "由极限运算，`a_n → S - S = 0`",
        "故收敛级数必有 `a_n→0`",
    ],
    "11-2": [
        "设 `0≤a_n≤b_n` 且 `∑ b_n` 收敛",
        "记 `A_n=∑_{k=1}^n a_k`，`B_n=∑_{k=1}^n b_k`",
        "则 `0≤A_n≤B_n`",
        "`B_n` 收敛说明其有上界，故 `A_n` 单调递增且有上界",
        "于是 `A_n` 收敛，故 `∑ a_n` 收敛",
        "若 `∑ a_n` 发散到 `∞`，则 `B_n≥A_n→∞`，故 `∑ b_n` 发散",
    ],
    "11-3": [
        "设 `L=lim |a_{n+1}/a_n|` 存在",
        "若 `L<1`，取 `r` 使 `L<r<1`",
        "则存在 `N` 使 `n≥N` 时 `|a_{n+1}|≤r|a_n|`",
        "递推得 `|a_n|≤C r^n`（`C=|a_N|/r^N`）",
        "几何级数 `∑ C r^n` 收敛，故 `∑ |a_n|` 收敛",
        "若 `L>1`，则存在 `N` 使 `|a_{n+1}|≥(1+ε)|a_n|`",
        "于是 `|a_n|` 不趋于 0，级数发散",
    ],
    "11-4": [
        "设 `L=limsup |a_n|^{1/n}`",
        "若 `L<1`，取 `r` 使 `L<r<1`",
        "存在 `N` 使 `n≥N` 时 `|a_n|^{1/n}≤r`，故 `|a_n|≤r^n`",
        "与几何级数比较得 `∑ |a_n|` 收敛",
        "若 `L>1`，则存在子序列使 `|a_n|^{1/n}>1+ε`",
        "于是 `|a_n|` 不趋于 0，级数发散",
    ],
    "11-5": [
        "设 `f` 在 `[1,∞)` 正、单调递减，且 `a_n=f(n)`",
        "对每个 `n`，有 `∫_{n}^{n+1} f(x)dx ≤ a_n ≤ ∫_{n-1}^{n} f(x)dx`",
        "对 `n=1..N` 求和，得 `∫_1^{N+1} f(x)dx ≤ ∑_{n=1}^N a_n ≤ a_1 + ∫_1^{N} f(x)dx`",
        "令 `N→∞`，若积分收敛则级数收敛",
        "若积分发散，则下界趋于 `∞`，级数发散",
    ],
    "11-6": [
        "设 `a_n≥0` 单调递减且 `a_n→0`",
        "记部分和 `S_n=∑_{k=1}^n (-1)^{k-1} a_k`",
        "偶数部分和 `S_{2n}` 单调递增，且 `S_{2n}≤S_{2n+1}`",
        "奇数部分和 `S_{2n+1}` 单调递减，且 `S_{2n}≤S_{2n+1}`",
        "又有 `S_{2n+1}-S_{2n}=a_{2n+1}→0`",
        "故两列有共同极限，级数收敛",
    ],
    "11-7": [
        "设 `∑ |a_n|` 收敛，则其部分和 `T_n` 为 Cauchy 列",
        "给定 `ε>0`，存在 `N` 使 `m>n≥N` 时 `∑_{k=n+1}^m |a_k|<ε`",
        "由三角不等式，`|∑_{k=n+1}^m a_k| ≤ ∑_{k=n+1}^m |a_k| < ε`",
        "故 `∑ a_n` 的部分和列为 Cauchy 列",
        "实数完备性保证其收敛，故 `∑ a_n` 收敛",
    ],
    "11-8": [
        "设幂级数 `∑ a_n (x-x0)^n`，记 `L=limsup |a_n|^{1/n}`",
        "定义收敛半径 `R=1/L`（约定 `1/0=∞`，`1/∞=0`）",
        "若 `|x-x0|<R`，则 `limsup |a_n(x-x0)^n|^{1/n} = |x-x0| L < 1`",
        "由根值判别，级数绝对收敛",
        "若 `|x-x0|>R`，则 `|x-x0| L > 1`，项不趋于 0，级数发散",
    ],
    "11-9": [
        "设幂级数 `∑ a_n (x-x0)^n` 的收敛半径为 `R`",
        "对任意 `r<R`，在闭区间 `|x-x0|≤r` 上有一致收敛",
        "逐项求导得到 `∑ n a_n (x-x0)^{n-1}`，其收敛半径仍为 `R`",
        "由一致收敛与逐项求导定理，原级数可逐项求导",
        "同理逐项积分 `∫ ∑ a_n (x-x0)^n dx = ∑ a_n (x-x0)^{n+1}/(n+1) + C`",
        "故在 `|x-x0|<R` 内可逐项求导与积分，且半径不变",
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
            if tid.startswith("11-"):
                block = rewrite_proof_block(block, tid)
            out.extend(block)
            i = j
        else:
            out.append(lines[i])
            i += 1

    MD_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("chapter11 proofs rewritten:", sum(1 for k in PROOFS if k.startswith("11-")))


if __name__ == "__main__":
    main()
