# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util
import re

root = Path(r"D:\spot\K6\siyuan_university_physics")
topics = root / "siyuan_topics_refined"


def load_details(path: Path, modname: str) -> dict:
    spec = importlib.util.spec_from_file_location(modname, str(path))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return dict(getattr(mod, "DOUBLE_DETAILS", {}))


DETAILS = {}
DETAILS.update(load_details(root / "_double_detail_b1.py", "b1"))
DETAILS.update(load_details(root / "_double_detail_b2.py", "b2"))
DETAILS.update(load_details(root / "_double_detail_b3.py", "b3"))
DETAILS.update(load_details(root / "_double_detail_b4.py", "b4"))
DETAILS.update(load_details(root / "_double_detail_b5.py", "b5"))


def rewrite_double(name: str, detail: str) -> None:
    path = topics / name
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")

    # Find earliest marker of any previous/corrupted double-detail section
    starts = []
    patterns = [
        r"^##\s*本章加倍细化\s*$",
        r"^##\s*\?+\s*$",
        r"<a\s+id=\"double[^\n]*",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.M)
        if m:
            starts.append(m.start())
    if starts:
        text = text[: min(starts)].rstrip() + "\n"

    text = text.rstrip() + "\n\n" + detail.strip() + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for name, detail in DETAILS.items():
        rewrite_double(name, detail)


if __name__ == "__main__":
    main()
    print("Double-detail repair done.")
