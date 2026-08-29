import argparse
import os
import re
import unicodedata

AD_KEYWORDS = [
    "闲鱼", "小红书", "知枫", "Heycys",
]
AD_HINTS = [
    "公众号", "扫码", "微信", "QQ群", "加群", "群号", "二维码",
]

PUA_MAP = {
    "\ue09b": "=",   # looks like fullwidth equals in source docs
    "\ue083": "【",
    "\ue084": "】",
}

PAGE_FOOTER_RE = re.compile(r"\*\*\d+\*\*\s*/\s*\*\*\d+\*\*")


def is_ad_line(line):
    l = line.strip()
    if not l:
        return False
    if any(k in l for k in AD_KEYWORDS):
        return True
    if any(k in l for k in AD_HINTS) and len(l) <= 40:
        return True
    return False


def is_footer_line(line):
    l = line.strip()
    if not l:
        return False
    # Typical page footer from merged/scanned docs, e.g. "**1** / **1226**"
    return PAGE_FOOTER_RE.search(l) is not None


def normalize_blank_lines(lines):
    out = []
    blank = False
    for line in lines:
        if line.strip() == "":
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(line.rstrip())
            blank = False
    # trim leading/trailing blanks
    while out and out[0].strip() == "":
        out.pop(0)
    while out and out[-1].strip() == "":
        out.pop()
    return out


def clean_code_blocks(lines):
    out = []
    in_code = False
    buffer = []
    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                # close: flush buffer with trimmed trailing spaces
                while buffer and buffer[0].strip() == "":
                    buffer.pop(0)
                while buffer and buffer[-1].strip() == "":
                    buffer.pop()
                out.extend(buffer)
                buffer = []
                out.append("```")
                in_code = False
            else:
                out.append(line.strip())
                in_code = True
            continue
        if in_code:
            buffer.append(line.rstrip().replace("\t", "    "))
        else:
            out.append(line)
    # if unterminated code block, flush buffer
    if buffer:
        out.extend(buffer)
    return out


def parse_table_row(line):
    row = line.strip().strip("|")
    cells = [c.strip() for c in row.split("|")]
    return cells


def is_separator_row(cells):
    if not cells:
        return False
    for c in cells:
        if not re.fullmatch(r"-{3,}", c):
            return False
    return True


def rebuild_table(rows):
    # rows: list[list[str]] extracted from markdown table lines
    if not rows:
        return []

    max_cols = max(len(r) for r in rows)
    rows = [r + [""] * (max_cols - len(r)) for r in rows]

    first_is_sep = is_separator_row(rows[0])
    first_is_blank = all(not c.strip() for c in rows[0])

    # Drop all separator rows; we'll rebuild exactly one separator line.
    rows = [r for r in rows if not is_separator_row(r)]
    # Drop fully empty rows
    rows = [r for r in rows if any(c.strip() for c in r)]
    if not rows:
        return []

    # Remove empty columns across all remaining rows
    keep_cols = [col for col in range(max_cols) if any(r[col].strip() for r in rows)]
    if not keep_cols:
        return []
    rows = [[r[c] for c in keep_cols] for r in rows]
    if not rows or not rows[0]:
        return []

    if first_is_sep or first_is_blank:
        header = [""] * len(rows[0])
        data_rows = rows
    else:
        header = rows[0]
        data_rows = rows[1:]

    sep = ["---"] * len(header)
    out_lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for r in data_rows:
        out_lines.append("| " + " | ".join(r) + " |")
    return out_lines


def clean_tables(lines):
    out = []
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].lstrip().startswith("|"):
            block = []
            while i < n and (lines[i].lstrip().startswith("|") or lines[i].strip() == ""):
                if lines[i].lstrip().startswith("|"):
                    block.append(lines[i])
                i += 1
            # parse rows
            rows = [parse_table_row(l) for l in block]
            new_block = rebuild_table(rows)
            if new_block:
                out.extend(new_block)
            # ensure blank line after table
            if i < n and lines[i].strip() != "":
                out.append("")
        else:
            out.append(lines[i])
            i += 1
    return out


def iter_lines_with_code_state(lines):
    in_code = False
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code = not in_code
        yield i, line, in_code


def fix_hash_headings(lines):
    # Normalize headings like "##Title" -> "## Title" (avoid single-# comment lines).
    out = lines[:]
    pat = re.compile(r"^(#{2,6})([A-Za-z\u4e00-\u9fff])")
    for i, line, in_code in iter_lines_with_code_state(lines):
        if in_code:
            continue
        m = pat.match(line)
        if not m:
            continue
        hashes = m.group(1)
        out[i] = hashes + " " + line[len(hashes):]
    return out


def promote_bold_headings(lines):
    # Convert standalone bold-only lines into headings, e.g. "**VCS** **篇**" -> "## VCS 篇".
    out = lines[:]
    bold_only_re = re.compile(r"^(?:\s*\*\*[^*]+\*\*\s*)+$")
    seg_re = re.compile(r"\*\*([^*]+)\*\*")
    for i, line, in_code in iter_lines_with_code_state(lines):
        if in_code:
            continue
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if not bold_only_re.fullmatch(s):
            continue
        segs = [t.strip() for t in seg_re.findall(s)]
        text = " ".join(t for t in segs if t)
        if not text or len(text) > 60:
            continue
        if text.endswith(("篇", "章", "部分", "Part")):
            out[i] = "## " + text
        else:
            out[i] = "### " + text
    return out


def fix_numbered_lists(lines):
    # Normalize "1.xxx" -> "1. xxx" when it looks like a list item (avoid decimals like 1.8V).
    out = lines[:]
    pat = re.compile(r"^(\s*)(\d+)\.([^\s\d])")
    for i, line, in_code in iter_lines_with_code_state(lines):
        if in_code:
            continue
        m = pat.match(line)
        if not m:
            continue
        prefix = m.group(1)
        num = m.group(2)
        out[i] = f"{prefix}{num}. {line[len(prefix) + len(num) + 1:]}"
    return out


def normalize_heading_levels(lines):
    heading_re = re.compile(r"^(#{1,6})\s+(.*)$")
    headings = []
    for i, line, in_code in iter_lines_with_code_state(lines):
        if in_code:
            continue
        m = heading_re.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    if not headings:
        return lines
    min_level = min(level for _, level, _ in headings)
    prev_level = None
    new_lines = lines[:]
    normalized = []
    for i, level, text in headings:
        new_level = level - min_level + 1
        if prev_level is not None and new_level > prev_level + 1:
            new_level = prev_level + 1
        new_level = max(1, min(6, new_level))
        new_lines[i] = "#" * new_level + " " + text
        prev_level = new_level
        normalized.append((i, new_level, text))

    # If there are multiple H1s, treat the first as title and demote the rest
    has_extra_h1 = any(level == 1 for _, level, _ in normalized[1:])
    if normalized and normalized[0][1] == 1 and has_extra_h1:
        for i, level, text in normalized[1:]:
            demoted = min(6, level + 1)
            new_lines[i] = "#" * demoted + " " + text
    return new_lines


def strip_images_from_heading_text(text):
    # Remove inline images from heading text, keep the textual label.
    t = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def demote_noisy_headings(lines):
    # Demote or flatten headings that are actually command-lines / long sentences,
    # so the H1/H2 index stays useful.
    out = lines[:]
    heading_re = re.compile(r"^(#{1,6})\s+(.*)$")
    noisy_tokens = [
        "+=",
        "$(",
        "ifeq",
        "endif",
        "set_",
        "process run",
        "create_",
        "DUT_",
        "CMP_OPTIONS",
        "Section",
    ]
    for i, line, in_code in iter_lines_with_code_state(lines):
        if in_code:
            continue
        m = heading_re.match(line)
        if not m:
            continue
        level = len(m.group(1))
        raw = m.group(2).strip()
        cleaned = strip_images_from_heading_text(raw)

        if not cleaned:
            # Keep image-only headings as plain content.
            out[i] = raw
            continue

        if level == 1:
            out[i] = "# " + cleaned
            continue

        if level == 2:
            if cleaned.startswith(("表示", "表明", "简单理解", "可以这样写")) and len(cleaned) > 20:
                out[i] = cleaned
                continue
            if re.match(r"^在\s*PD\d", cleaned) or ("PIN" in cleaned and "VDD" in cleaned):
                out[i] = "### " + cleaned
                continue
            if len(cleaned) > 60 or any(tok in cleaned for tok in noisy_tokens):
                out[i] = "### " + cleaned
                continue
            if sum(cleaned.count(ch) for ch in "=;{}$") >= 2:
                out[i] = "### " + cleaned
                continue

        out[i] = "#" * level + " " + cleaned
    return out


def remove_existing_toc(lines):
    toc_re = re.compile(r"^#{1,6}\s*目录\s*$")
    i = 0
    while i < len(lines):
        if toc_re.match(lines[i].strip()):
            start = i
            i += 1
            while i < len(lines):
                s = lines[i].strip()
                if s == "":
                    i += 1
                    continue
                if re.match(r"^[-*+]\s+.+", s) or re.match(r"^\d+\.\s+.+", s):
                    i += 1
                    continue
                break
            return lines[:start] + lines[i:]
        i += 1
    return lines


def slugify(text):
    text = unicodedata.normalize("NFKC", text)
    s = text.strip().lower()
    s = re.sub(r"[^0-9a-z\u4e00-\u9fff\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        s = "section"
    return s


def should_skip_toc_item(text):
    t = text.strip()
    if not t:
        return True
    if len(t) > 80:
        return True
    if re.fullmatch(r"[-_=\.\s]+", t):
        return True
    if t.startswith(("表示", "表明", "简单理解", "可以这样写")):
        return True
    if any(tok in t for tok in ["+=", "$(", "ifeq", "endif", "set_", "process run", "create_", "DUT_", "CMP_OPTIONS", "Section"]):
        return True
    return False


def build_and_insert_toc(lines):
    heading_re = re.compile(r"^(#{1,6})\s+(.*)$")
    headings = []
    for _, line, in_code in iter_lines_with_code_state(lines):
        if in_code:
            continue
        m = heading_re.match(line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2).strip()
        if should_skip_toc_item(text):
            continue
        headings.append((level, text))
    if not headings:
        return lines
    toc = ["## 目录", ""]
    seen = set()
    for level, text in headings:
        if level > 2:
            continue
        if text in seen:
            continue
        seen.add(text)
        indent = "  " * (level - 1)
        toc.append(f"{indent}- [{text}](#{slugify(text)})")
    if len(toc) == 2:
        return lines
    toc.append("")
    insert_at = 0
    for idx, line, in_code in iter_lines_with_code_state(lines):
        if in_code:
            continue
        m0 = heading_re.match(line)
        if m0 and len(m0.group(1)) == 1:
            insert_at = idx + 1
            if insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            break
    return lines[:insert_at] + toc + lines[insert_at:]


def ensure_title(lines, title):
    # If there's already a top-level title near the top (allow leading HTML anchors), keep it.
    for line in lines[:30]:
        if line.startswith("# "):
            return lines
        if line.strip() == "":
            continue
    if not title:
        return lines
    return [f"# {title}", ""] + lines


def drop_duplicate_title_heading(lines, title):
    if not title:
        return lines
    title_line = f"# {title}"
    has_title = any(line.strip() == title_line for line in lines[:50])
    if not has_title:
        return lines
    pat = re.compile(rf"^#{{2,6}}\s+{re.escape(title)}\s*$")
    out = lines[:]
    for i, line in enumerate(out[:200]):
        if pat.match(line.strip()):
            out[i] = ""
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Markdown file path")
    args = ap.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if PUA_MAP:
        trans = str.maketrans(PUA_MAP)
        lines = [line.translate(trans) for line in lines]
        # drop any remaining PUA chars
        lines = ["".join(ch for ch in line if not (0xE000 <= ord(ch) <= 0xF8FF)) for line in lines]

    lines = [line for line in lines if not is_footer_line(line)]

    title = os.path.splitext(os.path.basename(args.path))[0]
    lines = ensure_title(lines, title)
    lines = drop_duplicate_title_heading(lines, title)
    lines = fix_hash_headings(lines)
    lines = promote_bold_headings(lines)
    lines = drop_duplicate_title_heading(lines, title)

    # normalize headings and rebuild TOC
    lines = normalize_heading_levels(lines)
    lines = demote_noisy_headings(lines)
    lines = drop_duplicate_title_heading(lines, title)
    lines = remove_existing_toc(lines)
    lines = build_and_insert_toc(lines)

    # remove ad lines
    lines = [line for line in lines if not is_ad_line(line)]

    lines = fix_numbered_lists(lines)
    lines = clean_code_blocks(lines)
    lines = clean_tables(lines)
    lines = normalize_blank_lines(lines)

    with open(args.path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
