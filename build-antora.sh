#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv-antora" ]]; then
  python3 -m venv .venv-antora
fi

source .venv-antora/bin/activate

if ! python -c "import IPython, ipykernel, jupyter" >/dev/null 2>&1; then
  pip install -r requirements.txt
fi

npx antora --stacktrace generate --log-failure-level warn --cache-dir cache --clean site.yml

python scripts/build-course-bundle.py
python scripts/check-course-bundle.py
mkdir -p public/cours-project/_attachments
cp cours-project.zip public/cours-project/_attachments/

python scripts/check-site-links.py public
python scripts/check-course-navigation.py public
