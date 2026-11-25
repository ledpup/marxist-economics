"""Convert a Marxists Internet Archive (marxists.org) HTML page to Markdown.

Written for Pannekoek's "Workers' Councils" but kept general, so it should
work on other MIA pages with little or no change.  Uses only the standard
library.

What it does with MIA markup:
  title block  the <h2> author, <h1> title and <h3> date before the first
               <hr> become the title, a bold byline and a plain line;
               <p class="information"> (Published, Transcriber ...) is kept
               with its line breaks, followed by a link to the source page
  contents     lists whose links all point inside the page (the MIA's own
               table of contents) and a "Contents" heading are dropped
  headings     levels are mapped by --levels (default h1/h2 -> #, h3 -> ##,
               h4 -> ###); ALL-CAPS words are put in title case unless
               --keep-caps is given; <br> inside a heading becomes a space
  text         <em>/<i> -> *..*, <strong>/<b> -> **..**, <u> -> <ins>..</ins>,
               <sup>/<sub> kept as HTML, <blockquote> and
               <p class="quoteb"> -> "> ", <ul>/<ol> -> "- " / "1. ",
               <br> -> hard line break (two trailing spaces); links to
               other pages are kept as absolute URLs, anchors are dropped
  notes        an internal link whose text is a number ("[12]", "12") is a
               note marker -> [^12]; a paragraph that starts with one is
               the note itself -> "[^12]: ..."; the endnote paragraphs that
               follow it are indented as its continuation.  A starred number
               ("[12*]", an editor's annotation) -> [^s12].  A heading with
               only note definitions under it ("Notes") is dropped, since
               renderers gather footnotes elsewhere and it would be empty
  figures      <img> -> ![caption](...), the caption taken from a <th> just
               before it (MIA's figure tables) or else the alt text; with
               --figures DIR the image is downloaded into DIR and linked
               relative to the output file, otherwise linked by URL
  dropped      <head>, scripts, styles, <hr>, empty paragraphs and the
               classes skip, updat, footer, toc, link, title (MIA navigation)

Usage: python html_to_markdown.py <url-or-file> output.md [--base URL]
                                  [--levels h1=1,h2=1,h3=2,h4=3] [--keep-caps]
                                  [--figures DIR]
"""
import argparse
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

DROP_CLASSES = {"skip", "updat", "footer", "toc", "link", "title"}
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in",
               "into", "nor", "of", "on", "or", "the", "to", "with"}
ROMAN = re.compile(r"^[IVXLC]+\.?$")
NOTE_TEXT = re.compile(r"^\[?(\d+)((?:\\?\*)?)\]?$")   # text is escaped: "1\*"


def title_case(text):
    """Title-case ALL-CAPS words; leave words with lower-case letters alone."""
    words = text.split(" ")
    out = []
    for i, w in enumerate(words):
        letters = re.sub(r"[^A-Za-z]", "", w)
        if len(letters) > 1 and letters.isupper() and not ROMAN.match(w):
            low = w.lower()
            first = i == 0 or re.match(r"^\d+\.$|^[IVXLC]+\.$", words[i - 1])
            if low in SMALL_WORDS and not first:
                w = low
            else:
                w = re.sub(r"[a-z]", lambda m: m.group(0).upper(), low, count=1)
        out.append(w)
    return " ".join(out)


def escape(text):
    """Escape what Markdown would read as syntax in running text."""
    text = re.sub(r"([*_\\`])", r"\\\1", text)
    text = re.sub(r"^(\s*)([#>+-])(\s)", r"\1\\\2\3", text)
    return re.sub(r"^(\s*\d+)\.(\s)", r"\1\\.\2", text)


class Converter(HTMLParser):
    def __init__(self, base, levels, keep_caps, figures=None, out_dir="."):
        super().__init__(convert_charrefs=True)
        self.base, self.levels, self.keep_caps = base, levels, keep_caps
        self.figures, self.out_dir = figures, out_dir
        self.blocks = []          # finished Markdown blocks
        self.buf = None           # inline text of the block being built
        self.kind = None          # "p", "h1".."h6", "li", "info"
        self.skip = 0             # depth inside dropped elements
        self.stack = []           # open tags, to match ends to starts
        self.quote = 0            # blockquote depth
        self.lists = []           # open lists: ["ul"|"ol", counter, toc?, items]
        self.link = None          # (href, start index in buf) of an open <a>
        self.seen_hr = False
        self.head = []            # title block before the first <hr>
        self.drop_next_list = False
        self.in_note = False      # the last block was (part of) an endnote
        self.para_classes = set() # classes of the <p> being built
        self.caption = None       # text of a <th> figure caption
        self.images = []          # (url, local path) of figures to download

    # ------------------------------------------------------------ helpers
    def start_block(self, kind):
        self.end_block()
        self.buf, self.kind = [], kind

    def end_block(self):
        if self.buf is None:
            return
        text = re.sub(r"[ \t\r\n]+", " ", "".join(self.buf))
        text = re.sub(r" *\n *", "\n", text.replace("\x00BR\x00", "\n")).strip()
        kind, self.buf, self.kind = self.kind, None, None
        if not text.strip():
            return
        if kind.startswith("h"):
            text = re.sub(r"\s+", " ", text)
            if re.fullmatch(r"(?i)(table of )?contents:?", text):
                self.drop_next_list = True
                return
            if not self.seen_hr:
                self.head.append((kind, text))
                return
            if not self.keep_caps:
                text = title_case(text)
            self.in_note = False
            self.blocks.append("#" * self.levels.get(kind, 2) + " " + text)
            return
        if kind == "caption":
            self.caption = re.sub(r"\s+", " ", text)
            return
        if kind == "info":
            self.head.append(("info", text))
            return
        if kind == "li":
            ltype, n, toc, items = self.lists[-1]
            self.lists[-1][1] += 1
            mark = f"{n}." if ltype == "ol" else "-"
            indent = "  " * (len(self.lists) - 1)
            items.append(indent + mark + " " + text.replace("\n", "  \n" + indent + "  "))
            return
        m = re.match(r"^\x00NOTE(s?\d+)\x00\s*", text)
        continuation = False
        if m:                                  # a note: "[^n]: text"
            text = f"[^{m.group(1)}]: " + text[m.end():]
            self.in_note = True
        elif self.in_note and "endnote" in self.para_classes:
            continuation = True                # a further paragraph of it
        else:
            self.in_note = False
        text = re.sub(r"\x00NOTE(s?\d+)\x00", r"[^\1]", text)
        text = text.replace("\n", "  \n")
        if continuation:
            text = "\n".join("    " + line for line in text.split("\n"))
        if self.quote:
            text = "\n".join("> " * self.quote + line for line in text.split("\n"))
        self.blocks.append(text)

    def emit(self, s):
        if self.skip:
            return
        if self.buf is None:
            if not s.strip():
                return
            self.start_block("p")      # loose text outside any block
        self.buf.append(s)

    # ------------------------------------------------------------ parser
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        if tag in ("br", "hr", "img", "meta", "link", "input"):
            if tag == "img" and not self.skip and a.get("src"):
                self.figure(a)
            elif tag == "br":
                self.emit(" " if self.kind and self.kind.startswith("h") else "\x00BR\x00")
            elif tag == "hr":
                self.end_block()
                self.seen_hr = True
            return
        self.stack.append(tag)
        if self.skip or tag in ("head", "script", "style") or classes & DROP_CLASSES:
            self.skip += 1
            return
        if tag == "p":
            if "quoteb" in classes:
                self.end_block()
                self.quote += 1
            self.start_block("info" if "information" in classes else "p")
            self.para_classes = classes
        elif tag == "th":
            self.start_block("caption")
        elif re.fullmatch(r"h[1-6]", tag):
            self.start_block(tag)
        elif tag == "blockquote":
            self.end_block()
            self.quote += 1
        elif tag in ("ul", "ol"):
            self.end_block()
            self.lists.append([tag, 1, self.drop_next_list, []])
            self.drop_next_list = False
        elif tag == "li":
            self.start_block("li")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag == "u":
            self.emit("<ins>")
        elif tag in ("sup", "sub"):
            self.emit(f"<{tag}>")
        elif tag == "a":
            self.link = (a.get("href"), len(self.buf) if self.buf is not None else 0)

    def handle_endtag(self, tag):
        if tag not in self.stack:
            return
        while self.stack:                     # close anything left open inside
            t = self.stack.pop()
            if self.skip:
                self.skip -= 1
                if t == tag:
                    return
                continue
            self.close(t)
            if t == tag:
                return

    def close(self, tag):
        if tag == "p" and "quoteb" in self.para_classes:
            self.end_block()
            self.quote -= 1
            self.para_classes = set()
        elif tag in ("p", "th") or re.fullmatch(r"h[1-6]", tag) or tag == "li":
            self.end_block()
            self.para_classes = set()
        elif tag == "blockquote":
            self.end_block()
            self.quote -= 1
        elif tag in ("ul", "ol"):
            self.end_block()
            ltype, n, toc, items = self.lists.pop()
            if self.lists:                     # nested: hand items to the parent
                self.lists[-1][3].extend(items)
                self.lists[-1][2] = self.lists[-1][2] or toc
                return
            if items and not toc and not self._list_is_toc:
                self.blocks.append("\n".join(items))
            self._list_is_toc = False
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag == "u":
            self.emit("</ins>")
        elif tag in ("sup", "sub"):
            self.emit(f"</{tag}>")
        elif tag == "a" and self.link and self.buf is not None:
            href, start = self.link
            self.link = None
            text = "".join(self.buf[start:])
            if href and href.startswith("#"):
                m = NOTE_TEXT.match(text.strip())
                if m:                          # a note marker
                    del self.buf[start:]
                    if self.buf and self.buf[-1] in ("<sup>", "["):
                        self.buf.pop()
                        self._drop_sup = True
                    label = ("s" if m.group(2) else "") + m.group(1)
                    self.buf.append(f"\x00NOTE{label}\x00")
                elif self.lists:
                    self._list_is_toc = True   # an in-page contents list
            elif href and not href.startswith(("mailto:", "javascript:")) and text.strip():
                del self.buf[start:]
                self.buf.append(f"[{text.strip()}]({urljoin(self.base, href)})")
        if tag == "sup" and getattr(self, "_drop_sup", False):
            self._drop_sup = False
            if self.buf and self.buf[-1] == "</sup>":
                self.buf.pop()

    _list_is_toc = False

    def figure(self, a):
        """An <img>: its own block, captioned by a preceding <th> or its alt."""
        self.end_block()
        url = urljoin(self.base, a["src"])
        caption = self.caption or a.get("alt") or ""
        self.caption = None
        target = url
        if self.figures:
            local = os.path.join(self.figures, os.path.basename(a["src"]))
            self.images.append((url, local))
            target = os.path.relpath(local, self.out_dir).replace(os.sep, "/")
        self.blocks.append(f"![{caption}]({target.replace(' ', '%20')})")

    def handle_data(self, data):
        if self.skip:
            return
        if self.buf is None and not data.strip():
            return
        self.emit(escape(data) if not (self.kind or "").startswith("h") else data)

    # ------------------------------------------------------------ result
    def markdown(self):
        self.end_block()
        out = []
        heads = [t for k, t in self.head if k != "info"]
        info = [t for k, t in self.head if k == "info"]
        title = next((t for k, t in self.head if k == "h1"), None)
        if title:
            out.append(f"# {title}")
            for k, t in self.head:
                if k == "h2":
                    out.append(f"**{t}**")
                elif k.startswith("h") and k != "h1":
                    out.append(t)
        else:
            out += heads
        for t in info:
            lines = t.split("\n")
            out.append("  \n".join(re.sub(r"^([^:]{1,30}):", r"**\1:**", l.strip()) for l in lines))
        if self.base.startswith("http"):
            out.append(f"Source: <{self.base}>")
        return "\n\n".join(out + self.without_note_headings()).strip() + "\n"

    def without_note_headings(self):
        """Drop a heading ("Notes") with nothing under it but note
        definitions: Markdown renderers gather footnotes elsewhere, so it
        would be left empty."""
        blocks = self.blocks
        keep = []
        for i, b in enumerate(blocks):
            if b.startswith("#"):
                j = i + 1
                while j < len(blocks) and re.match(r"\[\^|    ", blocks[j]):
                    j += 1
                if j > i + 1 and (j == len(blocks) or blocks[j].startswith("#")):
                    continue
            keep.append(b)
        return keep


def fetch(src):
    """The bytes of a URL or a local file."""
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (html_to_markdown.py)"})
        with urllib.request.urlopen(req) as r:
            return r.read()
    with open(src, "rb") as f:
        return f.read()


def read(src):
    raw = fetch(src)
    m = re.search(rb'charset=["\']?([\w-]+)', raw[:2000])
    charset = m.group(1).decode() if m else "utf-8"
    try:
        return raw.decode(charset)
    except (LookupError, UnicodeDecodeError):
        return raw.decode("latin-1")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("src", help="URL or local .htm file")
    ap.add_argument("out", help="Markdown file to write")
    ap.add_argument("--base", help="URL of the page, for links (default: src if a URL)")
    ap.add_argument("--levels", default="h1=1,h2=1,h3=2,h4=3,h5=4,h6=5")
    ap.add_argument("--keep-caps", action="store_true", help="don't title-case ALL-CAPS headings")
    ap.add_argument("--figures", help="download images into this folder and link them relatively")
    args = ap.parse_args()
    levels = {k: int(v) for k, v in (p.split("=") for p in args.levels.split(","))}
    base = args.base or (args.src if re.match(r"https?://", args.src) else "")
    out_dir = os.path.dirname(os.path.abspath(args.out))
    figures = os.path.abspath(args.figures) if args.figures else None
    conv = Converter(base, levels, args.keep_caps, figures, out_dir)
    conv.feed(read(args.src))
    if conv.images:
        os.makedirs(figures, exist_ok=True)
    for url, local in conv.images:
        with open(local, "wb") as f:
            f.write(fetch(url if re.match(r"https?://", url) else
                          os.path.join(os.path.dirname(args.src), url)))
    md = conv.markdown()
    md = re.sub(r"\n{3,}", "\n\n", md)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)


if __name__ == "__main__":
    main()
