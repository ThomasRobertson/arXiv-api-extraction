#!/bin/bash

cd /app

export PYTHONPATH=$PWD

# wait for Neo4j to be ready
until [ "$(curl -o /dev/null -s -w "%{http_code}\n" http://$2:7474)" == "200" ]; do
    echo "Neo4j is unavailable - sleeping"
    sleep 1
done
echo "Neo4j is available !"

# Prepare arguments for the Python scripts
args_harvester=""
[ "$1" != "False" ] && args_harvester+=" --mock"
[ "$2" != "False" ] && args_harvester+=" --neo4j_uri neo4j://$2:7687"
[ "$3" != "False" ] && args_harvester+=" --resumption_token $3"
[ "$4" != "False" ] && args_harvester+=" --from_date $4"
[ "$5" != "False" ] && args_harvester+=" --until_date $5"
[ "$6" != "False" ] && args_harvester+=" --set_cat $6"

args_api=""
[ "$2" != "False" ] && args_api+=" --neo4j_uri neo4j://$2:7687"

# Run the first Python script with arguments
echo "## INFO : Launching harvester"
if [ "$7" != "True" ]; then
    python /app/harvest_and_collect/main.py $args_harvester
fi
# Once the first script finishes, run the second Python script with arguments
echo "## INFO : Launching API worker"
python /app/api_worker/main.py $args_api

exit $?