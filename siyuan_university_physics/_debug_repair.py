# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(r"D:\spot\K6\siyuan_university_physics\siyuan_topics_refined\00_foundations.md")
text = path.read_text(encoding="utf-8")

patterns = [
    r"^##\s*本章加倍细化\s*$",
    r"^##\s*\?+\s*$",
    r"<a\s+id=\"double[^\n]*",
]

for pat in patterns:
    m = re.search(pat, text, flags=re.M)
    print(pat, m.start() if m else None)

# show earliest marker context
starts = [m.start() for pat in patterns for m in [re.search(pat, text, flags=re.M)] if m]
print("min", min(starts) if starts else None)

