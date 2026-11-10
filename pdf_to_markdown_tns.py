"""Convert Cockshott and Cottrell's "Towards a New Socialism" from PDF to
Markdown. Shared code is in pdf_markdown_common.py. Figures are written as
PNGs to <output dir>/<output name>/figures/.

W. Paul Cockshott and Allin Cottrell, "Towards a New Socialism": a pdfTeX
print (2020) of the text of the 2000 Swedish edition. Layout facts:
  text block   x 134.1-477.9 on US letter; Computer Modern 10pt, lines
               11.95pt apart; a paragraph starts with a 15pt indent (x 149.1)
               and no extra space, except the first after a heading
  running head y 98 (page number and a slanted title); the page number of
               a chapter opening sits at y 689 instead
  headings     small caps 14.3pt = chapter (a "Chapter N" line, then the
               title); small caps 10pt = section; an italic line of its own =
               subsection. Sections and subsections are confirmed against the
               PDF outline
  quotes       9pt, indented to x 159.1 on both sides; verse is 10pt at x 159.1
  lists        "(1)", "(a)" or "•" at x 141-171, with a hanging indent
  footnotes    8pt below a 137pt rule at x 134.1, each starting with a 6pt
               number; markers are raised 7pt digits. Numbering restarts in
               every chapter, so labels here are "<chapter>-<n>" ("3-2")
  floats       "Table n.m:" and "Figure n.m:" captions sit above the float;
               figures are vector drawings with text labels, saved as PNGs
  display math centred lines; equation numbers "(3.1)" at the right margin
  glyphs       ligatures (ﬁ ﬀ ﬂ ﬃ ﬄ) and TeX accents (` ´ ˆ) set as separate
               glyphs over the letter; a word space after a ligature is lost

Usage: python pdf_to_markdown_tns.py "PDFs/TOWARDS A NEW SOCIALISM.pdf" Documents/towards_a_new_socialism.md
"""
import os
import re
import sys
import unicodedata
from collections import Counter, namedtuple

import pymupdf

from pdf_markdown_common import (Line, block_escape, build_vocab, escape, join_lines, raw_lines, render,
                                 smart_title, tokens_of)

SKIP_PAGES = {0, 4, 5, 6, 7}  # title page (read by front_matter), Contents
LEFT, INDENT, RIGHT = 134.1, 149.1, 477.9
CENTRE = (LEFT + RIGHT) / 2
HANGING = (159.1, 181.0)      # continuation lines of list items
SMALL = 7.5                   # 8pt notes and 9pt quotes are text, 7pt is not
CELL_GAP = 8                  # horizontal gap that separates table cells
LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}
ACCENTS = {"`": "̀", "´": "́", "ˆ": "̂", "¨": "̈", "˜": "̃"}
LIST_ITEM = re.compile(r"\s*(\(\w{1,3}\)|•)\s")
EQNO = re.compile(r"\(\d+\.\d+\)\s*$")
CAPTION = re.compile(r"\s*(Table|Figure) (\d+)\.(\d+):")

# Displays that line-by-line rendering garbles (stacked fractions, sums),
# keyed by (page, n-th display on the page); hand-made Markdown tables, keyed
# by table number.
MATH = {
    (46, 2): "(1 + R<sub>0</sub>SP + R<sub>0</sub><sup>2</sup>SP<sup>2</sup> + R<sub>0</sub><sup>3</sup>SP<sup>3</sup>"
             " + · · · + R<sub>0</sub><sup>*n*</sup>SP<sup>*n*</sup>)TH<sub>0</sub>.",
    (46, 3): "R<sub>*f*</sub> = (1−R<sub>0</sub>SP)<sup>−1</sup>TH<sub>0</sub>/AH.D.",
    # the second and third lines overlap (u², √u) and are read as one
    (91, 0): "Let *u* = (output − goal)/goal.<br>\n"
             "If *u* < 0 then harmony = −*u*<sup>2</sup>,<br>\n"
             "otherwise harmony = √*u*.",
    # single equations that the book breaks over two lines
    (104, 0): "Net Savings = (Retirement Asset Acquisition − Retirement Asset Disbursement)"
              " + (Saving Deposit Acquisition − Withdrawals − New Credit).",
    (130, 0): "total labour = (cars × German labour per car) + (blouses × German labour per blouse)",
    (130, 1): "total labour = (cars × Chinese labour per car) + (blouses × Chinese labour per blouse)",
}
TABLES = {
    # four panels: c and s down the left, v and the value flows on the right
    "1.1": """**Calculation of** *c*

| Intermediate consumption | £M |
|---|---:|
| total UK | 812757 |
| *less* |  |
| public administration | 2757 |
| financial intermediation | 229221 |
| total unproductive costs | 231978 |
| *leaving* |  |
| productive consumption | 580779 |
| fixed capital consumption | 85834 |
| *c* Total value of means of production consumed | **666613** |

**Calculation of** *v*

| Compensation of employees | £M |
|---|---:|
| total UK | 432388 |
| *less* |  |
| public administration | 33026 |
| financial intermediation | 75038 |
| total unproductive wages | 108064 |
| *leaving* |  |
| *v* productive wages | **324324** |

**Calculation of** *s*

| Net tax on production | £M |
|---|---:|
| Total UK | 17048 |
| *less* |  |
| Public administration | 837 |
| Financial intermediation | 304 |
| *leaving* |  |
| Productive sector tax | 13207 |
| Gross operating surplus |  |
| total UK | 264178 |
| *less* |  |
| Public administration | 4977 |
| Financial intermediation | 106121 |
| *leaving* |  |
| Productive sector surplus | 153080 |
| Total unproductive costs | 231978 |
| Total surplus *s* | **316272** |

**Value flows**

|  | £M |
|---|---:|
| *c* | 666613 |
| *v* | 324324 |
| *s* | 316272 |
| gross value product: *c* + *v* + *s* | 1307209 |
| net value product: *v* + *s* | 640596 |
| rate of exploitation: *s*/*v* | **98%** |""",
}

# Inline maths that the line-by-line rendering garbles: exact replacements in
# the finished Markdown, each of which must match exactly once.
TEXT_FIXES = {
    # p. iv: the preface is signed on four lines, two for each author
    " Paul Cockshott Glasgow, Scotland, July 2000 Allin Cottrell Winston-Salem, North Carolina, July 2000\n":
    "\n\nPaul Cockshott<br>\nGlasgow, Scotland, July 2000\n\n"
    "Allin Cottrell<br>\nWinston-Salem, North Carolina, July 2000\n",
    # p. 109: the PDF itself prints a LaTeX label, "conc1", as a section (also
    # in its Contents) after "Conclusion". An editorial fix, not a conversion one
    "## Conclusion\n\n## conc1\n\n": "## Conclusion\n\n",
    # p. 15: s/v and 4,000/2,000 are set as stacked fractions
    "ratio *<sub>v</sub><sup>s</sup>*.": "ratio *s*/*v*.",
    "be *<sub>v</sub><sup>s</sup>* = <sup>4</sup><sub>2</sub>*<sup>,</sup><sub>,</sub>*<sup>0</sup><sub>0</sub>"
    "<sup>0</sup><sub>0</sub><sup>0</sup><sub>0</sub> or 200%.": "be *s*/*v* = 4,000/2,000 or 200%.",
    # p. 39 and p. 76 (a note): an exponent of −1
    "(1-R<sub>0</sub>SP)*<sup>−</sup>*<sup>1</sup>TH": "(1-R<sub>0</sub>SP)<sup>−1</sup>TH",
    "(I − A)<sup>−</sup>*<sup>1</sup>*f*": "(I − A)<sup>−1</sup>f*",
    # p. 47, note 3 of chapter 3: an array of equations
    "of the form: *L*<sub>1</sub> + *I*<sub>11</sub>*v*<sub>1</sub> + *I*<sub>12</sub>*v*<sub>2</sub> + "
    "*I*<sub>13</sub>*v*<sub>3</sub> + · · · + *I*<sub>1</sub>*<sub>n</sub>v<sub>n</sub> = Q*<sub>1</sub>"
    "*v*<sub>1</sub> *L*<sub>2</sub> + *I*<sub>21</sub>*v*<sub>1</sub> + *I*<sub>22</sub>*v*<sub>2</sub> + "
    "*I*<sub>23</sub>*v*<sub>3</sub> + · · · + *I*<sub>2</sub>*<sub>n</sub>v<sub>N</sub> = Q*<sub>2</sub>"
    "*v*<sub>2</sub> · · · *L<sub>n</sub> + I<sub>n</sub>*<sub>1</sub>*v*<sub>1</sub> + *I<sub>n</sub>*<sub>2</sub>"
    "*v*<sub>2</sub> + *I<sub>n</sub>*<sub>3</sub>*v*<sub>3</sub> + · · · + *I<sub>nn</sub>v<sub>n</sub> = "
    "Q<sub>n</sub>v<sub>n</sub>* where":
    "of the form:<br>\n"
    "*L*<sub>1</sub> + *I*<sub>11</sub>*v*<sub>1</sub> + *I*<sub>12</sub>*v*<sub>2</sub> + *I*<sub>13</sub>*v*<sub>3</sub>"
    " + · · · + *I*<sub>1*n*</sub>*v*<sub>*n*</sub> = *Q*<sub>1</sub>*v*<sub>1</sub><br>\n"
    "*L*<sub>2</sub> + *I*<sub>21</sub>*v*<sub>1</sub> + *I*<sub>22</sub>*v*<sub>2</sub> + *I*<sub>23</sub>*v*<sub>3</sub>"
    " + · · · + *I*<sub>2*n*</sub>*v*<sub>*N*</sub> = *Q*<sub>2</sub>*v*<sub>2</sub><br>\n"
    "· · ·<br>\n"
    "*L*<sub>*n*</sub> + *I*<sub>*n*1</sub>*v*<sub>1</sub> + *I*<sub>*n*2</sub>*v*<sub>2</sub> + *I*<sub>*n*3</sub>*v*<sub>3</sub>"
    " + · · · + *I*<sub>*nn*</sub>*v*<sub>*n*</sub> = *Q*<sub>*n*</sub>*v*<sub>*n*</sub><br>\n"
    "where",
}

Block = namedtuple("Block", "page y0 md")


def clean_chars(chars):
    """Expand ligatures, put accents on their letters, restore lost spaces."""
    chars = [c._replace(c=LIGATURES.get(c.c, c.c)) for c in chars]
    drop = set()
    for i, c in enumerate(chars):
        if c.c not in ACCENTS:
            continue
        mid = (c.x0 + c.x1) / 2  # the accent sits over the letter before or after it
        for j in (i - 1, i + 1):
            if 0 <= j < len(chars) and chars[j].c.isalpha() and chars[j].x0 - 1 <= mid <= chars[j].x1 + 1:
                chars[j] = chars[j]._replace(c=unicodedata.normalize("NFC", chars[j].c + ACCENTS[c.c]))
                drop.add(i)
                break
    out = []
    for i, c in enumerate(chars):
        if i in drop:
            continue
        if out and c.c.strip() and out[-1].c.strip() and c.x0 - out[-1].x1 > 0.15 * max(c.size, out[-1].size):
            out.append(out[-1]._replace(c=" ", x0=out[-1].x1, x1=c.x0))
        out.append(c)
    # "2,000" set in maths mode has a space after the comma
    return [c for i, c in enumerate(out)
            if not (c.c == " " and 0 < i < len(out) - 1 and out[i - 1].c == ","
                    and "CMMI" in out[i - 1].font and out[i + 1].c.isdigit())]


def overlapping(line):
    """True if the line's letters overlap: two lines of a display read as one."""
    cs = [c for c in line.chars if c.c.strip()]
    return sum(b.x0 < a.x1 - 1 and b.x0 < a.x1 - 0.5 * min(a.x1 - a.x0, b.x1 - b.x0)
               for a, b in zip(cs, cs[1:])) >= 2


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def is_page_number(text):
    return re.fullmatch(r"\s*([0-9]+|[ivxlc]+)\s*", text) is not None


def footnote_rule(page):
    """y of the footnote rule, or None."""
    for d in page.get_drawings():
        r = d["rect"]
        if r.height < 1 and abs(r.x0 - LEFT) < 1 and 130 < r.width < 145:
            return r.y0
    return None


def extract(doc):
    """Return (body lines, {label: [note lines]}, {(page, n): label})."""
    body, notes, starts = [], {}, {}
    chapter, last, title_page = "front", None, None
    for pno in range(len(doc)):
        if pno in SKIP_PAGES:
            continue
        page = doc[pno]
        lines = [l for l in raw_lines(page, pno, SMALL, clean_chars)
                 if 110 < l.y0 and not (l.y0 > 680 and is_page_number(l.text))]
        rule = footnote_rule(page)
        for l in lines:
            # Only the first large line of a page names the chapter: the rest
            # is its title, which can run over two lines ("... Budgetary / Policy")
            if l.size >= 13 and pno != title_page:
                m = re.match(r"\s*Chapter (\d+)", l.text)
                chapter = m.group(1) if m else norm(l.text.split()[0])
                title_page = pno
            if rule is None or l.y0 < rule:
                body.append(l)
                continue
            first = next(c for c in l.chars if c.c.strip())
            if first.size < SMALL and first.c.isdigit():
                digits = ""
                for c in l.chars:
                    if c.c.strip() and not (c.size < SMALL and c.c.isdigit()):
                        break
                    digits += c.c
                last = f"{chapter}-{int(digits)}"
                starts[(pno, int(digits))] = last
                l.chars = l.chars[len(digits):]
                notes[last] = [l]
            else:  # continuation of the previous note, possibly from the previous page
                notes[last].append(l)
    return body, notes, starts


# ----------------------------------------------------------- tables, figures

def cells(line):
    """[[chars]] of one table row, split at wide gaps."""
    out, prev = [[]], None
    for c in line.chars:
        if c.c.strip() and prev is not None and c.x0 - prev.x1 > CELL_GAP:
            out.append([])
        out[-1].append(c)
        if c.c.strip():
            prev = c
    return [cell for cell in out if any(c.c.strip() for c in cell)]


def table(rows, fn):
    """A GFM table from visual rows, with columns found from the fullest rows."""
    grid = [[Line(cell, row.page, row.small) for cell in cells(row)] for row in rows]
    width = max(len(r) for r in grid)
    cols = []
    for r in grid:
        if len(r) == width:
            for i, cell in enumerate(r):
                if i == len(cols):
                    cols.append([cell.x0, cell.x1])
                cols[i] = [min(cols[i][0], cell.x0), max(cols[i][1], cell.x1)]
    out = ["|" + "   |" * width, "|" + "---|" * width]
    for r in grid:
        row = [""] * width
        for cell in r:
            def fit(i):  # overlap with column i, then nearness of the centres
                overlap = min(cell.x1, cols[i][1]) - max(cell.x0, cols[i][0])
                return overlap, -abs((cell.x0 + cell.x1) - sum(cols[i]))
            i = max(range(width), key=fit)
            md = render(tokens_of(cell, fn)).replace("|", "\\|")
            row[i] = f"{row[i]} {md}".strip()
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def cluster(rects, y, direction, gap=30):
    """The drawings that run on from `y` (down if direction is 1, up if -1)
    without a vertical gap wider than `gap`: one figure, not the rule of a
    square root in the text after it. The first may sit further off, below
    the figure's top labels."""
    out, edge = [], y
    for r in sorted(rects, key=lambda r: r.y0 if direction == 1 else -r.y1):
        near = r.y0 - edge if direction == 1 else edge - r.y1
        if near > (gap if out else 2 * gap):
            break
        out.append(r)
        edge = max(edge, r.y1) if direction == 1 else min(edge, r.y0)
    return out


def extract_floats(doc, body, fn, fig_dir, fig_rel):
    """Replace each table and figure, with its caption, by a Block."""
    pages = {}
    for l in body:
        pages.setdefault(l.page, []).append(l)
    out = []
    for pno, lines in pages.items():
        page = doc[pno]
        draws = [d["rect"] for d in page.get_drawings()
                 if not (abs(d["rect"].x0 - LEFT) < 1 and d["rect"].width > 130)]  # footnote rule
        caps = [i for i, l in enumerate(lines)
                if CAPTION.match(l.text) and abs((l.x0 + l.x1) / 2 - CENTRE) < 20]

        def body_like(l):  # a table row has wide gaps, a line of text does not
            return l.size >= 9.5 and min(abs(l.x0 - LEFT), abs(l.x0 - INDENT)) < 1                 and len(cells(l)) == 1

        floats = {}  # index of first line -> (caption index, member indices, drawings)
        for n, i in enumerate(caps):
            cap = lines[i]
            lo = lines[caps[n - 1]].y1 if n else 0
            hi = lines[caps[n + 1]].y0 if n + 1 < len(caps) else 10_000
            below = cluster([r for r in draws if r.y0 > cap.y1 and r.y1 < hi], cap.y1, 1)
            above = cluster([r for r in draws if r.y1 < cap.y0 and r.y0 > lo], cap.y0, -1)
            if CAPTION.match(cap.text).group(1) == "Figure" and above and not below:
                top = min(r.y0 for r in above)  # caption under the figure
                k = i
                while k > 0 and lines[k - 1].y0 > lo and (lines[k - 1].y0 > top - 2 or
                                                           (lines[k - 1].y0 > top - 14 and not body_like(lines[k - 1]))):
                    k -= 1
                floats[k] = (i, list(range(k, i + 1)), above)
                continue
            bottom = max((r.y1 for r in below), default=cap.y1)
            k = i + 1
            while k < len(lines) and k not in caps:
                if lines[k].y0 > bottom + 2 and body_like(lines[k]):
                    break
                k += 1
            floats[i] = (i, list(range(i, k)), below)
        skip = set()
        for i, l in enumerate(lines):
            if i in floats:
                c, members, fdraws = floats[i]
                skip.update(members)
                out.append(Block(pno, l.y0, render_float(page, lines[c], [lines[m] for m in members if m != c],
                                                      fdraws, fn, fig_dir, fig_rel)))
            elif i not in skip:
                out.append(l)
    return out


def render_float(page, cap, content, draws, fn, fig_dir, fig_rel):
    kind, a, b = CAPTION.match(cap.text).groups()
    notes = []  # notes under the float: 8pt lines ("Source: ...", bullets)
    while content and content[-1].size < 9 and content[-1].y0 > cap.y0:
        notes.insert(0, content.pop())
    md = [render(tokens_of(cap, fn))]
    if kind == "Table":
        md.append(TABLES.get(f"{a}.{b}") or table(content, fn))
    else:
        rects = [pymupdf.Rect(l.x0, l.y0, l.x1, l.y1) for l in content] + draws
        if min(r.y0 for r in rects) > cap.y0:  # figure under its caption
            top, bottom = max(cap.y1 + 0.5, min(r.y0 for r in rects) - 4), max(r.y1 for r in rects) + 4
        else:
            top, bottom = min(r.y0 for r in rects) - 4, cap.y0 - 2
        clip = pymupdf.Rect(min(r.x0 for r in rects) - 4, top, max(r.x1 for r in rects) + 4, bottom)
        name = f"figure-{a}-{b}.png"
        os.makedirs(fig_dir, exist_ok=True)
        page.get_pixmap(clip=clip, dpi=200).save(os.path.join(fig_dir, name))
        md.append(f"![{escape(cap.text.strip())}]({fig_rel}/{name})")
    para = []
    for l in notes:
        if para and (l.text.lstrip().startswith("•") or l.x0 < para[-1].x0 - 5):
            md.append(note_para(para, fn))
            para = []
        para.append(l)
    if para:
        md.append(note_para(para, fn))
    return "\n\n".join(md)


def note_para(lines, fn):
    md = render(join_lines(lines, VOCAB, fn))
    return "- " + md.lstrip("• ") if md.startswith("•") else block_escape(md)


# --------------------------------------------------------------- paragraphs

def outline(doc):
    """{(page, normalised title): heading level} for sections and subsections."""
    toc = {(1, norm("About this book")): 2}
    for level, title, page in doc.get_toc():
        if level > 1:
            toc[(page - 1, norm(title))] = level
    return toc


def line_kind(l, toc):
    if isinstance(l, Block):
        return "block"
    t = l.text.strip()
    if l.size >= 13:
        return "h1"
    level = toc.get((l.page, norm(t)))
    if level:
        return f"h{level}"
    if all("CMCSC" in c.font for c in l.chars if c.c.strip()):
        return "h2"  # a section heading that differs from the outline
    eq = EQNO.search(t)
    if eq and l.chars[-1].x0 > 440:
        return "eqno" if eq.start() == 0 else "display"
    if LIST_ITEM.match(l.text) and LEFT + 3 < l.x0 < 175 and l.size >= 9.5:
        return "item"
    if 8.5 <= l.size < 9.5 and l.x0 > LEFT + 20:
        return "quote"
    if l.size >= 9.5 and abs(l.x0 - HANGING[0]) < 1 and l.x1 < RIGHT - 3:
        return "verse"
    standard = (LEFT, INDENT) + HANGING
    if l.size >= 9.5 and l.x1 < RIGHT - 1 and abs((l.x0 + l.x1) / 2 - CENTRE) < 15 \
            and min(abs(l.x0 - x) for x in standard) > 1:
        return "display"
    return "text"


def paragraphs(body, toc):
    paras, refs = [], False  # dicts: kind, lines (+ level, joined)
    for l in body:
        kind = line_kind(l, toc)
        if refs and kind != "h1":
            kind = "text"  # entries have a hanging indent: their later lines are not verse
        cur = paras[-1] if paras else None
        if cur and cur["kind"] == "item" and kind in ("text", "verse", "display") and l.x0 > INDENT + 5:
            if cur["level"] == 1 and l.x0 < HANGING[1] - 5 and not cur.get("cont"):
                # back at the outer item's indent: a new paragraph of that item
                paras.append({"kind": "item", "lines": [l], "level": 0, "cont": True})
                continue
            cur["lines"].append(l)  # continuation of a list item
            continue
        if kind == "h1":
            refs = norm(l.text) == "references"
            if cur and cur["kind"] == "h1" and cur["lines"][-1].page == l.page:
                cur["lines"].append(l)
                continue
        elif kind in ("h2", "h3"):
            if cur and cur["kind"] == kind and cur["lines"][-1].page == l.page                     and l.y0 - cur["lines"][-1].y0 < 1.6 * l.size:
                cur["lines"].append(l)
                continue
        elif kind in ("display", "eqno"):
            if cur and cur["kind"] == "display" and cur["lines"][-1].page == l.page \
                    and l.y0 - cur["lines"][-1].y1 < 25:
                cur["lines"].append(l)
                continue
            kind = "display"
        elif kind == "verse":
            if cur and cur["kind"] == "verse":
                cur["lines"].append(l)
                continue
        elif kind == "quote":
            if cur and cur["kind"] == "quote":
                prev = cur["lines"][-1]
                close = prev.page != l.page or l.y0 - prev.y0 < 1.6 * l.size
                if close and l.x0 < cur["lines"][0].x0 + 5:
                    cur["lines"].append(l)
                    continue
                paras.append({"kind": kind, "lines": [l], "joined": close})
                continue
        elif kind == "text":
            indented = abs(l.x0 - INDENT) < 1 or (refs and l.x0 < LEFT + 3)
            # a float may interrupt a paragraph; the paragraph then goes on
            # after it, and the float follows the whole paragraph
            last = next((p for p in reversed(paras) if p["kind"] != "block"), None)
            if not indented and last and last["kind"] == "text" and \
                    all(p["kind"] == "block" for p in paras[paras.index(last) + 1:]):
                last["lines"].append(l)
                continue
        para = {"kind": kind, "lines": [l]}
        if kind == "item":
            para["level"] = 0 if l.x0 < INDENT else 1
        paras.append(para)
    return paras


# --------------------------------------------------------------------- main

def front_matter(doc):
    lines = [l for b in doc[0].get_text("dict")["blocks"] for l in b.get("lines", [])]
    def words(big):
        return " ".join(re.sub(r"(?<=\S) (?=\S)", "", "".join(s["text"] for s in l["spans"]))
                        for l in lines if (l["spans"][0]["size"] > 20) == big)
    return [f"# {smart_title(words(True))}", f"**{smart_title(words(False))}**"]


VOCAB = Counter()


def convert(doc, dst):
    global VOCAB
    body, notes, starts = extract(doc)
    VOCAB = build_vocab(body + [l for ls in notes.values() for l in ls])
    vocab = VOCAB

    def fn(line, digits):
        return starts.get((line.page, int(digits)))

    slug = os.path.splitext(os.path.basename(dst))[0]
    body = extract_floats(doc, body, fn, os.path.join(os.path.dirname(dst), slug, "figures"), f"{slug}/figures")
    paras = paragraphs(body, outline(doc))

    blocks, chapter_notes, ordinals = front_matter(doc), [], {}

    def add(md):
        blocks.append(md)
        chapter_notes.extend(n for n in re.findall(r"\[\^([\w-]+)\]", md) if n not in chapter_notes)

    def flush_notes():
        for n in chapter_notes:
            if n in notes:
                blocks.append(f"[^{n}]: " + render(join_lines(notes[n], vocab, fn)))
        chapter_notes.clear()

    def heading(lines):
        toks = join_lines(lines, vocab, fn)
        for t in toks:
            t[1] = False  # subsection headings are set in italic
        return render(toks, headline=True)

    for i, p in enumerate(paras):
        kind, lines = p["kind"], p["lines"]
        if kind == "block":
            add(lines[0].md)
        elif kind == "h1":
            flush_notes()
            title = [heading([l]) for l in lines]
            add("# " + (f"{title[0]}. {' '.join(title[1:])}" if len(title) > 1 else title[0]))
        elif kind in ("h2", "h3"):
            add("#" * int(kind[1]) + " " + heading(lines))
        elif kind == "item":
            md = render(join_lines(lines, vocab, fn))
            if p.get("cont"):  # a further paragraph of the item above
                md = "\n  " + block_escape(md)
            else:
                md = ("  " * p["level"]) + "- " + (md[1:].lstrip() if md.startswith("•") else md)
            if i and paras[i - 1]["kind"] == "item":
                blocks[-1] += "\n" + md
                chapter_notes.extend(re.findall(r"\[\^([\w-]+)\]", md))
            else:
                add(md)
        elif kind == "quote":
            md = "> " + block_escape(render(join_lines(lines, vocab, fn)))
            if p.get("joined") and blocks[-1].startswith(">"):
                blocks[-1] += "\n>\n" + md
                chapter_notes.extend(re.findall(r"\[\^([\w-]+)\]", md))
            else:
                add(md)
        elif kind == "verse":
            add("<br>\n".join("> " + block_escape(render(tokens_of(l, fn))) for l in lines))
        elif kind == "display":
            page = lines[0].page
            n = ordinals[page] = ordinals.get(page, -1) + 1
            if (page, n) in MATH:
                add(MATH[(page, n)])
                continue
            rows = []
            for l in lines:
                row = block_escape(render(tokens_of(l, fn)))
                eq = EQNO.search(row)
                if eq and not row[:eq.start()].strip():  # a number on a line of its own
                    if rows:
                        rows[-1] += " " + eq.group(0).strip()
                    else:  # the number of an equation that was set as text
                        print(f"warning: equation number {row} on page {page} has no display", file=sys.stderr)
                        blocks[-1] += " " + eq.group(0).strip()
                    continue
                rows.append(row)
            if not rows:
                continue
            for j in range(len(rows) - 1):  # "a = b (3.2)" / "= c": the number goes last
                eq = EQNO.search(rows[j])
                if eq and rows[j + 1].lstrip("\\ ").startswith("="):
                    rows[j] = rows[j][:eq.start()].rstrip()
                    rows[j + 1] += " " + eq.group(0).strip()
            if any(l.size < 9.5 or overlapping(l) for l in lines):
                print(f"warning: display on page {page} (#{n}) may be garbled: {rows}", file=sys.stderr)
            add("<br>\n".join(rows))
        else:
            add(block_escape(render(join_lines(lines, vocab, fn))))
    flush_notes()

    md = "\n\n".join(blocks) + "\n"
    for old, new in TEXT_FIXES.items():
        if md.count(old) != 1:
            print(f"warning: text fix matches {md.count(old)} times: {old[:60]}", file=sys.stderr)
        md = md.replace(old, new)

    used = set(re.findall(r"\[\^([\w-]+)\](?!:)", md))
    missing = sorted(set(notes) - used)
    if missing:
        print(f"warning: footnotes without markers: {missing}", file=sys.stderr)
    unknown = sorted(used - set(notes))
    if unknown:
        print(f"warning: markers without footnotes: {unknown}", file=sys.stderr)
    return md

if __name__ == "__main__":
    src, dst = sys.argv[1:3]
    md = convert(pymupdf.open(src), dst)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(f"wrote {dst} ({len(md):,} chars)")
