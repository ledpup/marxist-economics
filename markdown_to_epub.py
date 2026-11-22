"""Build EPUB 3 e-books from the single-file Markdown texts in Documents/.

    python markdown_to_epub.py                       # the books in BOOKS
    python markdown_to_epub.py Documents/<slug>.md   # any single-file text
    python markdown_to_epub.py Documents/<slug>.md --split 2
    python markdown_to_epub.py --out-dir somewhere --no-cover

Output goes to epub/<slug>.epub. For a Kindle, send the file with Send to
Kindle (the app, amazon.com/sendtokindle, or by email): Amazon converts the
EPUB and delivers it to older Kindles too. Kindles can't open an EPUB copied
over USB; convert it to AZW3 with Calibre for that.

What the script relies on in the Markdown:
- The first `# ` heading is the book's title, and the first line in bold
  after it (`**…**`) is the author. Authors joined by " and " become
  separate creators.
- Every heading down to the book's split level starts a chapter: `# ` for
  most books, `# ` and `## ` for a book whose `# ` headings are parts with
  `## ` chapters (Workers' Councils). Each chapter is its own XHTML file, so
  it starts on a new page in every reader. A part heading followed directly
  by its first chapter shares that chapter's page. Everything before the
  second such heading is the title page. The table of contents lists the
  same headings, nested by level.
- Footnotes are GFM `[^label]` markers with `[^label]: …` definitions, which
  may sit anywhere in the file. Each definition goes to the end of the
  chapter that first cites it. The note shows its label as the book numbers
  it (`[^21]` shows 21; a chapter-prefixed `[^3-2]` shows 2). Markers and
  notes use EPUB's noteref/footnote markup, which Kindles show as pop-ups,
  and each note's number links back to the text.
- Images are relative to the Markdown file and are copied into the book.

Needs markdown-it-py and mdit-py-plugins. The cover is the first page of
the book's PDF, rendered with PyMuPDF; without PyMuPDF, or with --no-cover,
the book has no cover image.
"""
import argparse
import html
import mimetypes
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin

ROOT = Path(__file__).resolve().parent

# The books built when no file is named: the PDF whose first page is the
# cover, and the deepest heading level that starts a chapter.
BOOKS = {
    "Documents/fundamental_principles_of_communist_production_and_distribution.md": {
        "cover": "PDFs/FUNDAMENTAL PRINCIPLES OF COMMUNIST PRODUCTION AND DISTRIBUTION.pdf",
        "split": 1},
    "Documents/towards_a_new_socialism.md": {
        "cover": "PDFs/TOWARDS A NEW SOCIALISM.pdf", "split": 1},
    "Documents/Workers_Councils.md": {
        "cover": "PDFs/WORKERS' COUNCILS.pdf", "split": 2},
}

LANGUAGE = "en"

CSS = """\
body { margin: 0 2%; }
h1 { page-break-before: always; break-before: page; margin: 1.5em 0 1em; font-size: 1.6em; line-height: 1.2; }
h2 { margin: 1.4em 0 0.6em; font-size: 1.3em; line-height: 1.25; page-break-after: avoid; }
h3, h4, h5, h6 { margin: 1.2em 0 0.5em; font-size: 1.1em; page-break-after: avoid; }
p { margin: 0 0 0.6em; text-align: left; }
blockquote { margin: 0.8em 1.5em; }
ins { text-decoration: underline; }
sup, sub { font-size: 0.75em; line-height: 0; }
a.noteref { text-decoration: none; }
table { border-collapse: collapse; margin: 0.8em 0; }
th, td { border: 1px solid #000; padding: 0.15em 0.4em; vertical-align: top; }
img { max-width: 100%; }
hr { margin: 1.2em 20%; border: 0; border-top: 1px solid #000; }
section.footnotes { margin-top: 2em; font-size: 0.9em; }
aside.footnote { margin: 0 0 0.6em; }
.titlepage h1 { page-break-before: auto; margin-top: 3em; font-size: 2em; text-align: center; }
.titlepage > p { text-align: center; }
.cover { margin: 0; padding: 0; text-align: center; }
.cover img { height: 100%; max-width: 100%; }
nav ol { list-style-type: none; padding-left: 1.2em; }
"""

XHTML = """\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{lang}" lang="{lang}">
<head>
<meta charset="utf-8" />
<title>{title}</title>
<link rel="stylesheet" type="text/css" href="../style.css" />
</head>
<body{body_attrs}>
{body}
</body>
</html>
"""


def esc(text):
    return html.escape(text, quote=True)


# ---------------------------------------------------------------- Markdown

def split_chapters(markdown, split=1):
    """Split at headings of level 1 to `split`, outside code fences. The first
    part is the title page. A part that is only headings joins the next one."""
    heading = re.compile(rf"^#{{1,{split}}} ")
    parts, current, fenced = [], [], False
    for line in markdown.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        if not fenced and heading.match(line) and any(heading.match(l) for l in current):
            if len(parts) > 0 and all(heading.match(l) or not l.strip() for l in current):
                current.append(line)   # e.g. a part heading directly above its first chapter
                continue
            parts.append(current)
            current = []
        current.append(line)
    parts.append(current)
    return ["\n".join(p).strip() + "\n" for p in parts]


DEF_START = re.compile(r"^\[\^([^\]\s]+)\]:")
REF = re.compile(r"\[\^([^\]\s]+)\](?!:)")


def extract_definitions(markdown):
    """Remove the footnote definitions; return (text, {label: definition}).
    A definition runs until a blank line followed by an unindented line."""
    lines = markdown.splitlines()
    body, defs, i = [], {}, 0
    while i < len(lines):
        m = DEF_START.match(lines[i])
        if not m:
            body.append(lines[i])
            i += 1
            continue
        block = [lines[i]]
        i += 1
        while i < len(lines) and not DEF_START.match(lines[i]):
            if lines[i].strip() == "":
                nxt = next((l for l in lines[i:] if l.strip()), "")
                if not nxt.startswith(("    ", "\t")):
                    break
            block.append(lines[i])
            i += 1
        defs[m.group(1)] = "\n".join(block)
    return "\n".join(body), defs


def slugify(text):
    """GitHub's heading anchor: lower case, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"[^\w\- ]", "", text.lower())
    return text.replace(" ", "-") or "section"


def plain_text(inline):
    out = []
    for t in inline.children or []:
        if t.type in ("text", "code_inline"):
            out.append(t.content)
        elif t.type in ("softbreak", "hardbreak"):
            out.append(" ")
    return re.sub(r"\s+", " ", "".join(out)).strip()


def note_id(label):
    return re.sub(r"[^A-Za-z0-9_-]", "_", label)


def note_number(label):
    return label.rsplit("-", 1)[-1]


def make_renderer():
    md = MarkdownIt("commonmark", {"xhtmlOut": True, "html": True}).enable(
        ["table", "strikethrough"]).use(footnote_plugin)
    rules = md.add_render_rule

    def footnote_ref(self, tokens, idx, options, env):
        meta = tokens[idx].meta
        nid = note_id(meta["label"])
        ref_id = f"fnref-{nid}" + (f"-{meta['subId']}" if meta["subId"] else "")
        return (f'<a class="noteref" epub:type="noteref" id="{ref_id}" href="#fn-{nid}">'
                f'<sup>{esc(note_number(meta["label"]))}</sup></a>')

    def footnote_block_open(self, tokens, idx, options, env):
        return '<section class="footnotes" epub:type="endnotes">\n<hr />\n'

    def footnote_block_close(self, tokens, idx, options, env):
        return "</section>\n"

    def footnote_open(self, tokens, idx, options, env):
        label = tokens[idx].meta["label"]
        nid = note_id(label)
        back = f'<a href="#fnref-{nid}">{esc(note_number(label))}.</a>'
        out = f'<aside class="footnote" epub:type="footnote" id="fn-{nid}">\n'
        if idx + 1 < len(tokens) and tokens[idx + 1].type == "paragraph_open":
            tokens[idx + 1].meta["note_back"] = back   # the number opens the note's first paragraph
        else:
            out += f"<p>{back}</p>\n"
        return out

    def footnote_close(self, tokens, idx, options, env):
        return "</aside>\n"

    def footnote_anchor(self, tokens, idx, options, env):
        return ""   # the note's number is already the link back

    def paragraph_open(self, tokens, idx, options, env):
        back = tokens[idx].meta.get("note_back")
        return f"<p>{back} " if back else self.renderToken(tokens, idx, options, env)

    for name, fn in list(locals().items()):
        if name.startswith(("footnote_", "paragraph_")):
            rules(name, fn)
    return md


# ---------------------------------------------------------------- Book

class Chapter:
    def __init__(self, filename, html_body, headings):
        self.filename = filename
        self.body = html_body
        self.headings = headings     # [(level, text, id)]

    @property
    def title(self):
        return self.headings[0][1] if self.headings else self.filename


def build_chapters(md_path, md, split):
    text, defs = extract_definitions(md_path.read_text(encoding="utf-8"))
    parts = split_chapters(text, split)
    placed, images, chapters = set(), {}, []
    for n, part in enumerate(parts):
        notes = []
        for label in dict.fromkeys(REF.findall(part)):
            if label in defs and label not in placed:
                notes.append(defs[label])
                placed.add(label)
            elif label not in defs:
                print(f"  warning: [^{label}] has no definition", file=sys.stderr)
        source = part + ("\n\n" + "\n\n".join(notes) + "\n" if notes else "")
        env = {}
        tokens = md.parse(source, env)
        headings, used = [], set()
        for i, tok in enumerate(tokens):
            if tok.type == "heading_open":
                title = plain_text(tokens[i + 1])
                hid = base = slugify(title)
                k = 1
                while hid in used:
                    hid = f"{base}-{k}"
                    k += 1
                used.add(hid)
                tok.attrSet("id", hid)
                headings.append((int(tok.tag[1]), title, hid))
            for child in tok.children or []:
                if child.type == "image":
                    src = (md_path.parent / child.attrGet("src")).resolve()
                    name = images.setdefault(src, f"images/{len(images) + 1:03d}{src.suffix.lower()}")
                    child.attrSet("src", "../" + name)
        body = md.renderer.render(tokens, md.options, env)
        body = re.sub(r"<(br|hr)\s*>", r"<\1 />", body)   # raw HTML from the source
        filename = "titlepage.xhtml" if n == 0 else f"chapter-{n:02d}.xhtml"
        chapters.append(Chapter(filename, body, headings))
    for label in defs.keys() - placed:
        print(f"  warning: [^{label}] is defined but never cited", file=sys.stderr)
    return chapters, images


def render_cover(pdf_path):
    try:
        import pymupdf
    except ImportError:
        print("  PyMuPDF isn't installed, so no cover", file=sys.stderr)
        return None
    with pymupdf.open(pdf_path) as doc:
        page = doc[0]
        zoom = 1600 / page.rect.height
        return page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes("jpeg", jpg_quality=85)


def title_and_authors(titlepage_md):
    title = re.search(r"^# (.+)$", titlepage_md, re.M).group(1).strip()
    m = re.search(r"^\*\*(.+?)\*\*\s*$", titlepage_md, re.M)
    authors = [a.strip() for a in m.group(1).split(" and ")] if m else []
    return title, authors


def toc_items(chapters, split):
    """The headings that start chapters (level 1 to `split`), nested by level,
    as (text, href, children)."""
    root = []
    stack = [(0, root)]   # (level, list that headings below that level go into)
    for ch in chapters:
        for n, (level, text, hid) in enumerate(ch.headings):
            if level > split:
                continue
            while stack[-1][0] >= level:
                stack.pop()
            children = []
            stack[-1][1].append((text, ch.filename if n == 0 else f"{ch.filename}#{hid}", children))
            stack.append((level, children))
    return root


def nav_xhtml(items, title):
    def ol(entries, depth):
        pad = "  " * depth
        lines = [f"{pad}<ol>"]
        for text, href, children in entries:
            inner = f'<a href="{esc(href)}">{esc(text)}</a>'
            if children:
                lines.append(f"{pad}  <li>{inner}")
                lines.append(ol(children, depth + 2))
                lines.append(f"{pad}  </li>")
            else:
                lines.append(f"{pad}  <li>{inner}</li>")
        lines.append(f"{pad}</ol>")
        return "\n".join(lines)

    body = (f'<nav epub:type="toc" id="toc">\n<h1>Contents</h1>\n{ol(items, 0)}\n</nav>\n'
            '<nav epub:type="landmarks" hidden="hidden">\n<ol>\n'
            '  <li><a epub:type="toc" href="nav.xhtml">Contents</a></li>\n'
            '  <li><a epub:type="bodymatter" href="titlepage.xhtml">Start</a></li>\n'
            '</ol>\n</nav>')
    return XHTML.format(lang=LANGUAGE, title=esc(title), body_attrs="", body=body)


def ncx(items, title, book_id, depth):
    counter = [0]

    def points(entries, depth):
        out = []
        for text, href, children in entries:
            counter[0] += 1
            pad = "  " * depth
            out.append(f'{pad}<navPoint id="np{counter[0]}" playOrder="{counter[0]}">'
                       f'<navLabel><text>{esc(text)}</text></navLabel>'
                       f'<content src="text/{esc(href)}"/>')
            out.extend(points(children, depth + 1))
            out.append(f"{pad}</navPoint>")
        return out

    nav = "\n".join(points(items, 1))
    return f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{book_id}"/><meta name="dtb:depth" content="{depth}"/></head>
<docTitle><text>{esc(title)}</text></docTitle>
<navMap>
{nav}
</navMap>
</ncx>
"""


def build_epub(md_path, out_dir, cover_pdf, split=1):
    md_path = Path(md_path).resolve()
    slug = md_path.stem
    chapters, images = build_chapters(md_path, make_renderer(), split)
    title, authors = title_and_authors(split_chapters(md_path.read_text(encoding="utf-8"), split)[0])
    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'marxist-economics/' + slug)}"
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cover = render_cover(cover_pdf) if cover_pdf else None

    manifest = ['<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="nav" href="text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>']
    spine = []
    if cover:
        manifest += ['<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
                     '<item id="cover" href="text/cover.xhtml" media-type="application/xhtml+xml"/>']
        spine.append('<itemref idref="cover" linear="no"/>')
    for i, ch in enumerate(chapters):
        cid = "titlepage" if i == 0 else f"c{i:02d}"
        props = ' properties="svg"' if "<svg" in ch.body else ""
        manifest.append(f'<item id="{cid}" href="text/{ch.filename}" media-type="application/xhtml+xml"{props}/>')
        spine.append(f'<itemref idref="{cid}"/>')
        if i == 0:
            spine.append('<itemref idref="nav"/>')
    for n, name in enumerate(images.values()):
        mtype = mimetypes.guess_type(name)[0]
        manifest.append(f'<item id="img{n + 1:03d}" href="{name}" media-type="{mtype}"/>')

    creators = "\n".join(f'<dc:creator id="creator{n}">{esc(a)}</dc:creator>'
                         for n, a in enumerate(authors, 1))
    nl = "\n"
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{LANGUAGE}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{book_id}</dc:identifier>
<dc:title>{esc(title)}</dc:title>
{creators}
<dc:language>{LANGUAGE}</dc:language>
<meta property="dcterms:modified">{modified}</meta>
{'<meta name="cover" content="cover-image"/>' if cover else ''}
</metadata>
<manifest>
{nl.join(manifest)}
</manifest>
<spine toc="ncx">
{nl.join(spine)}
</spine>
</package>
"""
    items = toc_items(chapters, split)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{slug}.epub"
    with zipfile.ZipFile(out, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", zipfile.ZIP_STORED)
        put = lambda name, data: z.writestr(name, data, zipfile.ZIP_DEFLATED)
        put("META-INF/container.xml", """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
""")
        put("OEBPS/content.opf", opf)
        put("OEBPS/style.css", CSS)
        put("OEBPS/toc.ncx", ncx(items, title, book_id, split))
        put("OEBPS/text/nav.xhtml", nav_xhtml(items, title))
        if cover:
            put("OEBPS/images/cover.jpg", cover)
            put("OEBPS/text/cover.xhtml", XHTML.format(
                lang=LANGUAGE, title="Cover", body_attrs=' class="cover"',
                body=f'<div class="cover"><img src="../images/cover.jpg" alt="{esc(title)}" /></div>'))
        for i, ch in enumerate(chapters):
            put(f"OEBPS/text/{ch.filename}", XHTML.format(
                lang=LANGUAGE, title=esc(ch.title),
                body_attrs=' class="titlepage"' if i == 0 else "", body=ch.body))
        for src, name in images.items():
            put(f"OEBPS/{name}", src.read_bytes())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("markdown", nargs="*", help="single-file Markdown texts (default: the books in BOOKS)")
    ap.add_argument("--out-dir", default=str(ROOT / "epub"), help="where to write the .epub files")
    ap.add_argument("--cover-pdf", help="PDF whose first page is the cover (one input file only)")
    ap.add_argument("--no-cover", action="store_true", help="don't add a cover image")
    ap.add_argument("--split", type=int, choices=range(1, 7), metavar="LEVEL",
                    help="deepest heading level that starts a chapter (default: 1, or the book's in BOOKS)")
    args = ap.parse_args()

    inputs = args.markdown or list(BOOKS)
    for name in inputs:
        path = (ROOT / name) if not Path(name).is_absolute() else Path(name)
        key = path.resolve().relative_to(ROOT).as_posix() if path.resolve().is_relative_to(ROOT) else None
        book = BOOKS.get(key, {})
        cover = args.cover_pdf or (ROOT / book["cover"] if "cover" in book else None)
        split = args.split or book.get("split", 1)
        print(f"{path.name}:")
        out = build_epub(path, Path(args.out_dir), None if args.no_cover else cover, split)
        print(f"  wrote {out}")


if __name__ == "__main__":
    main()
