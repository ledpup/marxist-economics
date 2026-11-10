"""Convert the GIC's "Fundamental Principles of Communist Production and
Distribution" from PDF to Markdown. Shared code is in pdf_markdown_common.py.

Layout facts the converter relies on (found by inspecting the PDF):
  body text    Garamond 12 (11 on the front-matter page), justified,
               lines ~15.5pt apart, paragraphs ~23.5pt apart
  headings     bold 16pt = chapter  ->  "# ..."
               bold 13pt (a few bold 12pt "a. ...") = section  ->  "## ..."
  block quotes italic paragraphs opened with » (or “ / ") and closed with «
  emphasis     italic / bold fonts; letter-spaced text (real spaces with a
               ~2pt advance) is the German "Sperrsatz" and becomes bold
  footnotes    Garamond 11 below a ~144pt rule, each starting with a 7pt
               number; numbering is continuous through the book
  markers      7-8.5pt superscript digits in the text
  page numbers Calibri 11 at the bottom centre; no running headers

Usage: python pdf_to_markdown_gic.py "PDFs/FUNDAMENTAL PRINCIPLES OF COMMUNIST PRODUCTION AND DISTRIBUTION.pdf" Documents/fundamental_principles.md
"""
import re
import sys

import pymupdf

from pdf_markdown_common import (block_escape, build_vocab, escape, is_bold, is_italic, join_lines,
                                 raw_lines, render, smart_title)

FIRST_PAGE, LAST_PAGE = 3, 301  # 0-based: "Objective" .. end of Literature
SKIP_PAGES = {4, 5}             # printed table of contents
# Pages 0-2 are cover, title and imprint (handled by front_matter); pages
# 302+ are the back cover and the publisher's adverts for other books.

# Formula displays set in Cambria Math, keyed by (page, n-th display on page).
MATH = {
    (174, 0): r"$$\frac{L - (F_p + C_p)}{L + L_p}$$",
    (174, 1): r"$$\text{FIC} = \frac{600 - 58}{600 + 50} = \frac{542}{650} = 0.83$$",
    (181, 0): r"$$\text{FIC} = \frac{L - \{(F_p + C_p) - (F'_p + C'_p)\}}{L + L_p}$$",
}

SMALL = 9.5          # anything smaller is a superscript/subscript/note number
CELL_GAP = 15        # horizontal gap that separates table cells
QUOTE_OPEN = "»“„\""
TERMINAL = ".!?:«\"”"
DATE = re.compile(r"(\d{1,2} )?[A-Z][a-z]+( \d{1,2},)? \d{4}$")


# ----------------------------------------------------------------- extraction

def footnote_top(page, lines):
    """y of the footnote separator rule, or None."""
    rules = sorted((d["rect"] for d in page.get_drawings()), key=lambda r: r.y0)
    for r in rules:
        if r.height < 2 and 130 < r.width < 160 and r.x0 < 80:
            below = [l for l in lines if r.y0 < l.y0 < r.y0 + 20]
            if below and below[0].chars and starts_with_number(below[0]):
                return r.y0
    return None


def starts_with_number(line):
    first = next(c for c in line.chars if c.c.strip())
    return first.size < SMALL and first.c.isdigit()


def extract(doc):
    """Return (body lines in reading order, {note number: [lines]})."""
    body, notes, last_note = [], {}, None
    for pno in range(FIRST_PAGE, LAST_PAGE + 1):
        if pno in SKIP_PAGES:
            continue
        page = doc[pno]
        lines = [l for l in raw_lines(page, pno, SMALL)
                 if not (l.y0 > 500 and all("Calibri" in c.font for c in l.chars if c.c.strip()))]
        top = footnote_top(page, lines)
        for l in lines:
            if top is None or l.y0 < top:
                body.append(l)
            elif starts_with_number(l):
                digits = ""
                for c in l.chars:
                    if c.c.strip() and not (c.size < SMALL and c.c.isdigit()):
                        break
                    digits += c.c
                last_note = int(digits)
                l.chars = l.chars[len(digits):]
                notes[last_note] = [l]
            else:  # continuation of the previous note (possibly from the previous page)
                notes[last_note].append(l)
    return body, notes


# --------------------------------------------------------------- paragraphs

def line_kind(l):
    if l.math:
        return "math"
    if l.bold > 0.8 and l.size >= 14:
        return "h1"
    if l.bold > 0.8 and l.size >= 12.5:
        return "h2"
    if len(cells(l)) > 1:
        return "row"
    return "text"


def paragraphs(body):
    paras = []  # dicts: kind, lines
    right_edge = {}
    for l in body:
        right_edge[l.page] = max(right_edge.get(l.page, 0), l.x1)
    for l in body:
        kind = line_kind(l)
        cur = paras[-1] if paras else None
        if cur and cur["kind"] == kind and kind != "row" and continues(cur["lines"][-1], l, kind, right_edge):
            cur["lines"].append(l)
        else:
            paras.append({"kind": kind, "lines": [l]})
    return paras


def continues(a, b, kind, right_edge):
    if kind in ("h1", "h2"):
        return a.page == b.page and b.y0 - a.y0 < 1.6 * a.size and \
            not re.match(r"\s*([a-z]\.|\d+\.)\s", b.text + " ")
    if a.page == b.page:
        return b.y0 - a.y0 < 1.6 * a.size
    # page break: continue a paragraph whose last line runs to the margin
    first = b.text.lstrip()[:1]
    last = a.text.rstrip()
    if first.islower() or last.endswith("-"):
        return True
    full = a.x1 > right_edge[a.page] - 12
    return full and not (last[-1:] in TERMINAL and not first.islower())


def classify(paras):
    """Refine text paragraphs: bold-12 section headings and block quotes."""
    open_quote, appendix, prev = 0, False, ""
    for p in paras:
        text = " ".join(l.text for l in p["lines"]).strip()
        before, prev = prev, text
        if p["kind"] == "h1":
            appendix = text == "Appendix"
        if p["kind"] != "text":
            open_quote = 0
            continue
        chars = [c for l in p["lines"] for c in l.chars if c.c.isalnum() and c.size >= SMALL]
        italic = sum(is_italic(c) for c in chars) / max(len(chars), 1)
        bold = sum(is_bold(c) and not c.spaced for c in chars) / max(len(chars), 1)
        if bold > 0.85 and len(text) < 200 and (
                re.match(r"[a-z] ?\. [A-Z]", text) or
                # appendix sub-titles: bold and unpunctuated; the bold
                # entries of the chronology follow a date line instead
                (appendix and text[-1] not in TERMINAL and not DATE.match(before))):
            p["kind"] = "h2"
            open_quote = 0
            continue
        # a quote may mix the source's bold and italic emphasis, so count
        # letters that are either, not the larger of the two shares
        styled = sum(is_italic(c) or (is_bold(c) and not c.spaced) for c in chars) / max(len(chars), 1)
        if styled > 0.75 and (text[:1] in QUOTE_OPEN or open_quote > 0):
            p["kind"] = "quote"
            open_quote += text.count("»") - text.count("«")
            open_quote = max(open_quote, 0)
        else:
            open_quote = 0


def math_block(p, ordinals):
    page = p["lines"][0].page
    n = ordinals[page] = ordinals.get(page, -1) + 1
    if (page, n) in MATH:
        return MATH[(page, n)]
    print(f"warning: unmapped formula on page {page}: {[l.text for l in p['lines']]}", file=sys.stderr)
    return "```\n" + "\n".join(l.text.strip() for l in p["lines"]) + "\n```"


def cells(line):
    """Split at wide gaps (tab stops); returns one string per cell."""
    out, cur, prev = [], "", None
    for c in line.chars:
        if c.c.strip() and prev is not None and c.x0 - prev.x1 > CELL_GAP:
            out.append(cur)
            cur = ""
        cur += c.c
        if c.c.strip():
            prev = c
    return [s.strip() for s in out + [cur]]


def table(rows):
    grid = [cells(r) for r in rows]
    width = max(len(c) for c in grid)
    out = ["|" + "   |" * width, "|" + "---|" * width]
    for c in grid:
        c += [""] * (width - len(c))
        out.append("| " + " | ".join(escape(x).replace("|", "\\|") for x in c) + " |")
    return "\n".join(out)


# --------------------------------------------------------------------- main

def front_matter(doc):
    title_lines = [l for l in raw_lines(doc[1], 1, SMALL) if l.size >= 14]
    author = next(l.text.strip() for l in title_lines if l.size >= 15)
    title = " ".join(l.text.strip() for l in title_lines if l.size < 15)
    imprint = [l.text.strip() for l in raw_lines(doc[2], 2, SMALL)]
    imprint = imprint[next(i for i, t in enumerate(imprint) if t.startswith("©")):]
    imprint = [t for t in imprint if t and not t.isdigit()]
    return [f"# {smart_title(title)}", f"**{author}**", "  \n".join(escape(t) for t in imprint)]


def convert(pdf_path):
    doc = pymupdf.open(pdf_path)
    body, notes = extract(doc)
    vocab = build_vocab(body + [l for ls in notes.values() for l in ls])
    paras = paragraphs(body)
    classify(paras)

    blocks, chapter_notes, used = front_matter(doc), [], set()
    ordinals = {}

    def flush_notes():
        for n in chapter_notes:
            blocks.append(f"[^{n}]: " + render(join_lines(notes[n], vocab)))
        chapter_notes.clear()

    i = 0
    while i < len(paras):
        p = paras[i]
        kind = p["kind"]
        if kind == "row":
            rows = []
            while i < len(paras) and paras[i]["kind"] == "row":
                rows.extend(paras[i]["lines"])
                i += 1
            blocks.append(table(rows))
            continue
        i += 1
        if kind == "math":
            blocks.append(math_block(p, ordinals))
            continue
        toks = join_lines(p["lines"], vocab)
        for t in toks:
            if t[3] == "fn":
                n = int(t[0])
                if n in used:
                    raise SystemExit(f"duplicate footnote marker {n}")
                used.add(n)
                chapter_notes.append(n)
        if kind == "h1":
            flush_notes()
            blocks.append("# " + render(toks, headline=True))
        elif kind == "h2":
            blocks.append("## " + render(toks, headline=True))
        elif kind == "quote":
            md = "> " + block_escape(render(toks))
            if paras[i - 2]["kind"] == "quote" and blocks[-1].startswith(">"):
                blocks[-1] += "\n>\n" + md
            else:
                blocks.append(md)
        elif re.fullmatch(r"_+", "".join(t[0] for t in toks).strip()):
            blocks.append("---")  # a typed sum line under a calculation
        else:
            blocks.append(block_escape(render(toks)))
    flush_notes()

    missing = sorted(set(notes) - used)
    if missing:
        print(f"warning: footnotes without markers: {missing}", file=sys.stderr)
    unknown = sorted(used - set(notes))
    if unknown:
        print(f"warning: markers without footnotes: {unknown}", file=sys.stderr)
    return "\n\n".join(blocks) + "\n"


if __name__ == "__main__":
    src, dst = sys.argv[1:3]
    md = convert(src)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(f"wrote {dst} ({len(md):,} chars)")
