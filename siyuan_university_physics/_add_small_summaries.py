# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(r"D:\spot\K6\siyuan_university_physics")
base = root / "siyuan_topics_refined"

summary_marker = "**小结**"

changed_files = 0
added_blocks = 0

for path in sorted(base.glob("*.md")):
    lines = path.read_text(encoding="utf-8").splitlines()
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
            current_title = line.strip()[4:]
            current_title = current_title.replace("（加倍细化）", "").strip()

        out.append(line)

        if in_double and line.strip() == "**易错点**":
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.startswith("- "):
                    out.append(next_line)
                    i += 1
                    continue
                break
            if i < len(lines) and lines[i].strip() == summary_marker:
                out.append(lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("- "):
                    out.append(lines[i])
                    i += 1
            else:
                t = current_title or "本节"
                out.append(summary_marker)
                out.append(f"- {t}的核心是抓住主导物理量与适用条件。")
                out.append("- 先辨类型与方向，再代公式，最后检查量纲与数量级。")
                added_blocks += 1
                changed = True
            continue

        i += 1

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        changed_files += 1

print("changed_files", changed_files, "added_blocks", added_blocks)
