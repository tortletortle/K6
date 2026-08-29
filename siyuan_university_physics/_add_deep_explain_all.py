# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(r"D:\spot\K6\siyuan_university_physics")
base = root / "siyuan_topics_refined"

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

THEME_DEEP = {
    "foundations": [
        "- 量纲一致是所有公式的“最低门槛”，先过这一关再谈数值对错。",
        "- 把复杂问题先无量纲化，能看出主导项与可忽略项。",
        "- 量纲分析的价值在于“先判断合理性，再求精确”。",
    ],
    "mechanics": [
        "- 运动学回答“怎么动”，动力学回答“为什么这样动”，两者配合才能闭环。",
        "- 力不是让物体“有速度”，而是让速度发生变化。",
        "- 先选参考系再列方程，会显著降低符号与方向错误。",
    ],
    "thermo": [
        "- 热力学强调状态与过程：状态量与路径无关，过程量与路径有关。",
        "- 第一律是能量账本，第二律给出“自发方向”。",
        "- 微观随机性叠加成宏观确定规律，是统计物理的核心。",
    ],
    "waves": [
        "- 波动的核心是“相位”，许多公式都可归结为相位差判断。",
        "- 能量随介质传播，介质粒子只在平衡点附近振动。",
        "- 干涉与衍射不是不同现象，本质都是叠加。",
    ],
    "em": [
        "- 场是“局域作用”的语言，避免了远距离瞬时作用的矛盾。",
        "- 先找对称性再选高斯面/环路，是场论题的关键步骤。",
        "- 电路题先想等效简化，再写定律方程。",
    ],
    "emwaves": [
        "- 谐振把外驱能量“锁定”在系统中，因此振幅会显著放大。",
        "- 电磁波中电场与磁场相互生长，方向正交并共同传播。",
        "- 阻尼决定能量耗散速度，也决定共振峰的“尖锐程度”。",
    ],
    "optics": [
        "- 光学问题先判断“干涉/衍射/几何光学”哪一个主导。",
        "- 视宁度与相干性决定条纹清晰度与可见范围。",
        "- 分辨率受波动性限制，孔径与波长是决定因素。",
    ],
    "relativity": [
        "- 相对论不是“时间变慢”，而是不同参考系对时空的度量不同。",
        "- 四矢量与不变量是计算的安全路径，能避免混用公式。",
        "- 高速下能量与动量绑定，经典公式会系统性失效。",
    ],
    "quantum": [
        "- 量子力学强调“概率幅”，测量结果是概率分布而非确定值。",
        "- 量子化不是人为规定，而是边界条件与对易关系的结果。",
        "- 经典极限下量子结果会回到经典，这是对应原理。",
    ],
    "tech": [
        "- 技术章节先理解物理机制，再理解工程实现与约束条件。",
        "- 关键指标往往是“效率、稳定性、可重复性”。",
        "- 不同手段互补使用才能形成可靠表征结论。",
    ],
    "constants": [
        "- 常数和单位是“公共语言”，正确换算能避免一半的错误。",
        "- 数量级估算是快速校验答案是否合理的第一步。",
        "- 记住少数核心常数，剩下的通过关系式推导更稳。",
    ],
}

KEYWORD_DEEP = [
    (["质点运动", "运动学", "运动的描述"], [
        "- 位移、速度、加速度是同一链条上的三层“变化率”。",
        "- 任何坐标变换只改变表达，不改变真实运动轨迹。",
        "- 先判断“直线/曲线/圆周”，再选用合适公式。",
    ]),
    (["恒加速度", "抛体"], [
        "- 恒加速度意味着速度—时间图像是直线，位移—时间图像是抛物线。",
        "- 竖直方向独立于水平方向，这是分解法的根基。",
        "- 末速度平方公式来自消去时间，适用于无时间变量的题。",
    ]),
    (["圆周"], [
        "- 向心加速度不改变速率，只改变速度方向。",
        "- 切向加速度决定速率变化，两者合成总加速度。",
        "- 向心力不是新力，而是合力在指向圆心的分量。",
    ]),
    (["相对"], [
        "- 速度叠加是参考系转换的核心，先画速度矢量再列式。",
        "- 相对运动的矛盾多来自方向与符号的混淆。",
        "- 把地面系当“最终参考系”通常更直观。",
    ]),
    (["牛顿", "力"], [
        "- 牛顿第二定律是“合力=动量变化率”，不是“力产生速度”。",
        "- 惯性系中才可直接使用牛顿定律，非惯性系需加惯性力。",
        "- 受力分析图是力学题的第一步。",
    ]),
    (["摩擦"], [
        "- 静摩擦是“自适应”的，直到达到最大值才开始滑动。",
        "- 动摩擦方向总与相对运动趋势相反。",
        "- 先判断“滑/不滑”再选用摩擦模型。",
    ]),
    (["功", "能"], [
        "- 功的本质是力沿位移方向的“能量转移”。",
        "- 保守力的功只与始末位置有关，是能量法的基础。",
        "- 能量法可绕开复杂受力与路径。",
    ]),
    (["动量", "冲量"], [
        "- 冲量是力对时间的积分，决定动量的变化。",
        "- 碰撞过程很短但力很大，用冲量方法最稳。",
        "- 动量守恒要求系统合外力为零或外力冲量可忽略。",
    ]),
    (["角动量"], [
        "- 角动量守恒来自系统对外无合力矩。",
        "- 角动量与转动惯量和角速度共同决定旋转状态。",
        "- 收缩转动半径会提高角速度，这是花滑加速原理。",
    ]),
    (["转动惯量"], [
        "- 转动惯量是“转动的惯性”，分布越外越难转。",
        "- 平行轴与垂直轴定理可快速求复杂形状。",
        "- 对称性是转动惯量计算的捷径。",
    ]),
    (["引力", "万有引力"], [
        "- 万有引力随距离平方衰减，是轨道稳定的关键。",
        "- 椭圆轨道体现“引力中心力+初速度”的叠加结果。",
        "- 轨道能量与角动量共同决定形状。",
    ]),
    (["简谐", "振动", "共振"], [
        "- 简谐运动是“线性回复力”的直接结果。",
        "- 共振强调外驱频率接近固有频率时能量输入最有效。",
        "- 阻尼越小，共振越尖锐但更易失稳。",
    ]),
    (["波", "波动"], [
        "- 波速由介质性质决定，与频率无关（在无色散介质中）。",
        "- 频率由源决定，波长由波速与频率共同决定。",
        "- 能量传播与质点振动方向可不同，形成横波与纵波。",
    ]),
    (["干涉"], [
        "- 条纹位置取决于相位差，强度取决于振幅叠加。",
        "- 相干性决定干涉是否可见。",
        "- 反射相位反转常是明暗判断的关键。",
    ]),
    (["衍射"], [
        "- 衍射体现波动性，孔径越小扩散越大。",
        "- 远场衍射等价于孔径函数的傅里叶变换。",
        "- 衍射极限决定了光学系统的分辨率上限。",
    ]),
    (["多普勒"], [
        "- 频率变化来自相对运动引起的相位压缩或拉伸。",
        "- 声音与光的多普勒公式不同，注意相对论修正。",
        "- 观测到的红移/蓝移可反推速度。",
    ]),
    (["电场"], [
        "- 电场是单位正电荷受力的描述，方向与受力方向一致。",
        "- 场强叠加遵循矢量叠加，先分解再合成。",
        "- 高斯定理的优势来自对称性简化。",
    ]),
    (["电势"], [
        "- 电势是标量，计算时更方便，电场是其梯度。",
        "- 电势差决定能量变化，与路径无关。",
        "- 先求电势再求电场常更稳。",
    ]),
    (["电容"], [
        "- 电容描述“储存电荷的能力”，几何结构决定大小。",
        "- 平行板电容的关键是面积与板距。",
        "- 介质提高电容相当于降低有效电场。",
    ]),
    (["电流"], [
        "- 电流是电荷定向运动的宏观表现。",
        "- 电流方向按正电荷流动定义，电子实际运动相反。",
        "- 稳恒电流需闭合回路与持续电动势。",
    ]),
    (["电阻"], [
        "- 电阻源于载流子与晶格的散射。",
        "- 温度变化会显著改变金属电阻。",
        "- 微观欧姆定律联系电场与电流密度。",
    ]),
    (["磁场"], [
        "- 磁场对运动电荷做功为零，但改变运动方向。",
        "- 右手定则是判断方向的核心工具。",
        "- 安培环路定理对对称电流极有效。",
    ]),
    (["电磁感应", "磁通"], [
        "- 感应电动势来自磁通量变化率。",
        "- 楞次定律给出方向，反映能量守恒。",
        "- 变化的磁场必然伴随感应电场。",
    ]),
    (["折射"], [
        "- 折射本质是波速改变导致传播方向改变。",
        "- 折射率越大，光速越慢，折射角越小。",
        "- 全反射发生在从密到疏介质且入射角大时。",
    ]),
    (["偏振"], [
        "- 偏振说明光的横波特性，电场方向决定偏振态。",
        "- 偏振片通过投影选择特定振动方向。",
        "- 马吕斯定律来自投影平方关系。",
    ]),
    (["相对论", "时间膨胀", "洛伦兹"], [
        "- 时间膨胀与长度收缩是同一洛伦兹变换的不同表现。",
        "- 事件同时性依赖参考系，是相对论的核心改变。",
        "- 不变量是跨参考系的“安全锚点”。",
    ]),
    (["量子", "不确定", "波粒"], [
        "- 波粒二象性意味着“实验条件决定表现”。",
        "- 不确定性反映状态本身的限制，而非仪器误差。",
        "- 量子态叠加是微观系统的常态。",
    ]),
    (["熵"], [
        "- 熵衡量微观态数，宏观上体现为“无序程度”。",
        "- 可逆过程熵不增，自发过程熵增加。",
        "- 熵增给出时间方向的物理含义。",
    ]),
    (["温度", "热量", "热"], [
        "- 温度与内能相关，但并非内能本身。",
        "- 热量是过程量，只在传热过程中有意义。",
        "- 热平衡意味着温度相等而非能量相等。",
    ]),
    (["压强", "气体"], [
        "- 压强是分子碰撞壁面的平均结果。",
        "- 平均动能与温度直接关联，是气体状态方程的基础。",
        "- 理想气体假设忽略分子体积与相互作用。",
    ]),
    (["半导体"], [
        "- 掺杂改变载流子类型和浓度，控制导电性。",
        "- PN 结形成内建电场，是二极管单向导电的原因。",
        "- 少子扩散与复合决定器件的动态特性。",
    ]),
    (["激光"], [
        "- 受激辐射要求粒子数反转，这是激光的门槛。",
        "- 谐振腔选模并放大特定频率。",
        "- 激光的高相干性来自相位同步放大。",
    ]),
    (["光纤"], [
        "- 传输损耗主要来自吸收与散射。",
        "- 色散决定脉冲展宽，是高速通信的关键限制。",
        "- 单模光纤通过限制传播模式提高带宽。",
    ]),
]

EXTEND_MORE = {
    "foundations": [
        "- 可用无量纲数对实验与仿真结果进行跨尺度对比。",
        "- 工程中常用“量纲检验”排查公式错误。",
        "- 估算题先做数量级，能快速定位答案范围。",
    ],
    "mechanics": [
        "- 工程中常把复杂体系简化为质点/刚体，再逐步修正。",
        "- 交通与航天轨道设计广泛使用能量与动量方法。",
        "- 振动与冲击问题通常用等效模型先做稳定性评估。",
    ],
    "thermo": [
        "- 热机效率上限由卡诺循环给出，是工程设计的“天花板”。",
        "- 制冷与热泵问题常用能量与熵双重约束分析。",
        "- 传热问题需结合对流、传导与辐射综合判断。",
    ],
    "waves": [
        "- 声学设计利用驻波与共振控制噪声与音质。",
        "- 波动模型可迁移到电磁、地震与量子系统。",
        "- 频谱分析是理解复杂波形的核心工具。",
    ],
    "em": [
        "- 电磁场理论支撑通信、成像、传感与能量传输。",
        "- 屏蔽与接地是工程中控制电磁干扰的关键。",
        "- 等效电路把复杂场问题转化为可计算模型。",
    ],
    "emwaves": [
        "- 共振系统用于滤波、频率选择与稳定振荡。",
        "- 电磁波传播与介质参数决定天线与波导设计。",
        "- 阻尼与损耗直接影响系统品质因数与带宽。",
    ],
    "optics": [
        "- 现代光学测量大量依赖干涉与衍射的高灵敏度。",
        "- 成像系统优化本质是在分辨率、亮度与噪声间权衡。",
        "- 激光与非线性光学拓展了传统光学的应用边界。",
    ],
    "relativity": [
        "- 高能粒子实验与天体物理都必须使用相对论修正。",
        "- GPS 时间校正是相对论最直接的工程应用。",
        "- 引力透镜与引力波是广义相对论的观测证据。",
    ],
    "quantum": [
        "- 量子概念是半导体、激光、超导与量子信息的基础。",
        "- 隧穿效应在器件缩小后变得越来越重要。",
        "- 量子测量与退相干是工程实现的关键挑战。",
    ],
    "tech": [
        "- 新技术评估通常从“物理可行性 + 工艺可行性”双维度入手。",
        "- 先进表征手段常组合使用，形成互补证据链。",
        "- 工程应用需关注成本、可靠性与规模化能力。",
    ],
    "constants": [
        "- 自然单位制在高能物理中可显著简化公式。",
        "- 在工程实践中，单位一致性是最常见错误来源之一。",
        "- 建议建立个人常数速查表并反复使用。",
    ],
}


analogy_marker = "**类比形象解释**"
meaning_marker = "**物理意义**"
deep_marker = "**讲透说明**"
extend_marker = "**进一步扩展**"

changed_files = 0
inserted_deep = 0
inserted_extend = 0

for path in sorted(base.glob("*.md")):
    theme = FILE_THEME.get(path.name, "mechanics")
    lines = path.read_text(encoding="utf-8").splitlines()

    # locate double-detail section
    try:
        double_start = next(i for i, l in enumerate(lines) if l.strip() == "## 本章加倍细化")
    except StopIteration:
        continue

    out = []
    in_double = False
    current_title = None
    changed = False

    in_extend_section = False
    extend_has_marker = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if i == double_start:
            in_double = True

        # detect section headings
        if in_double and line.startswith("### "):
            # leaving extend section
            if in_extend_section:
                if not extend_has_marker:
                    out.append(extend_marker)
                    out.extend(EXTEND_MORE.get(theme, EXTEND_MORE["mechanics"]))
                    inserted_extend += 1
                    changed = True
                in_extend_section = False
                extend_has_marker = False

            title = line.strip()[4:]
            title = title.replace("（加倍细化）", "").strip()
            current_title = title

            if "扩展与应用（加倍细化）" in line:
                in_extend_section = True

        out.append(line)

        # insert deep explanation after 物理意义
        if in_double and line.strip() == meaning_marker:
            # copy meaning bullets
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.startswith("- "):
                    out.append(next_line)
                    i += 1
                    continue
                break
            # check if already has deep marker
            if i < len(lines) and lines[i].strip() == deep_marker:
                out.append(lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("- "):
                    out.append(lines[i])
                    i += 1
            else:
                # pick deep bullets
                bullets = None
                for kws, deep in KEYWORD_DEEP:
                    if current_title and any(kw in current_title for kw in kws):
                        bullets = deep
                        break
                if bullets is None:
                    bullets = THEME_DEEP.get(theme, THEME_DEEP["mechanics"])
                out.append(deep_marker)
                out.extend(bullets)
                inserted_deep += 1
                changed = True
            continue

        if in_extend_section and line.strip() == extend_marker:
            extend_has_marker = True

        i += 1

    # close extend section at EOF
    if in_extend_section and not extend_has_marker:
        out.append(extend_marker)
        out.extend(EXTEND_MORE.get(theme, EXTEND_MORE["mechanics"]))
        inserted_extend += 1
        changed = True

    # if no extend section at all, append one at end of double detail
    if in_double and ("扩展与应用（加倍细化）" not in "\n".join(lines)):
        out.append("")
        out.append("### 扩展与应用（加倍细化）")
        out.append(extend_marker)
        out.extend(EXTEND_MORE.get(theme, EXTEND_MORE["mechanics"]))
        inserted_extend += 1
        changed = True

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        changed_files += 1

print("changed_files", changed_files, "deep_blocks", inserted_deep, "extend_blocks", inserted_extend)
