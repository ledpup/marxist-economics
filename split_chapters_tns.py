"""Split the single-file Markdown of Cockshott and Cottrell's "Towards a New
Socialism" into one file per chapter, following Documents/fundamental_principles/
as the model (see AGENTS.md, "Books split into chapters").

Input facts it relies on (as written by pdf_to_markdown_tns.py):
  "# Towards a New Socialism"  the title, then "**authors**" and "## About this
                               book"; these become the folder's README.md
  other "#" headings           one per file: the preface, the introduction,
                               "Chapter N. Title" and "References"
  footnotes                    labelled "<chapter>-<n>" ("3-2", "policy-1"),
                               defined at the end of their chapter. In a
                               chapter file the prefix is dropped ("[^2]"),
                               giving the book's own numbering back
  links                        relative to Documents/ ("towards_a_new_socialism/
                               figures/figure-4-1.png"); rewritten to be
                               relative to the chapter folder

The chapter folder is generated: make corrections in the single file (or the
converter) and re-run this script. Old numbered .md files in the folder that
this run did not write are deleted; figures/ is left alone.

Usage: python split_chapters_tns.py [Documents/towards_a_new_socialism.md [Documents/towards_a_new_socialism]]
"""
import os
import re
import sys

BOOK = "Towards a New Socialism"
AUTHOR = "W. Paul Cockshott and Allin Cottrell"
SMALL_WORDS = {"a", "an", "and", "as", "at", "between", "by", "for", "in", "of",
               "on", "or", "the", "to", "with"}

FOOTNOTE = re.compile(r"\[\^([^\]\s]+)\]")
LINK = re.compile(r"(!?\[(?:[^\]\\]|\\.)*\])\((<[^>]*>|[^)\s]+)((?:\s+\"[^\"]*\")?)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


# ----------------------------------------------------------------- anchors

def anchor(text):
    """GitHub's anchor for a heading: rendered text in lower case, punctuation
    dropped, spaces turned into "-"."""
    text = FOOTNOTE.sub(lambda m: m.group(1).rsplit("-", 1)[-1], text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> their text
    text = re.sub(r"<[^>]+>", "", text)                       # inline HTML tags
    text = re.sub(r"(\*+|`+)", "", text)                      # emphasis, code
    text = re.sub(r"(?<!\w)_+|_+(?!\w)", "", text)            # _emphasis_
    return "".join(c for c in text.lower() if c.isalnum() or c in " -_").replace(" ", "-")


class Anchors:
    """Hands out unique anchors in document order, as GitHub does ("x", "x-1")."""

    def __init__(self):
        self.seen = {}

    def __call__(self, text):
        base = anchor(text)
        n = self.seen.get(base, 0)
        self.seen[base] = n + 1
        return base if n == 0 else f"{base}-{n}"


def headings(lines):
    """(level, text) of each ATX heading outside fenced code."""
    fenced = False
    for line in lines:
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and (m := HEADING.match(line)):
            yield len(m.group(1)), m.group(2)


# ---------------------------------------------------------------- sections

def split(text):
    """[(heading text, [lines])] for each "#" section; the first is the title page."""
    sections, fenced = [], False
    for line in text.split("\n"):
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        if not fenced and line.startswith("# "):
            sections.append((line[2:].strip(), []))
        elif not sections:
            if line.strip():
                sys.exit(f"text before the first heading: {line[:60]!r}")
        else:
            sections[-1][1].append(line)
    return sections


def words(title):
    """File-name words: "Work, Time and Computers" -> "Work_Time_and_Computers"."""
    ws = re.sub(r"[^\w\s-]", "", title).replace("-", " ").split()
    return "_".join(w if i and w.lower() in SMALL_WORDS else w[:1].upper() + w[1:]
                    for i, w in enumerate(ws))


def describe(heading, front_count):
    """(file name, display title) for one "#" section."""
    if m := re.match(r"Chapter (\d+)\.\s*(.*)", heading):
        n, title = int(m.group(1)), m.group(2)
        if not 1 <= n <= 89:
            sys.exit(f"chapter number out of range: {heading}")
        return f"{n:02d}_{words(title)}.md", f"Chapter {n}: {title}"
    if heading == "References":
        return f"90_{words(heading)}.md", heading
    return f"00{chr(ord('a') + front_count)}_{words(heading)}.md", heading


def strip_blank(lines):
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


# -------------------------------------------------------------- rewriting

def relabel_footnotes(body, name):
    """Drop the "<chapter>-" prefix from footnote labels, and check that each
    marker in this file has its definition here and the other way round."""
    labels = list(dict.fromkeys(FOOTNOTE.findall(body)))
    new = {l: l.rsplit("-", 1)[1] if re.fullmatch(r".+-\d+", l) else l for l in labels}
    if len(set(new.values())) != len(new):
        print(f"warning: {name}: footnote labels would collide; kept as they are")
        new = {l: l for l in labels}
    body = FOOTNOTE.sub(lambda m: f"[^{new[m.group(1)]}]", body)

    defined = set(re.findall(r"^\[\^([^\]\s]+)\]:", body, re.M))
    used = set(re.findall(r"\[\^([^\]\s]+)\](?!:)", body))
    for l in sorted(used - defined):
        print(f"warning: {name}: footnote [^{l}] has no definition in this file")
    for l in sorted(defined - used):
        print(f"warning: {name}: footnote [^{l}] is defined but never used")
    return body


def rewrite_links(body, name, slug, anchor_map):
    """Make relative links work from Documents/<slug>/ instead of Documents/."""
    def fix(m):
        label, target, title = m.groups()
        bracketed = target.startswith("<")
        t = target[1:-1] if bracketed else target
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", t) or t.startswith("/"):
            return m.group(0)
        if t.startswith("#"):
            if t[1:] not in anchor_map:
                print(f"warning: {name}: link to unknown anchor {t}")
                return m.group(0)
            file, a = anchor_map[t[1:]]
            t = f"#{a}" if file == name else f"{file}#{a}"
        elif t.startswith(slug + "/"):
            t = t[len(slug) + 1:]
        else:
            t = "../" + t
        return f"{label}({'<' + t + '>' if bracketed else t}{title})"
    return LINK.sub(fix, body)


def front_matter(title, prev, nxt):
    q = lambda s: '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    lines = ["---", f"title: {q(title)}", f"book: {q(BOOK)}", f"author: {AUTHOR}",
             "up: README.md"]
    if prev:
        lines.append(f"prev: {prev[0]}")
    if nxt:
        lines.append(f"next: {nxt[0]}")
    return "\n".join(lines + ["---"])


def nav(prev, nxt):
    parts = []
    if prev:
        parts.append(f"[← {prev[1]}]({prev[0]})")
    parts.append("[↑ Contents](README.md)")
    if nxt:
        parts.append(f"[{nxt[1]} →]({nxt[0]})")
    return " · ".join(parts)


# -------------------------------------------------------------------- main

def build(text, slug):
    """{file name: content} for the chapter folder, README.md included."""
    sections = split(text)
    (book_title, title_page), chapters = sections[0], sections[1:]
    if book_title != BOOK:
        sys.exit(f"expected '# {BOOK}' first, found '# {book_title}'")

    files, front_count = [], 0  # [(name, display title, heading, lines)]
    for heading, lines in chapters:
        name, title = describe(heading, front_count)
        front_count += name.startswith("00")
        if any(name == f[0] for f in files):
            sys.exit(f"two sections map to {name}")
        files.append((name, title, heading, lines))
    files.sort(key=lambda f: f[0])

    # Anchors in the single file -> (chapter file, anchor there).
    whole, anchor_map = Anchors(), {}
    whole(book_title)
    for _, text_ in headings(title_page):
        anchor_map[whole(text_)] = ("README.md", anchor(text_))
    contents = []
    for name, title, heading, lines in files:
        local = Anchors()
        anchor_map[whole(heading)] = (name, local(heading))
        contents.append(f"- [{title}]({name})")
        for level, text_ in headings(lines):
            a = local(text_)
            anchor_map[whole(text_)] = (name, a)
            if level == 2:
                contents.append(f"  - [{text_}]({name}#{a})")

    out = {}
    for i, (name, title, heading, lines) in enumerate(files):
        prev = files[i - 1][:2] if i else None
        nxt = files[i + 1][:2] if i + 1 < len(files) else None
        body = "\n".join(strip_blank(lines))
        body = relabel_footnotes(body, name)
        body = rewrite_links(body, name, slug, anchor_map)
        bar = nav(prev, nxt)
        out[name] = (f"{front_matter(title, prev, nxt)}\n\n{bar}\n\n---\n\n"
                     f"# {heading}\n\n{body}\n\n---\n\n{bar}\n")

    intro = rewrite_links("\n".join(strip_blank(title_page)), "README.md", slug, anchor_map)
    out["README.md"] = (
        f"# {book_title}\n\n{intro}\n\n"
        f"The whole book is also available as a single file: "
        f"[{slug}.md](../{slug}.md).\n\n---\n\n## Contents\n\n"
        + "\n".join(contents)
        + f"\n\n---\n\n[Start reading: {files[0][1]} →]({files[0][0]})\n")
    return out


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "Documents/towards_a_new_socialism.md"
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0]
    slug = os.path.basename(os.path.normpath(dst))
    with open(src, encoding="utf-8") as f:
        files = build(f.read().replace("\r\n", "\n"), slug)

    os.makedirs(dst, exist_ok=True)
    for old in sorted(os.listdir(dst)):
        if re.fullmatch(r"\d\d[a-z]?_.*\.md", old) and old not in files:
            os.remove(os.path.join(dst, old))
            print(f"removed {old}")
    for name, content in files.items():
        with open(os.path.join(dst, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
    print(f"wrote {len(files)} files to {dst}")


if __name__ == "__main__":
    main()
