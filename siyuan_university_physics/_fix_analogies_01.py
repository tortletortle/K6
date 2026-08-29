# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(r"D:\spot\K6\siyuan_university_physics")
base = root / "siyuan_topics_refined"

THEME_FALLBACK = {
    "mechanics": [
        "- 力与运动的关系像推购物车，推得更大更久，速度变化越明显。",
        "- 惯性像“守住原状的习惯”，不被打扰就继续当前运动状态。",
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
    (["圆周"], [
        "- 圆周运动像用绳子拴着小球转圈，绳子不断拉着球“拐弯”。",
        "- 向心加速度像“拐弯时向内的拉力”。",
    ]),
    (["相对"], [
        "- 相对运动像在行驶的公交车里走路，地面看到的速度是两者叠加。",
        "- 有风飞行像人走在自动扶梯上，地面速度=自身速度+扶梯速度。",
    ]),
]


def pick_analogies(title: str):
    for kws, bullets in KEYWORD_ANALOGIES:
        if any(kw in title for kw in kws):
            return bullets
    return THEME_FALLBACK["mechanics"]

analogy_marker = "**类比形象解释**"
meaning_marker = "**物理意义**"

path = base / "01_kinematics.md"
lines = path.read_text(encoding="utf-8").splitlines()

try:
    double_start = next(i for i, l in enumerate(lines) if l.strip() == "## 本章加倍细化")
except StopIteration:
    raise SystemExit("double section not found")

out = []
in_double = False
current_title = None
changed = False


def is_bad_bullet(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("-") and set(stripped) <= set("- ?")


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
            existing = []
            while i < len(lines) and lines[i].startswith("- "):
                existing.append(lines[i])
                i += 1
            if any(is_bad_bullet(x) for x in existing):
                bullets = pick_analogies(current_title or "")
                out.extend(bullets)
                changed = True
            else:
                out.extend(existing)
        else:
            bullets = pick_analogies(current_title or "")
            out.append(analogy_marker)
            out.extend(bullets)
            changed = True
        continue

    i += 1

if changed:
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("fixed 01_kinematics.md")
else:
    print("no changes")
