"""Convert a book on Situationist International Online to one Markdown file.

Written for Ratgeb's "From Wildcat Strike to Total Self Management"
(sionline.researche-editions.cddc.vt.edu/postsi/ratgeb.html).  SI Online
splits a book into an index page and one page per chapter, and its pages
(made with Adobe GoLive) set almost all text in heading tags.  Uses only the
standard library.

What it relies on in SI Online's markup:
  index page   after the content <h2> (the title) come <h3> (author), <h1>
               (original title and edition) and <h5> (translators); the
               links after it, in order, are the chapter pages
  chapters     everything before the content <h2> (logo, menu, breadcrumb
               <h1>) is navigation and dropped; the <h2> is the chapter
               title -> "#"; <h3> and <h1> after it (preface author, date)
               -> plain lines, the <h5> translator credit -> an italic line
  paragraphs   each <h4> is a paragraph; <h4>s are often nested two deep,
               and the inner one holds the text.  An <h4> that is bold
               throughout is a section heading -> "##"
  text         <i> -> *..*, <b> -> **..**, <blockquote> -> "> ", <br> ->
               hard line break; <font> is dropped; <li type="A"> in an <ol>
               keeps its letter ("A. ..."); numbers that open a paragraph
               ("1. ...") are escaped so they don't become Markdown lists
  links        a paragraph that only links to another page of the book
               (the "next chapter" link) is dropped; other links are kept
               as absolute URLs

Usage: python sionline_to_markdown.py <index-url-or-file> output.md
"""
import argparse
import re
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin


def escape(text):
    """Escape what Markdown would read as syntax in running text."""
    return re.sub(r"([*_\\`])", r"\\\1", text)


def escape_start(text):
    """Escape a list or quote marker at the start of a paragraph."""
    text = re.sub(r"^([#>+-])(\s)", r"\\\1\2", text)
    return re.sub(r"^(\d+)([.)])(\s)", r"\1\\\2\3", text)


class Page(HTMLParser):
    """One SI Online page: its title block, paragraphs and links."""

    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.started = False      # past the content <h2>
        self.title = None
        self.meta = []            # (tag, text) of h1/h3/h5 after the title
        self.blocks = []          # finished Markdown blocks
        self.links = []           # hrefs after the title, in order
        self.buf = None           # inline text of the block being built
        self.kind = None          # "p", "h1", "h2", ...
        self.quote = 0
        self.letters = []         # counters of open <ol type="A"> lists
        self.link = None          # (href, start index in buf)
        self.only_links = True    # the block so far is nothing but links
        self.opened = None        # index in buf of a just-opened * or **

    def start_block(self, kind):
        self.end_block()
        self.buf, self.kind, self.only_links = [], kind, True

    def end_block(self):
        if self.buf is None:
            return
        text = re.sub(r"[ \t\r\n]+", " ", "".join(self.buf))
        text = re.sub(r" *\x00BR\x00 *", "\n", text).strip()
        kind, self.buf, self.kind = self.kind, None, None
        if not text:
            return
        if kind == "h2":
            self.title = text.replace("\n", " ")
            return
        if kind in ("h1", "h3", "h5"):
            self.meta.append((kind, text.replace("\n", " ")))
            return
        if self.only_links:       # navigation: "next chapter" and the like
            return
        bold = re.fullmatch(r"\*\*([^*]+)\*\*", text)
        if bold and not self.quote:
            self.blocks.append("## " + bold.group(1).replace("\n", " "))
            return
        text = escape_start(text).replace("\n", "  \n")
        if self.quote:
            text = "\n".join("> " * self.quote + line for line in text.split("\n"))
        self.blocks.append(text)

    def emit(self, s):
        if self.buf is None:
            if not s.strip():
                return
            self.start_block("p")
        self.buf.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h2" and not self.started:
            self.started = True
            self.start_block("h2")
            return
        if not self.started:
            return
        if tag in ("h1", "h3", "h5") and not self.blocks:
            self.start_block(tag)
        elif tag in ("h1", "h3", "h4", "h5", "h6", "p"):
            self.start_block("p")
        elif tag == "blockquote":
            self.end_block()
            self.quote += 1
        elif tag == "ol":
            self.end_block()
            self.letters.append(0 if (a.get("type") or "A").isalpha() else None)
        elif tag == "li":
            if self.buf is None:
                self.start_block("p")
            if self.letters and self.letters[-1] is not None:
                self.buf.append(chr(ord("A") + self.letters[-1]) + ". ")
                self.letters[-1] += 1
                self.only_links = False
        elif tag == "br":
            self.emit("\x00BR\x00")
        elif tag in ("i", "em"):
            self.emit("*")
            self.opened = len(self.buf) - 1
        elif tag in ("b", "strong"):
            self.emit("**")
            self.opened = len(self.buf) - 1
        elif tag == "a" and a.get("href"):
            if self.buf is None:
                self.start_block("p")
            self.link = (a["href"], len(self.buf))
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if not self.started:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p"):
            self.end_block()
        elif tag == "blockquote":
            self.end_block()
            self.quote = max(0, self.quote - 1)
        elif tag == "ol":
            self.end_block()
            if self.letters:
                self.letters.pop()
        elif tag in ("i", "em"):
            self.close_emphasis("*")
        elif tag in ("b", "strong"):
            self.close_emphasis("**")
        elif tag == "a" and self.link and self.buf is not None:
            href, start = self.link
            self.link = None
            text = "".join(self.buf[start:]).strip()
            del self.buf[start:]
            if re.match(r"(?i)https?:|mailto:", href):
                self.buf.append(f"[{text}]({href})")
                self.only_links = False
            elif "/" not in href.strip("./"):    # another page of the book
                self.buf.append(text)
            else:
                self.buf.append(f"[{text}]({urljoin(self.base, href)})")
                self.only_links = False

    def close_emphasis(self, mark):
        """Close *..* or **..**: drop it if empty, keep spaces outside it."""
        if self.buf is None:
            return
        space = ""
        while self.buf and self.buf[-1] != mark and not self.buf[-1].strip():
            space = self.buf.pop() + space
        if self.buf and self.buf[-1] == mark:
            self.buf.pop()
        else:
            if self.buf and self.buf[-1] != self.buf[-1].rstrip():
                space = " " + space
                self.buf[-1] = self.buf[-1].rstrip()
            self.buf.append(mark)
        if space:
            self.buf.append(space)

    def handle_data(self, data):
        if not self.started or (self.buf is None and not data.strip()):
            return
        if self.buf and self.opened == len(self.buf) - 1 and data[:1].isspace():
            self.buf.insert(-1, " ")           # "<i> and</i>": space outside
            data = data.lstrip()
        self.emit(escape(data))
        if data.strip() and self.link is None:
            self.only_links = False


def fetch(src):
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (sionline_to_markdown.py)"})
        with urllib.request.urlopen(req) as r:
            raw = r.read()
    else:
        with open(src, "rb") as f:
            raw = f.read()
    return raw.decode("cp1252", errors="replace")


def parse(src, base):
    page = Page(base)
    page.feed(fetch(src))
    page.end_block()
    return page


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("src", help="URL or local file of the book's index page")
    ap.add_argument("out", help="Markdown file to write")
    args = ap.parse_args()

    index = parse(args.src, args.src)
    meta = dict(index.meta)
    out = [f"# {index.title}"]
    if "h3" in meta:
        out.append(f"**{meta['h3']}**")
    out += [meta[k] for k in ("h1", "h5") if k in meta]
    if re.match(r"https?://", args.src):
        out.append(f"Source: <{args.src}>")
    chapters = [h for h in dict.fromkeys(index.links) if re.fullmatch(r"[\w-]+\.html?", h)]
    for href in chapters:
        url = urljoin(args.src, href)
        page = parse(url, url)
        out.append(f"# {page.title}")
        for tag, text in page.meta:
            out.append(f"*{text}*" if tag == "h5" else text)
        out += page.blocks
    md = "\n\n".join(out).strip() + "\n"
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)


if __name__ == "__main__":
    main()
