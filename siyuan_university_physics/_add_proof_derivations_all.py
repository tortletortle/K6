# -*- coding: utf-8 -*-
"""Add step-by-step proof/derivation blocks to every double-detail subsection.

We insert a **推导详解（证明）** block right after **推导要点**'s bullet list,
inside the "## 本章加倍细化" area, unless the block already exists.

The goal is to make the notes more review-ready by showing where formulas come from.
"""

from __future__ import annotations

from pathlib import Path
import textwrap

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
- 先写出物理量的量纲（如 \([v]=LT^{-1}\)、\([a]=LT^{-2}\)），用量纲一致性筛掉不可能的形式。
- 对“近似/小量”问题，用泰勒展开保留主导项，并标注适用条件（例如 \(\sin\theta\approx\theta\) 需 \(|\theta|\ll 1\)）。
- 对测量类结论，可从误差传播公式出发：若 \(y=f(x_1,\dots,x_n)\)，则
$$
 u_y^2=\sum_i\left(\frac{\partial f}{\partial x_i}\right)^2u_{x_i}^2\quad(\text{独立误差})
$$
- 推导末尾用“极限检验”：参数趋零、趋大时是否回到已知特例。
""",
    "mechanics": r"""
- 先把文字条件翻译成数学关系：\(\vec v=d\vec r/dt\)、\(\vec a=d\vec v/dt\)、\(\sum\vec F=d\vec p/dt\)。
- 若力恒定或加速度恒定，优先用积分得到速度与位移表达式，并用初始条件定常数。
- 若出现保守力，写能量链：\(W=\Delta K\)，或 \(K+U=\text{const}\)，常比逐分量更稳。
- 若出现碰撞/短时强力，写冲量：\(\vec J=\int\vec F\,dt=\Delta\vec p\)。
- 最后做量纲与方向检查：矢量量必须包含方向信息，不能只算大小。
""",
    "thermo": r"""
- 先区分状态量与过程量：\(U,S,T,P,V\) 为状态量；\(\delta Q,\delta W\) 为过程量。
- 第一律写成微分形式：\(dU=\delta Q-\delta W\)，对准路径积分，注意 \(\delta Q,\delta W\) 不是全微分。
- 对准静过程的体积功：\(\delta W=P\,dV\)，可据过程方程（等温/绝热/等压等）积分得到功与热。
- 第二律用可逆过程建立：\(dS=\delta Q_{rev}/T\)，再用熵增判据判断自发方向。
- 理想气体模型常配合 \(PV=nRT\) 与 \(U=U(T)\)（单原子：\(U=\tfrac32nRT\)）。
""",
    "waves": r"""
- 对机械波先做“微元受力”建模：取长度 \(dx\) 的微段，用牛顿第二定律写出微分方程。
- 线性近似（小振幅、小斜率）使方程变为波动方程，这是能叠加的根本原因。
- 把解写成行波形式 \(y=f(x-vt)\) 或简谐波 \(y=A\cos(\omega t-kx+\phi)\)，并由边界条件确定允许的 \(k\)。
- 许多结论来自相位：相位差 \(\Delta\varphi\) 决定增强/相消与驻波节点位置。
""",
    "em": r"""
- 从“定义+积分定理+对称性”三件套出发：\(\vec E=\vec F/q\)、\(V=-W/q\)、\(\Phi_E=\oint\vec E\cdot d\vec A\)。
- 若有球/柱/平面对称，选高斯面让 \(\vec E\) 在面上大小恒定且方向与法线一致，以便把积分化为乘法。
- 静电场满足 \(\oint\vec E\cdot d\vec l=0\)，因此可引入电势并得 \(\vec E=-\nabla V\)。
- 电路类问题先写守恒：电荷守恒给出结点方程，能量守恒给出回路方程。
""",
    "emwaves": r"""
- 先把系统写成线性微分方程：例如 LC 回路由 KVL 得 \(L\,dI/dt+Q/C=0\)，再用 \(I=dQ/dt\) 化成二阶方程。
- 对电磁波，用麦克斯韦方程组联立并取旋度，可得到波动方程与传播速度。
- 能量与功率用坡印廷矢量：\(\vec S=\frac1{\mu_0}\vec E\times\vec B\)，便于解释能流方向。
""",
    "optics": r"""
- 干涉先写光程差 \(\Delta\) 或相位差 \(\Delta\varphi=2\pi\Delta/\lambda\)，明暗条件由 \(\cos\Delta\varphi\) 决定。
- 薄膜/反射问题要单独检查“反射相位反转”（是否多了 \(\pi\)）。
- 衍射可从惠更斯-菲涅耳原理出发，远场衍射与孔径函数的傅里叶变换对应。
- 分辨率用瑞利判据建立：圆孔第一暗环角度 \(\theta\approx1.22\lambda/D\)。
""",
    "relativity": r"""
- 先明确两条公设：相对性原理与光速不变，并由此得到洛伦兹因子 \(\gamma=1/\sqrt{1-\beta^2}\)。
- 把结论尽量写成不变量形式（如 \(s^2=c^2t^2-x^2-y^2-z^2\)、\(E^2-(pc)^2=m^2c^4\)），可避免参考系混乱。
- 时间膨胀与尺缩都来自同一变换：\(t'=\gamma(t-vx/c^2)\)、\(x'=\gamma(x-vt)\)。
""",
    "quantum": r"""
- 量子化往往来自“边界条件+驻波”思想：允许的波函数必须单值、有限、可归一。
- 由德布罗意关系 \(\lambda=h/p\) 把粒子动量与波长关联，再由驻波条件得到离散量。
- 不确定性可从波包傅里叶展开理解：波包越窄，频谱越宽，从而 \(\Delta x\Delta p\ge\hbar/2\)。
- 若需要概率解释，使用 \(|\psi|^2\) 为概率密度，并用归一化确定常数。
""",
    "tech": r"""
- 技术章节的推导通常从“物理机制+关键近似”出发：先写出决定性参数，再解释工程约束。
- 例如光纤先由全反射与临界角推出接受角与 NA，再讨论色散如何导致脉冲展宽。
- 推导时要明确假设（单模/多模、弱导近似、忽略损耗等），否则公式适用范围不清。
""",
    "constants": r"""
- 常数与单位的“推导”重点是关系式与量纲一致：例如 \(c^2=1/(\varepsilon_0\mu_0)\)、\(R=N_Ak_B\)。
- 单位换算可写成等式链：\(1\,\text{eV}=1.602\times10^{-19}\,\text{J}\)，保持量纲不变。
- 用数量级估算先判断合理范围，再做精算。
""",
}


KEYWORD_PROOFS: list[tuple[list[str], str]] = [
    # Kinematics
    (["加速度为恒", "恒加速度"], r"""
- 从 \(\vec a=d\vec v/dt\) 出发，若 \(\vec a\) 为常矢量，则
$$
\vec v(t)=\vec v_0+\vec a\,t
$$
- 再由 \(\vec v=d\vec r/dt\) 积分得
$$
\vec r(t)=\vec r_0+\vec v_0 t+\tfrac12\vec a\,t^2
$$
- 需要消去时间时，用链式法则：\(\vec a=d\vec v/dt=(d\vec v/dx)(dx/dt)=v\,d\vec v/dx\)（一维时为 \(a=v\,dv/dx\)）。
- 由 \(a=v\,dv/dx\) 积分得到常用末速度关系：\(v^2=v_0^2+2a(x-x_0)\)。
"""),
    (["圆周运动"], r"""
- 采用平面极坐标：\(\vec r=r\hat e_r\)。基矢满足
$$
\dot{\hat e}_r=\dot\theta\,\hat e_\theta,\qquad \dot{\hat e}_\theta=-\dot\theta\,\hat e_r
$$
- 速度为
$$
\vec v=\dot r\,\hat e_r+r\dot\theta\,\hat e_\theta
$$
- 加速度为
$$
\vec a=(\ddot r-r\dot\theta^2)\hat e_r+(r\ddot\theta+2\dot r\dot\theta)\hat e_\theta
$$
- 匀速圆周运动：\(\dot r=0,\ddot r=0,\dot\theta=\omega\) 常数，得 \(\vec a=-r\omega^2\hat e_r\)，大小 \(a_n=v^2/r\)。
"""),
    (["相对运动"], r"""
- 两惯性系 S 与 S' 若相对速度为 \(\vec V\)，伽利略变换写成 \(\vec r' = \vec r-\vec V t\)、\(t'=t\)。
- 对时间求导：\(\vec v'=d\vec r'/dt=\vec v-\vec V\)（速度叠加）。
- 再求导：\(\vec a'=d\vec v'/dt=\vec a\)（惯性系间加速度不变）。
- 复杂相对运动题建议先画速度矢量三角形，再写分量方程，避免符号混乱。
"""),

    # Newton & momentum/energy
    (["牛顿定律"], r"""
- 更一般的表述是动量形式：
$$
\sum\vec F=\frac{d\vec p}{dt}
$$
- 若质量恒定 \(\vec p=m\vec v\)，则化为 \(\sum\vec F=m\vec a\)。
- 对时间积分得动量定理（冲量定理）：
$$
\int_{t_1}^{t_2}\sum\vec F\,dt=\Delta\vec p
$$
- 对封闭系统，若内力满足第三定律并成对出现，则 \(\sum\vec F_{ext}=d\vec P/dt\)，外力为零时总动量守恒。
"""),
    (["功", "功率", "能量"], r"""
- 从微元功定义：\(\delta W=\vec F\cdot d\vec r\)。
- 用 \(\vec F=m\vec a\)、\(\vec a=d\vec v/dt\)、以及 \(d\vec r=\vec v\,dt\)，得
$$
\delta W=m\frac{d\vec v}{dt}\cdot\vec v\,dt=m\,\vec v\cdot d\vec v=d\left(\tfrac12 m v^2\right)
$$
- 积分得到功-能定理：\(W_{1\to2}=\Delta K\)。
- 功率是做功快慢：\(P=dW/dt=\vec F\cdot\vec v\)。
"""),
    (["动量", "冲量"], r"""
- 由 \(\sum\vec F=d\vec p/dt\) 两端积分：\(\vec J=\int\sum\vec F\,dt=\Delta\vec p\)。
- 若碰撞时间很短，可把外力冲量近似为 0，则系统总动量近似守恒。
- 对一维完全弹性碰撞，可同时使用动量守恒与动能守恒联立求解。
"""),
    (["角动量"], r"""
- 定义角动量：\(\vec L=\vec r\times\vec p\)。对时间求导：
$$
\frac{d\vec L}{dt}=\vec r\times\frac{d\vec p}{dt}+\vec v\times\vec p
$$
- 因 \(\vec v\times\vec p=\vec v\times m\vec v=0\)，得
$$
\frac{d\vec L}{dt}=\vec r\times\sum\vec F=\sum\vec\tau
$$
- 若外力矩为零，则 \(\vec L\) 守恒。
"""),
    (["转动惯量"], r"""
- 刚体绕定轴转动时，质点速度 \(v=\omega r_\perp\)。转动动能是各质点动能之和：
$$
K=\sum\tfrac12 m_i v_i^2=\tfrac12\omega^2\sum m_i r_{\perp i}^2
$$
- 定义转动惯量：\(I=\sum m_i r_{\perp i}^2\)，连续体时
$$
I=\int r_\perp^2\,dm
$$
- 平行轴定理：\(I=I_{cm}+Md^2\)，可由坐标平移后展开 \(r_\perp^2\) 并用质心条件推出。
"""),

    # Gravitation
    (["万有引力"], r"""
- 从万有引力定律：\(F=GmM/r^2\)。若把 \(M\) 看作地球，\(m\) 为试探质量，则重力场强
$$
 g=\frac{F}{m}=\frac{GM}{r^2}
$$
- 圆轨道由向心力条件：\(mv^2/r=GMm/r^2\)，得
$$
 v=\sqrt{\frac{GM}{r}},\qquad \omega=\sqrt{\frac{GM}{r^3}}
$$
- 由能量守恒可得逃逸速度：\(\tfrac12mv_e^2=GMm/r\Rightarrow v_e=\sqrt{2GM/r}\)。
"""),

    # Thermodynamics
    (["第一定律", "内能"], r"""
- 热力学第一定律是能量守恒在热过程中的表述：
$$
 dU=\delta Q-\delta W
$$
- 准静体积功 \(\delta W=P\,dV\)，则
$$
 dU=\delta Q-P\,dV
$$
- 对给定过程积分：\(\Delta U=Q-W\)。若为理想气体且 \(U=U(T)\)，即可用温度变化替代内能变化。
"""),
    (["卡诺", "熵", "第二定律"], r"""
- 熵用可逆过程定义：\(dS=\delta Q_{rev}/T\)。
- 对任意循环过程，克劳修斯不等式：
$$
\oint \frac{\delta Q}{T}\le 0
$$
- 卡诺循环效率由可逆性推出：
$$
\eta=1-\frac{T_2}{T_1}
$$
- 物理含义是：在同一对热源间，没有热机能超过卡诺效率。
"""),

    # Kinetic theory
    (["压强", "理想气体"], r"""
- 把气体分子视为弹性小球。对一分子与壁面碰撞，动量变化约 \(\Delta p_x=2mv_x\)。
- 单位时间内与面积 \(A\) 发生碰撞的分子数与速度分布有关，结果可汇总为
$$
P=\frac13 n m\langle v^2\rangle
$$
- 乘以体积 \(V\) 并记 \(N=nV\)，得
$$
PV=\frac13 N m\langle v^2\rangle
$$
- 再用平均平动动能 \(\tfrac12m\langle v^2\rangle=\tfrac32k_BT\)，推出理想气体状态方程 \(PV=Nk_BT=nRT\)。
"""),

    # Electrostatics
    (["电荷守恒"], r"""
- 宏观电荷守恒可写成连续性方程：
$$
\frac{\partial\rho}{\partial t}+\nabla\cdot\vec J=0
$$
- 对任意体积 \(V\) 积分并用高斯定理：
$$
\frac{d}{dt}\int_V\rho\,d\tau=-\oint_{\partial V}\vec J\cdot d\vec A
$$
- 左边是体内总电荷变化率，右边是电流穿出通量，表明电荷只能“流出/流入”，不能凭空产生或消失。
"""),
    (["库仑定律"], r"""
- 点电荷间作用力大小：\(F=k\,|q_1q_2|/r^2\)，方向沿连线。
- 定义电场：\(\vec E=\vec F/q\)，则点电荷电场为
$$
\vec E(\vec r)=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\,\hat r
$$
- 多个点电荷用叠加：\(\vec E=\sum\vec E_i\)。连续分布时写成积分 \(\vec E=\int d\vec E\)。
"""),
    (["高斯定理"], r"""
- 对点电荷，球面对称给出 \(E\) 在球面上恒定且径向：
$$
\Phi_E=\oint\vec E\cdot d\vec A=E\,4\pi r^2
$$
- 代入 \(E=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\) 得 \(\Phi_E=q/\varepsilon_0\)。
- 由叠加原理可推广到任意电荷分布与任意闭合面：
$$
\oint\vec E\cdot d\vec A=\frac{q_{\text{in}}}{\varepsilon_0}
$$
"""),
    (["环路定理"], r"""
- 静电场中 \(\nabla\times\vec E=0\)（或积分形式 \(\oint\vec E\cdot d\vec l=0\)）。
- 因此可引入标量势函数 \(V\)，使得
$$
\vec E=-\nabla V
$$
- 电势差由功定义：\(V_B-V_A=-\int_A^B\vec E\cdot d\vec l\)，与路径无关。
"""),
    (["电势"], r"""
- 由力做功：\(dW=\vec F\cdot d\vec l=q\vec E\cdot d\vec l\)。定义电势差
$$
\Delta V=V_B-V_A=-\frac{1}{q}\int_A^B dW=-\int_A^B\vec E\cdot d\vec l
$$
- 对点电荷，选无穷远为零电势，沿径向积分得
$$
V(r)=\frac{1}{4\pi\varepsilon_0}\frac{q}{r}
$$
"""),
    (["电势梯度", "电场强度与电势"], r"""
- 从 \(V_B-V_A=-\int_A^B\vec E\cdot d\vec l\) 出发，取 \(B=A+d\vec l\) 得
$$
 dV=-\vec E\cdot d\vec l
$$
- 与微分定义 \(dV=\nabla V\cdot d\vec l\) 对比，得到
$$
\vec E=-\nabla V
$$
- 在直角坐标下：\(E_x=-\partial V/\partial x\) 等。
"""),

    # Circuits
    (["电容器", "充放电", "RC"], r"""
- RC 充电回路：KVL 给 \(\mathcal{E}-IR-U_C=0\)，且 \(I=dQ/dt\)、\(U_C=Q/C\)。
- 得一阶方程：
$$
R\frac{dQ}{dt}+\frac{Q}{C}=\mathcal{E}
$$
- 解为
$$
Q(t)=C\mathcal{E}\left(1-e^{-t/RC}\right),\quad U_C(t)=\mathcal{E}\left(1-e^{-t/RC}\right)
$$
- 放电同理：\(R\,dQ/dt+Q/C=0\Rightarrow Q=Q_0e^{-t/RC}\)。
"""),

    # Magnetism
    (["安培环路", "安培定理"], r"""
- 安培环路定理（静磁）：\(\oint\vec B\cdot d\vec l=\mu_0 I_{enc}\)。
- 对无限长直导线，取同心圆环路，\(\vec B\) 切向且大小恒定：
$$
B\,(2\pi r)=\mu_0 I\Rightarrow B=\frac{\mu_0 I}{2\pi r}
$$
- 对长螺线管，取矩形环路并用对称性，得内部 \(B\approx\mu_0 n I\)。
"""),
    (["毕奥", "Biot", "萨伐尔"], r"""
- 毕奥-萨伐尔定律给电流元产生的磁场：
$$
d\vec B=\frac{\mu_0}{4\pi}\frac{I\,d\vec l\times\hat r}{r^2}
$$
- 对具体导体形状对全回路积分 \(\vec B=\int d\vec B\)。
- 若对称性好（长直导线、圆环、螺线管），常可与安培定理互证以减少积分。
"""),
    (["电磁感应", "法拉第"], r"""
- 法拉第电磁感应定律（积分形式）：
$$
\mathcal{E}=\oint\vec E\cdot d\vec l=-\frac{d\Phi_B}{dt}
$$
- 若为动生电动势，可从洛伦兹力 \(q\vec v\times\vec B\) 出发：导体中电荷受力分离形成电势差。
- 楞次定律决定方向：感应效应总反抗磁通变化，实质体现能量守恒。
"""),

    # Oscillation & waves
    (["简谐", "简谐运动"], r"""
- 恢复力与位移成正比：\(F=-kx\)。用牛顿第二定律：
$$
m\ddot x=-kx\Rightarrow \ddot x+\omega^2x=0,\quad \omega=\sqrt{k/m}
$$
- 其通解为 \(x=A\cos(\omega t+\varphi)\)。由 \(v=\dot x\)、\(a=\ddot x\) 可推出相位差关系。
- 能量由积分功得到：\(U=\tfrac12kx^2\)，总能量 \(E=K+U=\tfrac12kA^2\) 常量（无阻尼）。
"""),
    (["阻尼", "受迫", "共振"], r"""
- 阻尼受迫振动方程：
$$
m\ddot x+b\dot x+kx=F_0\cos\Omega t
$$
- 先解齐次方程得瞬态项（指数衰减），再设稳态特解 \(x=A\cos(\Omega t-\delta)\) 代入求 \(A,\delta\)。
- 稳态振幅随频率的响应曲线由
$$
A=\frac{F_0/m}{\sqrt{(\omega_0^2-\Omega^2)^2+(2\beta\Omega)^2}},\quad \beta=b/(2m)
$$
- 共振峰位置与阻尼有关，\(Q\) 越大峰越尖锐。
"""),
    (["波动方程", "弦"], r"""
- 取张紧弦上一小段 \(dx\)，两端张力大小近似同为 \(T\)，方向略有差异。
- 竖直方向合力约为 \(T\,\partial^2 y/\partial x^2\,dx\)（小斜率近似）。质量为 \(\mu dx\)。
- 牛顿第二定律给
$$
\mu dx\,\frac{\partial^2 y}{\partial t^2}=T\frac{\partial^2 y}{\partial x^2}dx
\Rightarrow \frac{\partial^2 y}{\partial t^2}=v^2\frac{\partial^2 y}{\partial x^2},\quad v=\sqrt{T/\mu}
$$
"""),

    # EM waves
    (["LC", "电磁振荡"], r"""
- LC 回路由 KVL：\(L\,dI/dt+Q/C=0\)，再用 \(I=dQ/dt\) 得
$$
\frac{d^2Q}{dt^2}+\frac{1}{LC}Q=0
$$
- 因而角频率 \(\omega=1/\sqrt{LC}\)，电荷与电流相差 \(\pi/2\)。
- 能量在电场与磁场之间交换：\(U_E=Q^2/(2C)\)、\(U_B=LI^2/2\)。
"""),
    (["电磁波", "麦克斯韦"], r"""
- 在真空中 \(\nabla\cdot\vec E=0\)、\(\nabla\times\vec E=-\partial\vec B/\partial t\)、\(\nabla\times\vec B=\mu_0\varepsilon_0\,\partial\vec E/\partial t\)。
- 对 \(\nabla\times\vec E\) 再取旋度，并用恒等式 \(\nabla\times(\nabla\times\vec E)=\nabla(\nabla\cdot\vec E)-\nabla^2\vec E\)，得
$$
\nabla^2\vec E-\mu_0\varepsilon_0\frac{\partial^2\vec E}{\partial t^2}=0
$$
- 因此波速 \(c=1/\sqrt{\mu_0\varepsilon_0}\)。磁场同理。
"""),

    # Optics
    (["双缝", "杨氏"], r"""
- 两缝间距 \(d\)，屏距 \(L\)。到屏上横向位置 \(x\) 处的光程差近似
$$
\Delta\approx d\sin\theta\approx d\,\frac{x}{L}
$$
- 明纹条件 \(\Delta=m\lambda\)，因此亮纹位置 \(x_m=m\lambda L/d\)，条纹间距 \(\Delta x=\lambda L/d\)。
- 强度来自振幅叠加：\(I=I_1+I_2+2\sqrt{I_1I_2}\cos\Delta\varphi\)。
"""),
    (["单缝"], r"""
- 将缝宽 \(a\) 分解为许多等分波源，远场相位随横向位置线性变化。
- 相位差对应的几何关系给出暗纹条件：
$$
a\sin\theta=m\lambda\quad(m=1,2,\dots)
$$
- 强度分布可写成 \(I=I_0(\sin\beta/\beta)^2\)，其中 \(\beta=\pi a\sin\theta/\lambda\)。
"""),
    (["光栅"], r"""
- 相邻缝的光程差为 \(\Delta=d\sin\theta\)。主极大条件
$$
d\sin\theta=m\lambda
$$
- 若共有 \(N\) 条缝，同一阶主极大的角宽约随 \(1/N\) 缩小，因此主峰更尖锐。
- 分辨本领可由相邻两波长主极大可分辨条件推出：\(R=\lambda/\Delta\lambda=mN\)。
"""),

    # Relativity
    (["洛伦兹", "狭义相对论"], r"""
- 由光速不变与线性假设可得洛伦兹变换：
$$
 x'=\gamma(x-vt),\qquad t'=\gamma\left(t-\frac{vx}{c^2}\right),\quad \gamma=\frac{1}{\sqrt{1-\beta^2}}
$$
- 令 \(\Delta x=0\)（同地事件）可推出时间膨胀：\(\Delta t=\gamma\Delta t_0\)。
- 令 \(\Delta t'=0\)（同时测量）可推出长度收缩：\(L=L_0/\gamma\)。
"""),
    (["能量", "动量"], r"""
- 定义相对论动量：\(\vec p=\gamma m\vec v\)，总能量：\(E=\gamma mc^2\)。
- 用四动量不变量可得能量动量关系：
$$
E^2=(pc)^2+(mc^2)^2
$$
- 因而动能 \(K=E-mc^2=(\gamma-1)mc^2\)。当 \(v\ll c\) 时展开 \(\gamma\approx1+\tfrac12\beta^2\) 回到 \(K\approx\tfrac12mv^2\)。
"""),

    # Quantum
    (["光电效应"], r"""
- 爱因斯坦光电方程来自能量守恒：单个光子能量 \(h\nu\) 分成逸出功 \(\phi\) 与电子最大动能：
$$
 h\nu=\phi+K_{max}
$$
- 遏止电压满足 \(eV_s=K_{max}\)，因此 \(V_s\) 随频率线性变化，斜率为 \(h/e\)。
- 强度只影响光子数，从而影响光电流大小，而不改变 \(K_{max}\)。
"""),
    (["康普顿"], r"""
- 把光看作光子，使用能量与动量守恒。
- 光子动量 \(p=h/\lambda\)。散射前后写守恒方程并消去电子动量，可得波长变化：
$$
\Delta\lambda=\lambda'-\lambda=\frac{h}{m_ec}(1-\cos\theta)
$$
- 最大位移在 \(\theta=\pi\) 时：\(\Delta\lambda_{max}=2h/(m_ec)\)。
"""),
    (["玻尔"], r"""
- 轨道半径由向心力条件：\(mv^2/r=k e^2/r^2\)。
- 角动量量子化：\(mvr=n\hbar\)。联立消去 \(v\) 得
$$
 r_n=a_0 n^2
$$
- 再由 \(E=K+U=\tfrac12mv^2-ke^2/r\) 得能级
$$
 E_n=-\frac{13.6\,\text{eV}}{n^2}
$$
"""),
    (["德布罗意"], r"""
- 德布罗意假设：\(\lambda=h/p\)。对加速电压 \(V\) 的电子，非相对论近似 \(eV=\tfrac12mv^2\)，得
$$
\lambda=\frac{h}{\sqrt{2meV}}
$$
- 若 \(eV\) 很大，需用相对论动量 \(p=\gamma mv\) 修正。
"""),
    (["不确定"], r"""
- 用波包表示粒子：位置分布宽度 \(\Delta x\) 越小，波数谱宽度 \(\Delta k\) 越大。
- 傅里叶变换给出基本不等式：\(\Delta x\Delta k\gtrsim 1/2\)。
- 乘以 \(\hbar\) 并用 \(p=\hbar k\)，得
$$
\Delta x\,\Delta p\ge \frac{\hbar}{2}
$$
"""),
]


def pick_block(title: str, theme: str) -> list[str]:
    for kws, block in KEYWORD_PROOFS:
        if any(kw in title for kw in kws):
            return textwrap.dedent(block).strip().splitlines()
    fb = THEME_FALLBACK.get(theme, THEME_FALLBACK["mechanics"])
    return textwrap.dedent(fb).strip().splitlines()


def main() -> None:
    changed_files = 0
    inserted_blocks = 0

    for path in sorted(TOPICS.glob("*.md")):
        theme = FILE_THEME.get(path.name, "mechanics")
        lines = path.read_text(encoding="utf-8").splitlines()

        try:
            double_start = next(i for i, l in enumerate(lines) if l.strip() == DOUBLE_TITLE)
        except StopIteration:
            # Some files might not have double-detail (shouldn't happen here)
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

            if in_double and line.startswith("### "):
                # title without trailing tag
                t = line[4:].strip()
                current_title = t.replace("（加倍细化）", "").strip()

            out.append(line)

            if in_double and line.strip() == DERIVE_MARKER:
                # copy existing derive bullets
                i += 1
                while i < len(lines) and lines[i].startswith("- "):
                    out.append(lines[i])
                    i += 1

                # if proof already present, keep it; otherwise insert
                if i < len(lines) and lines[i].strip() == PROOF_MARKER:
                    out.append(lines[i])
                    i += 1
                    while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("$$") or lines[i].strip() in {"$$", ""}):
                        out.append(lines[i])
                        i += 1
                else:
                    out.append(PROOF_MARKER)
                    out.extend(pick_block(current_title, theme))
                    inserted_blocks += 1
                    changed = True
                continue

            i += 1

        if changed:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")
            changed_files += 1

    print("changed_files", changed_files, "inserted_blocks", inserted_blocks)


if __name__ == "__main__":
    main()
