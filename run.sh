#!/bin/bash
set -e

cd $(dirname $0)

if ! [[ -e .venv ]]; then
  virtualenv .venv --system-site-packages
fi
source .venv/bin/activate

pip install -r requirements.txt
python src/main/python/streamdeck/main.py $@
