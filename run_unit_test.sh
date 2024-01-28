#!/bin/bash

# Start services
docker compose -f docker-compose-unit-test.yml up -d

# Wait for Python service to finish
docker wait python

# Get Python service exit code
exit_code=$(docker inspect python -f '{{.State.ExitCode}}')

# Output Python service logs
docker compose -f docker-compose-unit-test.yml logs python

# Stop Neo4j service
docker stop neo4j

# Remove all services
docker compose -f docker-compose-unit-test.yml down

# Return the exit code of the Python service
exit $exit_code