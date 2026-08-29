# -*- coding: utf-8 -*-
from pathlib import Path

base = Path(r"D:\spot\K6\siyuan_university_physics\siyuan_topics_refined")

def fix_text(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n and text[i + 1] == "n":
            next_char = text[i + 2] if i + 2 < n else ""
            if next_char and next_char.isalpha():
                out.append("\\")
                out.append("n")
            else:
                out.append("\n")
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)

changed = 0
for path in sorted(base.glob("*.md")):
    text = path.read_text(encoding="utf-8")
    fixed = fix_text(text)
    if fixed != text:
        path.write_text(fixed, encoding="utf-8")
        changed += 1

print("fixed files", changed)
