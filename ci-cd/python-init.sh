#!/bin/bash

cd /app

# install requirements
pip install -r requirements.txt

# launch pytest
pytest --cov=src

exit $?
