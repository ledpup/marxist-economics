"""Convert a book PDF to Markdown using PyMuPDF.

Two PDFs are supported, each with its own layout code; the book is told
apart by its title page:
  - the GIC's "Fundamental Principles of Communist Production and
    Distribution" (layout facts below; convert())
  - Cockshott and Cottrell's "Towards a New Socialism" (layout facts at the
    head of its section; convert_tns()). Its figures are written as PNGs to
    <output dir>/<output name>/figures/

The tokenising, dehyphenation and rendering code is shared.

GIC layout facts the converter relies on (found by inspecting the PDF):
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

Usage: python pdf_to_markdown.py input.pdf output.md
"""
import os
import re
import sys
import unicodedata
from collections import Counter, namedtuple

import pymupdf
from spellchecker import SpellChecker

ENGLISH = SpellChecker(distance=1)

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
TIGHT_SPACE = 2.45   # space advance below this = letter-spacing, not a word gap
CELL_GAP = 15        # horizontal gap that separates table cells
QUOTE_OPEN = "»“„\""
TERMINAL = ".!?:«\"”"
FRACTIONS = {("1", "2"): "½", ("1", "4"): "¼", ("3", "4"): "¾", ("1", "3"): "⅓", ("2", "3"): "⅔"}
KEEP_HYPHEN_PREFIXES = {"self", "non", "anti", "semi", "quasi", "pseudo", "half", "well"}
DATE = re.compile(r"(\d{1,2} )?[A-Z][a-z]+( \d{1,2},)? \d{4}$")

Char = namedtuple("Char", "c x0 y0 x1 y1 font size flags spaced under")


class Line:
    def __init__(self, chars, page):
        self.chars = sorted(chars, key=lambda c: c.x0)
        self.page = page
        main = [c for c in self.chars if c.size >= SMALL and c.c.strip()] or \
            [c for c in self.chars if c.c.strip()]
        self.y0 = min(c.y0 for c in main)
        self.y1 = max(c.y1 for c in main)
        self.x0 = min(c.x0 for c in main)
        self.x1 = max(c.x1 for c in main)
        self.size = Counter(round(c.size, 1) for c in main).most_common(1)[0][0]
        self.text = "".join(c.c for c in self.chars)
        letters = [c for c in main if c.c.isalnum()]
        self.bold = sum(is_bold(c) for c in letters) / max(len(letters), 1)
        self.math = any("CambriaMath" in c.font for c in self.chars)

    def cells(self):
        """Split at wide gaps (tab stops); returns one string per cell."""
        out, cur, prev = [], "", None
        for c in self.chars:
            if c.c.strip() and prev is not None and c.x0 - prev.x1 > CELL_GAP:
                out.append(cur)
                cur = ""
            cur += c.c
            if c.c.strip():
                prev = c
        return [s.strip() for s in out + [cur]]


def is_italic(c):
    return "Italic" in c.font or bool(c.flags & 2)


def is_bold(c):
    return "Bold" in c.font or bool(c.flags & 16) or c.spaced


# ----------------------------------------------------------------- extraction

def raw_lines(page, pno, clean=None):
    """Visual lines of a page, with spans on the same baseline merged.

    `clean`, if given, fixes up each merged line's characters (sorted by x)
    before letter-spacing is collapsed."""
    # underlines are thin filled rectangles ~2pt above the bottom of the text
    rules = [d["rect"] for d in page.get_drawings() if d["rect"].height < 1.2]

    def underlined(bbox, size):
        x, y1 = (bbox[0] + bbox[2]) / 2, bbox[3]
        return size >= SMALL and any(r.x0 <= x <= r.x1 and y1 - 4 <= r.y0 <= y1 + 1 for r in rules)

    rows = []
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            chars = [Char(ch["c"], *ch["bbox"], s["font"], s["size"], s["flags"], False,
                          underlined(ch["bbox"], s["size"]))
                     for s in l["spans"] for ch in s["chars"]]
            if not any(c.c.strip() for c in chars):
                continue
            line = Line(chars, pno)
            for row in rows:
                overlap = min(row.y1, line.y1) - max(row.y0, line.y0)
                if overlap > 0.5 * min(row.y1 - row.y0, line.y1 - line.y0):
                    rows[rows.index(row)] = Line(row.chars + line.chars, pno)
                    break
            else:
                rows.append(line)
    rows.sort(key=lambda r: r.y0)
    if clean:
        rows = [Line(clean(r.chars), pno) for r in rows]
    return [Line(despace(r.chars), pno) for r in rows]


def despace(chars):
    """Collapse letter-spaced runs ("T h e  p r i c e") and flag them."""
    n = len(chars)
    tight = [i for i in range(1, n - 1)
             if chars[i].c == " " and chars[i - 1].c != " " and chars[i + 1].c != " "
             and chars[i].size >= 10 and chars[i + 1].x0 - chars[i].x0 < TIGHT_SPACE]
    drop, spaced = set(), set()
    def edge(i):  # outside the line, a space or punctuation
        return i < 0 or i >= n or not chars[i].c.isalnum()

    # group tight spaces into runs that join single characters; the run must
    # start and end on word boundaries ("from a social" is not letter-spaced)
    run = []
    for i in tight + [None]:
        if run and (i is None or i != run[-1] + 2):
            if edge(run[0] - 2) and edge(run[-1] + 2):
                drop.update(run)
                spaced.update(range(run[0] - 1, run[-1] + 2))
            run = []
        if i is not None:
            run.append(i)
    return [c._replace(spaced=i in spaced) for i, c in enumerate(chars) if i not in drop]


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
        lines = [l for l in raw_lines(page, pno)
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


# ------------------------------------------------------------------- tokens
# A token is [text, italic, bold, kind]; kind is "t" (text), "fn" (marker),
# "sub" or "sup".

def tokens_of(line, fn_label=None):
    """`fn_label(line, digits)`, if given, returns the label of the footnote
    a raised number refers to, or None if the number is a plain superscript."""
    toks = []
    main_y1 = line.y1
    for c in line.chars:
        if c.size < SMALL and c.c.strip():
            sup = bool(c.flags & 1) or c.y1 < main_y1 - 2
            kind = "fn" if sup and c.c.isdigit() else ("sup" if sup else "sub")
        else:
            kind = "t"
        style = [is_italic(c), is_bold(c), kind, c.under]
        if toks and toks[-1][1:] == style:
            toks[-1][0] += c.c
        else:
            toks.append([c.c] + style)
    # a raised digit, a slash and a lowered digit form a fraction ("1¼")
    for i in range(len(toks) - 2):
        a, s, b = toks[i:i + 3]
        if a[3] == "fn" and s[0] in "/⁄" and b[3] == "sub" and b[0].isdigit():
            frac = FRACTIONS.get((a[0], b[0]), f" {a[0]}/{b[0]}")
            toks[i:i + 3] = [[frac, s[1], s[2], "t", s[4]], ["", *s[1:3], "t", s[4]], ["", *s[1:3], "t", s[4]]]
    if fn_label:
        for t in toks:
            if t[3] == "fn":
                label = fn_label(line, t[0])
                if label:
                    t[0] = label
                else:
                    t[3] = "sup"
    return [t for t in toks if t[0]]


def build_vocab(lines):
    vocab = Counter()
    for l in lines:
        # the last word of a line may be a hyphenation fragment
        for w in re.findall(r"[\w'-]+", l.text)[:-1]:
            vocab[w.lower().strip("-")] += 1
    return vocab


def join_lines(lines, vocab, fn_label=None):
    """Concatenate line tokens, fixing words hyphenated across lines."""
    toks = []
    for line in lines:
        new = tokens_of(line, fn_label)
        while new and not new[0][0].strip():
            new.pop(0)
        if not new:
            continue
        if toks:
            while not toks[-1][0].strip():
                toks.pop()
            toks[-1][0] = toks[-1][0].rstrip()
            new[0][0] = new[0][0].lstrip()
            left, right = toks[-1][0], new[0][0]
            if toks[-1][3] == "t" and re.search(r"\w-$", left) and re.match(r"\w", right):
                if dehyphenate(left, right, vocab):
                    toks[-1][0] = left[:-1]
                # else: genuine hyphen, join without a space
            else:
                toks.append([" ", None, None, "t", None])
        toks.extend(new)
    return toks


def dehyphenate(left, right, vocab):
    """True if the hyphen at the end of `left` is a line-break hyphen.

    Decided by the book's own vocabulary first, then an English word list:
    "head-|quarters" joins, "revolutionary-|democratic" keeps its hyphen."""
    m1 = re.search(r"([\w'-]*\w)-$", left)
    m2 = re.match(r"[\w'-]*\w", right)
    if not (m1 and m2):
        return False
    a, b = m1.group(1), m2.group(0)
    if a[-1].isdigit() or b[0].isdigit() or b[0].isupper():
        return False
    joined, hyph = (a + b).lower(), (a + "-" + b).lower()
    if vocab[joined]:
        return vocab[joined] >= vocab[hyph]
    if vocab[hyph]:
        return False
    a_last, b_first = a.split("-")[-1].lower(), b.split("-")[0].lower()
    if ENGLISH.known([a_last + b_first]):
        return True
    if a_last in KEEP_HYPHEN_PREFIXES:
        return False
    # two complete words on either side of the break: a genuine compound
    return not (len(a_last) > 2 and len(b_first) > 2 and len(ENGLISH.known([a_last, b_first])) == 2)


# ---------------------------------------------------------------- rendering

def escape(s):
    s = s.replace("\\", "\\\\")
    s = re.sub(r"([*_\[\]`])", r"\\\1", s)
    return re.sub(r"<(?=[A-Za-z/!])", "&lt;", s)


def render(toks, headline=False):
    toks = [list(t) for t in toks]
    # collapse runs of spaces across token boundaries
    out, prev_space = [], True
    for t in toks:
        if t[3] == "t":
            t[0] = re.sub(r"\s+", " ", t[0])
            if prev_space:
                t[0] = t[0].lstrip(" ")
            if not t[0]:
                continue
            prev_space = t[0].endswith(" ")
        else:
            prev_space = False
        out.append(t)
    toks = out
    while toks and toks[-1][3] == "t" and not toks[-1][0].strip():
        toks.pop()
    if toks and toks[-1][3] == "t":
        toks[-1][0] = toks[-1][0].rstrip()

    items = []  # [markdown, italic, bold, underline]; None = takes its neighbours' style
    for text, it, bo, kind, un in toks:
        if kind == "fn":
            if items and not items[-1][0].strip():
                items.pop()  # attach the marker to the preceding word
            elif items:
                items[-1][0] = items[-1][0].rstrip()
            items.append([f"[^{text}]", None, None, None])
        elif kind in ("sub", "sup"):
            items.append([f"<{kind}>{escape(text)}</{kind}>", it, bo, un])
        else:
            # punctuation at the edges of a styled run takes the style of its
            # neighbours only when they agree, so emphasis markers always sit
            # next to letters ("**word**. *Next*", not "**word***. Next*")
            lead, core, trail = re.match(r"(\W*)(.*?)(\W*)$", text, re.S).groups()
            if lead:
                items.append([escape(lead), None, None, None])
            if core:
                items.append([escape(core), it, bo and not headline, un])
            if trail:
                items.append([escape(trail), None, None, None])
    for attr in (1, 2, 3):
        for i, item in enumerate(items):
            if item[attr] is None:
                before = next((x[attr] for x in reversed(items[:i]) if x[attr] is not None), False)
                after = next((x[attr] for x in items[i + 1:] if x[attr] is not None), False)
                item[attr] = before and after
    def styled(group, attr, opening, closing):
        return "".join(wrap(text(sub, attr + 1), opening, closing) if on else text(sub, attr + 1)
                       for on, sub in groupby(group, attr))

    def text(group, attr):  # italic outermost, then bold, then underline
        if attr == 1:
            return styled(group, 1, "*", "*")
        if attr == 2:
            return styled(group, 2, "**", "**")
        if attr == 3:
            return styled(group, 3, "<ins>", "</ins>")
        return "".join(x[0] for x in group)

    md = text(items, 1)
    # "F t" -> "Ft": a one-letter variable and its index
    return re.sub(r"\b([A-Za-z]'?) (<sub>)", r"\1\2", md)


def groupby(items, attr):
    out = []
    for x in items:
        if out and out[-1][0] == x[attr]:
            out[-1][1].append(x)
        else:
            out.append((x[attr], [x]))
    return out


def wrap(s, opening, closing):
    core = s.strip()
    if not core:
        return s
    lead, trail = s[:len(s) - len(s.lstrip())], s[len(s.rstrip()):]
    return f"{lead}{opening}{core}{closing}{trail}"


def block_escape(md):
    """Stop paragraph text from being read as a heading, quote or list."""
    if re.match(r"(#|>|[-+=] |\d+[.)] )", md):
        md = re.sub(r"^(\d+)([.)])", r"\1\\\2", md) if md[0].isdigit() else "\\" + md
    return md


# --------------------------------------------------------------- paragraphs

def line_kind(l):
    if l.math:
        return "math"
    if l.bold > 0.8 and l.size >= 14:
        return "h1"
    if l.bold > 0.8 and l.size >= 12.5:
        return "h2"
    if len(l.cells()) > 1:
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


def table(rows):
    cells = [r.cells() for r in rows]
    width = max(len(c) for c in cells)
    out = ["|" + "   |" * width, "|" + "---|" * width]
    for c in cells:
        c += [""] * (width - len(c))
        out.append("| " + " | ".join(escape(x).replace("|", "\\|") for x in c) + " |")
    return "\n".join(out)


# --------------------------------------------------------------------- main

def smart_title(s):
    small = {"of", "and", "the", "in", "a", "an", "to", "for", "on"}
    words = s.lower().split()
    return " ".join(w if i and w in small else w.capitalize() for i, w in enumerate(words))


def front_matter(doc):
    title_lines = [l for l in raw_lines(doc[1], 1) if l.size >= 14]
    author = next(l.text.strip() for l in title_lines if l.size >= 15)
    title = " ".join(l.text.strip() for l in title_lines if l.size < 15)
    imprint = [l.text.strip() for l in raw_lines(doc[2], 2)]
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


# ====================================================== Towards a New Socialism
# W. Paul Cockshott and Allin Cottrell, "Towards a New Socialism": a pdfTeX
# print (2020) of the text of the 2000 Swedish edition. Layout facts:
#   text block   x 134.1-477.9 on US letter; Computer Modern 10pt, lines
#                11.95pt apart; a paragraph starts with a 15pt indent (x 149.1)
#                and no extra space, except the first after a heading
#   running head y 98 (page number and a slanted title); the page number of
#                a chapter opening sits at y 689 instead
#   headings     small caps 14.3pt = chapter (a "Chapter N" line, then the
#                title); small caps 10pt = section; an italic line of its own =
#                subsection. Sections and subsections are confirmed against the
#                PDF outline
#   quotes       9pt, indented to x 159.1 on both sides; verse is 10pt at x 159.1
#   lists        "(1)", "(a)" or "•" at x 141-171, with a hanging indent
#   footnotes    8pt below a 137pt rule at x 134.1, each starting with a 6pt
#                number; markers are raised 7pt digits. Numbering restarts in
#                every chapter, so labels here are "<chapter>-<n>" ("3-2")
#   floats       "Table n.m:" and "Figure n.m:" captions sit above the float;
#                figures are vector drawings with text labels, saved as PNGs
#   display math centred lines; equation numbers "(3.1)" at the right margin
#   glyphs       ligatures (ﬁ ﬀ ﬂ ﬃ ﬄ) and TeX accents (` ´ ˆ) set as separate
#                glyphs over the letter; a word space after a ligature is lost

TNS_SKIP = {0, 4, 5, 6, 7}        # title page (read by tns_front_matter), Contents
TNS_LEFT, TNS_INDENT, TNS_RIGHT = 134.1, 149.1, 477.9
TNS_CENTRE = (TNS_LEFT + TNS_RIGHT) / 2
TNS_HANGING = (159.1, 181.0)      # continuation lines of list items
TNS_SMALL = 7.5                   # 8pt notes and 9pt quotes are text, 7pt is not
TNS_TABLE_GAP = 8                 # horizontal gap that separates table cells
LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}
ACCENTS = {"`": "̀", "´": "́", "ˆ": "̂", "¨": "̈", "˜": "̃"}
LIST_ITEM = re.compile(r"\s*(\(\w{1,3}\)|•)\s")
EQNO = re.compile(r"\(\d+\.\d+\)\s*$")
CAPTION = re.compile(r"\s*(Table|Figure) (\d+)\.(\d+):")

# Displays that line-by-line rendering garbles (stacked fractions, sums),
# keyed by (page, n-th display on the page); hand-made Markdown tables, keyed
# by table number.
TNS_MATH = {
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
TNS_TABLES = {
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
TNS_TEXT = {
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


def tns_clean(chars):
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


def tns_rule(page):
    """y of the footnote rule, or None."""
    for d in page.get_drawings():
        r = d["rect"]
        if r.height < 1 and abs(r.x0 - TNS_LEFT) < 1 and 130 < r.width < 145:
            return r.y0
    return None


def tns_extract(doc):
    """Return (body lines, {label: [note lines]}, {(page, n): label})."""
    body, notes, starts = [], {}, {}
    chapter, last, after_chapter_line = "front", None, False
    for pno in range(len(doc)):
        if pno in TNS_SKIP:
            continue
        page = doc[pno]
        lines = [l for l in raw_lines(page, pno, tns_clean)
                 if 110 < l.y0 and not (l.y0 > 680 and is_page_number(l.text))]
        rule = tns_rule(page)
        for l in lines:
            if l.size >= 13:
                m = re.match(r"\s*Chapter (\d+)", l.text)
                if m:
                    chapter = m.group(1)
                elif not after_chapter_line:
                    chapter = norm(l.text.split()[0])
                after_chapter_line = bool(m)
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

def tns_cells(line):
    """[[chars]] of one table row, split at wide gaps."""
    out, prev = [[]], None
    for c in line.chars:
        if c.c.strip() and prev is not None and c.x0 - prev.x1 > TNS_TABLE_GAP:
            out.append([])
        out[-1].append(c)
        if c.c.strip():
            prev = c
    return [cell for cell in out if any(c.c.strip() for c in cell)]


def tns_table(rows, fn):
    """A GFM table from visual rows, with columns found from the fullest rows."""
    cells = [[Line(cell, row.page) for cell in tns_cells(row)] for row in rows]
    width = max(len(r) for r in cells)
    cols = []
    for r in cells:
        if len(r) == width:
            for i, cell in enumerate(r):
                if i == len(cols):
                    cols.append([cell.x0, cell.x1])
                cols[i] = [min(cols[i][0], cell.x0), max(cols[i][1], cell.x1)]
    out = ["|" + "   |" * width, "|" + "---|" * width]
    for r in cells:
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


def tns_floats(doc, body, fn, fig_dir, fig_rel):
    """Replace each table and figure, with its caption, by a Block."""
    pages = {}
    for l in body:
        pages.setdefault(l.page, []).append(l)
    out = []
    for pno, lines in pages.items():
        page = doc[pno]
        draws = [d["rect"] for d in page.get_drawings()
                 if not (abs(d["rect"].x0 - TNS_LEFT) < 1 and d["rect"].width > 130)]  # footnote rule
        caps = [i for i, l in enumerate(lines)
                if CAPTION.match(l.text) and abs((l.x0 + l.x1) / 2 - TNS_CENTRE) < 20]

        def body_like(l):  # a table row has wide gaps, a line of text does not
            return l.size >= 9.5 and min(abs(l.x0 - TNS_LEFT), abs(l.x0 - TNS_INDENT)) < 1                 and len(tns_cells(l)) == 1

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
                out.append(Block(pno, l.y0, tns_float(page, lines[c], [lines[m] for m in members if m != c],
                                                      fdraws, fn, fig_dir, fig_rel)))
            elif i not in skip:
                out.append(l)
    return out


def tns_float(page, cap, content, draws, fn, fig_dir, fig_rel):
    kind, a, b = CAPTION.match(cap.text).groups()
    notes = []  # notes under the float: 8pt lines ("Source: ...", bullets)
    while content and content[-1].size < 9 and content[-1].y0 > cap.y0:
        notes.insert(0, content.pop())
    md = [render(tokens_of(cap, fn))]
    if kind == "Table":
        md.append(TNS_TABLES.get(f"{a}.{b}") or tns_table(content, fn))
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
            md.append(tns_note_para(para, fn))
            para = []
        para.append(l)
    if para:
        md.append(tns_note_para(para, fn))
    return "\n\n".join(md)


def tns_note_para(lines, fn):
    md = render(join_lines(lines, VOCAB, fn))
    return "- " + md.lstrip("• ") if md.startswith("•") else block_escape(md)


# --------------------------------------------------------------- paragraphs

def tns_toc(doc):
    """{(page, normalised title): heading level} for sections and subsections."""
    toc = {(1, norm("About this book")): 2}
    for level, title, page in doc.get_toc():
        if level > 1:
            toc[(page - 1, norm(title))] = level
    return toc


def tns_kind(l, toc):
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
    if LIST_ITEM.match(l.text) and TNS_LEFT + 3 < l.x0 < 175 and l.size >= 9.5:
        return "item"
    if 8.5 <= l.size < 9.5 and l.x0 > TNS_LEFT + 20:
        return "quote"
    if l.size >= 9.5 and abs(l.x0 - TNS_HANGING[0]) < 1 and l.x1 < TNS_RIGHT - 3:
        return "verse"
    standard = (TNS_LEFT, TNS_INDENT) + TNS_HANGING
    if l.size >= 9.5 and l.x1 < TNS_RIGHT - 1 and abs((l.x0 + l.x1) / 2 - TNS_CENTRE) < 15 \
            and min(abs(l.x0 - x) for x in standard) > 1:
        return "display"
    return "text"


def tns_paragraphs(body, toc):
    paras, refs = [], False  # dicts: kind, lines (+ level, joined)
    for l in body:
        kind = tns_kind(l, toc)
        if refs and kind != "h1":
            kind = "text"  # entries have a hanging indent: their later lines are not verse
        cur = paras[-1] if paras else None
        if cur and cur["kind"] == "item" and kind in ("text", "verse", "display") and l.x0 > TNS_INDENT + 5:
            if cur["level"] == 1 and l.x0 < TNS_HANGING[1] - 5 and not cur.get("cont"):
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
            indented = abs(l.x0 - TNS_INDENT) < 1 or (refs and l.x0 < TNS_LEFT + 3)
            # a float may interrupt a paragraph; the paragraph then goes on
            # after it, and the float follows the whole paragraph
            last = next((p for p in reversed(paras) if p["kind"] != "block"), None)
            if not indented and last and last["kind"] == "text" and \
                    all(p["kind"] == "block" for p in paras[paras.index(last) + 1:]):
                last["lines"].append(l)
                continue
        para = {"kind": kind, "lines": [l]}
        if kind == "item":
            para["level"] = 0 if l.x0 < TNS_INDENT else 1
        paras.append(para)
    return paras


# --------------------------------------------------------------------- main

def tns_front_matter(doc):
    lines = [l for b in doc[0].get_text("dict")["blocks"] for l in b.get("lines", [])]
    def words(big):
        return " ".join(re.sub(r"(?<=\S) (?=\S)", "", "".join(s["text"] for s in l["spans"]))
                        for l in lines if (l["spans"][0]["size"] > 20) == big)
    return [f"# {smart_title(words(True))}", f"**{smart_title(words(False))}**"]


VOCAB = Counter()


def convert_tns(doc, dst):
    global SMALL, VOCAB
    SMALL = TNS_SMALL
    body, notes, starts = tns_extract(doc)
    VOCAB = build_vocab(body + [l for ls in notes.values() for l in ls])
    vocab = VOCAB

    def fn(line, digits):
        return starts.get((line.page, int(digits)))

    slug = os.path.splitext(os.path.basename(dst))[0]
    body = tns_floats(doc, body, fn, os.path.join(os.path.dirname(dst), slug, "figures"), f"{slug}/figures")
    paras = tns_paragraphs(body, tns_toc(doc))

    blocks, chapter_notes, ordinals = tns_front_matter(doc), [], {}

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
            if (page, n) in TNS_MATH:
                add(TNS_MATH[(page, n)])
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
    for old, new in TNS_TEXT.items():
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
    doc = pymupdf.open(src)
    if norm(doc[0].get_text()).startswith("towardsanewsocialism"):
        md = convert_tns(doc, dst)
    else:
        md = convert(src)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(f"wrote {dst} ({len(md):,} chars)")
