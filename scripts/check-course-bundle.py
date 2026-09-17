#!/usr/bin/env python3
"""Check that the download contains only notebooks and their execution files."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import tempfile
from zipfile import ZipFile

import nbformat
from IPython.core.inputtransformer2 import TransformerManager

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bundle', ROOT / 'scripts/build-course-bundle.py')
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


class Downloads(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'jupyter-download' in attrs.get('class', '').split():
            self.links.append(attrs.get('href', ''))


def check(archive_path):
    with ZipFile(archive_path) as archive, tempfile.TemporaryDirectory() as temp:
        names = archive.namelist()
        assert len(names) == len(set(names)), 'Duplicate ZIP members'
        notebooks = bundle.teaching_notebooks()
        resources = {name: source for files in bundle.NOTEBOOK_RESOURCES.values()
                     for name, source in files.items()}
        expected = set(bundle.WORKSPACE_FILES) | notebooks.keys() | resources.keys()
        assert set(names) == {'course-project/' + name for name in expected}, \
            'Missing files or unrelated/stale content in the archive'
        archive.extractall(temp)
        root = Path(temp) / 'course-project'
        for name in bundle.WORKSPACE_FILES:
            assert (root / name).read_bytes() == (ROOT / 'support/course-bundle' / name).read_bytes()
        for name, source in resources.items():
            assert (root / name).read_bytes() == (ROOT / source).read_bytes()
        for path in (root / '.vscode').glob('*.json'):
            json.loads(path.read_text())
        transform = TransformerManager()
        code_count = 0
        for name in notebooks:
            nb = nbformat.read(root / name, as_version=4)
            nbformat.validate(nb)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    ast.parse(transform.transform_cell(cell.source), filename=name)
                    assert not cell.outputs and cell.execution_count is None
                    code_count += 1
            # Both standard and custom page layouts must expose the individual
            # notebook download, in addition to the complete archive button.
            relative = Path(name).relative_to('notebooks')
            module, *parts = relative.parts
            html = ROOT / 'public/course-project'
            if module != 'ROOT':
                html /= module
            html = html / Path(*parts).with_suffix('.html')
            links = Downloads(html.read_text()).links
            assert links, f'Missing individual notebook download on {html}'
            for link in links:
                target = (html.parent / unquote(urlsplit(link).path)).resolve()
                assert target.is_file() and target.suffix == '.ipynb', link
                nbformat.validate(nbformat.read(target, as_version=4))
        print(f'Bundle verified: {len(notebooks)} notebooks, {code_count} valid code cells, '
              f'{len(resources)} required resources, and only the VS Code/uv setup files.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', nargs='?', type=Path, default=ROOT / 'cours-project.zip')
    check(parser.parse_args().archive)
