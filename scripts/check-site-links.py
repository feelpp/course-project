#!/usr/bin/env python3
"""Check generated local HTML links and fragments without external HTTP requests."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default="public")
    parser.add_argument("--site-path", default="/course-project/")
    args = parser.parse_args()
    root = Path(args.directory).resolve()
    pages = {path: Page(path) for path in root.rglob("*.html")}
    if not pages:
        raise SystemExit(f"No generated HTML found under {root}")
    failures = set()
    for source, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if path.startswith(args.site_path):
                target = root / path[len(args.site_path):]
            elif path.startswith("/"):
                target = root / path.lstrip("/")
            else:
                target = (source.parent / path).resolve() if path else source
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                reason = "missing file"
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                reason = "missing anchor"
            else:
                continue
            failures.add((str(source.relative_to(root)), href, reason))
    for source, href, reason in sorted(failures):
        print(f"{source}: {reason}: {href}")
    print(f"Checked {len(pages)} HTML pages; {len(failures)} broken local links.")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
