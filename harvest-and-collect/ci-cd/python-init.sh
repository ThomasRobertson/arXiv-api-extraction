#!/bin/bash

cd /app

python -m venv .venv

source .venv/bin/activate

pip --version
python --version

# install requirements
pip install -r requirements.txt

# launch pytest
pytest --cov=harvest_and_collect

exit $?
