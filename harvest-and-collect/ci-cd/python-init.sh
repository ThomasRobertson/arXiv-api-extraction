#!/bin/bash

cd /app

python -m venv .venv

source .venv/bin/activate

pip --version
python --version

# install requirements
pip install -r requirements.txt

export PYTHONPATH=$PWD

# wait for Neo4j to be ready
until curl http://neo4j:7474; do
  echo "Neo4j is unavailable - sleeping"
  sleep 1
done

echo "Neo4j is up - executing command"

# launch pytest
pytest --cov=harvest_and_collect

exit $?
