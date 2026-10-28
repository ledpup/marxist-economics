# Working in this repository

This repository collects texts on the economics of the first phase of communism (labour time accounting, labour certificates) as Markdown. It also holds Patrick's notes on them. The files aren't written for any one viewer. **The target is portable Markdown: GitHub-flavoured Markdown (GFM), plus a few standard HTML tags where GFM has no syntax.** That means a file should read correctly in VS Code preview, on GitHub (github.com/ledpup/marxist-economics, a convenient bonus), and in any CommonMark renderer that passes HTML through. Don't use syntax that belongs to one tool.

## Layout

| Path | What it holds |
| --- | --- |
| `README.md` | Front page: what the collection is, plus a table of every text (Author, Title, Description) |
| `Documents/` | Source texts: books, extracts, articles |
| `Documents/<slug>.md` | A whole text in one file |
| `Documents/<slug>/` | The same book split into one file per chapter, with its own `README.md` as a table of contents |
| `PDFs/` | Original PDFs that texts were converted from |
| `notes-pat/` | Patrick's own notes and collected quotes |
| `pdf_to_markdown.py` | Converter from PDF to a single Markdown file (tuned to the GIC PDF; its docstring lists the layout facts it relies on) |

## Source texts are faithful reproductions

- Don't change the wording, spelling (including American or British spelling), or emphasis of a source text. Only fix conversion errors, such as broken hyphenation, merged words, or misplaced footnotes, and check those against the PDF.
- Keep the source's quotation marks, including the GIC's `»…«` guillemets.
- Commentary, summaries, and opinions go in `notes-pat/`, never in a source file.
- A book exists both as a single file and as a chapter folder. **A correction in one must be made in the other.**
- An extract (such as `Critique_of_the_Gotha_Programme-certificates.md`) must say in `README.md` what it is extracted from, and link to the full text.

## Books split into chapters

Follow `Documents/fundamental_principles_of_communist_production_and_distribution/` as the model.

**File names:** `NN_Title_In_Words.md`, where the number sets the sort order.
- `00a`–`00z` are front matter (objective, forewords).
- `01`–`89` are chapters. A chapter split across files gets letter suffixes: `14a`, `14b`.
- `90`+ is back matter (appendix, literature).

**Each chapter file contains, in order:**

1. YAML front matter:
   ```yaml
   ---
   title: "Chapter 3: The unit of account in communism"
   book: "Fundamental Principles of Communist Production and Distribution"
   author: Group of International Communists
   up: README.md
   prev: 02_The_Social_Democratic_Revision_of_Marxism.md
   next: 04_Progress_in_the_Formulation_of_the_Problem.md
   ---
   ```
   The first file has no `prev`, and the last has no `next`.
2. A navigation bar, then `---`:
   `[← <prev title>](prev.md) · [↑ Contents](README.md) · [<next title> →](next.md)`
3. One `#` heading with the chapter number and title as the book gives it (`# 3. The unit of account in communism`). Sections use `##` (`## a. The regulation of production`), and so on down.
4. The text.
5. The footnote definitions used in this chapter.
6. `---`, then the same navigation bar again.

**Footnotes** keep the book's numbering, which runs continuously through the whole book. Chapter 3 therefore starts at `[^21]`, not `[^1]`. Each chapter file holds only the definitions for its own markers.

**Book `README.md`:** title, author, and bibliographic details; a link to the single-file version; then a nested contents list that links to each file and to each `##` section by its GitHub anchor.

## Markdown dialect

Use plain GFM wherever it can do the job: `*italic*`, `**bold**`, `>` block quotes, tables, `[^n]` footnotes, and relative links. GFM has no syntax for the cases below, so use these conventions instead:

| Need | Write | Notes |
| --- | --- | --- |
| Underline | `<ins>text</ins>` | Used where the source underlines. The converter emits it. Not `<u>`: GitHub strips that, while `<ins>` is underlined by default everywhere HTML is rendered. |
| Subscript | `C<sub>p</sub>` | For the GIC's formulas, such as `(P<sub>p</sub> + C<sub>p</sub>) + L<sub>p</sub>`. Don't use LaTeX `$…$`: keep formulas in the same style as the source. |
| Superscript | `<sup>…</sup>` | Not for footnote markers; those are `[^n]`. |
| Letter-spaced emphasis (German *Sperrsatz*) | `**bold**` | Converted to bold, as the converter does. |
| Hard line break | two trailing spaces | Used in title pages and addresses. Editors that trim trailing whitespace will break these; use `<br>` where that's a risk. |
| Metadata | YAML front matter | Most tools read it. GitHub shows it as a small table at the top of the file. |
| Section break | `---` on its own line, with blank lines around it | |

Avoid these, because only some tools support them:
- `[[wikilinks]]`, `==highlight==`, Obsidian callouts, and GitHub's `> [!NOTE]` alerts. Use normal relative links: `[text](../path/file.md#anchor)`.
- Inline `style=` attributes, `<font>`, and `<u>`, which some renderers strip.
- Raw HTML beyond the tags listed above. If a new need comes up, choose a standard semantic HTML element and add it to this table.

**Links and anchors:** a heading's anchor is its text in lower case, with punctuation (including apostrophes and quotation marks) removed and spaces turned into `-`. For example, `## a. The workers' councils as the organizational basis` becomes `#a-the-workers-councils-as-the-organizational-basis`. If you rename a heading, find and update every link to it.

## Notes (`notes-pat/`)

Notes are separate from the source texts and loosely follow Zettelkasten practice:

- **Quote collections** are one file per source, named `quotes-<source-abbrev>.md` (e.g. `quotes-fpcpd.md`). Each quote is a block quote followed by its location: `- Page 107`. Where possible, also link to the chapter section: `- Page 107 · [Ch. 9 b](../Documents/<book>/09_….md#anchor)`.
- **Idea notes** hold one idea per file, written in Patrick's own words, with a kebab-case name such as `labour-certificates.md` or `average-social-working-hour.md`. Each one links to the source passages it rests on and to related idea notes. Connections between texts (Marx → GIC → later writers) are recorded in these links.
- Don't move or reword notes Patrick has written. Ask first.

## Adding a new text

1. Put the PDF (if there is one) in `PDFs/`.
2. Convert it to `Documents/<slug>.md`. `pdf_to_markdown.py` is tuned to one PDF, so expect to adjust it or clean up by hand. Check the output against the PDF.
3. For a book, split it into `Documents/<slug>/` as described above.
4. Add a row to the table in the root `README.md`: Author, linked Title, and a short plain-language Description that says what the text argues and links to the full text online if there is one.
