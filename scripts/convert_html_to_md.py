#!/usr/bin/env python3
"""
Convert tenniskb/tenniskb's static HTML pages (both the hand-typed pages and
the handful of genuine mkdocs-material builds like Home/About) into real
Markdown source for a fresh, consistent mkdocs-material build.

Usage:
    python convert_html_to_md.py <old_site_dir> <docs_out_dir>

Walks <old_site_dir>/en and <old_site_dir>/vi for every index.html, extracts
the <article class="md-content__inner ..."> ... </article> inner content
(present in both page styles), cleans up mkdocs-internal cruft (headerlink
permalink anchors, code-line-number anchors, the hardcoded cross-language
button paragraph), converts to Markdown, and writes to
<docs_out_dir>/<lang>/<same relative path>/index.md.

Designed to run on GitHub Actions against a full checkout of the gh-pages
branch -- doing this against ~200 small files one-by-one over a slow/limited
sandbox network is impractical, so this script assumes local disk access to
every file already.
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify as md

SKIP_TOP_DIRS = {"assets", "stylesheets"}

LANG_SWITCH_MARKERS = ("english", "tiếng việt", "🇬🇧", "🇻🇳", "phiên bản")


def extract_title(soup: BeautifulSoup, article) -> str:
    h1 = article.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    if soup.title and soup.title.string:
        t = str(soup.title.string)
        return t.split(" — ")[0].split(" - ")[0].strip()
    return "Untitled"


def clean_article(article):
    """Strip mkdocs-internal cruft that shouldn't survive into fresh source."""
    # Permalink anchors mkdocs-material injects after every heading.
    for a in article.select("a.headerlink"):
        a.decompose()

    # Empty code-line-number anchors inside real mkdocs code blocks.
    for a in article.find_all("a", id=re.compile(r"^__codelineno")):
        a.decompose()
    for span in article.find_all("span", id=re.compile(r"^__span")):
        # unwrap (keep children/text, drop the span itself)
        span.unwrap()

    # Empty leftover <span></span> markers inside <pre><code> blocks.
    for span in article.find_all("span"):
        if not span.get_text(strip=True) and not span.find(True):
            span.decompose()

    # The hardcoded "switch language" button paragraph at the end of most
    # hand-typed pages -- language switching will be a real nav feature in
    # the rebuilt site, so this per-page hardcoded button is redundant.
    for p in article.find_all("p", recursive=False):
        text = p.get_text(strip=True).lower()
        if any(marker in text for marker in LANG_SWITCH_MARKERS) and len(text) < 80:
            p.decompose()

    return article


def convert_file(html_path: Path, lang_root: Path, docs_root: Path, lang: str, report):
    try:
        html = html_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        report["errors"].append(f"{html_path}: read failed: {e}")
        return

    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article", class_="md-content__inner")
    if article is None:
        report["errors"].append(f"{html_path}: no <article class='md-content__inner'> found")
        return

    article = clean_article(article)
    title = extract_title(soup, article)

    body_html = "".join(str(c) for c in article.contents)
    markdown = md(body_html, heading_style="ATX", bullets="-", wrap=False)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip() + "\n"

    rel = html_path.relative_to(lang_root)
    out_rel = rel.parent / "index.md" if rel.name == "index.html" else rel.with_suffix(".md")
    out_path = docs_root / lang / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)

    safe_title = title.replace('"', "'")
    front_matter = f'---\ntitle: "{safe_title}"\n---\n\n'
    out_path.write_text(front_matter + markdown, encoding="utf-8")
    report["converted"] += 1
    report["files"].append(str(out_path.relative_to(docs_root)))


def walk_lang(old_site_dir: Path, docs_root: Path, lang: str, report):
    lang_root = old_site_dir / lang
    if not lang_root.is_dir():
        report["errors"].append(f"missing lang root: {lang_root}")
        return
    for html_path in sorted(lang_root.rglob("index.html")):
        if any(part in SKIP_TOP_DIRS for part in html_path.relative_to(lang_root).parts):
            continue
        convert_file(html_path, lang_root, docs_root, lang, report)


def main():
    if len(sys.argv) != 3:
        print("usage: convert_html_to_md.py <old_site_dir> <docs_out_dir>")
        sys.exit(1)
    old_site_dir = Path(sys.argv[1]).resolve()
    docs_root = Path(sys.argv[2]).resolve()
    report = {"converted": 0, "errors": [], "files": []}

    walk_lang(old_site_dir, docs_root, "en", report)
    walk_lang(old_site_dir, docs_root, "vi", report)

    print(f"Converted: {report['converted']} pages")
    if report["errors"]:
        print(f"Errors: {len(report['errors'])}")
        for e in report["errors"]:
            print(f"  - {e}")
    report_path = docs_root.parent / "conversion_report.txt"
    report_path.write_text(
        f"Converted: {report['converted']}\nErrors: {len(report['errors'])}\n\n"
        + "\n".join(report["errors"])
        + "\n\nFiles:\n" + "\n".join(report["files"]),
        encoding="utf-8",
    )
    if report["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
