import argparse
import hashlib
import os
import re
import unicodedata
from collections import Counter

from docx import Document
from docx.oxml.ns import qn
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run

def iter_block_items(parent):
    parent_elm = parent.element.body
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def build_numbering_map(doc):
    try:
        numbering = doc.part.numbering_part.element
    except Exception:
        return {}
    num_id_to_abs = {}
    abs_lvl_fmt = {}
    for num in numbering.findall(qn('w:num')):
        num_id = num.get(qn('w:numId'))
        abs_id_elm = num.find(qn('w:abstractNumId'))
        if num_id and abs_id_elm is not None:
            num_id_to_abs[num_id] = abs_id_elm.get(qn('w:val'))
    for abs_num in numbering.findall(qn('w:abstractNum')):
        abs_id = abs_num.get(qn('w:abstractNumId'))
        for lvl in abs_num.findall(qn('w:lvl')):
            ilvl = lvl.get(qn('w:ilvl'))
            num_fmt = lvl.find(qn('w:numFmt'))
            if abs_id and ilvl is not None and num_fmt is not None:
                abs_lvl_fmt[(abs_id, ilvl)] = num_fmt.get(qn('w:val'))
    final = {}
    for num_id, abs_id in num_id_to_abs.items():
        for (abs_id2, ilvl), fmt in abs_lvl_fmt.items():
            if abs_id2 == abs_id:
                final[(num_id, ilvl)] = fmt
    return final


def get_heading_level(style_name):
    if not style_name:
        return None
    m = re.search(r"Heading\s*(\d+)", style_name, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"标题\s*(\d+)", style_name)
    if m:
        return int(m.group(1))
    if style_name.lower() in ("title", "标题"):
        return 1
    return None


def is_code_style(style_name):
    if not style_name:
        return False
    name = style_name.lower()
    return ("code" in name) or ("代码" in style_name) or ("预格式" in style_name)


def is_toc_style(style_name):
    if not style_name:
        return False
    name = style_name.lower()
    return name.startswith("toc") or "toc " in name


def get_list_info(paragraph, numbering_map):
    ppr = paragraph._p.pPr
    if ppr is None or ppr.numPr is None:
        return None
    num_pr = ppr.numPr
    num_id = num_pr.numId.val if num_pr.numId is not None else None
    ilvl = num_pr.ilvl.val if num_pr.ilvl is not None else 0
    if num_id is None:
        return None
    num_id = str(num_id)
    ilvl = str(ilvl)
    fmt = numbering_map.get((num_id, ilvl))
    style_name = paragraph.style.name if paragraph.style is not None else ""
    if fmt == "bullet" or "bullet" in style_name.lower() or "项目符号" in style_name:
        list_type = "bullet"
    else:
        list_type = "number"
    return list_type, int(ilvl)


RADICAL_MAP = {
    "\u2ec4": "西",
    "\u2ec5": "见",
    "\u2ec6": "角",
    "\u2ec9": "贝",
    "\u2ecb": "车",
    "\u2ed3": "长",
    "\u2ed4": "门",
    "\u2ee2": "马",
    "\u2ee5": "鱼",
    "\u2ee9": "黄",
    "\u2eec": "齐",
}


def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    return text.translate(str.maketrans(RADICAL_MAP))


def escape_md(text):
    if not text:
        return ""
    text = normalize_text(text)
    # Normalize tabs and non-breaking spaces
    text = text.replace("\t", "    ").replace("\xa0", " ")
    # Escape markdown special chars
    text = text.replace("\\", "\\\\")
    text = text.replace("`", "\\`")
    text = text.replace("*", "\\*")
    text = text.replace("_", "\\_")
    text = text.replace("|", "\\|")
    text = text.replace("[", "\\[")
    text = text.replace("]", "\\]")
    return text


def iter_paragraph_items(paragraph):
    for child in paragraph._p:
        if child.tag == qn('w:r'):
            yield ("run", Run(child, paragraph))
        elif child.tag == qn('w:hyperlink'):
            yield ("hyperlink", child)
        elif child.tag == qn('w:smartTag'):
            for sub in child:
                if sub.tag == qn('w:r'):
                    yield ("run", Run(sub, paragraph))


def iter_run_image_parts(run):
    blips = run._element.xpath('.//a:blip')
    for blip in blips:
        r_id = blip.get(qn('r:embed'))
        if not r_id:
            continue
        part = run.part.related_parts.get(r_id)
        if part is not None:
            yield part


def save_image(part, image_dir, image_map):
    blob = part.blob
    sha = hashlib.sha1(blob).hexdigest()
    if sha in image_map:
        return image_map[sha]
    content_type = getattr(part, 'content_type', 'image/png')
    ext = content_type.split('/')[-1].lower()
    if ext == 'jpeg':
        ext = 'jpg'
    if ext not in ('png', 'jpg', 'gif', 'bmp', 'tiff', 'webp'):
        ext = 'png'
    filename = f"img_{len(image_map)+1:04d}.{ext}"
    out_path = os.path.join(image_dir, filename)
    with open(out_path, 'wb') as f:
        f.write(blob)
    image_map[sha] = filename
    return filename


def render_run(run, image_dir, image_map, allow_format=True):
    segments = []
    text = run.text
    if text:
        t = escape_md(text) if allow_format else normalize_text(text)
        if allow_format:
            if run.bold and run.italic:
                t = f"***{t}***"
            elif run.bold:
                t = f"**{t}**"
            elif run.italic:
                t = f"*{t}*"
        segments.append(t)
    for part in iter_run_image_parts(run):
        filename = save_image(part, image_dir, image_map)
        segments.append(f"![]({os.path.basename(image_dir)}/{filename})")
    return segments


def render_hyperlink(hyperlink, paragraph, image_dir, image_map):
    r_id = hyperlink.get(qn('r:id'))
    text_parts = []
    for r in hyperlink.findall(qn('w:r')):
        text_parts.extend(render_run(Run(r, paragraph), image_dir, image_map, allow_format=True))
    text = "".join(text_parts).strip()
    url = None
    if r_id and r_id in paragraph.part.rels:
        url = paragraph.part.rels[r_id].target_ref
    if url:
        if text:
            return f"[{text}]({url})"
        return f"<{url}>"
    return text


def render_paragraph_plain(paragraph):
    parts = []
    for kind, obj in iter_paragraph_items(paragraph):
        if kind == "run":
            if obj.text:
                parts.append(normalize_text(obj.text))
        else:
            for r in obj.findall(qn('w:r')):
                run = Run(r, paragraph)
                if run.text:
                    parts.append(normalize_text(run.text))
    return "".join(parts).strip()


def render_paragraph(paragraph, image_dir, image_map):
    parts = []
    for kind, obj in iter_paragraph_items(paragraph):
        if kind == "run":
            parts.extend(render_run(obj, image_dir, image_map, allow_format=True))
        else:
            parts.append(render_hyperlink(obj, paragraph, image_dir, image_map))
    text = "".join(parts)
    return text.strip()


def render_cell(cell, image_dir, image_map):
    texts = []
    for p in cell.paragraphs:
        t = render_paragraph(p, image_dir, image_map)
        if t:
            texts.append(t)
    return "<br>".join(texts)


def table_to_md(table, image_dir, image_map):
    rows = []
    for row in table.rows:
        cells = [render_cell(cell, image_dir, image_map) for cell in row.cells]
        rows.append(cells)
    if not rows:
        return []
    max_cols = max(len(r) for r in rows)
    for r in rows:
        if len(r) < max_cols:
            r.extend([""] * (max_cols - len(r)))
    # Use first row as header
    header = rows[0]
    sep = ["---"] * max_cols
    md_lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for r in rows[1:]:
        md_lines.append("| " + " | ".join(r) + " |")
    return md_lines


def slugify(text, used):
    s = normalize_text(text).strip().lower()
    s = re.sub(r"[^0-9a-z\u4e00-\u9fff\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        s = "section"
    base = s
    i = 2
    while s in used:
        s = f"{base}-{i}"
        i += 1
    used.add(s)
    return s


def looks_like_toc_entry(paragraph, numbering_map):
    text = render_paragraph_plain(paragraph)
    if not text:
        return False
    text = text.replace("\t", "    ")
    # Page-number style: dot leaders or multiple spaces before trailing digits
    if re.search(r"(?:\.{2,}|\s{2,})\d+\s*$", text):
        return True
    # Fallback: numbered list item ending with digits
    if get_list_info(paragraph, numbering_map) and re.search(r"\d+\s*$", text):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--images", required=True)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(args.images, exist_ok=True)

    doc = Document(args.input)
    numbering_map = build_numbering_map(doc)

    lines = []
    image_map = {}
    used_slugs = set()
    toc_items = []

    in_code = False

    def close_code_block():
        nonlocal in_code
        if in_code:
            lines.append("```")
            lines.append("")
            in_code = False

    blocks = list(iter_block_items(doc))
    skip_manual_toc = False
    seen_heading = False

    for idx, block in enumerate(blocks):
        if isinstance(block, Paragraph):
            style_name = block.style.name if block.style is not None else ""
            # Skip built-in TOC entries
            if is_toc_style(style_name):
                continue
            # Skip a standalone "目录" heading if it precedes TOC entries
            if render_paragraph_plain(block) == "目录":
                if idx + 1 < len(blocks):
                    nxt = blocks[idx + 1]
                    if isinstance(nxt, Paragraph):
                        nxt_style = nxt.style.name if nxt.style is not None else ""
                        if is_toc_style(nxt_style):
                            continue
            heading_level = get_heading_level(style_name)
            is_code = is_code_style(style_name)
            list_info = get_list_info(block, numbering_map)
            heading_text = render_paragraph_plain(block)
            if heading_level is not None and heading_text:
                seen_heading = True

            # Heuristic: skip manual TOC sections (目录 + list of page-number entries)
            if skip_manual_toc:
                if heading_level is not None:
                    skip_manual_toc = False
                elif looks_like_toc_entry(block, numbering_map) or not heading_text:
                    continue
                else:
                    skip_manual_toc = False

            if heading_text == "目录" and heading_level is None:
                toc_like = 0
                for j in range(idx + 1, min(idx + 6, len(blocks))):
                    b = blocks[j]
                    if isinstance(b, Paragraph):
                        if looks_like_toc_entry(b, numbering_map):
                            toc_like += 1
                        elif render_paragraph_plain(b) == "":
                            continue
                        else:
                            break
                if toc_like >= 2:
                    skip_manual_toc = True
                    continue

            # Before the first real heading, drop TOC-like entries with page numbers
            if not seen_heading and looks_like_toc_entry(block, numbering_map):
                continue

            # Drop isolated TOC-like lines that precede a heading (common after cover pages)
            if looks_like_toc_entry(block, numbering_map):
                skip_line = False
                for j in range(idx + 1, min(idx + 5, len(blocks))):
                    b = blocks[j]
                    if isinstance(b, Paragraph):
                        b_text = render_paragraph_plain(b)
                        if not b_text:
                            continue
                        b_style = b.style.name if b.style is not None else ""
                        if get_heading_level(b_style) is not None and b_text:
                            skip_line = True
                        break
                if skip_line:
                    continue

            text = render_paragraph(block, args.images, image_map)

            if heading_level is not None and not heading_text:
                # If heading has no text (e.g., only images), treat as normal paragraph
                heading_level = None

            if not text and not list_info and not heading_level and not is_code:
                # preserve blank lines between blocks
                close_code_block()
                if lines and lines[-1].strip() != "":
                    lines.append("")
                continue

            if heading_level is not None:
                close_code_block()
                level = max(1, min(6, heading_level))
                line = "#" * level + " " + escape_md(heading_text)
                lines.append(line)
                lines.append("")
                if level <= 4 and heading_text:
                    slug = slugify(heading_text, used_slugs)
                    toc_items.append((level, heading_text, slug))
                continue

            if is_code:
                if not in_code:
                    lines.append("```")
                    in_code = True
                # For code, do not escape markdown
                raw = block.text.replace("\t", "    ")
                lines.append(raw)
                continue

            close_code_block()

            if list_info:
                list_type, level = list_info
                indent = "  " * level
                marker = "-" if list_type == "bullet" else "1."
                line = f"{indent}{marker} {text}".rstrip()
                lines.append(line)
            else:
                if text:
                    lines.append(text)
                    lines.append("")
        else:
            # Table
            close_code_block()
            table_lines = table_to_md(block, args.images, image_map)
            if table_lines:
                lines.extend(table_lines)
                lines.append("")

    close_code_block()

    # Build TOC (optional)
    if toc_items:
        toc_lines = ["## 目录", ""]
        # Build list with links
        for level, text, slug in toc_items:
            indent = "  " * (max(0, level - 2))
            toc_lines.append(f"{indent}- [{text}](#{slug})")
        toc_lines.append("")
        # Insert TOC after first heading if present
        insert_at = 0
        if lines and lines[0].startswith("# "):
            insert_at = 2  # after title and blank line
        lines = lines[:insert_at] + toc_lines + lines[insert_at:]

    # Normalize consecutive blank lines
    normalized = []
    blank = False
    for line in lines:
        if line.strip() == "":
            if not blank:
                normalized.append("")
            blank = True
        else:
            normalized.append(line.rstrip())
            blank = False
    # Trim leading/trailing blanks
    while normalized and normalized[0].strip() == "":
        normalized.pop(0)
    while normalized and normalized[-1].strip() == "":
        normalized.pop()

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("\n".join(normalized))

    # Print summary for logs
    print("saved:", args.output)
    print("images:", len(image_map))


if __name__ == "__main__":
    main()
