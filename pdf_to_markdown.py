"""Convert the GIC "Fundamental Principles of Communist Production and
Distribution" PDF to Markdown using PyMuPDF.

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

Usage: python pdf_to_markdown.py input.pdf output.md
"""
import re
import sys
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

def raw_lines(page, pno):
    """Visual lines of a page, with spans on the same baseline merged."""
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

def tokens_of(line):
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
    return [t for t in toks if t[0]]


def build_vocab(lines):
    vocab = Counter()
    for l in lines:
        # the last word of a line may be a hyphenation fragment
        for w in re.findall(r"[\w'-]+", l.text)[:-1]:
            vocab[w.lower().strip("-")] += 1
    return vocab


def join_lines(lines, vocab):
    """Concatenate line tokens, fixing words hyphenated across lines."""
    toks = []
    for line in lines:
        new = tokens_of(line)
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


if __name__ == "__main__":
    src, dst = sys.argv[1:3]
    md = convert(src)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(f"wrote {dst} ({len(md):,} chars)")
