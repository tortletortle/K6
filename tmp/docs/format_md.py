# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

ROOT = r"D:\\spot\\K6\\output\\doc"
TOC_PLACEHOLDER = "__TOC_PLACEHOLDER__"
ANCHOR_RE = re.compile(r"^<a id=\"sec-\d+\"></a>$")
LABELS = ["题目描述", "输入输出样例", "题解"]
ZERO_WIDTH = ["\ufeff", "\u200b", "\u200c", "\u200d"]
NOISE_TOKENS = "©®™□■◆◇▲△▢▪"


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def write_text(path, text):
    Path(path).write_text(text, encoding="utf-8")


def strip_control_chars(s):
    out = []
    for ch in s:
        code = ord(ch)
        if ch in ("\n", "\t"):
            out.append(ch)
        elif 32 <= code <= 126 or code >= 160:
            out.append(ch)
    return "".join(out)


def normalize_ocr_noise(line):
    if not line:
        return line
    line = line.replace("\ufffd", "")
    line = line.replace("•", "·")
    line = re.sub(rf"(?<!\S)[{re.escape(NOISE_TOKENS)}](?!\S)", "", line)
    return line


def normalize_common(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    for zw in ZERO_WIDTH:
        text = text.replace(zw, "")
    text = strip_control_chars(text)
    lines = [line.rstrip() for line in text.split("\n")]
    lines = [normalize_ocr_noise(l) for l in lines]
    lines = [l for l in lines if not ANCHOR_RE.match(l.strip())]
    return lines


def is_blank(line):
    return re.fullmatch(r"[\s\u200b\u200c\u200d\ufeff]*", line or "") is not None


def clean_mangled_bold(line):
    if line.count("*") >= 6:
        line = re.sub(r"\*+", "", line)
        line = re.sub(r"\s+", " ", line).strip()
    return line


def cleanup_italic_noise(line):
    line = re.sub(r"\*([A-Za-z0-9]+)\*\*\s*\*", r"*\1*", line)
    line = re.sub(r"\*\s*\*", "", line)
    return line


def is_heading(line):
    return bool(re.match(r"^#{1,6}\s+", line))


def is_image(line):
    return bool(re.match(r"^!\[[^\]]*\]\([^\)]+\)\s*$", line))


def is_list_line(line):
    return bool(re.match(r"^\s*[-*+]\s+", line)) or bool(re.match(r"^\s*\d+\.\s+", line))


def is_code_fence(line):
    return line.strip().startswith("```")


def is_table_line(line):
    return line.lstrip().startswith("|")


def is_hr(line):
    return bool(re.match(r"^\s*(-{3,}|_{3,}|\*{3,})\s*$", line))


def is_html_line(line):
    s = line.strip()
    return s.startswith("<") and s.endswith(">")


def is_label_line(line):
    return line.strip() in {f"**{label}**" for label in LABELS}


def is_plain_line(line):
    if is_blank(line):
        return False
    if is_heading(line) or is_image(line) or is_code_fence(line) or is_table_line(line):
        return False
    if is_list_line(line) or line.lstrip().startswith(">") or is_html_line(line) or is_hr(line):
        return False
    if line.strip() == TOC_PLACEHOLDER or is_label_line(line):
        return False
    return True


def is_reference_line(line):
    s = line.strip()
    if not s:
        return False
    if s.startswith("- "):
        s = s[2:].strip()
    s = re.sub(r"^[\[\(（]?\d+[\]\)）\.\)]*\s*", "", s)
    if re.match(r"^[\u4e00-\u9fff]{2,}(?:等|等人)?\s*[，,\.]?\s*\(?\d{4}\)?", s):
        return True
    if re.match(r"^(?:[A-Z][a-z]+\s+)?[A-Z][A-Za-z\-]+,\s*(?:[A-Z0-9]\.(?:-[A-Z]\.)?|[A-Z][a-z]+\.)", s):
        return True
    if re.match(r"^[A-Z][a-z]{2,}\\s+and\\s+[A-Z]\\.", s):
        return True
    return False


def is_caption_candidate(line):
    s = line.strip()
    if not s:
        return False
    if re.match(r"^(图|表)\s*\d", s):
        return True
    if len(s) <= 20 and not re.search(r"[。！？.!?]$", s):
        return True
    return False


def is_toc_residue_line(line):
    s = line.strip()
    if not s:
        return False
    if is_heading(line):
        if re.search(r"(\t|\s{2,}|\.{2,})\d{1,4}\s*$", s):
            return True
    if re.search(r"\d", s) and not re.search(r"[。！？!?]", s):
        if re.search(r"\.{2,}", s):
            return True
        num_groups = len(re.findall(r"\d{1,4}", s))
        if num_groups >= 2 and not re.search(r"[=+\-*/<>]", s):
            return True
        if re.search(r"\d{1,4}\s*$", s):
            prefix = re.sub(r"\d{1,4}\s*$", "", s).strip()
            prefix = re.sub(r"^[-*+]\s+", "", prefix)
            if prefix and len(prefix) <= 20 and not re.search(r"[=+\-*/<>。！？!?]", prefix):
                return True
        keywords = ["习题", "参考文献", "休息一会儿", "阅读材料", "索引", "后记", "附录"]
        hit = sum(1 for k in keywords if k in s)
        if hit >= 1 and num_groups >= 2:
            return True
        if hit >= 2 and num_groups >= 1:
            return True
    return False


def normalize_caption_text(text):
    s = re.sub(r"\s+", " ", text.strip())
    s = s.replace(":", "：")
    s = re.sub(r"\s*：\s*", "：", s)
    s = re.sub(r"^(图)\s*(\d+(?:\.\d+)*)", r"图 \2", s)
    s = re.sub(r"^(表)\s*(\d+(?:\.\d+)*)", r"表 \2", s)
    s = re.sub(r"^(图 \d+(?:\.\d+)*)(\S)", r"\1 \2", s)
    s = re.sub(r"^(表 \d+(?:\.\d+)*)(\S)", r"\1 \2", s)
    return s


def join_with_space(prev, nxt):
    if not prev:
        return nxt
    if not nxt:
        return prev
    p = prev
    n = nxt
    if re.search(r"[A-Za-z0-9]$", p) and re.match(r"[A-Za-z0-9]", n):
        return p + " " + n
    if re.search(r"[\.,;:!?]$", p) and re.match(r"[A-Za-z0-9]", n):
        return p + " " + n
    return p + n


def split_section_labels(lines):
    out = []
    for line in lines:
        if is_heading(line):
            out.append(line)
            continue
        stripped = line.strip()
        matched = False
        for label in LABELS:
            if stripped.startswith(label):
                rest = stripped[len(label):].lstrip("：: \t")
                out.append(f"**{label}**")
                if rest:
                    out.append(rest)
                matched = True
                break
        if not matched:
            out.append(line)
    return out


def normalize_label_headings(lines):
    out = []
    for line in lines:
        m = re.match(r"^#{1,6}\s+(题目描述|输入输出样例|题解)\s*(.*)$", line)
        if m:
            label = m.group(1)
            rest = m.group(2).strip()
            out.append(f"**{label}**")
            if rest:
                out.append(rest)
            continue
        out.append(line)
    return out


def fix_inline_labels_post(lines):
    out = []
    for line in lines:
        if is_heading(line) or is_list_line(line) or line.lstrip().startswith(">"):
            out.append(line)
            continue
        stripped = line.strip()
        m = re.match(r"^(题目描述|输入输出样例|题解)(.+)$", stripped)
        if m:
            label = m.group(1)
            rest = m.group(2).lstrip("：: \t")
            out.append(f"**{label}**")
            if rest:
                out.append(rest)
            continue
        out.append(line)
    return out


def ensure_blank_after_labels(lines):
    out = []
    for i, line in enumerate(lines):
        out.append(line)
        if is_label_line(line):
            if i + 1 < len(lines) and not is_blank(lines[i + 1]):
                out.append("")
    return out


def merge_notice_blockquotes(lines):
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith(">") and ("注意" in line or "提示" in line):
            content = line.lstrip()[1:].lstrip()
            j = i + 1
            while j < len(lines):
                if is_blank(lines[j]):
                    break
                if not is_plain_line(lines[j]):
                    break
                content = join_with_space(content, lines[j].strip())
                j += 1
            out.append("> " + content.strip())
            i = j
            continue
        out.append(line)
        i += 1
    return out


def merge_plain_lines(lines):
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_plain_line(line):
            buf = line.strip()
            i += 1
            while i < len(lines) and is_plain_line(lines[i]):
                buf = join_with_space(buf, lines[i].strip())
                i += 1
            out.append(buf)
        else:
            out.append(line)
            i += 1
    return out


def remove_toc_residue(lines):
    out = []
    for line in lines:
        s = line.strip()
        if not s:
            out.append(line)
            continue
        if is_toc_residue_line(line):
            continue
        if is_heading(line) or is_list_line(line) or is_table_line(line) or is_image(line) or is_code_fence(line):
            out.append(line)
            continue
        if is_pseudocode_like(line):
            out.append(line)
            continue
        if re.search(r"[。！？,:;，；：]", s):
            out.append(line)
            continue
        if re.search(r"\t|\s{2,}", line) and re.match(r"^[\w\u4e00-\u9fff\*·（）()【】]+(?:\s+|\t)+\d{1,4}\s*$", s):
            continue
        if re.match(r"^[\w\u4e00-\u9fff\*·（）()【】]+\.{2,}\s*\d{1,4}\s*$", s):
            continue
        out.append(line)
    return out


def split_inline_pseudocode_markers(lines):
    out = []
    for line in lines:
        if is_heading(line) or is_list_line(line) or is_table_line(line) or is_image(line):
            out.append(line)
            continue
        if line.lstrip().startswith(">") or is_html_line(line) or is_hr(line) or is_code_fence(line):
            out.append(line)
            continue
        if not re.search(r"(输入|输出|过程|算法|伪代码)\s*[:：]|\d+\s*[:：]", line):
            out.append(line)
            continue

        s = line
        s = re.sub(r"(输入|输出|过程|算法|伪代码)\s*[:：]", r"\n\1：", s)
        s = re.sub(r"(?<!\d)(\d{1,2})\s*[:：]", r"\n\1：", s)
        s = re.sub(r"(输出：[^图表]*)(图\s*\d+.*)", r"\1\n\2", s)
        parts = [p.strip() for p in s.split("\n") if p.strip()]
        if len(parts) <= 1:
            out.append(line)
            continue
        out.extend(parts)
    return out


def split_caption_lines(lines):
    out = []
    for line in lines:
        s = line.strip()
        if re.match(r"^(图|表)\s*\d", s) and len(s) > 30:
            if "。" in s:
                cap, rest = s.split("。", 1)
                out.append(cap.strip())
                if rest.strip():
                    out.append(rest.strip())
                continue
            m = re.search(r"(显然|一般|因此|注意|本节|下面|此时|可以|于是)", s)
            if m:
                cap = s[:m.start()].strip()
                rest = s[m.start():].strip()
                if cap:
                    out.append(cap)
                if rest:
                    out.append(rest)
                continue
        out.append(line)
    return out


def is_formula_snippet(s):
    if not s:
        return False
    if "$" in s:
        return False
    math_chars = sum(1 for c in s if c in "=+-/^_<>≤≥≈≠∑∏∞")
    if math_chars == 0:
        return False
    chinese = sum(1 for c in s if '\u4e00'<=c<='\u9fff')
    ascii_ratio = sum(1 for c in s if c.isascii() and not c.isspace()) / max(len(s), 1)
    if chinese <= 4 and ascii_ratio > 0.45:
        return True
    return False


def split_equation_lines(lines):
    out = []
    eq_re = re.compile(r"\(\d+(?:\.\d+)*\)")
    for line in lines:
        if is_heading(line) or is_list_line(line) or is_table_line(line) or is_image(line) or is_code_fence(line):
            out.append(line)
            continue
        m = eq_re.search(line)
        if not m:
            out.append(line)
            continue
        prefix = line[:m.start()].rstrip()
        suffix = line[m.end():].lstrip()
        delim_idx = max(prefix.rfind("。"), prefix.rfind("；"), prefix.rfind("："), prefix.rfind("，"))
        if delim_idx == -1:
            delim_idx = prefix.rfind(" ")
        formula = line[delim_idx + 1:m.end()].strip()
        pre = prefix[:delim_idx + 1].strip()
        if is_formula_snippet(formula):
            if pre:
                out.append(pre)
            out.append(formula)
            if suffix:
                out.append(suffix)
            continue
        out.append(line)
    return out


def should_merge_across_blank(prev, nxt):
    prev_s = prev.strip()
    if not prev_s:
        return False
    if re.search(r"[。！？.!?]$", prev_s):
        return False
    if re.search(r"[:：]$", prev_s):
        return False
    return True


def merge_across_blank(lines):
    out = []
    i = 0
    while i < len(lines):
        if i + 2 < len(lines) and is_plain_line(lines[i]) and is_blank(lines[i + 1]) and is_plain_line(lines[i + 2]):
            if should_merge_across_blank(lines[i], lines[i + 2]):
                merged = join_with_space(lines[i].strip(), lines[i + 2].strip())
                out.append(merged)
                i += 3
                continue
        out.append(lines[i])
        i += 1
    return out


def collapse_blank_lines(lines):
    out = []
    blank = False
    for line in lines:
        if is_blank(line):
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(line)
            blank = False
    return out


def normalize_chapter_heading(line):
    m = re.match(r"^(#{2,6})\s+第\s*(\d+)\s*章\s*(.*)$", line)
    if m:
        title = re.sub(r"\s+", " ", m.group(3)).strip()
        if title:
            return f"{m.group(1)} 第 {m.group(2)} 章 {title}"
        return f"{m.group(1)} 第 {m.group(2)} 章"
    return line


def normalize_toc_chapter_line(line):
    m = re.match(r"^(\s*-\s+\[)第\s*(\d+)\s*章\s*(.*?)(\]\(#[^\)]*\))", line)
    if m:
        title = re.sub(r"\s+", " ", m.group(3)).strip()
        if title:
            return f"{m.group(1)}第 {m.group(2)} 章 {title}{m.group(4)}"
        return f"{m.group(1)}第 {m.group(2)} 章{m.group(4)}"
    return line


def remove_existing_toc(lines, toc_title="目录"):
    cleaned = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m and m.group(2).strip() == toc_title:
            level = len(m.group(1))
            i += 1
            while i < len(lines):
                m2 = re.match(r"^(#{1,6})\s+", lines[i])
                if m2 and len(m2.group(1)) <= level:
                    break
                i += 1
            continue
        cleaned.append(line)
        i += 1
    return cleaned


def add_anchors_and_toc(lines, toc_title="目录", min_level=2, max_level=3, toc_filter=None):
    lines = remove_existing_toc(lines, toc_title=toc_title)

    headings = []
    out = []
    counter = 0
    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            counter += 1
            anchor_id = f"sec-{counter}"
            out.append(f"<a id=\"{anchor_id}\"></a>")
            out.append(line)
            if min_level <= level <= max_level and title != toc_title:
                if toc_filter is None or toc_filter(level, title):
                    headings.append((level, title, anchor_id))
        else:
            out.append(line)

    toc_lines = [f"## {toc_title}"]
    for level, title, anchor_id in headings:
        indent = "  " * (level - min_level)
        toc_lines.append(f"{indent}- [{title}](#{anchor_id})")

    out2 = []
    inserted = False
    for line in out:
        if line.strip() == TOC_PLACEHOLDER:
            out2.append("")
            out2.extend(toc_lines)
            out2.append("")
            inserted = True
        else:
            out2.append(line)

    if not inserted:
        out2 = toc_lines + [""] + out2

    return out2


def ensure_blank_before_blocks(lines):
    out = []
    for line in lines:
        if is_list_line(line) and out and is_list_line(out[-1]):
            out.append(line)
            continue
        if (is_heading(line) or is_list_line(line) or line.lstrip().startswith(">") or is_table_line(line)) and out and not is_blank(out[-1]):
            out.append("")
        out.append(line)
    return out


def is_code_like(line):
    if is_blank(line):
        return False
    if is_heading(line) or is_image(line) or is_table_line(line) or is_list_line(line) or line.lstrip().startswith(">"):
        return False
    s = line.rstrip()
    if s.startswith("    ") or s.startswith("\t"):
        return True
    patterns = [
        r"\b(def|class|return|for|while|if|elif|else|switch|case|break|continue|import|from|try|catch)\b",
        r"\b(int|float|double|char|bool|string|List|vector|dict|map|set)\b",
        r"#include|using\s+namespace|public|private|static|void",
        r"//|/\*|\*/",
        r"->|::|=>",
    ]
    if any(re.search(p, s) for p in patterns):
        ascii_ratio = sum(1 for c in s if c.isascii() and not c.isspace()) / max(len(s), 1)
        if ascii_ratio > 0.5:
            return True
    if re.search(r"[{};]", s) and sum(1 for c in s if '\u4e00'<=c<='\u9fff') <= 2:
        return True
    if re.search(r"\b[a-zA-Z_]+\s*=\s*[^=]", s) and sum(1 for c in s if '\u4e00'<=c<='\u9fff') <= 2:
        return True
    return False


def wrap_code_blocks(lines):
    out = []
    in_fence = False
    buffer = []

    def detect_code_language(buf):
        text = "\n".join(buf)
        if re.search(r"#include|std::|using\s+namespace|vector<|unordered_map|unordered_set|nullptr|cout<<|cin>>|#define|public:|private:", text):
            return "cpp"
        if re.search(r"\bdef\b|\bclass\b\s+\w+\s*:\s*$|import\s+|from\s+\w+\s+import|self\b|None\b|True\b|False\b|elif\b|print\(", text):
            return "python"
        return ""

    def flush():
        if buffer:
            lang = detect_code_language(buffer)
            fence = f"```{lang}" if lang else "```"
            out.append(fence)
            out.extend(buffer)
            out.append("```")
            buffer.clear()

    for line in lines:
        if is_code_fence(line):
            if buffer:
                flush()
            out.append(line)
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(line)
            continue
        if is_code_like(line):
            buffer.append(line)
        else:
            if buffer:
                flush()
            out.append(line)
    if buffer:
        flush()
    return out


def is_pseudocode_like(line):
    if is_blank(line):
        return False
    if is_heading(line) or is_image(line) or is_table_line(line) or is_list_line(line):
        return False
    if line.lstrip().startswith(">") or is_html_line(line) or is_hr(line):
        return False
    s = line.strip()
    if not s:
        return False
    if re.match(r"^(图|表)\s*\d", s):
        return False
    if re.match(r"^(输入|输出|过程|算法|伪代码)\s*[:：]", s):
        return True
    if len(s) > 160:
        return False
    if len(s) > 120 and re.search(r"[。！？]", s):
        return False

    indent = line.startswith("    ") or line.startswith("\t")
    step = re.match(r"^\s*\d+\s*[:：．.)]", line) or re.match(r"^\s*[A-Za-z]\)\s+", line)
    arrow = re.search(r"(<-|<-|:=|←|→|⇒|→)", s)
    cn_kw = re.search(r"(输入|输出|算法|伪代码|过程|步骤|初始化|重复|直到|返回|如果|否则|当|则|令|设)", s)
    en_kw = re.search(r"\b(for|while|if|else|return|repeat|until|begin|end|do)\b", s, re.IGNORECASE)

    if step or cn_kw or en_kw or arrow:
        return True
    if indent and len(s) <= 80:
        return True
    return False


def wrap_pseudocode_blocks(lines):
    out = []
    buffer = []
    pseudo_count = 0
    in_fence = False

    def flush():
        nonlocal buffer, pseudo_count
        if not buffer:
            return
        if pseudo_count >= 2:
            while buffer and is_blank(buffer[0]):
                buffer.pop(0)
            while buffer and is_blank(buffer[-1]):
                buffer.pop()
            if buffer:
                out.append("```")
                out.extend(buffer)
                out.append("```")
        else:
            out.extend(buffer)
        buffer = []
        pseudo_count = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        if is_code_fence(line):
            flush()
            out.append(line)
            in_fence = not in_fence
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue
        if is_pseudocode_like(line):
            buffer.append(line)
            pseudo_count += 1
            i += 1
            continue
        if is_blank(line) and buffer:
            j = i + 1
            while j < len(lines) and is_blank(lines[j]):
                j += 1
            if j < len(lines) and is_pseudocode_like(lines[j]):
                buffer.append("")
                i += 1
                continue
        flush()
        out.append(line)
        i += 1

    flush()
    return out


def convert_inline_math_line(line):
    if "$" in line:
        return line
    if is_code_like(line) or is_table_line(line) or is_heading(line) or is_image(line):
        return line

    def repl(m):
        token = m.group(1)
        if len(token) <= 3:
            return f"${token}$"
        if any(ch.isdigit() for ch in token):
            return f"${token}$"
        if token.isupper() or token[0].isupper():
            return f"${token}$"
        return m.group(0)

    line = re.sub(r"\*([A-Za-z][A-Za-z0-9_]*)\*", repl, line)
    line = re.sub(r"\$([A-Za-z])\$\s*\(\s*\$([A-Za-z0-9_]+)\$\s*\)", r"$\1(\2)$", line)
    return line


def apply_inline_math(lines):
    out = []
    in_fence = False
    for line in lines:
        if is_code_fence(line):
            out.append(line)
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(convert_inline_math_line(line))
    return out


def separate_adjacent_inline_math_line(line):
    if line.strip() == "$$":
        return line
    prev = None
    cur = line
    while prev != cur:
        prev = cur
        cur = re.sub(r"\$([^\$]+?)\$\$([^\$]+?)\$", r"$\1$ $\2$", cur)
    return cur


def separate_adjacent_inline_math(lines):
    out = []
    in_fence = False
    for line in lines:
        if is_code_fence(line):
            out.append(line)
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(separate_adjacent_inline_math_line(line))
    return out


def is_math_block_candidate(line):
    if is_blank(line):
        return False
    if is_heading(line) or is_list_line(line) or line.lstrip().startswith(">") or is_table_line(line) or is_code_like(line):
        return False
    s = line.strip()
    if re.fullmatch(r"\*[^*]+\*", s):
        return False
    if "$" in s:
        return False
    if len(s) > 120:
        return False
    chinese = sum(1 for c in s if '\u4e00'<=c<='\u9fff')
    if chinese > 2:
        return False
    math_chars = sum(1 for c in s if c in "=+-/^_<>≤≥≈≠∑∏∞")
    ascii_ratio = sum(1 for c in s if c.isascii() and not c.isspace()) / max(len(s), 1)
    eq_no = re.search(r"\(\d+(?:\.\d+)*\)", s)
    if eq_no and math_chars >= 1 and ascii_ratio > 0.5:
        return True
    if math_chars >= 2 and ascii_ratio > 0.65 and not re.search(r"[A-Za-z]{3,}\s+[A-Za-z]{3,}", s):
        return True
    return False


def wrap_math_blocks(lines):
    out = []
    in_ref = False
    ref_level = None
    in_fence = False
    for line in lines:
        if is_code_fence(line):
            out.append(line)
            in_fence = not in_fence
            continue
        if in_fence:
            out.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+参考文献\s*$", line)
        if m:
            in_ref = True
            ref_level = len(m.group(1))
            out.append(line)
            continue
        if in_ref:
            m2 = re.match(r"^(#{1,6})\s+", line)
            if m2 and len(m2.group(1)) <= (ref_level or 6):
                in_ref = False
            if in_ref:
                out.append(line)
                continue
        if is_reference_line(line):
            out.append(line)
            continue
        if is_math_block_candidate(line):
            if out and not is_blank(out[-1]):
                out.append("")
            out.append("$$")
            out.append(line.strip())
            out.append("$$")
            out.append("")
        else:
            out.append(line)
    return out


def split_reference_entries(text):
    if not text:
        return []
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("；", ";")

    def boundary_ok(idx):
        j = idx - 1
        while j >= 0 and text[j].isspace():
            j -= 1
        if j < 0:
            return True
        return text[j] in "。.;；:："

    def has_year_near(idx):
        return re.search(r"\(\d{4}[a-z]?\)", text[idx: idx + 140], re.IGNORECASE) is not None

    def is_initial_before(idx):
        j = idx - 1
        while j >= 0 and text[j].isspace():
            j -= 1
        if j <= 0 or text[j] != ".":
            return False
        k = j - 1
        while k >= 0 and text[k].isspace():
            k -= 1
        if k < 0:
            return False
        if text[k].isupper() and (k == 0 or not text[k - 1].isalpha()):
            return True
        return False

    starts = {0}
    cn_pat = re.compile(r"[\u4e00-\u9fff]{2,}(?:等|等人)?\s*[，,\.]?\s*\(?\d{4}\)?")
    en_pat = re.compile(r"(?:[A-Z][a-z]+\s+)?[A-Z][A-Za-z\-]+,\s*(?:[A-Z0-9]\.(?:-[A-Z]\.)?|[A-Z][a-z]+\.)")
    en_and_pat = re.compile(r"[A-Z][a-z]{2,}\s+and\s+[A-Z]\.")

    for m in cn_pat.finditer(text):
        idx = m.start()
        if idx == 0:
            continue
        if boundary_ok(idx):
            starts.add(idx)

    for m in en_pat.finditer(text):
        idx = m.start()
        if idx == 0:
            continue
        if boundary_ok(idx) and has_year_near(idx) and not is_initial_before(idx):
            starts.add(idx)

    for m in en_and_pat.finditer(text):
        idx = m.start()
        if idx == 0:
            continue
        if boundary_ok(idx) and has_year_near(idx) and not is_initial_before(idx):
            starts.add(idx)

    if len(starts) <= 1 and ";" in text:
        parts = [p.strip(" ;") for p in text.split(";") if p.strip()]
        return [re.sub(r"^[\[\(（]?\d+[\]\)）\.\)]*\s*", "", p).strip() for p in parts]

    starts = sorted(starts)
    parts = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        entry = text[start:end].strip(" ;")
        entry = re.sub(r"^[\[\(（]?\d+[\]\)）\.\)]*\s*", "", entry).strip()
        if entry:
            parts.append(entry)
    return parts


def restructure_references(lines):
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        heading_match = re.match(r"^(#{1,6})\s+参考文献\s*$", line)
        inline_idx = None
        if not heading_match and "参考文献" in line and not is_heading(line):
            inline_idx = line.find("参考文献")
        if heading_match or inline_idx is not None or re.match(r"^\s*参考文献", line):
            heading = "#### 参考文献"
            content = ""
            if inline_idx is not None:
                prefix = line[:inline_idx].rstrip()
                suffix = line[inline_idx + len("参考文献"):].strip(" ：:")
                if prefix:
                    out.append(prefix)
                if suffix:
                    content = suffix
            else:
                content = re.sub(r"^(#{1,6})\s+参考文献\s*$", "", line).strip()
                content = re.sub(r"^\s*参考文献[:：]?\s*", "", content).strip()
            buf = []
            if content:
                buf.append(content)
            i += 1
            while i < len(lines):
                l = lines[i]
                if is_blank(l):
                    break
                if is_heading(l) or ANCHOR_RE.match(l.strip()) or is_image(l) or is_table_line(l):
                    break
                if is_list_line(l) and l.strip().startswith("- "):
                    buf.append(l.strip().lstrip("- ").strip())
                    i += 1
                    continue
                buf.append(l.strip())
                i += 1
            out.append(heading)
            entries = split_reference_entries(" ".join(buf))
            if entries:
                out.extend([f"- {e}" for e in entries])
            else:
                out.append("")
            continue
        out.append(line)
        i += 1
    return out


def process_leetcode(text):
    lines = normalize_common(text)
    lines = [clean_mangled_bold(l) for l in lines]

    toc_start = None
    toc_end = None
    for i, line in enumerate(lines):
        if toc_start is None and line.lstrip().startswith("|") and "玩转双指针" in line:
            toc_start = i
        if toc_start is not None and re.match(r"^##\s+算法解释\s*$", line):
            toc_end = i
            break
    if toc_start is not None and toc_end is not None and toc_start < toc_end:
        lines = lines[:toc_start] + lines[toc_end:]

    for i, line in enumerate(lines):
        if "LeetCode 101" in line and "力扣刷题指南" in line:
            title_text = re.sub(r"^#+\s*", "", line)
            title_text = title_text.replace(" (第二版)", "（第二版）").replace("(第二版)", "（第二版）")
            title_text = title_text.replace("指南 （", "指南（")
            lines[i] = "# " + title_text
            if i + 1 < len(lines) and "Grinding" in lines[i + 1]:
                subtitle = re.sub(r"^\*|\*$", "", lines[i + 1].strip())
                lines[i + 1] = f"*{subtitle}*"
            break

    for i, line in enumerate(lines):
        if line.startswith("作者：") or line.startswith("语言：") or line.startswith("版本："):
            if not line.startswith("- "):
                lines[i] = "- " + line

    lines = [l for l in lines if not re.search(r"\b\d+\s*/\s*\d+\b", l)]

    new_lines = []
    for line in lines:
        l = line.strip()
        l = l.replace("注意 **", "注意 ")
        if re.match(r"^(\*\*\s*)?注意", l):
            content = re.sub(r"^(\*\*\s*)?注意\s*\**", "", l).strip()
            if content:
                new_lines.append(f"> **注意：** {content}")
            else:
                new_lines.append("> **注意：**")
        else:
            new_lines.append(line)
    lines = new_lines

    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            title = m.group(2).strip()
            if "LeetCode 101" in title and "力扣刷题指南" in title:
                lines[i] = "# " + title
            else:
                level = len(m.group(1))
                new_level = min(level + 1, 6)
                lines[i] = "#" * new_level + " " + title

    first_section_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^###\s+算法解释\s*$", line):
            first_section_idx = i
            break
    has_ch1 = any(re.match(r"^##\s+第\s*1\s*章", l) for l in lines)
    if first_section_idx is not None and not has_ch1:
        lines.insert(first_section_idx, "## 第 1 章 贪心算法")

    lines = split_section_labels(lines)
    lines = normalize_label_headings(lines)

    cleaned = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_image(line):
            cleaned.append(line)
            if i + 1 < len(lines) and is_caption_candidate(lines[i + 1]):
                cap = normalize_caption_text(clean_mangled_bold(lines[i + 1]))
                cleaned.append(f"*{cap}*")
                i += 2
                continue
        cleaned.append(line) if not is_image(line) else None
        i += 1
    lines = cleaned

    lines = [cleanup_italic_noise(l) for l in lines]
    lines = [normalize_chapter_heading(l) for l in lines]

    lines = merge_notice_blockquotes(lines)
    lines = merge_plain_lines(lines)
    lines = remove_toc_residue(lines)
    lines = merge_across_blank(lines)
    lines = collapse_blank_lines(lines)
    lines = restructure_references(lines)
    lines = fix_inline_labels_post(lines)
    lines = ensure_blank_after_labels(lines)
    lines = ensure_blank_before_blocks(lines)

    lines = apply_inline_math(lines)
    lines = separate_adjacent_inline_math(lines)
    lines = wrap_math_blocks(lines)
    lines = wrap_code_blocks(lines)

    if TOC_PLACEHOLDER not in lines:
        last_meta = None
        for i, line in enumerate(lines):
            if line.startswith("- 作者：") or line.startswith("- 语言：") or line.startswith("- 版本："):
                last_meta = i
        insert_at = (last_meta + 1) if last_meta is not None else 0
        lines.insert(insert_at, TOC_PLACEHOLDER)

    def toc_filter(level, title):
        if level == 2:
            return bool(re.match(r"第\s*\d+\s*章", title)) or title.startswith("全书完")
        if level == 3:
            if len(title) > 24:
                return False
            if re.search(r"[。！，,]", title):
                return False
            return True
        return False

    lines = add_anchors_and_toc(lines, toc_title="目录", min_level=2, max_level=3, toc_filter=toc_filter)
    lines = [normalize_toc_chapter_line(l) for l in lines]

    return "\n".join(lines).strip() + "\n"


def process_ml(text):
    lines = normalize_common(text)

    def remove_cn_spaces(line):
        return re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", line)

    lines = [remove_cn_spaces(l) for l in lines]

    if not any(is_heading(l) for l in lines[:10]):
        lines = ["# 机器学习（周志华）", ""] + lines

    new_lines = []
    current_chapter = None
    for line in lines:
        stripped = line.strip()
        m = re.match(r"^第\s*(\d+)\s*章\s*(.*)$", stripped)
        if m:
            current_chapter = m.group(1)
            title = m.group(2).strip()
            if title:
                new_lines.append(f"## 第 {current_chapter} 章 {title}")
            else:
                new_lines.append(f"## 第 {current_chapter} 章")
            continue
        m = re.match(r"^L(\d+)\s*(.*)$", stripped)
        if m and current_chapter:
            sec = f"{current_chapter}.{m.group(1)}"
            title = m.group(2).strip()
            if title:
                new_lines.append(f"### {sec} {title}")
            else:
                new_lines.append(f"### {sec}")
            continue
        m = re.match(r"^(\d+(?:\.\d+)+)\s*(.*)$", stripped)
        if m:
            sec = m.group(1)
            title = m.group(2).strip()
            if not title:
                new_lines.append(line)
                continue
            if len(title) > 40:
                new_lines.append(line)
                continue
            if re.search(r"[。！？!？；;：:,，]", title):
                new_lines.append(line)
                continue
            if "." in title and not re.search(r"\d\.\d", title):
                new_lines.append(line)
                continue
            if re.search(r"=|;", title):
                new_lines.append(line)
                continue
            if not re.search(r"[A-Za-z\u4e00-\u9fff]", title):
                new_lines.append(line)
                continue
            dots = sec.count(".")
            level = min(2 + dots, 6)
            new_lines.append(f"{'#'*level} {sec} {title}".strip())
            continue
        new_lines.append(line)
    lines = new_lines

    out = []
    pending_caption = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if pending_caption and is_image(line):
            out.append(line)
            out.append(f"*{pending_caption}*")
            pending_caption = None
            i += 1
            continue

        if is_image(line):
            out.append(line)
            if i + 1 < len(lines) and is_caption_candidate(lines[i + 1]):
                cap = normalize_caption_text(lines[i + 1])
                out.append(f"*{cap}*")
                i += 2
                continue
            i += 1
            continue

        if is_caption_candidate(line):
            j = i + 1
            while j < len(lines) and is_blank(lines[j]):
                j += 1
            if j < len(lines) and is_image(lines[j]):
                pending_caption = normalize_caption_text(line)
                i += 1
                continue
        out.append(line)
        i += 1

    lines = out

    lines = [cleanup_italic_noise(l) for l in lines]
    lines = [normalize_chapter_heading(l) for l in lines]

    lines = split_section_labels(lines)
    lines = normalize_label_headings(lines)
    lines = merge_notice_blockquotes(lines)
    lines = merge_plain_lines(lines)
    lines = split_inline_pseudocode_markers(lines)
    lines = split_caption_lines(lines)
    lines = split_equation_lines(lines)
    lines = merge_across_blank(lines)
    lines = remove_toc_residue(lines)
    lines = collapse_blank_lines(lines)
    lines = restructure_references(lines)
    lines = fix_inline_labels_post(lines)
    lines = ensure_blank_after_labels(lines)
    lines = ensure_blank_before_blocks(lines)

    lines = apply_inline_math(lines)
    lines = separate_adjacent_inline_math(lines)
    lines = wrap_pseudocode_blocks(lines)
    lines = wrap_math_blocks(lines)

    if TOC_PLACEHOLDER not in lines:
        title_idx = None
        for i, line in enumerate(lines):
            if line.startswith("# "):
                title_idx = i
                break
        insert_at = title_idx + 1 if title_idx is not None else 0
        lines.insert(insert_at, TOC_PLACEHOLDER)

    lines = add_anchors_and_toc(lines, toc_title="目录", min_level=2, max_level=3)
    lines = [normalize_toc_chapter_line(l) for l in lines]

    return "\n".join(lines).strip() + "\n"


def find_file(root, predicate):
    for name in os.listdir(root):
        if predicate(name):
            return os.path.join(root, name)
    return None


def main():
    leet_path = find_file(ROOT, lambda n: n.endswith('.md') and 'LeetCode+101' in n)
    ml_path = find_file(ROOT, lambda n: n.endswith('.md') and '机器学习' in n)

    if leet_path:
        text = read_text(leet_path)
        new_text = process_leetcode(text)
        write_text(leet_path, new_text)
        print(leet_path)

    if ml_path:
        text = read_text(ml_path)
        new_text = process_ml(text)
        write_text(ml_path, new_text)
        print(ml_path)


if __name__ == '__main__':
    main()
