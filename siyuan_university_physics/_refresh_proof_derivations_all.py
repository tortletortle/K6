# -*- coding: utf-8 -*-
"""Refresh (replace) proof/derivation blocks in all chapters.

We already have **推导详解（证明）** blocks. This script rewrites them to be
more detailed and more specific by using:
- title keyword matching
- derive-bullets pattern matching
- theme fallback

Output is UTF-8 and SiYuan-friendly Markdown.
"""

from __future__ import annotations

from pathlib import Path
import textwrap
import re

ROOT = Path(r"D:\spot\K6\siyuan_university_physics")
TOPICS = ROOT / "siyuan_topics_refined"

DOUBLE_TITLE = "## 本章加倍细化"
DERIVE_MARKER = "**推导要点**"
PROOF_MARKER = "**推导详解（证明）**"

FILE_THEME = {
    "00_foundations.md": "foundations",
    "01_kinematics.md": "mechanics",
    "02_newtonian_mechanics.md": "mechanics",
    "03_momentum_energy.md": "mechanics",
    "04_rigid_body_rotation.md": "mechanics",
    "05_gravitation.md": "mechanics",
    "06_thermodynamics.md": "thermo",
    "07_kinetic_theory.md": "thermo",
    "08_electrostatics.md": "em",
    "09_conductors_dielectrics.md": "em",
    "10_steady_current.md": "em",
    "11_magnetostatics.md": "em",
    "12_magnetic_materials.md": "em",
    "13_em_induction_em_field.md": "em",
    "14_mechanical_oscillation.md": "mechanics",
    "15_mechanical_waves.md": "waves",
    "16_em_oscillation_waves.md": "emwaves",
    "17_wave_optics.md": "optics",
    "18_relativity.md": "relativity",
    "19_quantum_physics.md": "quantum",
    "20_physics_and_technology.md": "tech",
    "A_constants_units.md": "constants",
}

THEME_FALLBACK = {
    "foundations": r"""
- 量纲一致性是所有推导的“底线检查”：把目标式的每一项写成 \(L^aM^bT^c\) 形式，必须完全一致。
- 小量近似用泰勒展开建立：\(f(x)\approx f(x_0)+f'(x_0)(x-x_0)\)，并明确误差阶（保留到几阶）。
- 误差传播可由一阶线性化得到：若 \(y=f(x_1,\dots,x_n)\)，则
$$
 u_y^2=\sum_i\left(\frac{\partial f}{\partial x_i}\right)^2u_{x_i}^2\quad(\text{独立误差})
$$
- 做完推导再做“极限检验”：参数趋零、趋大时是否回到熟悉的特例。
""",
    "mechanics": r"""
- 先写定义链：\(\vec v=d\vec r/dt\)、\(\vec a=d\vec v/dt\)、\(\sum\vec F=d\vec p/dt\)，把文字条件翻译成微分方程。
- 已知 \(\vec a(t)\) 时，先积分求速度再积分求位移：
$$
\vec v(t)=\vec v_0+\int_{0}^{t}\vec a(t')\,dt',\qquad
\vec r(t)=\vec r_0+\int_{0}^{t}\vec v(t')\,dt'
$$
- 若 \(\vec a\) 为常量，上式直接化简为常见运动学公式；若 \(a=a(x)\)，用链式法则 \(a=v\,dv/dx\) 走“相空间”推导。
- 动力学题优先画受力分析图，再按选定坐标分解 \(\sum F_x=ma_x\) 等，最后用初始条件定常数。
- 能量法来自对 \(\delta W=\vec F\cdot d\vec r\) 的积分，适合避开复杂约束力。
""",
    "thermo": r"""
- 先区分状态量与过程量：\(U,S,T,P,V\) 是状态量；\(\delta Q,\delta W\) 是过程量。
- 第一律：\(dU=\delta Q-\delta W\)。对准静体积功 \(\delta W=P\,dV\)，得 \(dU=\delta Q-P\,dV\)。
- 第二律用可逆过程建立：\(dS=\delta Q_{rev}/T\)，并用 \(\Delta S_{\text{isolated}}\ge 0\) 判断自发方向。
- 理想气体常用两条：\(PV=nRT\) 与 \(U=U(T)\)（单原子：\(U=\tfrac32nRT\)），配合过程方程做积分。
""",
    "waves": r"""
- 以“微元建模”导出波动方程：取 \(dx\) 微段，列出合力并用小斜率近似线性化。
- 得到形如 \(\partial^2 y/\partial t^2=v^2\partial^2 y/\partial x^2\) 后，行波解 \(f(x-vt)\) 自动成立。
- 叠加原理来自线性性，驻波由边界条件把允许的 \(k\) 离散化。
- 干涉/驻波问题的主线是相位差：\(\Delta\varphi=\omega\Delta t-k\Delta x\)。
""",
    "em": r"""
- 场论推导常走“定义 + 叠加 + 对称性”的路径：\(\vec E=\vec F/q\)、\(V=-W/q\)、\(\Phi_E=\oint\vec E\cdot d\vec A\)。
- 对称性决定高斯面/安培环路的选取，使积分化为乘法（把场强从积分号里提出）。
- 静电场满足 \(\oint\vec E\cdot d\vec l=0\)，因此 \(\vec E=-\nabla V\)。稳恒电流满足电荷守恒，从而导出结点方程。
- 电路推导本质是“守恒”：电荷守恒对应 KCL，能量守恒对应 KVL。
""",
    "emwaves": r"""
- 把电磁振荡/波动写成线性微分方程：LC 回路由 KVL 得二阶方程；电磁波由麦克斯韦方程取旋度得到波动方程。
- 能量交换与能流用 \(U_E, U_B\) 或坡印廷矢量 \(\vec S=\frac1{\mu_0}\vec E\times\vec B\) 解释最清楚。
- 阻尼项决定能量耗散，直接影响共振峰宽与品质因数 \(Q\)。
""",
    "optics": r"""
- 干涉先写光程差 \(\Delta\)，相位差 \(\Delta\varphi=2\pi\Delta/\lambda\)，再由 \(\cos\Delta\varphi\) 判明暗。
- 薄膜/反射必须检查是否发生 \(\pi\) 相位反转，这会把明暗条件整体互换。
- 远场衍射可视作孔径函数的傅里叶变换，暗纹条件往往来自相位相消配对。
- 分辨率由衍射极限给出，圆孔第一暗环 \(\theta\approx1.22\lambda/D\)。
""",
    "relativity": r"""
- 用光速不变与线性假设推出洛伦兹变换，并把主要结论写成不变量形式（\(s^2\)、\(E^2-(pc)^2\)）。
- 时间膨胀与尺缩来自同一变换，是参考系度量差异的结果，而不是“物理过程真的变慢”。
- 高速下优先用四动量守恒，避免混用经典能量与相对论动量。
""",
    "quantum": r"""
- 量子推导常从“驻波条件”出发：边界条件迫使波函数离散，从而能量或角动量量子化。
- 德布罗意关系 \(\lambda=h/p\) 连接粒子与波，配合驻波条件得到离散谱。
- 不确定关系可由波包傅里叶展开得到：\(\Delta x\Delta p\ge\hbar/2\)。
- 用 \(|\psi|^2\) 的概率解释与归一化确定常数，是定态问题的标准流程。
""",
    "tech": r"""
- 技术类推导强调“关键物理机制 + 工程近似”：写出决定性参数，再说明哪些效应被忽略。
- 推导结尾应明确适用范围（例如弱导近似、准静态、线性介质、忽略损耗等）。
- 若有多个指标（分辨率、带宽、效率），推导常体现为指标之间的权衡关系。
""",
    "constants": r"""
- 常数与单位推导重点是关系式与量纲一致：\(c^2=1/(\varepsilon_0\mu_0)\)、\(R=N_Ak_B\)。
- 用等式链做单位换算并保持量纲不变，是避免错一整个数量级的关键。
- 任何数值代入前先统一到 SI，再用数量级估算做 sanity check。
""",
}

# Section-id specific blocks (highest priority).
# Key by "§X-Y" (or "A-1") extracted from the subsection title.
#
# Notes:
# - Keep lines inside blocks free of standalone markdown headings ("###", "##")
#   and free of standalone bold markers ("**...**"), otherwise the refresh
#   script's block-skip logic may stop early on the next run.
SECTION_BLOCKS: dict[str, str] = {}

# "§3-10 ..." should not match "§3-1 ...", so we extract the exact id token.
_SEC_ID_RE = re.compile(r"^(§\d+-\d+)\s+")
_APP_ID_RE = re.compile(r"^(A-\d+)\s+")


def extract_section_id(title: str) -> str:
    m = _SEC_ID_RE.match(title)
    if m:
        return m.group(1)
    m = _APP_ID_RE.match(title)
    if m:
        return m.group(1)
    return ""


# -----------------------------------------------------------------------------
# Section Blocks (Full-Book Proof Library)
# -----------------------------------------------------------------------------
# Keep lines inside blocks free of markdown headings ("##/###") and standalone
# bold markers ("**...**"), otherwise the refresh script may stop early when
# removing old blocks on the next run.

# Chapter 0: Foundations
SECTION_BLOCKS.update(
    {
        "§0-1": r"""
- 物理建模常从“选对象、定边界、抓主导”开始：把研究对象从真实复杂系统中抽象出来，只保留对结果贡献最大的自由度与相互作用。
- 理想化不是“瞎简化”，而是有尺度依据的近似：若物体尺寸 \(l\) 远小于运动尺度 \(L\)（\(l/L\ll 1\)），可把物体视为质点；若转动细节重要，则升级为刚体模型。
- 把文字条件翻译成数学关系是关键一步：运动学用 \(\vec v=d\vec r/dt\)、\(\vec a=d\vec v/dt\)；动力学用 \(\sum\vec F=d\vec p/dt\)；热学用 \(dU=\delta Q-\delta W\)；电磁学用高斯/环路定理等积分关系。
- 许多“定律”在形式上就是微分方程：给定初始条件（\(t=t_0\) 时 \(\vec r,\vec v\) 或 \(Q,I\) 等），求解得到随时间演化的状态量，这称为初值问题。
- 例：抛体运动（忽略阻力）中 \(\vec a=(0,-g)\) 为常矢量，积分得
$$
x=v_0\cos\theta\,t,\qquad y=v_0\sin\theta\,t-\tfrac12gt^2
$$
消去 \(t\) 得轨迹 \(y=x\tan\theta-\frac{g}{2v_0^2\cos^2\theta}x^2\)。这一条“可检验预测”就是模型好坏的硬标准。
- 例：单摆（细绳、质点、无阻尼）满足转动方程 \(I\ddot\theta=\tau\)。取 \(I=ml^2\)、\(\tau=-mgl\sin\theta\)，得
$$
\ddot\theta+\frac{g}{l}\sin\theta=0
$$
小角近似 \(|\theta|\ll 1\) 时 \(\sin\theta\approx\theta\)，线性化为 \(\ddot\theta+\omega^2\theta=0\)，\(\omega=\sqrt{g/l}\)。
- 对称性是快速推理的“捷径”：若力为中心力 \(\vec F=F(r)\hat r\)，则力矩 \(\vec\tau=\vec r\times\vec F=0\)，由 \(d\vec L/dt=\vec\tau\) 得角动量守恒，进而面积速度恒定（开普勒第二定律的核心逻辑）。
- 推导完成后务必做三种检验：量纲检验（每项量纲一致）、极限检验（参数趋零/趋大回到熟悉特例）、数量级检验（代入典型值看是否离谱）。
""",
        "§0-2": r"""
- 量纲齐次性：任何物理公式两边必须具有相同量纲。把量写成 \([X]=L^aM^bT^cI^d\Theta^e\cdots\) 幂次形式即可系统检查。
- 例：速度 \([v]=LT^{-1}\)、加速度 \([a]=LT^{-2}\)、力 \([F]=MLT^{-2}\)（由 \(\sum\vec F=m\vec a\) 立得）、能量 \([E]=[F][L]=ML^2T^{-2}\)。
- 单位体系只是“刻度选择”，物理关系不变：\(1\,\mathrm{N}=1\,\mathrm{kg\cdot m/s^2}\)、\(1\,\mathrm{J}=1\,\mathrm{N\cdot m}\)、\(1\,\mathrm{W}=1\,\mathrm{J/s}\)。
- 量纲可用于“半推导”函数形式：设摆周期 \(T\) 仅与摆长 \(l\) 与重力加速度 \(g\) 有关，令 \(T\propto l^a g^b\)。比较量纲：
$$
[T]=[l]^a[g]^b=L^{a+b}T^{-2b}
$$
得 \(-2b=1\Rightarrow b=-\tfrac12\)，\(a+b=0\Rightarrow a=\tfrac12\)，因此 \(T\propto\sqrt{l/g}\)；精确动力学给出无量纲常数 \(2\pi\)。
- 对流体阻力的“数量级”也可由量纲看出：若阻力只由流体密度 \(\rho\)、迎风面积 \(A\)、速度 \(v\) 决定，则
$$
F\sim \rho A v^2
$$
（差一个无量纲阻力系数 \(C_D\)），这解释了高速时阻力近似与 \(v^2\) 成正比。
- 量纲是必要条件而非充分条件：量纲对了未必物理对（可能少了无量纲函数），但量纲不对一定错。
""",
        "§0-3": r"""
- 数量级分析的核心是“把精确方程变成尺度方程”：用特征尺度 \(L,T,V\) 估算导数大小，如 \(\dot x\sim L/T\)、\(\ddot x\sim L/T^2\)。
- 例：自由落体高度 \(h\) 的时间尺度由 \(h\sim \tfrac12 g t^2\) 给出 \(t\sim\sqrt{2h/g}\)。先估算再精算可快速排错。
- 若方程含多项，比较它们的尺度比值决定可忽略项：例如 \(A=B+C\)，若 \(|C/B|\sim\epsilon\ll1\)，则 \(A\approx B\) 且相对误差约 \(\epsilon\)。
- 非量纲化让“适用范围”一眼可见：令 \(x=L\tilde x\)、\(t=T\tilde t\)，把方程改写成只含无量纲参数（如 \(Re,Fr,Ma\) 等）的形式。
- 例：把惯性效应与黏性效应比值定义为雷诺数
$$
Re=\frac{\rho V L}{\eta}
$$
当 \(Re\ll 1\) 时黏性主导（阻力近似 \(\propto v\)），当 \(Re\gg 1\) 时惯性主导（阻力近似 \(\propto v^2\)）。
- 尺度分析常与泰勒展开结合：如小角近似 \(\sin\theta=\theta-\theta^3/6+\cdots\)，当 \(|\theta|\ll1\) 时保留一阶并明确忽略项为 \(O(\theta^3)\)。
""",
        "§0-4": r"""
- 直角坐标下 \(\vec r=x\hat i+y\hat j+z\hat k\)，基矢恒定，因此 \(\vec v=\dot x\hat i+\dot y\hat j+\dot z\hat k\)、\(\vec a=\ddot x\hat i+\ddot y\hat j+\ddot z\hat k\) 直接成立。
- 平面极坐标 \(\vec r=r\hat e_r\) 的难点在于基矢随 \(\theta\) 变：几何上有
$$
\dot{\hat e}_r=\dot\theta\,\hat e_\theta,\qquad \dot{\hat e}_\theta=-\dot\theta\,\hat e_r
$$
- 速度由乘积求导得
$$
\vec v=\dot{\vec r}=\dot r\,\hat e_r+r\dot\theta\,\hat e_\theta
$$
- 加速度对 \(\vec v\) 再求导（两项都要导，且基矢也要导）：
$$
\vec a=(\ddot r-r\dot\theta^2)\hat e_r+(r\ddot\theta+2\dot r\dot\theta)\hat e_\theta
$$
- 自然坐标（切向 \(\hat t\)、法向 \(\hat n\)）更贴近曲线运动本质。把速度写成 \(\vec v=v\hat t\)，则
$$
\vec a=\dot v\,\hat t+v\,\dot{\hat t}
$$
曲率半径 \(\rho\) 定义为 \(|d\hat t/ds|=1/\rho\)，又 \(ds/dt=v\)，因此 \(|\dot{\hat t}|=v/\rho\)，方向指向曲率中心，得到
$$
a_t=\dot v,\qquad a_n=\frac{v^2}{\rho}
$$
- 匀速圆周运动是 \(\dot v=0,\rho=r\)，立刻给出 \(a=v^2/r\) 指向圆心；这说明“方向变”同样会产生加速度。
""",
        "§0-5": r"""
- 设 \(y=f(x_1,\dots,x_n)\)，测量值附近作一阶泰勒展开：
$$
\delta y\approx \sum_i \frac{\partial f}{\partial x_i}\delta x_i
$$
- 若各 \(\delta x_i\) 独立、均值为 0，则方差（不确定度平方）近似为
$$
u_y^2=\langle(\delta y)^2\rangle\approx \sum_i\left(\frac{\partial f}{\partial x_i}\right)^2 u_{x_i}^2
$$
- 加减法最适合用绝对不确定度：\(y=x_1\pm x_2\Rightarrow u_y^2=u_1^2+u_2^2\)（独立时）。
- 乘除与幂函数最适合用相对不确定度：对 \(y=x_1x_2\) 或 \(y=x_1/x_2\)，取对数微分
$$
\frac{\delta y}{y}\approx \frac{\delta x_1}{x_1}\pm\frac{\delta x_2}{x_2}
$$
进而得到相对不确定度平方相加。
- 这一推导的适用前提是“小误差线性化”：若误差很大或函数高度非线性，需要保留更高阶项或用数值方法评估。
""",
        "§0-6": r"""
- 链式法则在物理推导里非常常见：若 \(v=v(x)\)，则 \(a=dv/dt=(dv/dx)(dx/dt)=v\,dv/dx\)，可把时间变量消去（运动学与能量法的桥梁）。
- 积分与初始条件：由 \(v=dx/dt\) 得 \(x(t)=x_0+\int_{t_0}^{t}v(t')dt'\)；积分常数都来自初始条件，这是“同一微分方程对应一族解”的根源。
- 泰勒展开提供小量近似：\(\sin\theta\approx\theta\)、\((1+\epsilon)^n\approx 1+n\epsilon\)（\(|\epsilon|\ll1\)），并应标注忽略项阶数。
- 向量算符 \(\nabla=(\partial_x,\partial_y,\partial_z)\) 定义梯度、散度、旋度：\(\nabla\phi\)、\(\nabla\cdot\vec A\)、\(\nabla\times\vec A\)。
- 高斯定理把体积分变成闭合曲面积分：
$$
\int_V\nabla\cdot\vec A\,d\tau=\oint_{\partial V}\vec A\cdot d\vec A
$$
斯托克斯定理把曲面积分变成边界线积分：
$$
\int_S(\nabla\times\vec A)\cdot d\vec A=\oint_{\partial S}\vec A\cdot d\vec l
$$
- 许多“场的微分形式”就是把积分定理套进去得到的：例如由 \(\oint\vec E\cdot d\vec l=0\) 得 \(\nabla\times\vec E=0\)，由 \(\oint\vec E\cdot d\vec A=q/\varepsilon_0\) 得 \(\nabla\cdot\vec E=\rho/\varepsilon_0\)。
""",
    }
)


# Chapter 1: Kinematics
SECTION_BLOCKS.update(
    {
        "§1-1": r"""
- 质点运动的数学描述从“位置随时间变化”开始：\(\vec r(t)\) 给出质点在选定参考系中的位置。
- 位移是端点差：\(\Delta\vec r=\vec r(t_2)-\vec r(t_1)\)；路程是轨迹长度 \(s=\int_{t_1}^{t_2}|\vec v|dt\)，二者在曲线运动中一般不同。
- 瞬时速度由极限定义：\(\vec v=d\vec r/dt\)。因此若已知 \(\vec r(t)\)，直接求导得到 \(\vec v(t)\)；若已知 \(\vec v(t)\)，积分得到 \(\vec r(t)\) 并由初始条件定常数：
$$
\vec r(t)=\vec r_0+\int_{t_0}^{t}\vec v(t')dt'
$$
- 加速度定义为 \(\vec a=d\vec v/dt=d^2\vec r/dt^2\)。这意味着“速度大小变”与“速度方向变”都会造成加速度。
- 速率是速度大小：\(v=|\vec v|\)。它等于弧长变化率：\(v=ds/dt\)，其中 \(ds=|d\vec r|\)。
- 曲线运动用自然坐标最清晰：\(\vec v=v\hat t\)。对时间求导：
$$
\vec a=\dot v\,\hat t+v\,\dot{\hat t}
$$
曲率半径 \(\rho\) 给出 \(|\dot{\hat t}|=v/\rho\)，因此
$$
a_t=\dot v,\qquad a_n=\frac{v^2}{\rho}
$$
其中 \(a_n\) 指向曲率中心（拐弯方向）。
- 坐标变换只改变分量表达，不改变几何事实：同一条轨迹在直角、极坐标、自然坐标下写法不同，但 \(\vec r,\vec v,\vec a\) 的物理意义一致。
""",
        "§1-2": r"""
- 恒加速度运动的核心是假设 \(\vec a\) 为常矢量（方向与大小均不随时间变），微分方程是 \(d\vec v/dt=\vec a\)。
- 对时间积分得到速度：
$$
\vec v(t)=\vec v_0+\int_0^t\vec a\,dt'=\vec v_0+\vec a\,t
$$
- 再积分得到位置：
$$
\vec r(t)=\vec r_0+\int_0^t\vec v(t')dt'=\vec r_0+\vec v_0 t+\tfrac12\vec a\,t^2
$$
- 一维消去时间常用链式法则：\(a=dv/dt=(dv/dx)(dx/dt)=v\,dv/dx\)，从而
$$
v\,dv=a\,dx\Rightarrow v^2=v_0^2+2a(x-x_0)
$$
- 抛体运动是二维恒加速度的分量叠加：取 \(a_x=0,a_y=-g\)，得到
$$
x=v_0\cos\theta\,t,\qquad y=v_0\sin\theta\,t-\tfrac12gt^2
$$
消去 \(t\) 得轨迹方程 \(y=x\tan\theta-\frac{g}{2v_0^2\cos^2\theta}x^2\)。
- 恒加速度公式的适用条件必须检查：若加速度随速度（阻力）或随位置（变场）变化，应回到积分形式或建立新的微分方程求解。
""",
        "§1-3": r"""
- 圆周运动最直接的推导在极坐标下完成：\(r=\text{常量}\)，角位置 \(\theta(t)\) 决定运动。
- 定义角速度与角加速度：\(\omega=d\theta/dt\)、\(\alpha=d\omega/dt\)。
- 由速度表达式 \(\vec v=r\omega\,\hat e_\theta\)，速率 \(v=r\omega\)。
- 对 \(\vec v\) 求导并用 \(\dot{\hat e}_\theta=-\omega\hat e_r\)，得到
$$
\vec a=r\alpha\,\hat e_\theta-r\omega^2\,\hat e_r
$$
- 因而切向加速度 \(a_t=r\alpha=dv/dt\) 决定速率变化；向心加速度
$$
a_n=r\omega^2=\frac{v^2}{r}
$$
决定方向变化，始终指向圆心。
- 匀速圆周运动是 \(\alpha=0\)，仍有 \(\vec a=-r\omega^2\hat e_r\neq 0\)。这就是“匀速但不匀向”的典型。
- 动力学中的向心力不是新力，而是合力的径向分量：\(F_n=ma_n\)。
""",
        "§1-4": r"""
- 相对运动的“证明”从位置叠加开始：\(\vec r_{PE}=\vec r_{PT}+\vec r_{TE}\)（P 相对地面 E 的位置等于 P 相对载体 T 的位置加上 T 相对 E 的位置）。
- 对时间求导得到速度叠加：
$$
\vec v_{PE}=\vec v_{PT}+\vec v_{TE}
$$
这就是伽利略速度变换的矢量版。
- 若两参考系之间只有平移且不相对转动，再求导得到加速度叠加：
$$
\vec a_{PE}=\vec a_{PT}+\vec a_{TE}
$$
- 两惯性系之间是匀速相对运动：\(\vec r'=\vec r-\vec V t\Rightarrow \vec v'=\vec v-\vec V,\ \vec a'=\vec a\)。因此经典力学中惯性系间加速度不变。
- 若参考系还发生转动（角速度 \(\vec\omega\)），时间导数需要加 \(\vec\omega\times\) 修正，进而出现科里奥利项等附加加速度；这正是非惯性系惯性力的来源。
""",
    }
)

# Chapter 2: Newtonian mechanics
SECTION_BLOCKS.update(
    {
        "§2-1": r"""
- 牛顿第二定律最稳健的表述是动量形式：
$$
\sum\vec F=\frac{d\vec p}{dt}
$$
其中 \(\vec p=m\vec v\)。
- 若 \(m\) 不随时间变，则 \(\frac{d\vec p}{dt}=m\frac{d\vec v}{dt}=m\vec a\)，得到常用形式 \(\sum\vec F=m\vec a\)。
- 对时间积分得到冲量-动量定理：
$$
\int_{t_1}^{t_2}\sum\vec F\,dt=\Delta\vec p
$$
冲量反映“力在时间上的积累”，碰撞问题优先用它。
- 第一、第二定律共同刻画惯性系：在惯性系中 \(\sum\vec F=0\Rightarrow \vec v=\text{常矢量}\)。反之，若某参考系中自由粒子不做匀速直线，则该系不是惯性系（或需加入惯性力）。
- 第三定律（经典近似）保证内力成对出现且反向，共同导致封闭系统总动量只受外力影响：\(\dot{\vec P}=\sum\vec F_{\text{ext}}\)。
""",
        "§2-2": r"""
- 由基本单位 \(kg,m,s\) 可推导力学常用派生单位：\(1\,N=1\,kg\cdot m/s^2\)，\(1\,J=1\,N\cdot m\)，\(1\,W=1\,J/s\)。
- 动量 \([p]=MLT^{-1}\)、角动量 \([L]=ML^2T^{-1}\)、功/能量 \([E]=ML^2T^{-2}\)、功率 \([P]=ML^2T^{-3}\)。
- 量纲检验用于公式排错：若某项量纲与目标量不同，则该推导或抄写必有问题。
- 量纲还能反推出常数单位：例如 \(F=GmM/r^2\Rightarrow [G]=M^{-1}L^3T^{-2}\)；写对单位可避免数值代入错数量级。
""",
        "§2-3": r"""
- 重力（近地面）\(\vec G=m\vec g\) 方向固定向下，属于场力；它的功只与高度差有关，因此可定义势能 \(U=mgh\)（差常数）。
- 弹簧在小形变范围满足胡克定律 \(F=-kx\)。由 \(\delta W=Fdx\) 得势能
$$
U(x)=\int_0^x kx'\,dx'=\tfrac12kx^2
$$
因此弹簧力是保守力。
- 支持力、拉力多来自约束。它们的大小一般不能先验给出，需要与 \(\sum\vec F=m\vec a\) 和约束条件联立求解；“静止/匀速”只是 \(a=0\) 的特例。
- 摩擦力模型是经验规律：动摩擦 \(f_k=\mu_k N\)；静摩擦满足 \(|f_s|\le \mu_s N\)，且其大小由“恰好满足不滑动”确定（因此静摩擦不是固定值）。
- 阻力常用两类近似：层流低速 \(F\propto v\)（如 \(6\pi\eta rv\)），湍流高速 \(F\propto v^2\)（数量级 \(F\sim\rho A v^2\)）。选择模型要看速度范围与介质状态。
""",
        "§2-4": r"""
- 两惯性系 S 与 S' 若相对做匀速直线运动，伽利略变换写为 \(\vec r'=\vec r-\vec V t,\ t'=t\)。
- 求导得 \(\vec v'=\vec v-\vec V\)，再求导得 \(\vec a'=\vec a\)。这就是经典力学中“惯性系间加速度不变”的数学事实。
- 若力的形式只依赖相对位置（以及在经典近似下的相对速度），则两系中受力相同，故
$$
\sum\vec F'=m\vec a' \iff \sum\vec F=m\vec a
$$
牛顿方程形式在惯性系间保持不变，这就是力学相对性原理。
- 该结论解释了为什么很多工程问题可以把地面系近似当惯性系：只要研究时间短、尺度小，地球自转/公转导致的非惯性效应可忽略。
""",
        "§2-5": r"""
- 牛顿定律应用的推导流程固定：画受力分析图 \(\Rightarrow\) 选坐标 \(\Rightarrow\) 写分量方程 \(\Rightarrow\) 联立约束 \(\Rightarrow\) 用初始条件定解。
- 斜面无摩擦：沿斜面方向 \(mg\sin\theta=ma\Rightarrow a=g\sin\theta\)；法向 \(N=mg\cos\theta\)。
- 斜面有动摩擦：沿斜面 \(mg\sin\theta-\mu_k mg\cos\theta=ma\Rightarrow a=g(\sin\theta-\mu_k\cos\theta)\)。
- 阿特伍德机：列
$$
m_2g-T=m_2a,\qquad T-m_1g=m_1a
$$
解得 \(a=\frac{(m_2-m_1)g}{m_1+m_2}\) 与张力 \(T=\frac{2m_1m_2}{m_1+m_2}g\)。
- 圆周运动动力学：径向方程永远是 \(\sum F_n=mv^2/r\)，把“提供向心加速度的那部分合力”投影到径向即可。
- 约束条件常给出额外方程：轻绳不可伸长给 \(a_1=a_2\)（或相反号），纯滚动给 \(v_{cm}=\omega R\)。不写约束，方程组不闭合。
""",
        "§2-6": r"""
- 平移加速参考系：若 S' 相对惯性系 S 以加速度 \(\vec a_0\) 运动，则同一质点满足 \(\vec a=\vec a'+\vec a_0\)。
- 代入 \(\sum\vec F=m\vec a\) 得 \(\sum\vec F-m\vec a_0=m\vec a'\)。于是定义惯性力 \(\vec F_{\text{in}}=-m\vec a_0\)，使 S' 中仍可写成 \(\sum\vec F+\vec F_{\text{in}}=m\vec a'\)。
- 旋转参考系：惯性系与旋转系导数关系
$$
\left(\frac{d\vec A}{dt}\right)_{\!S}=\left(\frac{d\vec A}{dt}\right)_{\!S'}+\vec\omega\times\vec A
$$
对 \(\vec r\) 与 \(\vec v\) 依次应用可得
$$
\vec a=\vec a'+2\vec\omega\times\vec v'+\vec\omega\times(\vec\omega\times\vec r)+\dot{\vec\omega}\times\vec r
$$
- 三个额外项对应三种惯性力：
$$
\vec F_C=-2m\vec\omega\times\vec v',\quad
\vec F_{cf}=-m\vec\omega\times(\vec\omega\times\vec r),\quad
\vec F_E=-m\dot{\vec\omega}\times\vec r
$$
分别为科里奥利力、离心力、欧拉力。
- 这些力不是新相互作用，只是非惯性系中“把运动学差别挪到力这一边”的记账方式；方向判断靠叉乘规则最可靠。
""",
    }
)

# Chapter 3: Momentum & energy
SECTION_BLOCKS.update(
    {
        "§3-1": r"""
- 从牛顿第二定律动量形式 \(\sum\vec F=d\vec p/dt\) 出发，两端从 \(t_1\) 到 \(t_2\) 积分：
$$
\int_{t_1}^{t_2}\sum\vec F\,dt=\vec p_2-\vec p_1\equiv \Delta\vec p
$$
- 定义冲量 \(\vec J\equiv\int_{t_1}^{t_2}\sum\vec F\,dt\)，则 \(\vec J=\Delta\vec p\)。冲量是“力随时间的累积效应”。
- 若力近似恒定，\(\vec J\approx \vec F_{\text{avg}}\Delta t\)。因此碰撞中“峰值力”很大但不稳定，冲量更稳健。
- 对质点系总动量 \(\vec P=\sum_i\vec p_i\)，求和各质点方程并用内力成对相消，得
$$
\frac{d\vec P}{dt}=\sum\vec F_{\text{ext}}
$$
这就是质点系动量定理。
""",
        "§3-2": r"""
- 由质点系动量定理 \(\dot{\vec P}=\sum\vec F_{\text{ext}}\)，若系统合外力为零，则 \(\dot{\vec P}=0\Rightarrow \vec P=\text{常矢量}\)。
- 更一般地，若外力不为零但外力冲量可忽略，则 \(\Delta\vec P\approx 0\) 仍近似守恒；这正是很多碰撞题成立的物理基础。
- 动量守恒是矢量守恒：在任意坐标方向上各分量都分别守恒，因此解题时可按分量列方程。
- 关键判据是“外力冲量是否可忽略”，而不是“外力是否存在”；例如重力存在但碰撞时间极短时，重力冲量远小于内力冲量，可忽略。
""",
        "§3-3": r"""
- 火箭方程来自“短时间内对系统用动量守恒”。设时刻 \(t\) 火箭质量 \(m\)、速度 \(v\)。
- 在 \(dt\) 内火箭喷出质量 \(-dm\)（\(dm<0\)），喷气相对火箭速度为 \(u\)（方向与火箭速度相反），则喷气在惯性系速度近似为 \(v-u\)。
- 对“火箭+喷气”整体（忽略外力）写动量守恒：
$$
mv=(m+dm)(v+dv)+(-dm)(v-u)
$$
- 展开并忽略二阶小量 \(dm\,dv\)，整理得
$$
m\,dv=-u\,dm
$$
- 积分得到理想火箭方程：
$$
v-v_0=u\ln\frac{m_0}{m}
$$
- 若存在外力（重力、阻力），应在动量方程中加入外力冲量项，火箭方程变为含外力积分的形式。
""",
        "§3-4": r"""
- 由 \(\sum\vec F=m\,d\vec v/dt\) 两端点乘 \(\vec v\)，得
$$
\sum\vec F\cdot\vec v=m\frac{d\vec v}{dt}\cdot\vec v=\frac{d}{dt}\left(\tfrac12mv^2\right)
$$
- 又因 \(d\vec r=\vec v\,dt\)，有 \(\sum\vec F\cdot\vec v\,dt=\sum\vec F\cdot d\vec r\equiv \delta W\)。
- 因此微元形式为 \(\delta W=d(\tfrac12mv^2)\)，积分得到动能定理：
$$
W_{1\to2}=\int_1^2 \sum\vec F\cdot d\vec r=\Delta K
$$
- 该定理对变力同样成立；“做功”本质是力沿位移方向的能量转移。
""",
        "§3-5": r"""
- 保守力的定义是做功与路径无关。等价地，对任意闭合回路有
$$
\oint \vec F\cdot d\vec r=0
$$
- 因此可以定义势能 \(U\) 使 \(\Delta U=-W\)，即
$$
U(\vec r)=-\int_{\vec r_0}^{\vec r}\vec F\cdot d\vec r'+\text{常数}
$$
- 写成微分形式：\(dU=-\vec F\cdot d\vec r\)。与全微分 \(dU=\nabla U\cdot d\vec r\) 对比得
$$
\vec F=-\nabla U
$$
- 在单连通区域内，\(\vec F=-\nabla U\) 等价于 \(\nabla\times\vec F=0\)。这是判断力是否保守的微分判据。
- 典型保守力：重力（近地面 \(U=mgh\)）、弹簧力（\(U=\tfrac12kx^2\)）、万有引力（\(U=-GMm/r\)）。摩擦与阻力一般非保守。
""",
        "§3-6": r"""
- 动能定理给 \(\Delta K=W=W_c+W_{nc}\)。对保守力 \(W_c=-\Delta U\)，代入得
$$
\Delta K=-\Delta U+W_{nc}
$$
- 移项得到功能原理（机械能形式）：
$$
\Delta(K+U)=W_{nc}
$$
- 若非保守力不做功（或其功可忽略），则 \(W_{nc}=0\Rightarrow K+U=\text{常量}\)，即机械能守恒。
- 这也解释了能量法的优势：很多理想约束力（如光滑支持力、理想绳张力在某些方向上）不做功，可直接绕开它们求速度与位移。
""",
        "§3-7": r"""
- 碰撞的首要守恒量是动量：相互作用时间短时常取外力冲量可忽略，从而总动量守恒。
- 一维两物体 \(m_1,m_2\)：动量守恒
$$
m_1v_1+m_2v_2=m_1v_1'+m_2v_2'
$$
- 完全弹性碰撞再加动能守恒，联立可解得
$$
v_1'=\frac{m_1-m_2}{m_1+m_2}v_1+\frac{2m_2}{m_1+m_2}v_2,\quad
v_2'=\frac{2m_1}{m_1+m_2}v_1+\frac{m_2-m_1}{m_1+m_2}v_2
$$
- 完全非弹性碰撞（粘连）末速度为
$$
v'=\frac{m_1v_1+m_2v_2}{m_1+m_2}
$$
动能减少转化为内能、形变、声等。
- 更一般用恢复系数 \(e\) 描述部分弹性碰撞：\(e=(v_2'-v_1')/(v_1-v_2)\)，与动量守恒联立可统一求解。
""",
        "§3-8": r"""
- 能量守恒的写法依赖系统边界：只要把所有能量形式都算进系统，总能量变化为 0（孤立系统）。
- 在力学范围内，由 \(\Delta(K+U)=W_{nc}\) 可看出非保守力做功会改变机械能。
- 若把非保守力所“损失”的机械能计入系统内能增加 \(\Delta U_{\text{int}}=-W_{nc}\)，则
$$
\Delta(K+U+U_{\text{int}})=0
$$
这就是“机械能不守恒但总能量守恒”的统一表述。
- 因此做题时要先讲清：摩擦生热算在系统内（内能上升）还是算向外界散热（热量流出），两种写法等价但符号不同。
""",
        "§3-9": r"""
- 定义质心：
$$
\vec R_{cm}=\frac{1}{M}\sum_i m_i\vec r_i,\quad M=\sum_i m_i
$$
- 求导得到质心速度 \(\vec V_{cm}=\frac{1}{M}\sum_i m_i\vec v_i=\vec P/M\)。
- 再求导并用 \(\dot{\vec P}=\sum\vec F_{\text{ext}}\) 得质心运动定律：
$$
M\vec A_{cm}=\sum \vec F_{\text{ext}}
$$
- 这表明系统整体平动只由外力决定；内力只能改变系统内部相对运动，不能改变质心加速度。
- 两体问题常用质心系与相对坐标，把问题降为“约化质量 \(\mu\) 的等效单粒子运动”，是守恒量方法的进一步应用。
""",
    }
)


# Chapter 4: Rigid body rotation
SECTION_BLOCKS.update(
    {
        "§4-1": r"""
- 定轴转动用角变量描述：角位移 \(\theta\)、角速度 \(\omega=d\theta/dt\)、角加速度 \(\alpha=d\omega/dt\)。
- 刚体上距转轴垂直距离为 \(r\) 的质点做圆周运动，弧长 \(s=r\theta\)，因此线速度大小
$$
v=\frac{ds}{dt}=r\frac{d\theta}{dt}=r\omega
$$
- 切向加速度来自速率变化：\(a_t=dv/dt=r\,d\omega/dt=r\alpha\)。
- 法向（向心）加速度来自方向变化：圆周运动给 \(a_n=v^2/r=r\omega^2\)，方向指向转轴。
- 用矢量形式更统一：\(\vec v=\vec\omega\times\vec r\)。若 \(\vec\omega\) 与 \(\vec\alpha\) 沿转轴方向，则
$$
\vec a=\vec\alpha\times\vec r+\vec\omega\times(\vec\omega\times\vec r)
$$
第一项为切向分量，第二项为向心分量。
- 当 \(\alpha\) 为常量时，角运动与直线恒加速度完全类比：\(\omega=\omega_0+\alpha t\)、\(\theta=\theta_0+\omega_0t+\tfrac12\alpha t^2\)。
""",
        "§4-2": r"""
- 力矩定义为 \(\vec\tau=\vec r\times\vec F\)。对质点角动量 \(\vec L=\vec r\times\vec p\) 求导：
$$
\frac{d\vec L}{dt}=\vec r\times\frac{d\vec p}{dt}+\vec v\times\vec p
$$
而 \(\vec v\times\vec p=\vec v\times m\vec v=0\)，所以
$$
\frac{d\vec L}{dt}=\vec r\times\sum\vec F\equiv \sum\vec\tau
$$
- 对刚体绕固定轴转动，把系统分解为许多质点：轴向角动量
$$
L=\sum_i m_i r_{\perp i}^2\,\omega \equiv I\omega
$$
其中定义转动惯量 \(I=\sum_i m_i r_{\perp i}^2\)，连续体写作 \(I=\int r_\perp^2\,dm\)。
- 对时间求导得转动定律（定轴）：
$$
\sum\tau=\frac{dL}{dt}=\frac{d(I\omega)}{dt}=I\alpha
$$
（这里用到 \(I\) 对定轴刚体为常量）。
- 平行轴定理来自把 \(r_\perp^2\) 在质心轴与平行轴间展开：结论 \(I=I_{cm}+Md^2\)，其中 \(d\) 为两轴距离。
""",
        "§4-3": r"""
- 角动量定义 \(\vec L=\sum_i \vec r_i\times\vec p_i\)。由上一节推导得到一般关系
$$
\frac{d\vec L}{dt}=\sum\vec\tau_{\text{ext}}
$$
即角动量定理。
- 若合外力矩为零，则 \(d\vec L/dt=0\Rightarrow \vec L=\text{常矢量}\)，这就是角动量守恒。
- 定轴刚体有 \(L=I\omega\)（方向沿转轴）。因此当外力矩为零时 \(I\omega=\text{常量}\)，典型现象是“收臂加速”：\(I\) 减小则 \(\omega\) 增大。
- 对质点系，若外力矩相对某点为零（或可忽略），则相对该点的角动量守恒；选择取矩点能简化计算（如碰撞中取接触点消去冲量力矩）。
""",
        "§4-4": r"""
- 转动功的微元定义与平动类比：\(\delta W=\tau\,d\theta\)（定轴时 \(\tau\) 为轴向力矩）。
- 用转动定律 \(\tau=I\alpha=I\,d\omega/dt\)，并用 \(d\theta=\omega\,dt\)，得
$$
\delta W=I\frac{d\omega}{dt}\,\omega\,dt=I\omega\,d\omega=d\left(\tfrac12 I\omega^2\right)
$$
- 积分得到刚体定轴转动的动能定理：
$$
W_{1\to2}=\int_{\theta_1}^{\theta_2}\tau\,d\theta=\tfrac12 I\omega_2^2-\tfrac12 I\omega_1^2\equiv \Delta K_{rot}
$$
- 因此转动动能自然定义为 \(K_{rot}=\tfrac12 I\omega^2\)。这与把刚体分解为质点、求和 \(\sum\tfrac12 m_iv_i^2\) 完全一致。
""",
        "§4-5": r"""
- 平面平行运动可分解为“质心平动 + 绕质心转动”：任一点速度
$$
\vec v=\vec V_{cm}+\vec\omega\times\vec r'
$$
其中 \(\vec r'\) 是该点相对质心的位置矢量。
- 刚体动能由质点求和：
$$
K=\sum\tfrac12 m_i v_i^2=\tfrac12 M V_{cm}^2+\tfrac12 I_{cm}\omega^2
$$
交叉项为零来自质心定义 \(\sum m_i\vec r'_i=0\)。
- 纯滚动（无滑动）约束来自接触点瞬时速度为零：因此 \(V_{cm}=\omega R\)。
- 纯滚动问题常用能量法：\(\tfrac12 M V_{cm}^2+\tfrac12 I_{cm}\omega^2+U=\text{常量}\)；若有静摩擦但无滑动，静摩擦通常不做功（接触点相对位移为零）。
""",
        "§4-6": r"""
- 经典力学的适用条件可用“无量纲小参数”刻画：相对论效应小要求 \(\beta=v/c\ll 1\)；量子效应小常要求德布罗意波长 \(\lambda=h/p\) 远小于系统特征尺度 \(L\)（\(\lambda/L\ll 1\)）。
- 例如相对论能量 \(E=\gamma mc^2\)，在 \(v\ll c\) 下展开 \(\gamma\approx 1+\tfrac12\beta^2\)，得到动能
$$
K=E-mc^2\approx \tfrac12mv^2
$$
这说明经典表达式是相对论的低速极限。
- 量子力学中角动量、能量出现离散，经典连续图像在宏观极限下通过“量子数很大/相位快速振荡”回到经典结果（对应 \(\hbar\to 0\) 的极限思想）。
""",
    }
)

# Chapter 5: Gravitation
SECTION_BLOCKS.update(
    {
        "§5-1": r"""
- 行星运动受中心力 \(\vec F=F(r)\hat r\) 作用，力矩 \(\vec\tau=\vec r\times\vec F=0\)，因此角动量守恒：\(\vec L=m r^2\dot\theta\,\hat z=\text{常量}\)。
- 面积速度为 \(\dot A=\tfrac12 r^2\dot\theta=\tfrac{L}{2m}\)，因此为常量，这就是开普勒第二定律（等面积定律）的动力学根源。
- 对圆轨道，用向心条件 \(mv^2/r=GMm/r^2\) 得
$$
v=\sqrt{\frac{GM}{r}},\quad \omega=\sqrt{\frac{GM}{r^3}},\quad T=\frac{2\pi}{\omega}
$$
从而 \(T^2=\frac{4\pi^2}{GM}r^3\)，这给出开普勒第三定律的形式（椭圆轨道把 \(r\) 替换为半长轴 \(a\)）。
- 开普勒第一定律（椭圆轨道）更深层来自反平方中心力的轨道方程 \(r=\frac{p}{1+e\cos\theta}\)，其推导见后续小节。
""",
        "§5-2": r"""
- 对球对称质量分布，外部引力场必径向且仅与 \(r\) 有关：\(\vec g(r)=g(r)\hat r\)。
- 选半径为 \(r\) 的球面为高斯面（引力版）：通量 \(\Phi_g=\oint \vec g\cdot d\vec A=g(r)4\pi r^2\)。
- 由反平方律可知通量与包围质量成正比：\(g(r)4\pi r^2=4\pi G M\)，从而
$$
g(r)=\frac{GM}{r^2}
$$
这就是“球对称体外场等效于质点在中心”的结论（壳层定理的结果之一）。
- 若球体密度均匀，内部半径 \(r\) 处只受内部质量 \(M(r)=\frac43\pi r^3\rho\) 作用，因此
$$
g(r)=\frac{GM(r)}{r^2}=\frac43\pi G\rho\,r
$$
内部场强与 \(r\) 成正比。
""",
        "§5-3": r"""
- 引力场强定义为单位质量所受引力：\(\vec g=\vec F/m\)。对点质量 \(M\)，\(\vec g=-GM/r^2\,\hat r\)。
- 引力势能来自“保守力做功与路径无关”：定义势函数 \(\Phi\) 使 \(\vec g=-\nabla\Phi\)，并令 \(\Phi(\infty)=0\)。
- 由 \(\vec g=-GM/r^2\,\hat r\)，沿径向积分得
$$
\Phi(r)=-\int_\infty^r \vec g\cdot d\vec r'=-\int_\infty^r \left(-\frac{GM}{r'^2}\right)dr'=-\frac{GM}{r}
$$
- 质量 \(m\) 在该场中的势能 \(U=m\Phi=-GMm/r\)。因此引力做功
$$
W_{1\to2}=\int_1^2 \vec F\cdot d\vec r=-\Delta U
$$
与势能变化相反。
""",
        "§5-4": r"""
- 两体系统势能（取无穷远为零）为
$$
U(r)=-\frac{Gm_1m_2}{r}
$$
其中 \(r\) 是两体间距离。
- 多体系统总引力势能为所有成对势能之和：
$$
U_{\text{tot}}=-G\sum_{i<j}\frac{m_im_j}{r_{ij}}
$$
- 力可由势能对坐标的梯度给出：对粒子 \(i\)，
$$
\vec F_i=-\nabla_i U_{\text{tot}}
$$
这体现“保守力 = 势能梯度”的一般规律。
""",
        "§5-5": r"""
- 反平方中心力的轨道方程可用 Binet 公式推导。设 \(u=1/r\)，角动量守恒给 \(r^2\dot\theta=h\)（常量）。
- 对中心力 \(F(r)=-GMm/r^2\)，可得到关于 \(u(\theta)\) 的方程
$$
\frac{d^2u}{d\theta^2}+u=\frac{GM}{h^2}
$$
- 解为
$$
u(\theta)=\frac{GM}{h^2}\left(1+e\cos\theta\right)\Rightarrow
r(\theta)=\frac{p}{1+e\cos\theta},\quad p=\frac{h^2}{GM}
$$
这就是圆锥曲线轨道（\(0\le e<1\) 为椭圆）。
- 面积速度恒定来自 \(\dot A=\tfrac12r^2\dot\theta=\tfrac12h\) 不变，与开普勒第二定律一致。
""",
    }
)

# Chapter 6: Thermodynamics
SECTION_BLOCKS.update(
    {
        "§6-1": r"""
- 理想气体的状态方程可由经验定律组合得到：玻意耳定律（等温）\(pV=\text{常量}\)、查理定律（等压）\(V\propto T\)、盖-吕萨克定律（等容）\(p\propto T\)。
- 统一写成 \(pV\propto T\)，引入物质的量 \(n\) 作为“多少气体”的度量，得到
$$
pV=nRT
$$
其中 \(R\) 为普适气体常数。
- 平衡态的数学含义是：系统宏观参量 \(p,V,T\) 在时间上不再发生自发变化（或变化极慢），且系统内部无明显宏观流动；这使得状态方程有意义。
- 理想气体模型的关键假设是：分子体积可忽略、相互作用可忽略（除弹性碰撞），因此许多性质只由 \(T\) 决定（如 \(U=U(T)\)）。
""",
        "§6-2": r"""
- 准静态过程的含义是过程足够慢，使系统在每一瞬间都可近似看作处于平衡态；因此可以使用状态参量 \(p,V,T\) 描述过程并在 \(p\text{-}V\) 图上表示。
- 体积功来自外界压强对体积变化所做的功（约定系统对外做功为正）：
$$
\delta W=p\,dV
$$
- 因此从 1 到 2 的功为路径积分：
$$
W_{1\to2}=\int_1^2 p\,dV
$$
几何上等于 \(p\text{-}V\) 图下的面积，说明功与路径有关。
- 热量 \(Q\) 不是状态量，而是过程量：它表示由于温差导致的能量传递；同一初末态不同路径的 \(Q\) 一般不同。
""",
        "§6-3": r"""
- 热力学第一定律是能量守恒在热过程中的表述（系统对外做功为正）：
$$
dU=\delta Q-\delta W
$$
- 对准静体积功 \(\delta W=p\,dV\)，有 \(dU=\delta Q-p\,dV\)。对给定过程积分得到 \(\Delta U=Q-W\)。
- 内能 \(U\) 是状态量。对理想气体，实验与动理论都表明 \(U\) 只与温度有关：\(U=U(T)\)，因此
$$
dU=nC_V\,dT
$$
其中 \(C_V\) 为定容摩尔热容。
- 这一点在求热量与功时非常关键：只要知道温度变化，就能确定 \(\Delta U\)，再由第一定律求 \(Q\) 或 \(W\)。
""",
        "§6-4": r"""
- 等体过程 \(dV=0\Rightarrow W=\int p\,dV=0\)。由第一定律 \(\Delta U=Q\)；对理想气体 \(\Delta U=nC_V\Delta T\)，故
$$
Q_V=nC_V\Delta T
$$
- 等压过程 \(p=\text{常量}\Rightarrow W=p(V_2-V_1)=nR\Delta T\)（用 \(pV=nRT\)）。
- 由第一定律 \(Q_p=\Delta U+W=nC_V\Delta T+nR\Delta T=nC_P\Delta T\)，得到
$$
C_P-C_V=R
$$
- 引入焓 \(H=U+pV\)。等压过程中 \(dH=dU+pdV+Vdp=dU+pdV\)（因 \(dp=0\)），而 \(dU=\delta Q-pdV\)，因此 \(dH=\delta Q_p\)，即等压吸热等于焓变。
""",
        "§6-5": r"""
- 等温过程：理想气体 \(U=U(T)\)，温度不变 \(\Delta T=0\Rightarrow \Delta U=0\)。由第一定律 \(Q=W\)。
- 等温过程的功：
$$
W=\int_{V_1}^{V_2}p\,dV=\int_{V_1}^{V_2}\frac{nRT}{V}\,dV=nRT\ln\frac{V_2}{V_1}
$$
因此 \(Q=nRT\ln(V_2/V_1)\)。
- 绝热过程：\(Q=0\)。第一定律给 \(dU=-p\,dV\)。对理想气体 \(dU=nC_VdT\)，并用 \(pV=nRT\) 消去 \(p\) 得
$$
nC_VdT=-\frac{nRT}{V}dV
$$
- 整理为
$$
\frac{dT}{T}=-(\gamma-1)\frac{dV}{V},\quad \gamma=\frac{C_P}{C_V}
$$
积分得 \(TV^{\gamma-1}=\text{常量}\)，再与状态方程联立得到著名绝热方程
$$
pV^\gamma=\text{常量}
$$
- 这些推导都依赖“准静态绝热”假设（过程可逆且无热交换），否则上述简单幂律不成立。
""",
        "§6-6": r"""
- 循环过程回到初态，因此状态量变化为零：\(\Delta U=0\)。由第一定律得一个循环内净功
$$
W_{\text{net}}=Q_{\text{in}}-Q_{\text{out}}
$$
并等于 \(p\text{-}V\) 图闭合曲线所围面积。
- 卡诺循环由两段等温（温度 \(T_1,T_2\)）与两段绝热组成。可逆等温段有 \(Q=T\Delta S\)，绝热段 \(\Delta S=0\)。
- 因为整循环总熵变为 0，得到
$$
\frac{Q_1}{T_1}=\frac{Q_2}{T_2}
$$
其中 \(Q_1\) 为高温吸热，\(Q_2\) 为低温放热。
- 热机效率定义为 \(\eta=W/Q_1=1-Q_2/Q_1\)，代入上式得卡诺效率
$$
\eta=1-\frac{T_2}{T_1}
$$
""",
        "§6-7": r"""
- 第二定律的两种常见表述：开尔文-普朗克表述（不可能把从单一热源吸收的热量完全转化为功而不产生其他影响）与克劳修斯表述（热量不可能自发从低温物体传到高温物体）。
- 卡诺定理证明思路是反证：假设存在效率高于可逆卡诺机的热机，与一台可逆机组合将导致违反第二定律的“第二类永动机”。
- 因此在同一对热源间：任何不可逆机 \(\eta<\eta_C\)，任何可逆机 \(\eta=\eta_C\)，且可逆机效率只取决于热源温度。
- 推导结果最终落实为效率上限：
$$
\eta_{\max}=1-\frac{T_2}{T_1}
$$
这不是工程不足，而是自然定律的限制。
""",
        "§6-8": r"""
- 熵通过可逆过程定义：
$$
dS=\frac{\delta Q_{rev}}{T}
$$
因此熵是状态量（全微分），只与初末态有关。
- 对不可逆过程，克劳修斯不等式给
$$
\Delta S\ge \int \frac{\delta Q}{T}
$$
等号仅对可逆过程成立。
- 理想气体熵变可由 \(dS=\frac{\delta Q_{rev}}{T}\) 与第一定律推得常用公式：
$$
dS=nC_V\frac{dT}{T}+nR\frac{dV}{V}
$$
积分得到 \(\Delta S\) 的显式表达（等温、等压、绝热等都可作为特例）。
- 熵增加原理：孤立系统 \(\delta Q=0\) 且无功交换时，\(\Delta S\ge 0\)。自发过程对应熵增加，平衡态对应熵取极大。
""",
    }
)

# Chapter 7: Kinetic theory of gases
SECTION_BLOCKS.update(
    {
        "§7-1": r"""
- 微观层面分子运动是随机的，但宏观量来自大量分子平均，波动相对幅度随粒子数增大而减小（典型 \(\sim 1/\sqrt{N}\)），因此呈现稳定的统计规律。
- 气体动理论用“分子弹性碰撞、分子间相互作用忽略（除碰撞）、分子速度各向同性”等假设，把压强、温度等宏观量与分子运动联系起来。
- 统计描述的关键是用分布函数替代单个分子轨迹：例如速率分布 \(f(v)\) 或能量分布 \(n(\varepsilon)\)，从而计算平均值 \(\langle v^2\rangle,\langle \varepsilon\rangle\) 等。
""",
        "§7-2": r"""
- 取边长为 \(L\) 的立方容器，考虑一分子与壁面弹性碰撞。若碰撞前速度分量为 \(v_x\)，反弹后为 \(-v_x\)，则分子动量变化 \(\Delta p_x=2mv_x\)。
- 同一分子两次撞同一壁的时间间隔约为 \(\Delta t=2L/|v_x|\)，因此该分子对壁的平均力
$$
F_x\approx \frac{\Delta p_x}{\Delta t}=\frac{2mv_x}{2L/|v_x|}=\frac{m v_x^2}{L}
$$
- 对所有分子求和并除以面积 \(A=L^2\)，得到压强
$$
p=\frac{1}{A}\sum \frac{m v_x^2}{L}=\frac{1}{V}\sum m v_x^2
$$
其中 \(V=L^3\)。
- 由各向同性 \(\langle v_x^2\rangle=\langle v_y^2\rangle=\langle v_z^2\rangle=\tfrac13\langle v^2\rangle\)，得到经典结果
$$
p=\frac13 n m \langle v^2\rangle
$$
其中 \(n=N/V\)。
""",
        "§7-3": r"""
- 由压强公式 \(p=\frac13 n m\langle v^2\rangle\)，两边乘以体积 \(V\) 得
$$
pV=\frac13 N m\langle v^2\rangle
$$
- 理想气体状态方程写成 \(pV=Nk_BT\)。对比两式可得
$$
\frac12 m\langle v^2\rangle=\frac32 k_BT
$$
即平均平动动能与温度成正比，比例系数为 \(\tfrac32k_B\)。
- 这一定义把“温度”从热学概念连接到微观运动强度：温度越高，分子平均动能越大。
""",
        "§7-4": r"""
- 能量均分定理：在经典平衡态下，能量表达式中每一个二次型自由度（如 \(p_x^2\)、\(x^2\)）平均贡献 \(\tfrac12k_BT\)。
- 若分子有 \(f\) 个二次自由度，则单分子平均能量 \(\langle\varepsilon\rangle=\tfrac{f}{2}k_BT\)，总内能
$$
U=N\langle\varepsilon\rangle=\frac{f}{2}Nk_BT=\frac{f}{2}nRT
$$
- 对单原子理想气体，只有 3 个平动自由度 \(f=3\)，因此 \(U=\tfrac32nRT\)；这也解释了定容热容 \(C_V=\tfrac32R\)（单原子）。
- 当温度不够高导致某些转动/振动自由度“冻结”时，均分定理不再直接适用，需要量子修正。
""",
        "§7-5": r"""
- 麦克斯韦速率分布基于三条：速度分量独立、各向同性、平衡态概率最大化。结果为
$$
f(v)=4\pi\left(\frac{m}{2\pi k_BT}\right)^{3/2}v^2 e^{-mv^2/(2k_BT)}
$$
其中 \(f(v)dv\) 为速率在 \([v,v+dv]\) 的概率。
- 用 \(df/dv=0\) 求最概然速率 \(v_p=\sqrt{2k_BT/m}\)。
- 由分布求平均速率与方均根速率：
$$
\bar v=\sqrt{\frac{8k_BT}{\pi m}},\qquad v_{rms}=\sqrt{\langle v^2\rangle}=\sqrt{\frac{3k_BT}{m}}
$$
- 三种“典型速率”满足 \(v_p<\bar v<v_{rms}\)，并都随 \(\sqrt{T}\) 增大。
""",
        "§7-6": r"""
- 玻尔兹曼分布给出能量为 \(\varepsilon\) 的微观状态占据数比例：
$$
n(\varepsilon)\propto e^{-\varepsilon/(k_BT)}
$$
这是统计物理中“最基本的指数律”。
- 在重力场中，分子位能 \(\varepsilon_p=mgz\)。若温度近似恒定，则数密度随高度：
$$
n(z)=n_0 e^{-mgz/(k_BT)}
$$
压强同样满足等温气压公式 \(p(z)=p_0 e^{-mgz/(k_BT)}\)。
- 指数衰减的特征长度称为尺度高度：
$$
H=\frac{k_BT}{mg}
$$
温度越高或分子质量越小，大气越“蓬松”。
""",
        "§7-7": r"""
- 设分子有效直径为 \(d\)，数密度为 \(n\)。把碰撞理解为“相对运动中目标截面”为 \(\pi d^2\) 的几何问题。
- 相对速度的平均效应带来 \(\sqrt{2}\) 因子，平均自由程为
$$
\lambda=\frac{1}{\sqrt{2}\pi d^2 n}
$$
- 平均碰撞频率近似为 \(z\approx \bar v/\lambda\)，平均碰撞时间 \(\tau\approx 1/z\)。
- 该推导体现：气体越稀薄（\(n\) 小）自由程越长；分子越大（\(d\) 大）越容易碰撞。
""",
        "§7-8": r"""
- 迁移现象（扩散、粘滞、导热）都源于分子随机运动把动量、能量、粒子数从“高密度/高温/高速度层”搬运到“低”的地方。
- 用平均自由程近似可得量纲正确的估算式：扩散系数
$$
D\sim \frac13 \bar v\,\lambda
$$
- 黏滞系数与动量输运相关，数量级
$$
\eta\sim \frac13 \rho \bar v\,\lambda
$$
其中 \(\rho\) 为密度。
- 导热系数与能量输运相关，数量级
$$
\kappa\sim \frac13 c_V \rho \bar v\,\lambda
$$
这些结果强调：迁移系数与“速度 \(\times\) 自由程”同阶。
""",
        "§7-9": r"""
- 理想气体忽略分子体积与吸引。范德瓦耳斯方程用两个修正捕捉主要偏离：
- 体积修正：分子有有限体积，实际可用体积 \(V_{\text{free}}=V-nb\)。
- 压强修正：分子间吸引使实际压强比理想小，经验写作 \(p_{\text{eff}}=p+a(n/V)^2\)。
- 把这两点代入理想气体方程，得到
$$
\left(p+a\frac{n^2}{V^2}\right)(V-nb)=nRT
$$
- 参数 \(a,b\) 由实验确定，分别表征吸引强弱与排斥体积效应。
""",
        "§7-10": r"""
- 统计意义的第二定律建立在“宏观状态对应的微观态数”上：宏观态越“无序/均匀”，对应的微观态数 \(\Omega\) 往往越大。
- 玻尔兹曼给出熵与态数关系：
$$
S=k_B\ln\Omega
$$
- 自发过程倾向于从小 \(\Omega\) 走向大 \(\Omega\)，因为后者占据了绝大多数微观可能性；这就是“熵增”在统计意义上的解释。
- 该观点也解释了不可逆性：从大 \(\Omega\) 自发回到小 \(\Omega\) 并非绝对不可能，但概率极小，宏观上几乎观察不到。
""",
    }
)

# Chapter 8: Electrostatics
SECTION_BLOCKS.update(
    {
        "§8-1": r"""
- 电荷量子化：孤立物体所带电荷总是基本电荷 \(e\) 的整数倍 \(q=ne\)（\(n\in\mathbb Z\)），这是大量实验事实的归纳。
- 电荷守恒可写成积分形式：任意闭合系统内总电荷不随时间变化。更一般的局域形式是连续性方程：
$$
\frac{\partial\rho}{\partial t}+\nabla\cdot\vec J=0
$$
- 其含义可由体积分推出：对任意体积 \(V\)，
$$
\frac{d}{dt}\int_V\rho\,d\tau=-\oint_{\partial V}\vec J\cdot d\vec A
$$
左边是体内电荷变化率，右边是穿出边界的电流通量，说明电荷只能流动，不能凭空产生或消失。
- 静电学里常研究稳恒或静止分布，此时 \(\partial\rho/\partial t=0\Rightarrow \nabla\cdot\vec J=0\)，为后续稳恒电流理论打基础。
""",
        "§8-2": r"""
- 库仑定律给两点电荷间相互作用力：
$$
\vec F=\frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{r^2}\,\hat r
$$
方向沿连线，满足叠加原理。
- 定义电场强度为单位正试探电荷所受力：
$$
\vec E\equiv \frac{\vec F}{q_0}
$$
对点电荷 \(q\) 得
$$
\vec E(\vec r)=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\,\hat r
$$
- 多电荷系统用矢量叠加：\(\vec E=\sum_i\vec E_i\)；连续分布写成积分 \(\vec E=\int d\vec E\)。
- 库仑定律与叠加原理共同奠定了静电场的“线性结构”，是高斯定理、势函数等结论的根源。
""",
        "§8-3": r"""
- 电场的定义 \(\vec E=\vec F/q_0\) 把“试探电荷受力”转化为“空间的场”，使得对任意电荷 \(q\) 都有 \(\vec F=q\vec E\)。
- 点电荷场由库仑定律直接得到：\(\vec E=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\hat r\)。
- 连续电荷分布的场由微元叠加：
$$
d\vec E=\frac{1}{4\pi\varepsilon_0}\frac{dq}{r^2}\hat r,\qquad \vec E=\int d\vec E
$$
其中 \(dq=\rho\,d\tau\)（体）、\(\sigma\,dA\)（面）、\(\lambda\,dl\)（线）。
- 对称性是把积分“降维”的关键：球/柱/平面对称分别对应选球面/柱面/平面高斯面或利用对称性消去分量。
""",
        "§8-4": r"""
- 对点电荷 \(q\)，球面对称使 \(\vec E\) 在球面上大小恒定且径向，电通量
$$
\Phi_E=\oint \vec E\cdot d\vec A=E\,4\pi r^2=\frac{q}{\varepsilon_0}
$$
- 由叠加原理，对任意电荷分布与任意闭合面都有高斯定理（积分形式）：
$$
\oint \vec E\cdot d\vec A=\frac{q_{\text{in}}}{\varepsilon_0}
$$
- 用散度定理把闭合曲面积分化为体积分：
$$
\oint \vec E\cdot d\vec A=\int_V(\nabla\cdot\vec E)\,d\tau
$$
从而得到微分形式
$$
\nabla\cdot\vec E=\frac{\rho}{\varepsilon_0}
$$
- 高斯定理的威力在于“对称性场”可把积分变成乘法：例如无限长直线电荷、无限大平面电荷、均匀带电球体等。
""",
        "§8-5": r"""
- 密立根油滴实验利用电场力与重力/阻力的平衡测定电荷量。油滴受力包括重力 \(mg\)、浮力 \(\rho_{\text{air}}Vg\)、黏滞阻力（斯托克斯）\(6\pi\eta r v\) 与电场力 \(qE\)。
- 先在无电场下让油滴达到终速 \(v_1\)，由力平衡求出油滴半径或有效重量：
$$
mg-\rho_{\text{air}}Vg=6\pi\eta r v_1
$$
- 再加电场使油滴以另一终速 \(v_2\) 上升或下降：
$$
qE+(\rho_{\text{air}}Vg-mg)=6\pi\eta r v_2
$$
- 联立两次终速条件可消去未知的 \(m\) 或 \(r\)，解出 \(q\)。实验发现 \(q\) 总是 \(e\) 的整数倍，从而验证电荷量子化并测得 \(e\)。
""",
        "§8-6": r"""
- 静电场中电荷分布不随时间变，电场是保守场，其环路积分为零：
$$
\oint \vec E\cdot d\vec l=0
$$
- 因此沿任意路径从 A 到 B 的积分只与端点有关，可定义电势差：
$$
V(B)-V(A)=-\int_A^B \vec E\cdot d\vec l
$$
- 取 \(B=A+d\vec l\)，有 \(dV=-\vec E\cdot d\vec l\)。与 \(dV=\nabla V\cdot d\vec l\) 对比得到
$$
\vec E=-\nabla V
$$
- 环路定理的微分形式是 \(\nabla\times\vec E=0\)，它与“存在势函数”在单连通区域内等价。
""",
        "§8-7": r"""
- 电势的物理定义是单位电荷的势能：\(V=U/q\)。更可操作的定义来自做功：把单位正电荷从无穷远移到点 \(P\) 所做功的负值。
- 电势差由电场线积分定义：
$$
V(B)-V(A)=-\int_A^B \vec E\cdot d\vec l
$$
- 对点电荷 \(q\)，取 \(V(\infty)=0\)，沿径向积分：
$$
V(r)=-\int_\infty^r \frac{1}{4\pi\varepsilon_0}\frac{q}{r'^2}\,dr'=\frac{1}{4\pi\varepsilon_0}\frac{q}{r}
$$
- 多点电荷电势满足标量叠加：\(V=\sum_i V_i\)；连续分布时 \(V=\frac{1}{4\pi\varepsilon_0}\int \frac{dq}{r}\)。
- 一旦得到 \(V\)，再用 \(\vec E=-\nabla V\) 求场往往比直接积分更省力。
""",
        "§8-8": r"""
- 由电势差定义 \(V(B)-V(A)=-\int_A^B\vec E\cdot d\vec l\)，取 \(B=A+d\vec l\) 得 \(dV=-\vec E\cdot d\vec l\)。
- 与微分恒等式 \(dV=\nabla V\cdot d\vec l\) 比较，得到电场与电势梯度关系：
$$
\vec E=-\nabla V
$$
- 结合高斯定理微分形式 \(\nabla\cdot\vec E=\rho/\varepsilon_0\)，可得泊松方程：
$$
\nabla^2 V=-\frac{\rho}{\varepsilon_0}
$$
无电荷区域 \(\rho=0\) 则为拉普拉斯方程 \(\nabla^2V=0\)。
- 这套“先解势函数再求场”的路线在有边界条件的静电问题里最强大（尤其导体/介质边界）。
""",
        "§8-9": r"""
- 定义电偶极矩 \(\vec p=q\vec d\)（由负到正）。在远场 \(r\gg d\) 处，偶极子电势可由两点电荷电势展开得到：
$$
V(\vec r)\approx \frac{1}{4\pi\varepsilon_0}\frac{\vec p\cdot\hat r}{r^2}
$$
- 电场由 \(\vec E=-\nabla V\) 得出，随 \(1/r^3\) 衰减（比点电荷的 \(1/r^2\) 更快），这体现了电偶极的“正负抵消”。
- 均匀电场中，偶极子受力为零（两端受力大小相等反向），但受力矩
$$
\vec\tau=\vec p\times\vec E
$$
使其趋向与 \(\vec E\) 对齐。
- 势能由做功或 \(\tau\) 积分得到：
$$
U=-\vec p\cdot\vec E
$$
在非均匀场中还会出现净力 \( \vec F\sim (\vec p\cdot\nabla)\vec E\)（高阶近似）。
""",
    }
)

# Chapter 9: Conductors & dielectrics
SECTION_BLOCKS.update(
    {
        "§9-1": r"""
- 导体内有自由电荷可移动。若静电平衡时导体内部仍有 \(\vec E\neq 0\)，自由电荷会在电场力作用下持续运动，违背“静电平衡”假设，因此必有
$$
\vec E=0\quad(\text{导体内部，静电平衡})
$$
- 由 \(\vec E=0\) 得 \(\nabla V=0\)，所以导体内部电势处处相等，导体是等势体。
- 导体内任取闭合回路，\(\oint\vec E\cdot d\vec l=0\)。若内部有切向场分量则会驱动电流，因此导体表面静电平衡时电场只能垂直于表面（切向分量为零）。
- 自由电荷最终分布在导体表面，使内部场抵消；这是“静电屏蔽/法拉第笼”现象的微观原因。
""",
        "§9-2": r"""
- 电容定义为 \(C\equiv Q/V\)（孤立导体）或 \(C\equiv Q/U\)（电容器两极板电势差）。它只由几何与介质决定，与 \(Q,V\) 的具体值无关（在线性介质中）。
- 平行板电容器：板面电荷密度 \(\sigma=Q/A\)，板间均匀场 \(E=\sigma/\varepsilon\)。电势差 \(U=Ed=Qd/(\varepsilon A)\)，故
$$
C=\frac{Q}{U}=\frac{\varepsilon A}{d}
$$
- 圆柱同轴电容（长度 \(L\)，内外半径 \(a,b\)）：由高斯定理得 \(E(r)=\frac{\lambda}{2\pi\varepsilon r}\)，积分得
$$
U=\int_a^b E\,dr=\frac{\lambda}{2\pi\varepsilon}\ln\frac{b}{a}\Rightarrow
C=\frac{Q}{U}=\frac{2\pi\varepsilon L}{\ln(b/a)}
$$
- 电场能量可由“给电容器充电所做功”得到：
$$
U_E=\int_0^Q V\,dQ'=\frac{Q^2}{2C}=\frac12CV^2
$$
""",
        "§9-3": r"""
- 电介质在外电场中发生极化，产生极化强度 \(\vec P\)（单位体积偶极矩）。极化导致束缚电荷：
$$
\rho_b=-\nabla\cdot\vec P,\qquad \sigma_b=\vec P\cdot\hat n
$$
- 总电荷密度 \(\rho=\rho_f+\rho_b\)（自由+束缚）。代入高斯定理微分形式 \(\nabla\cdot\vec E=\rho/\varepsilon_0\)，得到含 \(\vec P\) 的场方程。
- 线性各向同性电介质满足 \(\vec P=\varepsilon_0\chi_e \vec E\)，于是
$$
\vec D=\varepsilon_0\vec E+\vec P=\varepsilon_0(1+\chi_e)\vec E\equiv \varepsilon \vec E
$$
其中 \(\varepsilon=\varepsilon_0\varepsilon_r\)。
- 介质“减弱电场”的本质是束缚电荷产生的附加电场与外场部分抵消。
""",
        "§9-4": r"""
- 从高斯定理 \(\nabla\cdot\vec E=(\rho_f+\rho_b)/\varepsilon_0\)，并用 \(\rho_b=-\nabla\cdot\vec P\)，可写成
$$
\nabla\cdot(\varepsilon_0\vec E+\vec P)=\rho_f
$$
- 定义电位移矢量
$$
\vec D\equiv \varepsilon_0\vec E+\vec P
$$
则得到介质中的高斯定理（微分形式）：
$$
\nabla\cdot\vec D=\rho_f
$$
积分形式为
$$
\oint \vec D\cdot d\vec A=Q_{\text{free,in}}
$$
- 在线性各向同性介质 \(\vec D=\varepsilon\vec E\)，使得许多计算只需把 \(\varepsilon_0\) 替换为 \(\varepsilon\)（并注意自由/束缚电荷的区分）。
""",
        "§9-5": r"""
- 电场能量可由充电做功推导：\(dU=V\,dQ\)。对电容器 \(V=Q/C\)，积分得 \(U=\tfrac12QV=\tfrac12CV^2\)。
- 对连续介质，把能量写成场形式。在线性介质中可得能量密度
$$
u=\frac12\vec E\cdot\vec D=\frac12\varepsilon E^2
$$
总能量 \(U=\int u\,dV\)。
- 这一形式的物理含义是：能量不仅“存”在导体电荷上，也“分布”在电场占据的空间中；改变介质相当于改变单位场强可存储的能量。
""",
        "§9-6": r"""
- 静电应用的推导通常从“受力”入手：带电粒子在电场中受力 \(\vec F=q\vec E\)，因此可实现偏转、分离、收集等功能。
- 例：静电除尘器中粉尘被电离后带电，在强电场力作用下向集尘极板迁移；其效率与电场强度、粒子电荷量、气流速度等有关。
- 许多工程估算只需数量级：迁移时间 \(\sim\) 距离/漂移速度，而漂移速度可由受力平衡或能量平衡给出。
""",
        "§9-7": r"""
- 边界条件来自把麦克斯韦方程积分形式作用在“跨越边界的微小高斯柱/小矩形回路”上。
- 静电场环路定理 \(\oint\vec E\cdot d\vec l=0\) 作用于跨界小矩形，令高度 \(\to 0\)，得到切向分量连续：
$$
E_{t2}-E_{t1}=0
$$
- 高斯定理 \(\oint \vec D\cdot d\vec A=Q_f\) 作用于跨界小柱，得到法向 \(\vec D\) 的跃变由自由面电荷决定：
$$
D_{n2}-D_{n1}=\sigma_f
$$
- 若用 \(\vec E\) 表达，则 \(E_n\) 的跃变与总面电荷（自由+束缚）相关：\( \varepsilon_0(E_{n2}-E_{n1})=\sigma_{\text{total}}\)。
""",
        "§9-8": r"""
- 压电效应可用线性本构关系描述“力-电耦合”：机械应力引起极化（产生电位移），电场也可引起应变（逆压电）。
- 铁电体的关键特征是自发极化与滞回回线：\(\vec P\) 随外电场变化出现滞后，存在剩余极化与矫顽场。
- 驻极体可看作“电的永久体”：内部存在准永久的电偶极排列或空间电荷分布，宏观表现为长期保持电极化。
- 这些材料的推导重点是本构与能量函数：把 \(\vec D,\vec E\) 与应力/应变联系起来即可分析器件工作点与线性化响应。
""",
    }
)

# Chapter 10: Steady current
SECTION_BLOCKS.update(
    {
        "§10-1": r"""
- 电流定义为单位时间通过某截面的电荷量：
$$
I=\frac{dq}{dt}
$$
- 电流密度定义为单位面积电荷通量的矢量：
$$
\vec J=\frac{dq}{dt\,d\vec A},\qquad I=\int_S \vec J\cdot d\vec A
$$
- 若载流子数密度 \(n\)、电荷 \(q\)、平均漂移速度 \(\vec v_d\)，则单位体积电荷量为 \(nq\)，穿过截面的电荷通量给出
$$
\vec J=nq\vec v_d
$$
- 电荷守恒在稳恒电流下给出 \(\nabla\cdot\vec J=0\)（电荷不随时间积累），这是电路“节点电流守恒”的连续介质版本。
""",
        "§10-2": r"""
- 微观欧姆定律写成
$$
\vec J=\sigma \vec E
$$
其中 \(\sigma\) 为电导率，\(\rho=1/\sigma\) 为电阻率。
- 对均匀导体（长 \(L\)、截面积 \(A\)）：\(J=I/A\)、\(E=U/L\)。代入得
$$
\frac{I}{A}=\sigma\frac{U}{L}\Rightarrow U=\frac{L}{\sigma A}I
$$
因此电阻 \(R=U/I=\rho L/A\)。
- Drude 模型可给出 \(\sigma\) 的微观解释：电子在电场中平均漂移速度 \(v_d\propto E\)，比例系数由平均碰撞时间 \(\tau\) 决定，得到 \(\sigma=nq^2\tau/m\)（数量级）。
""",
        "§10-3": r"""
- 电动势 \(\mathcal E\) 的本质是非静电力（化学力、洛伦兹力等）把电荷从低势搬到高势所做的单位电荷功：
$$
\mathcal E=\oint \frac{\vec f_{\text{非静电}}}{q}\cdot d\vec l
$$
- 在电源内部，化学力把正负电荷分离形成电势差；在外电路中，静电场驱动电流并在电阻上耗散能量。
- 有内阻 \(r\) 的电源可等效为理想电动势串联内阻：端电压 \(U=\mathcal E-Ir\)。这来自把电源内部也视为电阻并应用能量守恒（KVL）。
""",
        "§10-4": r"""
- 全电路欧姆定律来自回路能量守恒：电源提供的电动势等于回路各电阻上的电势降之和。
- 对外电阻 \(R\) 与内阻 \(r\) 串联：
$$
\mathcal E=I(R+r)\Rightarrow I=\frac{\mathcal E}{R+r}
$$
- 端电压（外电路两端电压）为
$$
U=IR=\mathcal E-Ir
$$
随负载变化而变化：短路时 \(U\approx 0\)、开路时 \(I=0,U=\mathcal E\)。
""",
        "§10-5": r"""
- 节点定律（KCL）来自电荷守恒：稳恒电流下节点处电荷不积累，因此流入电流之和等于流出电流之和：
$$
\sum I_{\text{in}}=\sum I_{\text{out}}
$$
- 回路定律（KVL）来自能量守恒：沿闭合回路一周电势变化总和为零，等价于电场做功与非静电力做功平衡：
$$
\sum \mathcal E-\sum IR=0
$$
- 两条定律本质是“连续性方程 + 静电场保守性”的电路化表达，在直流稳恒条件下成立。
""",
        "§10-6": r"""
- RC 充电回路：KVL 写 \(\mathcal E-IR-U_C=0\)，其中 \(U_C=Q/C\)、\(I=dQ/dt\)。得到一阶方程
$$
R\frac{dQ}{dt}+\frac{Q}{C}=\mathcal E
$$
- 解得
$$
Q(t)=C\mathcal E\left(1-e^{-t/RC}\right),\quad I(t)=\frac{\mathcal E}{R}e^{-t/RC}
$$
- 放电回路（无电源）：\(R\,dQ/dt+Q/C=0\Rightarrow Q=Q_0e^{-t/RC}\)。
- 时间常数 \(\tau=RC\) 决定充放电快慢；能量随时间耗散在电阻上，电容器储能为 \(U=\tfrac12CU_C^2\)。
""",
    }
)

# Chapter 11: Magnetostatics
SECTION_BLOCKS.update(
    {
        "§11-1": r"""
- 磁场的操作性定义来自洛伦兹力：带电粒子在磁场中运动受力
$$
\vec F=q\vec v\times\vec B
$$
因此 \(\vec B\) 的方向由力的方向确定，大小由 \(F=qvB\sin\theta\) 确定。
- 载流导体中电荷微观受洛伦兹力，总体表现为导线受力；因此磁场也可用“电流产生磁场”的规律描述（毕奥-萨伐尔、安培定理）。
- 静磁场满足叠加原理，许多结果来自对称性：长直导线、圆电流、螺线管、环形线圈等都可用对称面选取积分路径快速求 \(\vec B\)。
""",
        "§11-2": r"""
- 毕奥-萨伐尔定律给电流元 \(I\,d\vec l\) 在空间点产生的磁场微元：
$$
d\vec B=\frac{\mu_0}{4\pi}\frac{I\,d\vec l\times \hat r}{r^2}
$$
方向由叉乘决定。
- 对长直导线积分可得 \(B=\mu_0I/(2\pi r)\)；对圆电流在轴线上积分得到 \(B=\frac{\mu_0IR^2}{2(R^2+x^2)^{3/2}}\)（典型结果）。
- 很多对称体系可用安培环路定理更快得到同样结论，二者可互证。
""",
        "§11-3": r"""
- 磁通量定义为 \(\Phi_B=\int_S \vec B\cdot d\vec A\)。
- 实验事实表明不存在磁单极子，因此任意闭合面磁通量为零：
$$
\oint \vec B\cdot d\vec A=0
$$
- 用散度定理得到微分形式：
$$
\nabla\cdot\vec B=0
$$
这意味着磁力线总是闭合的，不会像电场线那样从正电荷出发到负电荷终止。
""",
        "§11-4": r"""
- 安培环路定理（静磁）：
$$
\oint \vec B\cdot d\vec l=\mu_0 I_{\text{enc}}
$$
- 对无限长直导线取同心圆环路，\(B\) 恒定且切向：\(B2\pi r=\mu_0I\Rightarrow B=\mu_0I/(2\pi r)\)。
- 对理想长螺线管，取矩形环路并用内部场近似均匀、外部近似为零，得 \(B\approx \mu_0 n I\)（\(n\) 为匝密度）。
""",
        "§11-5": r"""
- 匀强磁场中若 \(\vec v\perp\vec B\)，洛伦兹力大小 \(F=qvB\) 且始终垂直速度，做匀速圆周运动：
$$
\frac{mv^2}{r}=|q|vB\Rightarrow r=\frac{mv}{|q|B}
$$
- 角频率（回旋频率）由 \(v=r\omega\) 得
$$
\omega_c=\frac{|q|B}{m},\quad T=\frac{2\pi m}{|q|B}
$$
- 若速度有平行分量 \(v_\parallel\)，该分量不受磁力影响，叠加得到螺旋运动，螺距 \(h=v_\parallel T\)。
- 若同时存在匀强电场 \(\vec E\) 与 \(\vec B\)，可出现 \( \vec E\times\vec B\) 漂移等现象；本质仍是对运动方程 \(m\dot{\vec v}=q(\vec E+\vec v\times\vec B)\) 的分解求解。
""",
        "§11-6": r"""
- 导线中载流子受洛伦兹力 \(q\vec v_d\times\vec B\)，对单位体积电荷 \(nq\) 求和可得体力密度 \(\vec f=\vec J\times\vec B\)。
- 对截面积为 \(A\)、长度元 \(d\vec l\) 的导线，\(\vec J A\,d l=I\,d\vec l\)，因此导线元受力
$$
d\vec F=I\,d\vec l\times\vec B
$$
匀强场中直导线 \(\vec F=I\vec l\times\vec B\)。
- 两平行长直电流间相互作用可由此与 \(B=\mu_0I/(2\pi r)\) 推出吸引/排斥规律。
""",
        "§11-7": r"""
- 平面电流回路在匀强磁场中等效为磁偶极子，磁矩定义为
$$
\vec \mu=IS\,\hat n
$$
其中 \(S\) 为回路面积，\(\hat n\) 由右手定则确定。
- 回路受力矩可由两边受力形成的力偶推得，结果为
$$
\vec\tau=\vec\mu\times\vec B
$$
- 势能为
$$
U=-\vec\mu\cdot\vec B
$$
表明回路趋向使 \(\vec\mu\) 与 \(\vec B\) 同向以降低能量。
- 在非均匀磁场中还会有合力，近似为 \(\vec F=\nabla(\vec\mu\cdot\vec B)\)（在 \(\vec\mu\) 近似常量时）。
""",
    }
)

# Chapter 12: Magnetic materials
SECTION_BLOCKS.update(
    {
        "§12-1": r"""
- 磁介质中大量微观电流环（轨道/自旋）使介质出现磁化强度 \(\vec M\)（单位体积磁矩）。
- 磁化可等效为束缚电流：体束缚电流密度与面束缚电流密度分别为
$$
\vec J_b=\nabla\times\vec M,\qquad \vec K_b=\vec M\times\hat n
$$
- 磁感应强度与磁化关系可写作
$$
\vec B=\mu_0(\vec H+\vec M)
$$
其中 \(\vec H\) 用于把自由电流与束缚电流贡献分开处理。
""",
        "§12-2": r"""
- 静磁安培定理对总电流成立：\(\oint \vec B\cdot d\vec l=\mu_0(I_f+I_b)\)（自由+束缚）。
- 由 \(\vec B=\mu_0(\vec H+\vec M)\) 得
$$
\oint \vec H\cdot d\vec l=I_f
$$
这定义了磁场强度 \(\vec H\) 的意义：它的环路积分只与自由电流有关。
- 在线性各向同性磁介质中 \(\vec M=\chi_m\vec H\)，因此
$$
\vec B=\mu\mu_0\vec H,\quad \mu=1+\chi_m
$$
""",
        "§12-3": r"""
- 铁磁质的宏观高磁导率来自磁畴结构：外场使磁畴壁移动与磁矩转向，导致 \(B\text{-}H\) 关系强非线性。
- 磁滞回线反映不可逆过程：撤去外场仍保留剩磁 \(B_r\)，要用反向外场达到矫顽力 \(H_c\) 才能退磁。
- 这些现象的定量推导通常以经验本构曲线或能量最小化模型为基础；解题时关键是正确读取 \(B(H)\) 曲线与磁路近似。
""",
    }
)

# Chapter 13: Electromagnetic induction & field
SECTION_BLOCKS.update(
    {
        "§13-1": r"""
- 法拉第电磁感应定律（积分形式）：
$$
\mathcal E=\oint \vec E\cdot d\vec l=-\frac{d\Phi_B}{dt}
$$
其中 \(\Phi_B=\int \vec B\cdot d\vec A\)。
- 负号是楞次定律，体现能量守恒：感应电流的磁场总“反抗”磁通变化，避免无源增能。
- 用斯托克斯定理可写成微分形式：
$$
\nabla\times\vec E=-\frac{\partial\vec B}{\partial t}
$$
这表明感应电场是非保守场（环路积分不再为零）。
""",
        "§13-2": r"""
- 动生电动势来自导体在磁场中运动时自由电荷受洛伦兹力 \(q\vec v\times\vec B\)，等效为沿导体方向的“非静电力”做功。
- 对长度为 \(l\)、速度 \(v\)、且 \(v\perp B\) 的导体棒，有
$$
\mathcal E=Blv
$$
（方向由右手定则与楞次定律判定）。
- 感生电动势来自时变磁场产生的感应电场：即使导体不动，若 \(\Phi_B\) 随时间变化也有 \(\mathcal E=-d\Phi_B/dt\)。
- 两类电动势可统一理解为磁通变化率：变化原因可以是 \(B(t)\) 变、面积变、或相对取向变。
""",
        "§13-3": r"""
- 自感定义：回路电流 \(I\) 产生的磁通 \(\Phi\) 与 \(I\) 成正比，\(\Phi=LI\)，其中 \(L\) 为自感系数。
- 由法拉第定律，因电流变化引起的自感电动势
$$
\mathcal E_L=-\frac{d\Phi}{dt}=-L\frac{dI}{dt}
$$
负号体现楞次定律（反抗电流变化）。
- 互感定义：回路 1 的电流 \(I_1\) 在回路 2 中产生磁通 \(\Phi_{21}=MI_1\)，从而感应电动势
$$
\mathcal E_2=-M\frac{dI_1}{dt}
$$
- 在线性介质与固定几何下满足互易性 \(M_{12}=M_{21}=M\)。求 \(L,M\) 常用对称性与磁场积分（如螺线管 \(L\approx \mu_0n^2Al\)）。
""",
        "§13-4": r"""
- RL 串联电路 KVL：\(\mathcal E-IR-L\,dI/dt=0\)，得到一阶线性微分方程
$$
L\frac{dI}{dt}+RI=\mathcal E
$$
- 充电（电流建立）解为
$$
I(t)=\frac{\mathcal E}{R}\left(1-e^{-t/\tau}\right),\quad \tau=\frac{L}{R}
$$
- 断电（电流衰减）时 \(\mathcal E=0\)，解为
$$
I(t)=I_0e^{-t/\tau}
$$
- 时间常数 \(\tau=L/R\) 反映电感“反抗电流变化”的程度：\(L\) 越大或 \(R\) 越小，电流变化越慢。
""",
        "§13-5": r"""
- 建立电流时，电源需克服自感电动势做功。微元功率 \(P=I\mathcal E_L=I(L\,dI/dt)\)，因此微元能量
$$
dU=L I\,dI
$$
- 从 0 积分到 \(I\) 得电感储能：
$$
U=\int_0^I L I'\,dI'=\frac12LI^2
$$
- 把线圈能量视作磁场能量，可得到真空磁场能量密度
$$
u=\frac{B^2}{2\mu_0}
$$
更一般介质中常写 \(u=\tfrac12\vec B\cdot\vec H\)（线性情况下）。
- 这说明能量不仅“在元件里”，也分布在其周围磁场所占空间中。
""",
        "§13-6": r"""
- 若只用原安培定理 \(\nabla\times\vec B=\mu_0\vec J\)，对两边取散度得 \(0=\mu_0\nabla\cdot\vec J\)，这要求 \(\nabla\cdot\vec J=0\)，与一般连续性方程 \(\partial\rho/\partial t+\nabla\cdot\vec J=0\) 冲突（当 \(\partial\rho/\partial t\neq 0\)）。
- 麦克斯韦通过加入位移电流项修正为
$$
\nabla\times\vec B=\mu_0\vec J+\mu_0\varepsilon_0\frac{\partial\vec E}{\partial t}
$$
对其取散度并用 \(\nabla\cdot\vec E=\rho/\varepsilon_0\)，立刻得到连续性方程，矛盾消失。
- 因此定义位移电流密度
$$
\vec J_d=\varepsilon_0\frac{\partial\vec E}{\partial t}
$$
在充电电容中，导线内有传导电流，极板间无传导电流但有位移电流，使安培环路定理在任何截面上一致成立。
- 与法拉第定律、两条高斯定理一起，便得到电磁场基本方程的积分形式（麦克斯韦方程组）。
""",
    }
)

# Chapter 14: Mechanical oscillation
SECTION_BLOCKS.update(
    {
        "§14-1": r"""
- 简谐振动的动力学本质是“回复力与位移成正比且反向”：\(F=-kx\)。
- 用牛顿第二定律 \(m\ddot x=F\)，得到简谐方程
$$
\ddot x+\omega^2x=0,\quad \omega=\sqrt{\frac{k}{m}}
$$
- 特征方程根为 \(\pm i\omega\)，因此通解为
$$
x(t)=A\cos(\omega t+\varphi)
$$
其中 \(A,\varphi\) 由初始条件确定。
- 由 \(v=\dot x=-A\omega\sin(\omega t+\varphi)\)、\(a=\ddot x=-\omega^2x\) 可知加速度与位移反向且成正比。
- 能量由势能 \(U=\tfrac12kx^2\) 与动能 \(K=\tfrac12mv^2\) 构成，总能量 \(E=K+U=\tfrac12kA^2\) 为常量（无阻尼）。
""",
        "§14-2": r"""
- 由解 \(x=A\cos(\omega t+\varphi)\) 可直接读出：振幅 \(A\) 是最大位移，初相位 \(\varphi\) 决定 \(t=0\) 时刻位置与速度。
- 周期来自相位增加 \(2\pi\)：\(\omega T=2\pi\Rightarrow T=2\pi/\omega\)，频率 \(f=1/T=\omega/(2\pi)\)。
- 速度与位移相位相差 \(\pi/2\)：\(\dot x=-A\omega\sin(\omega t+\varphi)=A\omega\cos(\omega t+\varphi+\pi/2)\)。
- 由能量守恒可得 \(v\text{-}x\) 关系：\(E=\tfrac12kx^2+\tfrac12mv^2=\tfrac12kA^2\)，因此
$$
v^2=\omega^2(A^2-x^2)
$$
最大速度 \(v_{\max}=\omega A\) 出现在平衡位置 \(x=0\)。
""",
        "§14-3": r"""
- 把简谐量写成复指数形式最简：\(x(t)=\Re\{Ae^{i(\omega t+\varphi)}\}\)。这等价于“旋转矢量”的投影：长度 \(A\) 的矢量以角速度 \(\omega\) 匀速转动，其在某轴上的投影就是简谐运动。
- 旋转矢量法的关键优势是“合成变加法”：同频率简谐量的叠加可转化为相量（复数）相加。
- 若 \(x_1=A_1\cos(\omega t+\varphi_1)\)、\(x_2=A_2\cos(\omega t+\varphi_2)\)，则
$$
x=x_1+x_2=A\cos(\omega t+\varphi)
$$
其中合振幅由几何或余弦定理得
$$
A^2=A_1^2+A_2^2+2A_1A_2\cos(\varphi_1-\varphi_2)
$$
- 这就是把“时域叠加”变成“相位空间矢量叠加”的证明路线。
""",
        "§14-4": r"""
- 单摆：转矩 \(\tau=-mgl\sin\theta\)，转动方程 \(I\ddot\theta=\tau\)，且 \(I=ml^2\)。得到
$$
\ddot\theta+\frac{g}{l}\sin\theta=0
$$
- 小角近似 \(|\theta|\ll1\) 时 \(\sin\theta\approx\theta\)，线性化为 \(\ddot\theta+\omega^2\theta=0\)，\(\omega=\sqrt{g/l}\)，因此
$$
T=2\pi\sqrt{\frac{l}{g}}
$$
- 复摆（物理摆）：取转轴到质心距离为 \(d\)，力矩 \(\tau=-mgd\sin\theta\)，方程 \(I\ddot\theta=-mgd\sin\theta\)。
- 小角线性化得
$$
T=2\pi\sqrt{\frac{I}{mgd}}
$$
其中 \(I\) 是相对转轴的转动惯量。
""",
        "§14-5": r"""
- 对弹簧振子，势能 \(U=\tfrac12kx^2\)。由 \(x=A\cos(\omega t+\varphi)\) 与 \(v=-A\omega\sin(\omega t+\varphi)\)，得
$$
K=\tfrac12mv^2=\tfrac12m\omega^2A^2\sin^2(\cdot),\quad
U=\tfrac12kA^2\cos^2(\cdot)
$$
- 因 \(k=m\omega^2\)，所以
$$
E=K+U=\tfrac12kA^2(\sin^2+\cos^2)=\tfrac12kA^2=\text{常量}
$$
- 能量在 \(K\) 与 \(U\) 间周期交换：平衡点 \(x=0\) 处势能最小动能最大，端点 \(x=\pm A\) 处动能为零势能最大。
""",
        "§14-6": r"""
- 同频同向简谐合成可用相量法证明：\(x_1=A_1\cos(\omega t+\varphi_1)\)、\(x_2=A_2\cos(\omega t+\varphi_2)\) 写成复数叠加，合成仍为同频简谐 \(x=A\cos(\omega t+\varphi)\)。
- 合振幅满足
$$
A^2=A_1^2+A_2^2+2A_1A_2\cos\Delta\varphi
$$
其中 \(\Delta\varphi=\varphi_1-\varphi_2\)。
- 若频率略不同 \(x=A\cos\omega_1 t+A\cos\omega_2 t\)，用和差化积可得拍频：
$$
x=2A\cos\left(\frac{\Delta\omega}{2}t\right)\cos\left(\bar\omega t\right)
$$
包络频率为 \(\Delta\omega/2\pi\)。
- 垂直方向简谐合成（不同相位/频率比）产生李萨如图形，本质仍是参数方程消元问题。
""",
        "§14-7": r"""
- 阻尼受迫振动方程（线性阻尼）：
$$
m\ddot x+b\dot x+kx=F_0\cos\Omega t
$$
写作 \(\ddot x+2\beta\dot x+\omega_0^2x=(F_0/m)\cos\Omega t\)，其中 \(\beta=b/(2m)\)、\(\omega_0=\sqrt{k/m}\)。
- 解分为瞬态项（齐次解，指数衰减）与稳态项（特解）。稳态取 \(x=A\cos(\Omega t-\delta)\) 代入可得
$$
A=\frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2+(2\beta\Omega)^2}}
$$
相位滞后满足 \(\tan\delta=\frac{2\beta\Omega}{\omega_0^2-\Omega^2}\)。
- 共振来自 \(A(\Omega)\) 的峰值：阻尼越小峰越尖，品质因数 \(Q\sim \omega_0/(2\beta)\) 描述能量存储与损耗的比值。
- 这一推导依赖线性假设（小振幅、线性阻尼/弹性）；非线性会导致跳跃、倍频、混沌等更复杂现象。
""",
    }
)

# Chapter 15: Mechanical waves
SECTION_BLOCKS.update(
    {
        "§15-1": r"""
- 机械波是介质振动的传播。线性小振幅下，介质微元满足线性微分方程，叠加原理成立。
- 波速由介质性质决定，与振幅无关（在线性范围内）。例如弦波波速 \(v=\sqrt{T/\mu}\) 来自张力 \(T\) 与线密度 \(\mu\)。
- 重要区分：质点振动速度与波传播速度不同；前者是介质点上下振动的速度，后者是相位/扰动向前推进的速度。
- 相位决定干涉与驻波：相位差 \(\Delta\varphi\) 控制相长/相消，驻波节点位置由边界条件固定。
""",
        "§15-2": r"""
- 一维波动方程 \(\partial^2 y/\partial t^2=v^2\partial^2 y/\partial x^2\) 的行波解为 \(y=f(x-vt)\) 或 \(y=g(x+vt)\)。
- 取简谐形式得到平面简谐波波函数：
$$
y(x,t)=A\cos(\omega t-kx+\varphi)
$$
其中 \(k=2\pi/\lambda\)、\(\omega=2\pi f\)。
- 保持相位不变 \(\omega t-kx=\text{常量}\) 得相速度
$$
v=\frac{\omega}{k}=\lambda f
$$
- 波的空间周期 \(\lambda\) 与时间周期 \(T=2\pi/\omega\) 是两种“周期性”，二者由波速联系。
""",
        "§15-3": r"""
- 以弦波为例，能量由动能与势能组成。单位长度动能密度 \(dK/dx=\tfrac12\mu(\partial y/\partial t)^2\)。
- 小斜率下势能密度与弦的伸长相关，近似为 \(dU/dx=\tfrac12T(\partial y/\partial x)^2\)。
- 对简谐行波可得平均能流（功率）与强度关系：平均功率与 \(A^2\omega^2\) 成正比，且沿传播方向输运。
- 声波强度定义为单位面积平均功率，和压强/位移振幅的平方成正比；分贝刻度来自对数化表达宽动态范围。
""",
        "§15-4": r"""
- 惠更斯原理：波前上每一点都可看作次级波源，随后时刻的波前是这些次波的包络面。
- 反射定律可由相位匹配/波前几何推出：入射波前与反射波前关于法线对称，因此 \(\theta_i=\theta_r\)。
- 折射定律（斯涅尔定律）同样来自相位连续性：界面上相位必须一致，得到
$$
\frac{\sin\theta_1}{v_1}=\frac{\sin\theta_2}{v_2}
$$
对光学写成 \(n_1\sin\theta_1=n_2\sin\theta_2\)。
- 衍射与几何光学差别在于孔径有限导致次波不能完全相消，从而在阴影区仍有波动；定量描述需要菲涅耳/夫琅禾费衍射理论。
""",
        "§15-5": r"""
- 两相干波叠加：位移（或场）先线性相加，再平方取强度。设两波振幅 \(A_1,A_2\)，相位差 \(\Delta\varphi\)，则强度
$$
I=I_1+I_2+2\sqrt{I_1I_2}\cos\Delta\varphi
$$
- 相长干涉条件 \(\Delta\varphi=2m\pi\)，相消干涉条件 \(\Delta\varphi=(2m+1)\pi\)。
- 相位差可由程差 \(\Delta\) 给出：\(\Delta\varphi=2\pi\Delta/\lambda\)。因此干涉问题核心是把几何差异转成程差。
""",
        "§15-6": r"""
- 两列等振幅、等频率、反向传播的简谐波叠加：
$$
y=A\cos(\omega t-kx)+A\cos(\omega t+kx)=2A\cos\omega t\cos kx
$$
或等价形式 \(2A\sin kx\sin\omega t\)，这就是驻波。
- 节点满足 \(\cos kx=0\Rightarrow x=(2n+1)\lambda/4\)（取该形式时）或 \(x=n\lambda/2\)（取正弦形式），本质是空间因子为零。
- 两端固定弦长 \(L\) 的边界条件给允许波长
$$
\lambda_n=\frac{2L}{n},\quad f_n=\frac{nv}{2L}\quad(n=1,2,\dots)
$$
即固有频率离散化。
""",
        "§15-7": r"""
- 声波在气体中近似为绝热过程，因此声速由绝热压缩关系给出：
$$
v=\sqrt{\left(\frac{\partial p}{\partial \rho}\right)_S}=\sqrt{\frac{\gamma p}{\rho}}=\sqrt{\frac{\gamma RT}{M}}
$$
其中 \(\gamma=C_P/C_V\)。
- 超声与次声只是频率范围划分，传播机制与一般声波相同；衰减与吸收、散射、介质黏性和热传导有关。
- 声强与声压幅值平方成正比，分贝定义 \(L_I=10\log_{10}(I/I_0)\) 用于表达宽动态范围。
""",
        "§15-8": r"""
- 多普勒效应来自“相位到达频率”的变化。对声波（介质静止、波速 \(v\) 相对介质固定），观察到的频率依赖于源速 \(v_s\) 与观察者速 \(v_o\)：
$$
f'=f\frac{v\pm v_o}{v\mp v_s}
$$
上号取相向、下号取相背（符号按相对靠近/远离判）。
- 推导思路：源运动改变相邻波前间距（等效改变 \(\lambda\)），观察者运动改变单位时间穿过波前的数量（等效改变采样速率）。
- 光的多普勒需用相对论处理（波速对所有惯性系相同），这在相对论章节给出。
""",
    }
)

# Chapter 16: EM oscillation & waves
SECTION_BLOCKS.update(
    {
        "§16-1": r"""
- LC 回路由 KVL：\(L\,dI/dt+Q/C=0\)，并用 \(I=dQ/dt\) 化为二阶方程
$$
\frac{d^2Q}{dt^2}+\frac{1}{LC}Q=0
$$
- 这是简谐方程，角频率
$$
\omega=\frac{1}{\sqrt{LC}}
$$
电荷与电流相差 \(\pi/2\)。
- 能量在电容电场能 \(U_E=Q^2/(2C)\) 与电感磁场能 \(U_B=LI^2/2\) 间周期交换，总能量守恒（理想无阻尼）。
- 若加入电阻 \(R\)，得到 RLC 方程 \(L\ddot Q+R\dot Q+Q/C=0\)（自由振动）或含外源项（受迫振动），与阻尼振子完全同型。
""",
        "§16-2": r"""
- 在真空中麦克斯韦方程给 \(\nabla\times\vec E=-\partial\vec B/\partial t\)、\(\nabla\times\vec B=\mu_0\varepsilon_0\partial\vec E/\partial t\)，并有 \(\nabla\cdot\vec E=0,\nabla\cdot\vec B=0\)。
- 对 \(\nabla\times\vec E\) 取旋度并用恒等式 \(\nabla\times(\nabla\times\vec E)=\nabla(\nabla\cdot\vec E)-\nabla^2\vec E\)，得到波动方程：
$$
\nabla^2\vec E-\mu_0\varepsilon_0\frac{\partial^2\vec E}{\partial t^2}=0
$$
磁场同理。
- 因此传播速度
$$
c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}
$$
与光速相等，说明光是电磁波。
- 平面波中 \(\vec E\perp\vec B\perp \vec k\)，且 \(B=E/c\)。能流由坡印廷矢量
$$
\vec S=\frac{1}{\mu_0}\vec E\times\vec B
$$
给出，方向为传播方向。
""",
    }
)

# Chapter 17: Wave optics
SECTION_BLOCKS.update(
    {
        "§17-1": r"""
- 干涉要求相位关系稳定，即相干。时间相干性用相干时间 \(\tau_c\) 或相干长度 \(l_c=c\tau_c\) 描述。
- 频谱宽度与相干时间互为倒数（数量级）：\(\tau_c\sim 1/\Delta\nu\)，因此
$$
l_c\sim \frac{c}{\Delta\nu}
$$
频谱越窄，相干长度越长。
- 干涉可见度（条纹对比度）定义为 \(V=(I_{\max}-I_{\min})/(I_{\max}+I_{\min})\)，与两束光强比与相干度有关。
- 空间相干性与光源大小有关：有效光源越小（或越远、或经小孔），同屏幕上不同点的相位关联越好，条纹越清晰。
""",
        "§17-2": r"""
- 两缝干涉的几何主线是光程差：\(\Delta\approx d\sin\theta\approx d x/L\)（小角近似）。
- 明纹条件 \(\Delta=m\lambda\)，得到亮纹位置
$$
x_m=\frac{m\lambda L}{d},\quad \Delta x=\frac{\lambda L}{d}
$$
- 强度来自振幅叠加：\(I=I_1+I_2+2\sqrt{I_1I_2}\cos(2\pi\Delta/\lambda)\)，当两缝强度相等时暗纹可达零强度。
- 双镜、劳埃德镜等装置本质是“产生两相干虚光源”，几何上仍可化为两光源干涉，额外需要注意反射相位变化。
""",
        "§17-3": r"""
- 光程定义为折射率加权的几何路程：在介质中光程 \(=\int n\,ds\)。薄膜内近似为 \(2nt\cos r\)（来回一次）。
- 反射干涉要检查相位反转：从疏到密反射会产生 \(\pi\) 相位变换，相当于多了 \(\lambda/2\) 的光程差。
- 设薄膜厚度 \(t\)、折射率 \(n\)、折射角 \(r\)。若只有一次相位反转，则反射光的明暗条件为
$$
2nt\cos r=\left(m+\tfrac12\right)\lambda\ (\text{明}),\quad 2nt\cos r=m\lambda\ (\text{暗})
$$
若相位反转次数为 0 或 2，则明暗条件互换。
- 透射干涉与反射相反（能量守恒下明暗互补），推导同样从两束光的程差与相位差出发。
""",
        "§17-4": r"""
- 劈尖干涉中膜厚 \(t\) 随位置 \(x\) 线性变化：\(t\approx x\alpha\)（\(\alpha\) 为小楔角）。程差 \(\Delta\approx 2nt\) 也随 \(x\) 线性变化，因此条纹等间距。
- 牛顿环可视作球面与平板间空气膜干涉。膜厚与环半径关系由几何给出：\(t\approx r^2/(2R)\)（\(R\) 为曲率半径）。
- 若为反射干涉且有一次相位反转，暗环条件 \(2t=m\lambda\) 给出
$$
r_m^2=m\lambda R
$$
明暗互换取决于相位反转次数。
- 这一推导的关键是把“膜厚几何”与“程差相位”两条链条接起来。
""",
        "§17-5": r"""
- 迈克耳孙干涉仪的程差由两臂光程差决定。若一臂镜子移动距离 \(\Delta L\)，往返光程改变 \(2\Delta L\)。
- 条纹移动条数 \(N\) 满足
$$
2\Delta L=N\lambda\Rightarrow \lambda=\frac{2\Delta L}{N}
$$
因此可精密测量波长或长度。
- 时间相干性限制最大可见程差：当程差超过相干长度 \(l_c\) 时条纹消失，因此可用干涉仪反测 \(l_c\) 与谱宽。
""",
        "§17-6": r"""
- 惠更斯-菲涅耳原理把孔径/障碍物处的波前视作次级波源叠加，远场（夫琅禾费）衍射可近似为孔径函数的傅里叶变换。
- 衍射条纹的暗纹条件通常来自“孔径内配对相消”：当相位沿孔径累积差为 \(2\pi m\) 时出现系统性相消。
- 远场条件本质是几何尺度满足 \(L\gg a^2/\lambda\)（\(a\) 为孔径尺度），使得相位近似线性，从而可用简化积分。
""",
        "§17-7": r"""
- 单缝远场衍射把缝宽 \(a\) 分解为连续波源，观察方向 \(\theta\) 下两端程差为 \(a\sin\theta\)。
- 当程差等于整倍波长时，可将缝分成成对区间相消，得到暗纹条件：
$$
a\sin\theta=m\lambda\quad(m=1,2,\dots)
$$
- 更完整强度分布为
$$
I=I_0\left(\frac{\sin\beta}{\beta}\right)^2,\quad \beta=\frac{\pi a\sin\theta}{\lambda}
$$
主极大宽、旁瓣弱的形状来自 \(\sin x/x\)。
""",
        "§17-8": r"""
- 圆孔衍射的远场强度分布由贝塞尔函数给出，中心亮斑称艾里斑。第一暗环近似满足
$$
\sin\theta\approx 1.22\frac{\lambda}{D}
$$
其中 \(D\) 为孔径直径。
- 瑞利判据认为两点像“恰好可分辨”时，一个像的主极大落在另一个像的第一暗环处，因此角分辨率
$$
\theta_{min}\approx 1.22\frac{\lambda}{D}
$$
- 这表明分辨率的极限由衍射决定：增大口径或减小波长可提高分辨率。
""",
        "§17-9": r"""
- 光栅把 \(N\) 个等间距缝叠加，相邻缝程差为 \(\Delta=d\sin\theta\)。主极大条件
$$
d\sin\theta=m\lambda
$$
- 由于多缝叠加，主极大更尖锐，角宽约随 \(1/N\) 缩小；角色散
$$
\frac{d\theta}{d\lambda}=\frac{m}{d\cos\theta}
$$
- 分辨本领由瑞利判据推得
$$
R=\frac{\lambda}{\Delta\lambda}=mN
$$
阶数越高、有效缝数越多，分辨能力越强。
""",
        "§17-10": r"""
- X 射线波长与晶格间距同量级，可发生晶体衍射。把晶面间距为 \(d\) 的晶面看作反射面。
- 相邻晶面反射光的程差为 \(2d\sin\theta\)。相长干涉（布拉格条件）为
$$
2d\sin\theta=n\lambda
$$
- 通过测量衍射峰角度可反推出晶格常数 \(d\) 或 X 射线波长 \(\lambda\)，是晶体结构分析的重要方法。
""",
        "§17-11": r"""
- 全息记录的是物光与参考光的干涉条纹，即在感光材料上写入两波相位差信息。
- 设参考波 \(E_r\) 与物波 \(E_o\) 叠加，记录强度 \(I\propto |E_r+E_o|^2\) 含交叉项 \(E_rE_o^*\)，它携带物波的相位信息。
- 重建时用参考波照射全息图，衍射产生与原物波相同的波前，从而再现三维信息；本质是“用干涉把相位编码到强度，再用衍射解码”。
""",
        "§17-12": r"""
- 线偏振光通过检偏器后，电场振幅等于入射电场在透振方向的投影：\(E=E_0\cos\theta\)。
- 光强与振幅平方成正比，因此马吕斯定律：
$$
I=I_0\cos^2\theta
$$
- 该推导的关键是假设检偏器只允许某一方向的电场分量通过，其他分量被吸收或反射。
""",
        "§17-13": r"""
- 反射与折射时不同偏振分量的反射率不同（菲涅耳公式）。当入射角达到布儒斯特角时，反射光完全线偏振。
- 布儒斯特角条件是反射光与折射光互相垂直：\(\theta_B+\theta_t=90^\circ\)。
- 与斯涅尔定律 \(n_1\sin\theta_B=n_2\sin\theta_t\) 联立，得
$$
\tan\theta_B=\frac{n_2}{n_1}
$$
这是最常用的推导路线。
""",
        "§17-14": r"""
- 各向异性晶体存在双折射：同一传播方向上有两种折射率 \(n_o,n_e\)，对应两正交偏振（普通光、非常光）。
- 通过厚度为 \(t\) 的双折射晶体，二者相位延迟
$$
\delta=\frac{2\pi}{\lambda}(n_e-n_o)t
$$
- 当 \(\delta=\pi\) 为半波片，\(\delta=\pi/2\) 为四分之一波片，可用于旋转偏振方向或把线偏振变为圆/椭圆偏振。
- 偏振棱镜（如尼科尔棱镜）利用双折射与全反射选择性透过某一偏振，实现偏振分束。
""",
        "§17-15": r"""
- 旋光现象可理解为介质对左、右圆偏振的折射率不同（圆双折射），导致两圆偏振分量相位差积累。
- 线偏振光可分解为等振幅左、右圆偏振叠加。传播距离 \(l\) 后相位差 \(\Delta\phi\) 使合成线偏振方向旋转角
$$
\theta=\frac{\Delta\phi}{2}
$$
- 实验上常用旋光度与浓度、长度成正比的经验关系 \(\theta=[\alpha]cl\)（溶液中），推导核心仍是相位积累。
""",
        "§17-16": r"""
- 偏振光干涉的关键是：只有在同一偏振方向上有共同分量的两束光才能发生强度干涉。
- 若两束线偏振光夹角为 \(\theta\)，则可将它们投影到同一方向后叠加，干涉项会乘以 \(\cos\theta\) 因子，导致可见度降低。
- 用 Jones 矢量/矩阵可系统推导：先对两束光做偏振变换，再做复振幅叠加，最后取模平方得到强度分布。
""",
        "§17-17": r"""
- 非线性光学的起点是把极化强度展开为电场的幂级数：
$$
\vec P=\varepsilon_0\left(\chi^{(1)}\vec E+\chi^{(2)}\vec E^2+\chi^{(3)}\vec E^3+\cdots\right)
$$
- 当 \(\chi^{(2)}\neq 0\) 时，输入频率 \(\omega\) 的电场会产生 \(2\omega\) 分量（倍频）、\(\omega_1\pm\omega_2\)（和频/差频）等，这是二次非线性过程的直接结果。
- 推导上通常把 \(\vec E\) 代入波动方程，非线性极化项作为“源项”驱动新频率波产生；相位匹配条件决定转换效率高低。
- 非线性效应需要高光强（如激光）才能显著，因为高阶项相对线性项通常很小。
""",
    }
)

# Chapter 18: Relativity
SECTION_BLOCKS.update(
    {
        "§18-1": r"""
- 伽利略变换描述经典时空：两惯性系相对速度 \(v\) 沿 \(x\) 轴时
$$
x'=x-vt,\quad y'=y,\quad z'=z,\quad t'=t
$$
- 因 \(t'=t\)，经典力学默认“绝对时间”。速度变换 \(u_x'=u_x-v\)，加速度不变 \(a'=a\)，因此牛顿第二定律形式不变。
- 这一时空观与电磁学冲突：若按伽利略变换，光速应在不同惯性系中不同；但实验与麦克斯韦方程都指向光速不变，从而需要新的时空变换（洛伦兹变换）。
""",
        "§18-2": r"""
- 迈克耳孙-莫雷实验试图测量“以太风”导致的光速各向异性。干涉仪两臂等长 \(L\)，假设装置相对以太速度为 \(v\)。
- 沿运动方向臂：往返时间近似
$$
t_\parallel=\frac{L}{c-v}+\frac{L}{c+v}=\frac{2Lc}{c^2-v^2}\approx \frac{2L}{c}\left(1+\frac{v^2}{c^2}\right)
$$
- 垂直方向臂：光需斜走补偿横向速度，往返时间
$$
t_\perp=\frac{2L}{\sqrt{c^2-v^2}}\approx \frac{2L}{c}\left(1+\frac{v^2}{2c^2}\right)
$$
- 二者差
$$
\Delta t=t_\parallel-t_\perp\approx \frac{Lv^2}{c^3}
$$
旋转装置应导致条纹移动；实验却得到近似零结果，否定了简单以太模型并推动狭义相对论建立。
""",
        "§18-3": r"""
- 狭义相对论两公设：相对性原理（所有惯性系物理定律相同）与光速不变（真空光速对所有惯性系相同）。
- 由线性变换假设与两公设可推出洛伦兹变换（沿 \(x\) 方向相对运动）：
$$
x'=\gamma(x-vt),\quad t'=\gamma\left(t-\frac{vx}{c^2}\right),\quad \gamma=\frac{1}{\sqrt{1-\beta^2}},\ \beta=v/c
$$
- 同地事件 \(\Delta x=0\) 给时间膨胀：\(\Delta t=\gamma\Delta t_0\)。
- 同时测量 \(\Delta t'=0\) 给长度收缩：\(L=L_0/\gamma\)。
- 这些效应不是“钟变慢/尺变短”的力学过程变化，而是不同惯性系对时空坐标划分不同导致的测量结果差异。
""",
        "§18-4": r"""
- 相对论时空的核心是不变量：时空间隔
$$
s^2=c^2\Delta t^2-\Delta x^2-\Delta y^2-\Delta z^2
$$
在洛伦兹变换下保持不变。
- 同时性的相对性：在一个系中 \(\Delta t=0\) 的两事件，在另一个系中一般有 \(\Delta t'\ne 0\)，由 \(t'=\gamma(t-vx/c^2)\) 直接看出。
- 事件因果结构由 \(s^2\) 的符号决定：\(s^2>0\)（类时）可因果联系；\(s^2<0\)（类空）不能以低于光速的信号联系；这比“直觉时间先后”更根本。
""",
        "§18-5": r"""
- 光的相对论多普勒效应需用洛伦兹变换处理。沿相对运动方向（正向接近）有
$$
f'=f\sqrt{\frac{1+\beta}{1-\beta}}
$$
远离则互换 \(\beta\to -\beta\)。
- 推导思路：把电磁波相位 \(\phi=\omega t-kx\) 视作洛伦兹标量，在不同参考系中相位相同，比较 \(\omega\) 得到频率变换。
- 一般角度还会出现相对论光行差与角度因子，但本质仍是四波矢变换。
""",
        "§18-6": r"""
- 定义相对论动量与总能量：
$$
\vec p=\gamma m\vec v,\qquad E=\gamma mc^2
$$
- 用四动量不变量可得能量-动量关系：
$$
E^2=(pc)^2+(mc^2)^2
$$
- 动能定义为 \(K=E-mc^2=(\gamma-1)mc^2\)。当 \(v\ll c\) 时 \(\gamma\approx 1+\tfrac12\beta^2\)，因此
$$
K\approx \tfrac12mv^2
$$
回到经典结果。
- 高速碰撞/衰变问题应优先使用四动量守恒，避免把经典公式与相对论公式混用。
""",
        "§18-7": r"""
- 广义相对论的起点是等效原理：在足够小的时空区域内，引力场与加速参考系等效。
- 在弱场近似下，可得到引力时间膨胀的数量级关系：深处的钟走得更慢，频率相对变化 \(\Delta f/f\sim \Delta\Phi/c^2\)（\(\Phi\) 为引力势）。
- 光在引力场中偏折、引力红移、近日点进动等现象可视为“时空度规改变导致测地线改变”的结果；定量推导需要引入度规与场方程，这里作为拓展认识即可。
""",
    }
)

# Chapter 19: Quantum physics
SECTION_BLOCKS.update(
    {
        "§19-1": r"""
- 黑体辐射的经典推导（瑞利-金斯）在高频发散（紫外灾难）。普朗克假设振子能量量子化：
$$
E_n=nh\nu
$$
- 量子化后，频率为 \(\nu\) 的振子平均能量为
$$
\bar\varepsilon=\frac{h\nu}{e^{h\nu/(k_BT)}-1}
$$
- 电磁场模态密度为 \(g(\nu)\propto \nu^2\)，结合平均能量得到普朗克谱能量密度（形式）：
$$
u(\nu)=\frac{8\pi h\nu^3}{c^3}\frac{1}{e^{h\nu/(k_BT)}-1}
$$
- 低频极限 \(h\nu\ll k_BT\) 时 \(e^{h\nu/kT}\approx 1+h\nu/kT\)，回到瑞利-金斯 \(u(\nu)\propto \nu^2T\)；高频极限回到维恩指数衰减。这说明普朗克定律统一了两端极限并消除了发散。
""",
        "§19-2": r"""
- 光电效应的核心实验事实是：存在截止频率、遏止电压随频率线性、强度影响电流不影响最大动能。
- 爱因斯坦用光子能量 \(h\nu\) 解释：能量守恒给
$$
h\nu=\phi+K_{max}
$$
其中 \(\phi\) 为逸出功。
- 遏止电压满足 \(eV_s=K_{max}\)，因此
$$
V_s=\frac{h}{e}\nu-\frac{\phi}{e}
$$
为线性关系，斜率给出 \(h/e\)。
- 强度改变的是单位时间光子数，从而改变发射电子数（电流），但单个电子获得的最大能量由 \(\nu\) 决定。
""",
        "§19-3": r"""
- 康普顿散射把光看作光子，使用能量与动量守恒。光子动量 \(p=h/\lambda\)。
- 写出散射前后能量守恒与动量守恒，消去电子动量可得波长位移：
$$
\Delta\lambda=\lambda'-\lambda=\frac{h}{m_ec}(1-\cos\theta)
$$
- 该结果直接证明光子携带动量，且散射角越大波长增量越大；最大位移在 \(\theta=\pi\)。
""",
        "§19-4": r"""
- 玻尔模型对氢原子：向心力由库仑力提供
$$
\frac{mv^2}{r}=\frac{1}{4\pi\varepsilon_0}\frac{e^2}{r^2}
$$
- 角动量量子化假设：
$$
mvr=n\hbar
$$
- 联立两式解得轨道半径 \(r_n\propto n^2\)（\(r_n=a_0n^2\)），能量
$$
E_n=-\frac{13.6\,\text{eV}}{n^2}
$$
- 辐射/吸收满足 \(h\nu=E_{n_i}-E_{n_f}\)，因此谱线离散。玻尔理论能解释氢谱主结构，但无法处理多电子与精细结构，需量子力学升级。
""",
        "§19-5": r"""
- 弗兰克-赫兹实验中电子在加速电压 \(V\) 下获得动能 \(eV\)。当 \(eV\) 达到原子第一激发能 \(\Delta E\) 时，电子发生非弹性碰撞，把能量转移给原子。
- 因为电子损失能量，收集电极电流出现下降；随着 \(V\) 继续增加，电子再次达到激发阈值，电流呈周期性起伏。
- 相邻电流谷对应的电压差 \(\Delta V\) 满足
$$
e\Delta V=\Delta E
$$
从而直接测得原子能级差，证明能级离散。
""",
        "§19-6": r"""
- 德布罗意假设：粒子也具有波动性，波长
$$
\lambda=\frac{h}{p}
$$
- 对加速电压 \(V\) 的电子，非相对论近似 \(eV=\tfrac12mv^2\)，动量 \(p=\sqrt{2meV}\)，因此
$$
\lambda=\frac{h}{\sqrt{2meV}}
$$
- 电子衍射实验（晶体衍射）验证了这一关系；当能量很高需用相对论动量修正。
""",
        "§19-7": r"""
- 用波包表示粒子：位置分布越窄（\(\Delta x\) 小），波数分布越宽（\(\Delta k\) 大），这是傅里叶变换的数学必然。
- 基本不等式给 \(\Delta x\,\Delta k\gtrsim 1/2\)。乘以 \(\hbar\) 并用 \(p=\hbar k\)，得到海森堡不确定关系：
$$
\Delta x\,\Delta p\ge \frac{\hbar}{2}
$$
- 同理可得能量-时间形式的数量级关系 \(\Delta E\,\Delta t\gtrsim \hbar/2\)（解释为谱线展宽与寿命的联系）。
- 不确定关系不是测量误差，而是量子态本身的统计分布下限。
""",
        "§19-8": r"""
- 量子力学以波函数 \(\psi(\vec r,t)\) 描述系统。概率解释：\(|\psi|^2\) 为概率密度，必须满足归一化 \(\int |\psi|^2 d\tau=1\)。
- 量子动力学由薛定谔方程给出（非相对论）：
$$
i\hbar\frac{\partial\psi}{\partial t}=\left(-\frac{\hbar^2}{2m}\nabla^2+V(\vec r,t)\right)\psi
$$
- 可观测量对应算符，期望值 \(\langle A\rangle=\int \psi^* \hat A \psi\,d\tau\)。
- 守恒量与对称性相关：若哈密顿量不显含时间则能量守恒；若势场不依赖某坐标则相应动量守恒（量子版）。
""",
        "§19-9": r"""
- 氢原子量子理论解库仑势下的定态薛定谔方程，得到量子数 \(n,l,m\) 与离散能级：
$$
E_n=-\frac{13.6\,\text{eV}}{n^2}
$$
- 角动量量子化表现为
$$
L^2=l(l+1)\hbar^2,\quad L_z=m\hbar
$$
其中 \(l=0,1,\dots,n-1\)，\(m=-l,\dots,l\)。
- 波函数的径向与角向部分分别由拉盖尔多项式与球谐函数给出；节点结构决定电子云形状（s,p,d,\dots 轨道）。
- 这些结果在 \(n\) 很大时通过对应原理趋向经典轨道图像（统计意义上的）。
""",
        "§19-10": r"""
- 多电子原子需考虑电子-电子相互作用与泡利不相容原理：每个量子态最多容纳两个自旋相反的电子。
- 近似处理采用“有效中心势 + 电子屏蔽”，仍用 \(n,l,m\) 等量子数描述轨道，但能级发生分裂。
- 电子填充遵循构造原理（能量由低到高填充）与洪特规则（同一亚层先单占后成对），从而解释元素周期律的壳层结构。
- 定量推导需要自洽场方法（Hartree-Fock 等），本科阶段通常掌握原理与规则即可。
""",
        "§19-11": r"""
- 激光的关键机制是受激辐射：入射光子诱导处于高能级的原子发出同频、同相、同方向的光子，实现光放大。
- 要获得净放大必须实现粒子数反转：高能级粒子数多于低能级，否则吸收占优。
- 腔的反馈与选模条件决定激光频率与相干性；阈值条件来自“增益 = 损耗”平衡。
- 推导上常从爱因斯坦系数与速率方程出发，得到放大系数随反转密度与截面变化的关系。
""",
        "§19-12": r"""
- 半导体的能带结构决定导电性：价带与导带之间有带隙 \(E_g\)。热激发使电子跃迁到导带并留下空穴。
- 电导率由载流子浓度与迁移率决定：
$$
\sigma=q(n\mu_n+p\mu_p)
$$
其中 \(n,p\) 为电子/空穴浓度。
- 掺杂产生 n 型或 p 型：施主提高 \(n\)，受主提高 \(p\)。p-n 结在耗尽层形成内建电场，产生单向导通（整流）的 I-V 特性。
- 进一步的器件推导（晶体管、LED、太阳能电池）建立在载流子输运方程与边界条件之上。
""",
        "§19-13": r"""
- 超导的宏观特征是零电阻与迈斯纳效应（完全抗磁）：进入超导态后磁通被排斥或以量子化通量线形式穿透（II 类）。
- 伦敦方程给出磁场在超导体内的指数衰减（穿透深度 \(\lambda_L\)），体现超导电流的无耗散性质。
- 磁通量子化：
$$
\Phi=n\frac{h}{2e}
$$
反映库珀对电荷 \(2e\) 与量子相位单值性。
- 微观机制由 BCS 理论解释（电子经晶格相互作用成对凝聚），本科复习重点掌握现象、关键量与基本方程即可。
""",
    }
)

# Chapter 20: Physics & technology
SECTION_BLOCKS.update(
    {
        "§20-1": r"""
- 等离子体是大量带电粒子组成的准中性体系，具有集体行为。一个关键尺度是德拜长度：
$$
\lambda_D=\sqrt{\frac{\varepsilon_0 k_BT}{n e^2}}
$$
它表征电荷屏蔽的空间范围。
- 受控核聚变需要高温高密度并足够长的约束时间。劳森判据用三重积（数量级）刻画点火条件：\(nT\tau_E\) 达到阈值。
- 磁约束（托卡马克、仿星器）利用洛伦兹力使带电粒子绕磁力线做螺旋运动以减少横向扩散；惯性约束则利用短时高压缩实现高密度与温度。
""",
        "§20-2": r"""
- 光纤导光基于全反射：芯层折射率 \(n_1\) 大于包层 \(n_2\)。临界角满足 \(\sin\theta_c=n_2/n_1\)。
- 光纤数值孔径（接受角）由几何与斯涅尔定律推得：
$$
NA=\sqrt{n_1^2-n_2^2}
$$
入射半角 \(\theta_{max}\) 满足 \(NA=n_0\sin\theta_{max}\)（\(n_0\) 为外界折射率）。
- 弱导近似下，V 数 \(V=\frac{2\pi a}{\lambda}NA\) 决定是否单模（\(V<2.405\) 为单模），这是工程选型的关键判据。
- 色散（材料色散、波导色散）导致脉冲展宽，限制带宽；推导通常从群速度 \(v_g=d\omega/dk\) 出发。
""",
        "§20-3": r"""
- 液晶介于固体与液体之间，分子具有取向有序而位置无序，因而表现各向异性（双折射）。
- 外加电场可改变分子取向，进而改变对偏振光的相位延迟与透过率；这与偏振片组合构成 LCD 的光阀机制。
- 推导常以本构关系与能量最小化为主线：电场能与弹性能竞争决定取向分布，阈值电压来自两种能量平衡。
""",
        "§20-4": r"""
- 扫描隧道显微镜（STM）利用量子隧穿：尖端与样品间距 \(d\) 改变会指数级影响隧穿电流。
- 典型近似给
$$
I\propto V e^{-2\kappa d},\quad \kappa\sim \sqrt{\frac{2m\Phi}{\hbar^2}}
$$
其中 \(\Phi\) 为势垒高度。指数敏感性使 STM 具备原子级分辨率。
- 原子力显微镜（AFM）测量探针与样品间微弱力导致的悬臂偏转，通过反馈保持恒力或恒高，从而获得表面形貌。
""",
        "§20-5": r"""
- 纳米尺度检测常受衍射极限约束：光学分辨率 \(\sim \lambda/(2NA)\)。要突破需用更短波长（电子显微镜）或近场/扫描探针方法。
- 电子束波长由德布罗意关系给出，能量越高波长越短，分辨率越高（同时需考虑像差与散射）。
- 许多纳米表征方法（XRD、SEM/TEM、AFM、拉曼、XPS）本质是把材料结构信息编码到散射/隧穿/谱线等可测信号里，推导要抓住“信号与结构参数的对应关系”。
""",
    }
)

# Appendix A
SECTION_BLOCKS.update(
    {
        "A-1": r"""
- 常数本身无需推导，但常数间关系可由基本方程得到：例如由电磁波波速推导
$$
c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}\Rightarrow c^2=\frac{1}{\mu_0\varepsilon_0}
$$
- 统计物理常用 \(R=N_Ak_B\)（摩尔气体常数与玻尔兹曼常数关系），用于在“每分子”与“每摩尔”表述之间切换。
- 记忆常数时配合量纲：例如 \(\varepsilon_0\) 单位使库仑定律系数为 \(1/(4\pi\varepsilon_0)\)；\(\mu_0\) 单位使安培定理系数为 \(\mu_0\)。量纲可帮助避免代入时错数量级。
""",
        "A-2": r"""
- 单位换算的通用做法是写成“等式链”并保持量纲不变：例如
$$
1\,\text{eV}=1.602\times10^{-19}\,\text{J}
$$
把能量统一到 SI 后再代入公式。
- 前缀换算用 \(10^n\) 处理：\(1\,\text{nm}=10^{-9}\,\text{m}\)，\(1\,\text{mm}=10^{-3}\,\text{m}\) 等。
- 数值计算建议先做数量级 sanity check：例如把 \(10^{-6}\) 写错为 \(10^{-3}\) 会导致千倍误差，量纲与数量级双重检查能快速发现。
""",
        "A-3": r"""
- 常用微积分公式来自基本定理与线性性：\(\frac{d}{dx}\int_a^x f(t)\,dt=f(x)\)，\(\int u\,dv=uv-\int v\,du\)。
- 常用三角恒等式与指数形式可简化振动/波动推导：\(\cos\alpha+\cos\beta=2\cos\frac{\alpha+\beta}{2}\cos\frac{\alpha-\beta}{2}\)（拍频推导核心）。
- 向量恒等式与积分定理把“局部”与“整体”联系起来：高斯定理、斯托克斯定理分别对应通量守恒与环量守恒，是电磁学微分形式推导的桥梁。
""",
    }
)


# Title keyword specific blocks (high priority)
TITLE_BLOCKS: list[tuple[list[str], str]] = [
    (["质点运动的描述", "运动的描述"], r"""
- 由定义：\(\vec v\equiv d\vec r/dt\)。这不是“推出来”的结论，而是速度的数学定义。
- 把 \(\vec v\) 再对时间求导，得到加速度定义：\(\vec a\equiv d\vec v/dt=d^2\vec r/dt^2\)。
- 反过来，若已知 \(\vec v(t)\)，则位移来自积分：\(\vec r(t)=\vec r_0+\int_0^t\vec v(t')dt'\)。
- 若已知 \(\vec a(t)\)，先积分得 \(\vec v(t)=\vec v_0+\int_0^t\vec a(t')dt'\)，再积分得 \(\vec r(t)\)。
- 速度是矢量，速率是大小：\(|\vec v|\)。把矢量误当标量会在方向题里直接出错。
"""),
    (["电流", "电流密度"], r"""
- 电流定义为单位时间通过截面的电荷量：\(I\equiv dq/dt\)。
- 电流密度定义为单位面积上的电流矢量：
$$
\vec J\equiv \frac{dq}{dt\,d\vec A}\quad\Rightarrow\quad I=\int_S\vec J\cdot d\vec A
$$
- 若载流子数密度为 \(n\)，电荷量为 \(q\)，漂移速度为 \(\vec v_d\)，则单位体积电荷量 \(nq\)，流过面积的电荷通量给
$$
\vec J=nq\vec v_d
$$
- 方向按正电荷运动定义，电子漂移方向与 \(\vec J\) 相反，这是常见符号错误来源。
"""),
    (["欧姆定律的微分形式", "电阻率"], r"""
- 微观欧姆定律写成 \(\vec J=\sigma\vec E\)，来自载流子在电场中达到稳态漂移（加速与散射平衡）。
- 对长度 \(L\)、截面积 \(A\) 的均匀导体：\(J=I/A\)、\(E=U/L\)。代入得
$$
\frac{I}{A}=\sigma\frac{U}{L}\Rightarrow U=\frac{L}{\sigma A}I
$$
- 因而电阻 \(R\equiv U/I=\rho L/A\)，其中 \(\rho\equiv 1/\sigma\)。
- 该推导隐含均匀各向同性材料与稳恒电流条件。
"""),
]

# Derive-bullets pattern based blocks (medium priority)
PATTERN_BLOCKS: list[tuple[list[str], str]] = [
    (["t^2", "v = v_0", "v^2 = v_0"], r"""
- 从 \(\vec a=d\vec v/dt\) 且 \(\vec a\) 常量出发，时间积分得 \(\vec v=\vec v_0+\vec a t\)。
- 再由 \(\vec v=d\vec r/dt\) 积分得 \(\vec r=\vec r_0+\vec v_0 t+\tfrac12\vec a t^2\)。
- 为消去时间，用链式法则（一维）：\(a=dv/dt=v\,dv/dx\)，积分得 \(v^2=v_0^2+2a(x-x_0)\)。
- 适用条件是加速度恒定，若 \(a\) 随时变或随位移变需改用积分或能量法。
"""),
    (["v^2/r", "r\\omega^2", "a_n"], r"""
- 速度方向变化导致向心加速度。用极坐标基矢导数：\(\dot{\hat e}_r=\dot\theta\hat e_\theta\)、\(\dot{\hat e}_\theta=-\dot\theta\hat e_r\)。
- 匀速圆周时 \(\vec v=r\omega\hat e_\theta\)，求导得 \(\vec a=-r\omega^2\hat e_r\)，大小 \(a_n=v^2/r\)。
- 另一条常用推导：\(\vec v=\vec\omega\times\vec r\Rightarrow \vec a=\vec\omega\times(\vec\omega\times\vec r)\)（\(\omega\) 常量）。
"""),
    (["\\oint\\vec E", "\\nabla V", "\\vec E=-\\nabla"], r"""
- 静电场满足 \(\oint\vec E\cdot d\vec l=0\)，因此沿不同路径积分得到的做功相同，电势差与路径无关。
- 定义电势：\(V(B)-V(A)=-\int_A^B\vec E\cdot d\vec l\)。取 \(B=A+d\vec l\) 得 \(dV=-\vec E\cdot d\vec l\)。
- 与微分恒等式 \(dV=\nabla V\cdot d\vec l\) 对比，推出 \(\vec E=-\nabla V\)。
"""),
    (["\\oint\\vec E\\cdot d\\vec A", "q_{\\text{in}}", "\\varepsilon_0"], r"""
- 对点电荷，球面对称使 \(\vec E\) 在球面上大小恒定、方向径向。
- 通量：\(\Phi_E=\oint\vec E\cdot d\vec A=E\,4\pi r^2\)。代入 \(E=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\) 得 \(\Phi_E=q/\varepsilon_0\)。
- 由叠加原理推广到任意电荷分布：\(\oint\vec E\cdot d\vec A=q_{in}/\varepsilon_0\)。
- 这一步隐含库仑反平方律与空间各向同性，是高斯定理成立的数学根源。
"""),
    (["RC", "e^{-t/RC}", "\\tau=RC"], r"""
- 充电：KVL 写 \(\mathcal{E}=IR+Q/C\)，用 \(I=dQ/dt\) 得一阶方程 \(R\,dQ/dt+Q/C=\mathcal{E}\)。
- 解得 \(Q(t)=C\mathcal{E}(1-e^{-t/RC})\)，因此 \(U_C(t)=\mathcal{E}(1-e^{-t/RC})\)、\(I(t)=(\mathcal{E}/R)e^{-t/RC}\)。
- 放电：\(R\,dQ/dt+Q/C=0\Rightarrow Q=Q_0e^{-t/RC}\)。时间常数 \(\tau=RC\) 控制快慢。
"""),
    (["LC", "1/\\sqrt{LC}", "d^2Q/dt^2"], r"""
- LC 回路 KVL：\(L\,dI/dt+Q/C=0\)，且 \(I=dQ/dt\)。
- 得二阶方程：\(d^2Q/dt^2+(1/LC)Q=0\)，与简谐振子同型。
- 因而 \(\omega=1/\sqrt{LC}\)。能量在 \(U_E=Q^2/(2C)\) 与 \(U_B=LI^2/2\) 间周期交换。
"""),
    (["\\oint\\vec B\\cdot d\\vec l", "\\mu_0"], r"""
- 安培环路定理：\(\oint\vec B\cdot d\vec l=\mu_0 I_{enc}\)。
- 对长直导线取同心圆环路，\(B\) 恒定且切向：\(B2\pi r=\mu_0I\Rightarrow B=\mu_0I/(2\pi r)\)。
- 对螺线管用矩形环路与近似 \(B\) 仅在内部显著，可得 \(B\approx\mu_0 nI\)。
"""),
    (["d\\vec B", "I\\,d\\vec l\\times"], r"""
- 毕奥-萨伐尔定律给电流元贡献：\(d\vec B=\frac{\mu_0}{4\pi}\frac{I\,d\vec l\times\hat r}{r^2}\)。
- 对整条导体积分并用对称性化简，长直导线积分可得到 \(B=\mu_0I/(2\pi r)\)。
- 方向由叉乘决定，可用右手定则快速判定。
"""),
    (["-d\\Phi", "d\\Phi_B/dt"], r"""
- 法拉第定律：\(\mathcal{E}=\oint\vec E\cdot d\vec l=-d\Phi_B/dt\)。
- 负号（楞次定律）由能量守恒约束：感应电流的磁场总反抗磁通变化，避免“无源增能”。
- 若为动生电动势，可从洛伦兹力 \(q\vec v\times\vec B\) 推出沿导体长度方向的等效电场。
"""),
    (["\\ddot x+\\omega^2", "F=-kx"], r"""
- 由胡克定律 \(F=-kx\) 与牛顿第二定律 \(m\ddot x=F\) 得 \(\ddot x+\omega^2x=0\)，\(\omega=\sqrt{k/m}\)。
- 该方程的特征根为 \(\pm i\omega\)，因此解为正弦/余弦形式。
- 能量守恒可由 \(\delta W=Fdx\) 积分得到势能 \(U=\tfrac12kx^2\)，从而总能量 \(E=\tfrac12kA^2\)。
"""),
    (["\\partial^2 y", "\\sqrt{T/\\mu}"], r"""
- 对张紧弦取微段 \(dx\)。小斜率下竖直合力 \(\approx T\,\partial^2y/\partial x^2\,dx\)。
- 质量为 \(\mu dx\)，代入牛顿第二定律得
$$
\frac{\partial^2 y}{\partial t^2}=\frac{T}{\mu}\frac{\partial^2 y}{\partial x^2},\quad v=\sqrt{T/\mu}
$$
- 一般解为行波叠加：\(y=f(x-vt)+g(x+vt)\)，边界条件决定驻波允许频率。
"""),
    (["\\nabla^2\\vec E", "\\mu_0\\varepsilon_0"], r"""
- 在真空 \(\nabla\cdot\vec E=0\)、\(\nabla\times\vec E=-\partial\vec B/\partial t\)、\(\nabla\times\vec B=\mu_0\varepsilon_0\partial\vec E/\partial t\)。
- 对 \(\nabla\times\vec E\) 取旋度并用恒等式化简，得波动方程
$$
\nabla^2\vec E-\mu_0\varepsilon_0\frac{\partial^2\vec E}{\partial t^2}=0
$$
- 因此波速 \(c=1/\sqrt{\mu_0\varepsilon_0}\)。磁场同理。
"""),
    (["\\Delta x=", "\\lambda L/d", "d\\sin"], r"""
- 两缝到屏上点 \(x\) 的光程差 \(\Delta\approx d\sin\theta\approx d x/L\)。
- 明纹条件 \(\Delta=m\lambda\)，得到 \(x_m=m\lambda L/d\)，条纹间距 \(\Delta x=\lambda L/d\)。
- 强度由振幅叠加：\(I=I_1+I_2+2\sqrt{I_1I_2}\cos(2\pi\Delta/\lambda)\)。
"""),
    (["a\\sin\\theta", "(\\sin\\beta/\\beta"], r"""
- 单缝远场把缝看作连续二次波源。不同位置到观察点的相位线性变化。
- 当相位差对应半缝宽配对相消时出现暗纹：\(a\sin\theta=m\lambda\)。
- 更完整强度分布为 \(I=I_0(\sin\beta/\beta)^2\)，\(\beta=\pi a\sin\theta/\lambda\)。
"""),
    # NOTE: Avoid overly-broad patterns like "\gamma" which also appears as the
    # adiabatic exponent in thermodynamics. Relativity sections should be
    # matched by SECTION_BLOCKS or TITLE_BLOCKS, not by this generic pattern.
    (["h\\nu", "\\phi", "eV_s"], r"""
- 光电方程是能量守恒：\(h\nu=\phi+K_{max}\)。
- 遏止电压 \(V_s\) 满足 \(eV_s=K_{max}\)，因此 \(V_s\) 对 \(\nu\) 线性。
- 强度改变的是光子数，从而改变电流大小，不改变 \(K_{max}\)。
"""),
    (["\\Delta\\lambda", "m_ec"], r"""
- 康普顿散射用光子动量 \(p=h/\lambda\) 与能量守恒联立。
- 消去电子动量可得波长位移：\(\Delta\lambda=\frac{h}{m_ec}(1-\cos\theta)\)。
- 这直接证明光子携带动量，不能用纯经典波解释。
"""),
    (["d\\vec r/dt", "d\\vec v/dt", "d^2\\vec r"], r"""
- 由定义链：\(\vec v=d\vec r/dt\)、\(\vec a=d\vec v/dt\)；把已知的 \(\vec r(t)\) 求导即可得到 \(\vec v(t),\vec a(t)\)。
- 若已知 \(\vec a(t)\)，则反向积分：
$$
\vec v(t)=\vec v_0+\int_0^t\vec a(t')\,dt'
$$
$$
\vec r(t)=\vec r_0+\int_0^t\vec v(t')\,dt'
$$
- 若给的是标量函数 \(x(t)\)，上式对每一分量分别成立：\(v_x=\dot x\)、\(a_x=\ddot x\)。
"""),
]


def _dedent(s: str) -> list[str]:
    return textwrap.dedent(s).strip().splitlines()


def pick_block(title: str, theme: str, derive_text: str) -> list[str]:
    # 0) Section id blocks (highest priority)
    sec_id = extract_section_id(title)
    if sec_id and sec_id in SECTION_BLOCKS:
        return _dedent(SECTION_BLOCKS[sec_id])

    # 1) Title blocks
    for kws, blk in TITLE_BLOCKS:
        if any(kw in title for kw in kws):
            return _dedent(blk)

    # 2) Pattern blocks from derive bullets
    for pats, blk in PATTERN_BLOCKS:
        if any(pat in derive_text for pat in pats):
            return _dedent(blk)

    # 3) Theme fallback
    fb = THEME_FALLBACK.get(theme, THEME_FALLBACK["mechanics"])
    return _dedent(fb)


def is_section_marker(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if s.startswith("### ") or s.startswith("## "):
        return True
    # bold markers like **物理意义**
    if s.startswith("**") and s.endswith("**") and len(s) >= 6:
        return True
    return False


def main() -> None:
    changed_files = 0
    updated_blocks = 0

    for path in sorted(TOPICS.glob('*.md')):
        theme = FILE_THEME.get(path.name, 'mechanics')
        lines = path.read_text(encoding='utf-8').splitlines()

        try:
            double_start = next(i for i, l in enumerate(lines) if l.strip() == DOUBLE_TITLE)
        except StopIteration:
            continue

        out: list[str] = []
        in_double = False
        current_title = ""
        changed = False

        i = 0
        while i < len(lines):
            line = lines[i]
            if i == double_start:
                in_double = True

            if in_double and line.startswith('### '):
                t = line[4:].strip()
                current_title = t.replace('（加倍细化）', '').strip()

            out.append(line)

            if in_double and line.strip() == DERIVE_MARKER:
                # gather derive bullets
                derive_bullets: list[str] = []
                i += 1
                while i < len(lines) and lines[i].startswith('- '):
                    derive_bullets.append(lines[i])
                    out.append(lines[i])
                    i += 1

                derive_text = "\n".join(derive_bullets)

                # If an existing proof block exists, drop it.
                if i < len(lines) and lines[i].strip() == PROOF_MARKER:
                    # skip marker
                    i += 1
                    # skip until next marker (typically **物理意义**)
                    while i < len(lines) and not is_section_marker(lines[i]):
                        i += 1
                    changed = True

                # Insert refreshed proof block
                out.append(PROOF_MARKER)
                out.extend(pick_block(current_title, theme, derive_text))
                updated_blocks += 1
                changed = True
                continue

            i += 1

        if changed:
            path.write_text('\n'.join(out) + '\n', encoding='utf-8')
            changed_files += 1

    print('changed_files', changed_files, 'updated_blocks', updated_blocks)


if __name__ == '__main__':
    main()
