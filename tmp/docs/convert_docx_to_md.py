# -*- coding: utf-8 -*-
import os
import re
from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn


def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def escape_md(text):
    if text is None:
        return ""
    text = text.replace("\r", "")
    text = text.replace("|", "\\|")
    return text


def style_heading_level(style_name):
    if not style_name:
        return None
    m = re.search(r"(Heading|标题)\s*([0-9]+)", style_name, re.IGNORECASE)
    if m:
        try:
            return int(m.group(2))
        except ValueError:
            return None
    m = re.search(r"(Heading|标题)([0-9]+)", style_name, re.IGNORECASE)
    if m:
        try:
            return int(m.group(2))
        except ValueError:
            return None
    return None


def is_list_paragraph(p):
    style_name = p.style.name if p.style else ""
    if style_name:
        if "List" in style_name or "列表" in style_name:
            return True
    ppr = p._p.pPr
    if ppr is not None and ppr.numPr is not None:
        return True
    return False


def is_code_style(p):
    style_name = p.style.name if p.style else ""
    if not style_name:
        return False
    lowered = style_name.lower()
    if "code" in lowered or "代码" in style_name:
        return True
    return False


def paragraph_to_md(p, doc, image_ctx):
    fragments = []

    for run in p.runs:
        run_text = run.text or ""
        if run_text:
            if run.bold and run.italic:
                run_text = f"***{run_text}***"
            elif run.bold:
                run_text = f"**{run_text}**"
            elif run.italic:
                run_text = f"*{run_text}*"
            fragments.append(run_text)

        blips = run.element.xpath('.//a:blip')
        for blip in blips:
            rid = blip.get(qn('r:embed'))
            if not rid:
                continue
            if rid in image_ctx['rid_map']:
                rel_path = image_ctx['rid_map'][rid]
            else:
                part = doc.part.related_parts.get(rid)
                if part is None:
                    continue
                content_type = part.content_type or ""
                ext = content_type.split("/")[-1].lower() if "/" in content_type else "bin"
                if ext == "jpeg":
                    ext = "jpg"
                image_ctx['image_index'] += 1
                filename = f"image{image_ctx['image_index']}.{ext}"
                abs_path = os.path.join(image_ctx['asset_dir'], filename)
                with open(abs_path, "wb") as f:
                    f.write(part.blob)
                rel_path = os.path.join(image_ctx['asset_rel'], filename).replace("\\", "/")
                image_ctx['rid_map'][rid] = rel_path
            fragments.append(f"\n\n![]({rel_path})\n\n")

    text = "".join(fragments)
    text = text.replace("\u00a0", " ")  # nbsp
    return text


def table_to_md(table):
    rows = []
    max_cols = 0
    for row in table.rows:
        row_cells = []
        for cell in row.cells:
            cell_texts = []
            for p in cell.paragraphs:
                t = (p.text or "").strip()
                if t:
                    cell_texts.append(t)
            cell_text = "<br>".join(cell_texts)
            row_cells.append(escape_md(cell_text))
        max_cols = max(max_cols, len(row_cells))
        rows.append(row_cells)

    if not rows:
        return ""

    for row in rows:
        if len(row) < max_cols:
            row.extend([""] * (max_cols - len(row)))

    header = rows[0]
    body = rows[1:]

    md_lines = []
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join(["---"] * max_cols) + " |")

    for row in body:
        md_lines.append("| " + " | ".join(row) + " |")

    return "\n".join(md_lines)


def convert_docx_to_md(src_path, out_dir):
    doc = Document(src_path)
    base = os.path.splitext(os.path.basename(src_path))[0]
    asset_dir = os.path.join(out_dir, "assets", base)
    os.makedirs(asset_dir, exist_ok=True)
    asset_rel = os.path.join("assets", base)

    image_ctx = {
        "asset_dir": asset_dir,
        "asset_rel": asset_rel,
        "image_index": 0,
        "rid_map": {},
    }

    blocks = []
    in_code_block = False

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = paragraph_to_md(block, doc, image_ctx).strip()
            if not text:
                if in_code_block:
                    blocks.append("```")
                    in_code_block = False
                blocks.append("")
                continue

            if is_code_style(block):
                if not in_code_block:
                    blocks.append("```")
                    in_code_block = True
                blocks.append(text)
                continue
            elif in_code_block:
                blocks.append("```")
                in_code_block = False

            level = style_heading_level(block.style.name if block.style else "")
            if level:
                level = max(1, min(level, 6))
                blocks.append("#" * level + " " + text)
                continue

            if is_list_paragraph(block):
                blocks.append("- " + text)
                continue

            blocks.append(text)

        elif isinstance(block, Table):
            if in_code_block:
                blocks.append("```")
                in_code_block = False
            table_md = table_to_md(block)
            if table_md:
                blocks.append(table_md)
            blocks.append("")

    if in_code_block:
        blocks.append("```")

    cleaned = []
    blank = False
    for line in blocks:
        if line.strip() == "":
            if not blank:
                cleaned.append("")
            blank = True
        else:
            cleaned.append(line)
            blank = False

    content = "\n".join(cleaned).strip() + "\n"

    out_path = os.path.join(out_dir, base + ".md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    return out_path


if __name__ == "__main__":
    sources = [
        r"D:\\tortle\\Data\\download\\力扣刷题指南+LeetCode+101+-+A+Gri1773403212.docx",
        r"D:\\tortle\\Data\\download\\机器学习_周志华1772727397.docx",
    ]
    out_dir = r"D:\\spot\\K6\\output\\doc"
    for src in sources:
        if not os.path.exists(src):
            raise SystemExit(f"Source not found: {src}")
        out = convert_docx_to_md(src, out_dir)
        print(out)
