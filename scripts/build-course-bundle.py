#!/usr/bin/env python3
"""Build the notebook-only VS Code/uv download from current teaching notebooks."""
import argparse
import json
from pathlib import Path
import re
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = 'cours-project.zip'  # Keep the public download URL.
WORKSPACE_FILES = (
    'README.md', 'pyproject.toml', 'uv.lock', '.python-version',
    '.vscode/settings.json', '.vscode/extensions.json',
)
# Add only resources actually required by a notebook, keyed by its archive path.
# Paths on the right are repository-relative; paths on the left are relative to
# the extracted workspace. The current teaching notebooks need no local datasets.
NOTEBOOK_RESOURCES = {}


def teaching_notebooks():
    mappings = {}
    for page in sorted((ROOT / 'docs/course/modules').glob('*/pages/**/*.adoc')):
        if re.search(r'^:page-jupyter:\s*(?:true)?\s*$', page.read_text(), re.M):
            module, _, *parts = page.relative_to(ROOT / 'docs/course/modules').parts
            target = Path('notebooks') / module / Path(*parts).with_suffix('.ipynb')
            mappings[target.as_posix()] = page
    if not mappings:
        raise ValueError('No teaching notebooks found')
    return mappings


def build(output):
    mappings = teaching_notebooks()
    if set(NOTEBOOK_RESOURCES) - mappings.keys():
        raise ValueError('Resources declared for a notebook that no longer exists')
    with tempfile.TemporaryDirectory(prefix='notebook-bundle-') as temp:
        stage = Path(temp) / 'course-project'
        for name in WORKSPACE_FILES:
            dest = stage / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT / 'support/course-bundle' / name).read_bytes())
        for name, page in mappings.items():
            generated = ROOT / name
            if not generated.is_file():
                raise ValueError(f'Missing generated notebook for {page}: {generated}')
            content = json.loads(generated.read_text())
            # The converter omits display_name and supplies a stale Python version.
            content['metadata'] = {
                'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'},
                'language_info': {'name': 'python'},
            }
            for cell in content['cells']:
                if cell['cell_type'] == 'code':
                    cell['outputs'], cell['execution_count'] = [], None
            dest = stage / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(json.dumps(content, indent=2) + '\n')
            for relative, source in NOTEBOOK_RESOURCES.get(name, {}).items():
                target = stage / relative
                if not target.resolve().is_relative_to(stage.resolve()):
                    raise ValueError(f'Resource escapes the workspace: {relative}')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / source).read_bytes())
        output.parent.mkdir(parents=True, exist_ok=True)
        # Recreate the archive so files from older bundles cannot survive.
        with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
            for path in sorted(stage.rglob('*')):
                if path.is_file():
                    archive.write(path, path.relative_to(stage.parent))
        print(f'Bundled {len(mappings)} teaching notebooks and the VS Code/uv environment '
              f'({output.stat().st_size:,} bytes): {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / ARCHIVE)
    build(parser.parse_args().output.resolve())
