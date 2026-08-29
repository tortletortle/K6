# -*- coding: utf-8 -*-
from pathlib import Path
import re

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

THEME_FALLBACK = {
    "foundations": [
        "- 单位像“语言的语法”，换单位就像换语言表达同一件事。",
        "- 量纲像食谱里的配比维度，先看维度就能判断关系是否合理。",
    ],
    "mechanics": [
        "- 力与运动的关系像推购物车，推得更大更久，速度变化越明显。",
        "- 惯性像“守住原状的习惯”，不被打扰就继续当前运动状态。",
    ],
    "thermo": [
        "- 温度像“平均热劲”，热量像“传递的热劲”。",
        "- 熵增像房间自然变乱，自发变整齐需要外界做功。",
    ],
    "waves": [
        "- 波像水面上的起伏，能量和信息传播而物质不整体搬运。",
        "- 叠加像两个人同时拍水面，波峰波谷会增强或抵消。",
    ],
    "em": [
        "- 电场像地形坡度，电势像高度差，电荷像小球会“顺坡”移动。",
        "- 电流像水流，电阻像管道变窄，越窄越难流。",
    ],
    "emwaves": [
        "- 电磁波像相互牵引的“电—磁双人舞”，一涨一落共同向前。",
        "- 谐振与共振像荡秋千，频率合拍时振幅迅速增大。",
    ],
    "optics": [
        "- 光学干涉像两路水波叠加，亮暗条纹就是增强与相消。",
        "- 衍射像水波绕过障碍，孔越小，扩散越明显。",
    ],
    "relativity": [
        "- 高速运动像“慢动作视频”，时间尺度被拉长。",
        "- 时空像舞台布，运动越快“刻度”越倾斜。",
    ],
    "quantum": [
        "- 量子能级像楼梯台阶，只能一级一级上。",
        "- 电子像“云”，位置是概率分布而非确定轨迹。",
    ],
    "tech": [
        "- 半导体像阀门，能精细控制电流通断。",
        "- 光纤像水管靠全反射导光，几乎不“漏水”。",
    ],
    "constants": [
        "- 物理常数像固定刻度尺，给所有公式定标。",
        "- 单位换算像货币汇率，数值变了但物理量不变。",
    ],
}

KEYWORD_ANALOGIES = [
    (["参考系", "坐标"], [
        "- 参考系像选摄影机机位，换机位会改变看到的运动描述。",
        "- 坐标系像地图网格，只是表达方式，不改变事实。",
    ]),
    (["位移", "速度", "加速度"], [
        "- 位移像地图上的箭头，速度像读秒的速度表。",
        "- 加速度像速度表指针变化的快慢。",
    ]),
    (["牛顿", "力"], [
        "- 力像推购物车的手，越大越能改变运动状态。",
        "- 合力像多个人推车的“合力结果”。",
    ]),
    (["摩擦"], [
        "- 摩擦像鞋底与地面“抓地”的阻力，阻碍相对滑动。",
        "- 表面越粗糙，抓地越强。",
    ]),
    (["功", "能"], [
        "- 能量像账户余额，功像一次转账改变余额。",
        "- 势能像“高度优势”，动能像“速度优势”。",
    ]),
    (["动量", "冲量"], [
        "- 动量像“运动的惯性重量”，大卡车难停下。",
        "- 冲量像踢球时脚与球接触的“用力时间”。",
    ]),
    (["角动量"], [
        "- 角动量像旋转陀螺的“稳定性”，越大越不易改变方向。",
        "- 花样滑冰收紧手臂会转得更快。",
    ]),
    (["转动惯量"], [
        "- 质量离转轴越远越难转动，像用长杆转门。",
        "- 分布越外，转动惯量越大。",
    ]),
    (["引力", "万有引力"], [
        "- 引力像拉紧的橡皮绳，距离越远拉力越弱。",
        "- 轨道像“抛出去又被拉回”的平衡。",
    ]),
    (["简谐", "振动", "共振"], [
        "- 弹簧—小球像钟摆，拉开后会来回往复。",
        "- 共振像荡秋千合拍，推的节奏对了振幅变大。",
    ]),
    (["波", "波动"], [
        "- 波像水面起伏，能量传播但水并不整体前进。",
        "- 波峰波谷像“起伏的队列”。",
    ]),
    (["干涉"], [
        "- 两路水波叠加会更高或互相抵消，形成明暗条纹。",
        "- 条纹像“拍手重叠”的强弱节奏。",
    ]),
    (["衍射"], [
        "- 水波遇到障碍会绕过去，缝越窄绕得越明显。",
        "- 光也会“拐弯”，这就是衍射。",
    ]),
    (["多普勒"], [
        "- 救护车靠近时音调变高，远离时变低。",
        "- 频率变化体现相对运动。",
    ]),
    (["电场"], [
        "- 电场像坡度，电荷像小球会向“低电势”滚动。",
        "- 电场线像坡度方向指示牌。",
    ]),
    (["电势"], [
        "- 电势像海拔高度，电势差像高度差。",
        "- 电势能像“站在高处”的势能。",
    ]),
    (["电容"], [
        "- 电容像水桶容量，电压像水位，电荷像水量。",
        "- 容量越大，同样电荷电压越低。",
    ]),
    (["电流"], [
        "- 电流像水流，电荷像水分子在管中移动。",
        "- 电流大小对应单位时间流过的“水量”。",
    ]),
    (["电阻"], [
        "- 电阻像水管变窄，越窄越难流。",
        "- 线路越长、截面积越小阻力越大。",
    ]),
    (["磁场"], [
        "- 磁场像看不见的“旋涡水流”，对运动电荷产生偏转。",
        "- 磁力线像漩涡的流线。",
    ]),
    (["电磁感应", "磁通"], [
        "- 改变磁通量像切割磁力线，会“感应出电流”。",
        "- 发电机就像不停切割磁力线的装置。",
    ]),
    (["折射"], [
        "- 像小车一侧驶入沙地，速度变化导致轨迹偏折。",
        "- 光在不同介质中速度不同所以会“拐弯”。",
    ]),
    (["偏振"], [
        "- 偏振片像栅栏，只允许某一方向的振动通过。",
        "- 两片偏振片夹角改变透光强度。",
    ]),
    (["相对论", "时间膨胀", "洛伦兹"], [
        "- 高速运动像慢动作视频，钟表“走慢”。",
        "- 不同参考系像不同拍摄角度，时间和长度读数会变。",
    ]),
    (["量子", "不确定", "波粒"], [
        "- 量子能级像楼梯台阶，不能站在半层。",
        "- 粒子既像子弹又像水波，呈现波粒二象性。",
    ]),
    (["熵"], [
        "- 熵增像房间自然变乱，变整齐需要额外努力。",
        "- 自发过程倾向于更多微观“可能性”。",
    ]),
    (["温度", "热量", "热"], [
        "- 温度像平均热劲，热量像转移的热劲。",
        "- 热从高温流向低温像水从高处流向低处。",
    ]),
    (["压强", "气体"], [
        "- 压强像小球不断撞墙产生的“平均推力”。",
        "- 气体像一群乱跑的人，撞墙越频繁压强越大。",
    ]),
    (["半导体"], [
        "- 半导体像可控阀门，能调节电流通断与大小。",
        "- 掺杂就像往水管里加阀门零件改变通畅程度。",
    ]),
    (["激光"], [
        "- 激光像整齐列队行进的士兵，方向一致、步伐整齐。",
        "- 受激辐射像“你点我也点”的连锁反应。",
    ]),
    (["光纤"], [
        "- 光纤像水管，光在里面不断全反射前进。",
        "- 纤芯与包层折射率差像管壁与内壁的界面。",
    ]),
]


def pick_analogies(title: str, theme: str):
    for kws, bullets in KEYWORD_ANALOGIES:
        if any(kw in title for kw in kws):
            return bullets
    return THEME_FALLBACK.get(theme, THEME_FALLBACK["mechanics"])


analogy_marker = "**类比形象解释**"
meaning_marker = "**物理意义**"

changed_files = 0
inserted_total = 0

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

    i = 0
    while i < len(lines):
        line = lines[i]
        if i == double_start:
            in_double = True

        if line.startswith("### ") and in_double:
            title = line.strip()[4:]
            title = title.replace("（加倍细化）", "").strip()
            current_title = title

        out.append(line)

        if in_double and line.strip() == meaning_marker:
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.startswith("- "):
                    out.append(next_line)
                    i += 1
                    continue
                break
            if i < len(lines) and lines[i].strip() == analogy_marker:
                out.append(lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("- "):
                    out.append(lines[i])
                    i += 1
            else:
                bullets = pick_analogies(current_title or "", theme)
                out.append(analogy_marker)
                out.extend(bullets)
                inserted_total += 1
                changed = True
            continue

        i += 1

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        changed_files += 1

print("changed_files", changed_files, "inserted_blocks", inserted_total)
