#!/usr/bin/env python3
"""Check course navigation coverage and the Apptainer reading sequence after building."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Navigation(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = {"pagination": [], "breadcrumbs": []}
        self.current = None
        self.direction = None
        self.steps = {}
        self.redirect = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.redirect = True
        if tag == "nav":
            self.current = next((name for name in self.links if name in classes), None)
        elif tag == "span" and self.current == "pagination":
            self.direction = next((name for name in ("prev", "next") if name in classes), None)
        elif tag == "a" and self.current and "href" in attrs:
            self.links[self.current].append(attrs["href"])
            if self.current == "pagination" and self.direction:
                self.steps[self.direction] = attrs["href"]

    def handle_endtag(self, tag):
        if tag == "nav":
            self.current = self.direction = None
        elif tag == "span":
            self.direction = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default="public")
    args = parser.parse_args()
    root = Path(args.directory).resolve() / "course-project"
    pages = {path: Navigation(path) for path in root.rglob("*.html")}
    if not pages:
        raise SystemExit(f"No generated course pages under {root}")
    failures = []
    count = 0
    for path, nav in pages.items():
        if nav.redirect:
            continue
        count += 1
        for kind, links in nav.links.items():
            if not links:
                failures.append(f"{path.relative_to(root)}: missing {kind}")
    # Extra reference pages must remain children of Reference, including
    # catalog pages using the custom manuals layout.
    for relative in ("linux/editing.html", "containers/docker/index.html", "vscode/install.html"):
        path = root / relative
        links = pages[path].links["breadcrumbs"] if path in pages else []
        targets = {(path.parent / unquote(urlsplit(link).path)).resolve() for link in links}
        if root / "reference.html" not in targets:
            failures.append(f"{relative}: missing Reference breadcrumb ancestor")
    # Assert both directions at each boundary: the access page must be part of
    # the main M2 route, rather than getting unrelated reference neighbours.
    chain = [
        "m2/transition.html",
        "containers/apptainer/index.html",
        "containers/apptainer/apptainer-install.html",
        "containers/apptainer/tutorial.html",
        "m2/hpc-containers.html",
    ]
    for before, after in zip(chain, chain[1:]):
        for source, direction, expected in ((before, "next", after), (after, "prev", before)):
            path = root / source
            href = pages[path].steps.get(direction, "") if path in pages else ""
            target = (path.parent / unquote(urlsplit(href).path)).resolve()
            if not href or target != root / expected:
                failures.append(f"{source}: expected {direction} → {expected}, got {href!r}")
    for failure in failures:
        print(failure)
    print(f"Checked breadcrumbs/pagination on {count} course pages and Apptainer sequence; {len(failures)} failures.")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
