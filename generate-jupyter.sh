#! /bin/sh
set -eu

dir=${1:-.}
find "$dir" -name "*.adoc" | grep pages | while IFS= read -r file; do
    if grep -q ":page-jupyter:" "$file"; then
        echo "Generating Jupyter Notebook for $file: "
        ipynb=$(echo "$file" | sed -E 's#^docs/course/modules/([^/]+)/pages/(.*)$#\1/\2#')
        if [ "$ipynb" = "$file" ]; then
            ipynb=$(echo "$file" | sed -E 's#^docs/csmi/modules/([^/]+)/pages/(.*)$#\1/\2#')
        fi
        if [ "$ipynb" = "$file" ]; then
            ipynb=$(echo "$file" | sed -E 's#^docs/modules/([^/]+)/pages/(.*)$#\1/\2#')
        fi

        if [ "$ipynb" = "$file" ]; then
            echo "Skipping $file: unable to map output path."
            continue
        fi

        outdir=$(dirname "$ipynb")
        mkdir -p "notebooks/$outdir"
        echo "generating notebooks/$outdir/$(basename "$ipynb" .adoc).ipynb..."
        pwd
        npx asciidoctor -r asciidoctor-jupyter -b jupyter \
            -a 'project_name=Course Project' -a 'feelpp=Feel++' -a 'cpp=C++' \
            "$file" -o "notebooks/$outdir/$(basename "$ipynb" .adoc).ipynb"
        python - "notebooks/$outdir/$(basename "$ipynb" .adoc).ipynb" <<'PY'
import json
from pathlib import Path
import sys

path = Path(sys.argv[1])
notebook = json.loads(path.read_text())
notebook['metadata']['kernelspec'] = {
    'name': 'python3', 'display_name': 'Python 3', 'language': 'python',
}
notebook['metadata']['language_info'] = {'name': 'python'}
path.write_text(json.dumps(notebook, indent=2) + '\n')
PY
    fi
done
