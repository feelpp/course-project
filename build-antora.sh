#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv-antora" ]]; then
  python3 -m venv .venv-antora
fi

source .venv-antora/bin/activate

if ! python -c "import IPython, ipykernel, jupyter" >/dev/null 2>&1; then
  pip install -r requirements.txt
fi

npx antora --stacktrace generate --cache-dir cache --clean site.yml

zip_inputs=(notebooks)
if [[ -d .vscode ]]; then
  zip_inputs=(.vscode notebooks)
fi

zip -r cours-project.zip "${zip_inputs[@]}" -x "*.pyc" -x "*/__pycache__/"
mkdir -p public/cours-project/_attachments
cp cours-project.zip public/cours-project/_attachments/
