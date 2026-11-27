"""Convert an article on libcom.org to one Markdown file.

Written for the French original of Ratgeb's book (libcom.org/article/
de-la-greve-sauvage-lautogestion-generalisee-raoul-vaneigem) and Bill
Watson's "Counter-Planning on the Shop Floor".  Uses only the standard
library.

What it relies on in libcom's markup (the Drupal site of 2021 on):
  title        <title> is "<Title> - <Author> | libcom.org"
  introduction libcom's own summary is the <div> with class
               "field--name-field-introduction" -> an italic paragraph,
               marked as libcom's
  text         the article is the <div> with class "field--name-field-body".
               Its <p>s are paragraphs.  A <br> inside a <p> also starts a new
               paragraph, because libcom's texts use <br> where the original
               has separate lines (lettered items, headings).  <em>/<i> ->
               *..*, <strong>/<b> -> **..**, <h2>-<h4> -> "##"-"####", links
               kept as absolute URLs
  footnotes    a marker "[n]" in the text -> "[^n]"; a paragraph that starts
               "[n]" -> the definition "[^n]: ..."
  numbers      a number that opens a paragraph ("1. ...") is escaped so that
               it doesn't become a Markdown list

libcom's texts carry no headings as such: section and chapter headings are
plain paragraphs, so mark them up by hand after converting.

Usage: python libcom_to_markdown.py <url-or-file> output.md
"""
import argparse
import re
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

BASE = "https://libcom.org/"


def escape(text):
    """Escape what Markdown would read as syntax in running text."""
    return re.sub(r"([*_\\`])", r"\\\1", text)


def escape_start(text):
    """Escape a list or quote marker at the start of a paragraph."""
    text = re.sub(r"^([#>+])(\s)", r"\\\1\2", text)
    return re.sub(r"^(\d+)([.)])(\s)", r"\1\\\2\3", text)


class Article(HTMLParser):
    """The title, introduction and body paragraphs of a libcom article."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.in_title = False
        self.field = None      # "intro" or "body" while inside that <div>
        self.depth = 0         # <div> nesting inside the field
        self.intro, self.body = [], []
        self.buf = None
        self.kind = "p"
        self.href = None

    def start_block(self, kind="p"):
        self.end_block()
        self.buf, self.kind = [], kind

    def end_block(self):
        if self.buf is None:
            return
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = None
        if text:
            (self.intro if self.field == "intro" else self.body).append((self.kind, text))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "div":
            cls = attrs.get("class") or ""
            if self.field:
                self.depth += 1
            elif "field--name-field-introduction" in cls:
                self.field, self.depth = "intro", 0
            elif "field--name-field-body" in cls:
                self.field, self.depth = "body", 0
            return
        if not self.field:
            return
        if tag == "p":
            self.start_block()
        elif tag in ("h2", "h3", "h4"):
            self.start_block(tag)
        elif tag == "br":
            kind = self.kind
            self.start_block(kind)
        elif self.buf is None:
            self.start_block()
        if self.buf is None:
            return
        if tag in ("em", "i"):
            self.buf.append("*")
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag == "a" and attrs.get("href"):
            self.href = urljoin(BASE, attrs["href"])
            self.buf.append("[")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "div" and self.field:
            if self.depth == 0:
                self.end_block()
                self.field = None
            else:
                self.depth -= 1
            return
        if not self.field or self.buf is None:
            return
        if tag in ("p", "h2", "h3", "h4"):
            self.end_block()
        elif tag in ("em", "i"):
            self.buf.append("*")
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag == "a" and self.href:
            self.buf.append(f"]({self.href})")
            self.href = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.field:
            if self.buf is None:
                self.start_block()
            self.buf.append(escape(data))


def render(article, source):
    title, _, author = article.title.split(" | ")[0].rpartition(" - ")
    out = [f"# {title.strip() or author.strip()}", ""]
    if title.strip():
        out += [f"**{author.strip()}**", ""]
    out += [f"Source: <{source}>", ""]
    for _, text in article.intro:
        out += [f"*libcom's introduction:* {text.strip('*')}", ""]
    for kind, text in article.body:
        note = re.match(r"\\?\[(\d+)\\?\]\s*(.*)", text)
        if note:
            out += [f"[^{note.group(1)}]: {note.group(2)}", ""]
            continue
        text = re.sub(r"\[(\d+)\](?!\()", r"[^\1]", text)
        if kind != "p":
            out += ["#" * int(kind[1]) + " " + text, ""]
        else:
            out += [escape_start(text), ""]
    return "\n".join(out)


def fetch(source):
    if re.match(r"https?://", source):
        req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")
    with open(source, encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", help="libcom article URL or saved HTML file")
    ap.add_argument("output", help="Markdown file to write")
    ap.add_argument("--url", help="URL to cite when the source is a saved file")
    args = ap.parse_args()
    article = Article()
    article.feed(fetch(args.source))
    cited = args.url or args.source
    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write(render(article, cited))


if __name__ == "__main__":
    main()
