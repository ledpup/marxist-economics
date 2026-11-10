"""Shared code for converting a book PDF to Markdown with PyMuPDF.

Each book has its own converter, which knows that PDF's layout:
  pdf_to_markdown_gic.py  the GIC's "Fundamental Principles of Communist
                          Production and Distribution"
  pdf_to_markdown_tns.py  Cockshott and Cottrell's "Towards a New Socialism"

This module holds what they share: reading a page into visual lines of
styled characters, turning lines into tokens, joining words hyphenated
across lines, and rendering tokens as Markdown.
"""
import re
from collections import Counter, namedtuple

from spellchecker import SpellChecker

ENGLISH = SpellChecker(distance=1)

TIGHT_SPACE = 2.45   # space advance below this = letter-spacing, not a word gap
FRACTIONS = {("1", "2"): "½", ("1", "4"): "¼", ("3", "4"): "¾", ("1", "3"): "⅓", ("2", "3"): "⅔"}
KEEP_HYPHEN_PREFIXES = {"self", "non", "anti", "semi", "quasi", "pseudo", "half", "well"}

Char = namedtuple("Char", "c x0 y0 x1 y1 font size flags spaced under")


class Line:
    """A visual line of characters. Characters smaller than `small` points
    are note numbers, superscripts or subscripts; each book sets its own."""
    def __init__(self, chars, page, small):
        self.chars = sorted(chars, key=lambda c: c.x0)
        self.page = page
        self.small = small
        main = [c for c in self.chars if c.size >= small and c.c.strip()] or \
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


def is_italic(c):
    return "Italic" in c.font or bool(c.flags & 2)


def is_bold(c):
    return "Bold" in c.font or bool(c.flags & 16) or c.spaced


# ----------------------------------------------------------------- extraction

def raw_lines(page, pno, small, clean=None):
    """Visual lines of a page, with spans on the same baseline merged.

    `clean`, if given, fixes up each merged line's characters (sorted by x)
    before letter-spacing is collapsed."""
    # underlines are thin filled rectangles ~2pt above the bottom of the text
    rules = [d["rect"] for d in page.get_drawings() if d["rect"].height < 1.2]

    def underlined(bbox, size):
        x, y1 = (bbox[0] + bbox[2]) / 2, bbox[3]
        return size >= small and any(r.x0 <= x <= r.x1 and y1 - 4 <= r.y0 <= y1 + 1 for r in rules)

    rows = []
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            chars = [Char(ch["c"], *ch["bbox"], s["font"], s["size"], s["flags"], False,
                          underlined(ch["bbox"], s["size"]))
                     for s in l["spans"] for ch in s["chars"]]
            if not any(c.c.strip() for c in chars):
                continue
            line = Line(chars, pno, small)
            for row in rows:
                overlap = min(row.y1, line.y1) - max(row.y0, line.y0)
                if overlap > 0.5 * min(row.y1 - row.y0, line.y1 - line.y0):
                    rows[rows.index(row)] = Line(row.chars + line.chars, pno, small)
                    break
            else:
                rows.append(line)
    rows.sort(key=lambda r: r.y0)
    if clean:
        rows = [Line(clean(r.chars), pno, small) for r in rows]
    return [Line(despace(r.chars), pno, small) for r in rows]


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


# ------------------------------------------------------------------- tokens
# A token is [text, italic, bold, kind]; kind is "t" (text), "fn" (marker),
# "sub" or "sup".

def tokens_of(line, fn_label=None):
    """`fn_label(line, digits)`, if given, returns the label of the footnote
    a raised number refers to, or None if the number is a plain superscript."""
    toks = []
    main_y1 = line.y1
    for c in line.chars:
        if c.size < line.small and c.c.strip():
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


def smart_title(s):
    small = {"of", "and", "the", "in", "a", "an", "to", "for", "on"}
    words = s.lower().split()
    return " ".join(w if i and w in small else w.capitalize() for i, w in enumerate(words))
